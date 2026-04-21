from __future__ import annotations

import logging
import time
from datetime import datetime, timezone

import pandas as pd
import requests

logger = logging.getLogger(__name__)

_RATE_LIMIT_CODE = 10006
_MAX_RETRIES = 5
_RETRY_BACKOFF_BASE = 2.0  # seconds; doubles each attempt


def _parse_ts(value: str) -> int:
    """Parse a UTC datetime string to a UTC Unix timestamp in milliseconds."""
    import calendar

    return calendar.timegm(time.strptime(value, "%Y-%m-%d %H:%M:%S")) * 1000


def _to_bybit_interval(timeframe: str) -> str:
    tf = timeframe.strip().lower()
    mapping = {
        "1m": "1",
        "3m": "3",
        "5m": "5",
        "15m": "15",
        "30m": "30",
        "1h": "60",
        "2h": "120",
        "4h": "240",
        "6h": "360",
        "12h": "720",
        "1d": "D",
        "1day": "D",
        "3d": "3D",
        "1w": "W",
    }
    if tf in mapping:
        return mapping[tf]
    if tf in {"1", "3", "5", "15", "30", "60", "120", "240", "360", "720", "D", "3D", "W"}:
        return tf
    raise ValueError("Unsupported timeframe: %s" % timeframe)


def _to_bybit_base_url(market_type: str) -> str:
    return "https://api.bybit.com/v5/market/kline"


def _to_bybit_category(market_type: str) -> str:
    mt = market_type.lower()
    if mt == "spot":
        return "spot"
    if mt in {"futures", "linear", "swap"}:
        return "linear"
    if mt == "inverse":
        return "inverse"
    raise ValueError("market_type must be 'spot', 'futures', 'linear', 'swap', or 'inverse'")


def _normalize_symbol(symbol: str) -> str:
    return symbol.replace("-", "").upper()


def _candle_timestamp(candle: list[str] | dict[str, object]) -> int:
    if isinstance(candle, dict):
        raw = candle.get("id") or candle.get("open_time") or candle.get("start_at")
    else:
        raw = candle[0] if candle else 0
    return int(raw) if raw is not None else 0


def fetch_bybit_candles_chunk(
    symbol: str,
    market_type: str = "spot",
    timeframe: str = "1day",
    start_time: str | None = None,
    end_time: str | None = None,
):
    time.sleep(0.25)
    interval = _to_bybit_interval(timeframe)
    url = _to_bybit_base_url(market_type)
    symbol_norm = _normalize_symbol(symbol)
    category = _to_bybit_category(market_type)
    params: dict[str, str | int] = {
        "category": category,
        "symbol": symbol_norm,
        "interval": interval,
        "limit": 200,
    }
    if start_time is not None:
        params["start"] = _parse_ts(start_time)
    if end_time is not None:
        params["end"] = _parse_ts(end_time)

    for attempt in range(_MAX_RETRIES):
        try:
            resp = requests.get(url, params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as exc:
            wait = _RETRY_BACKOFF_BASE * (2 ** attempt)
            logger.warning(
                "Network error for %s (attempt %d/%d): %s. Retrying in %.1fs.",
                symbol_norm, attempt + 1, _MAX_RETRIES, exc, wait,
            )
            if attempt < _MAX_RETRIES - 1:
                time.sleep(wait)
                continue
            raise

        ret_code = data.get("retCode") or data.get("ret_code")

        if ret_code == _RATE_LIMIT_CODE:
            wait = _RETRY_BACKOFF_BASE * (2 ** attempt)
            logger.warning(
                "Bybit rate limit hit for %s (attempt %d/%d). Waiting %.1fs.",
                symbol_norm, attempt + 1, _MAX_RETRIES, wait,
            )
            time.sleep(wait)
            continue

        if ret_code not in (0, None):
            raise RuntimeError(f"Bybit API error: {data}")

        result = data.get("result", {})
        payload = result.get("list") if isinstance(result, dict) else result
        if payload is None:
            raise RuntimeError(f"Bybit returned no result: {data}")
        return payload

    raise RuntimeError(
        f"Bybit API not resolved after {_MAX_RETRIES} retries for {symbol_norm}"
    )


def fetch_all_bybit_candles(
    symbol: str,
    market_type: str = "spot",
    timeframe: str = "1day",
    start_time: str | None = None,
    end_time: str | None = None,
) -> pd.DataFrame:
    if not (start_time and end_time):
        raise ValueError("start_time and end_time are required")

    start_ts = _parse_ts(start_time)
    end_ts = _parse_ts(end_time)
    interval = _to_bybit_interval(timeframe)

    if interval.endswith("D"):
        step = 86400 * 1000
    elif interval.endswith("W"):
        step = 86400 * 7 * 1000
    else:
        step = int(interval) * 60 * 1000

    candles = []
    current_from = start_ts

    while current_from <= end_ts:
        current_to = min(end_ts, current_from + step * 199)
        chunk = fetch_bybit_candles_chunk(
            symbol,
            market_type,
            timeframe,
            datetime.fromtimestamp(current_from / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            datetime.fromtimestamp(current_to / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        )
        if not chunk:
            # Symbol may not be listed yet — advance past this window and try the next.
            # Once listed, subsequent windows will return data.  If we have already
            # collected some candles and hit empty, we are past the end of data.
            if candles:
                break
            current_from = current_to + step
            continue

        ordered_chunk = sorted(chunk, key=_candle_timestamp)
        candles.extend(ordered_chunk)
        last_ts = _candle_timestamp(ordered_chunk[-1])

        if last_ts <= current_from:
            break

        current_from = last_ts + step
        # Do NOT break on len(chunk) < 200 here — a partial chunk may mean the
        # pair was just listed (first window has fewer bars than the limit).
        # Termination is handled by: current_from > end_ts, or the empty-chunk
        # guard above (if candles: break) on the next iteration.

    if not candles:
        return pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])

    def normalize_row(c):
        if isinstance(c, dict):
            ts_raw = c.get("id") or c.get("open_time") or c.get("start_at")
            ts = int(ts_raw) if ts_raw is not None else 0
            return {
                "Timestamp": ts,
                "Open": float(c["open"]),
                "High": float(c["high"]),
                "Low": float(c["low"]),
                "Close": float(c["close"]),
                "Volume": float(c.get("volume", c.get("trade_volume", 0))),
            }
        ts_raw = c[0] if len(c) > 0 else 0
        ts = int(ts_raw) if ts_raw is not None else 0
        return {
            "Timestamp": ts,
            "Open": float(c[1]),
            "High": float(c[2]),
            "Low": float(c[3]),
            "Close": float(c[4]),
            "Volume": float(c[5]),
        }

    processed = [
        normalize_row(c)
        for c in candles
        if start_ts <= _candle_timestamp(c) <= end_ts
    ]
    processed.sort(key=lambda item: item["Timestamp"])
    df = pd.DataFrame(processed)
    df = df.drop_duplicates(subset=["Timestamp"], keep="last")
    df["Date"] = pd.to_datetime(df["Timestamp"], unit="ms", utc=True)
    df = df.set_index("Date")
    return df[["Open", "High", "Low", "Close", "Volume"]]


def get_bybit_candles_df(
    symbol: str = "BTCUSDT",
    market_type: str = "spot",
    timeframe: str = "1day",
    start_time: str = "2026-02-01 00:00:00",
    end_time: str | None = None,
) -> pd.DataFrame:
    if end_time is None:
        end_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return fetch_all_bybit_candles(symbol, market_type, timeframe, start_time, end_time)


def load_ohlcv_bybit(
    symbol: str = "BTCUSDT",
    market_type: str = "futures",
    timeframe: str = "1day",
    start_time: str = "2020-03-25 00:00:00",
    end_time: str | None = None,
) -> pd.DataFrame:
    return get_bybit_candles_df(
        symbol=symbol,
        market_type=market_type,
        timeframe=timeframe,
        start_time=start_time,
        end_time=end_time,
    )
