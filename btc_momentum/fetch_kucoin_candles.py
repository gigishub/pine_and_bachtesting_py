import pandas as pd
import requests
import time
from datetime import datetime, timezone
from typing import Optional


def _parse_ts(value: str) -> int:
    """Parse a UTC datetime string to a UTC Unix timestamp."""
    # calendar.timegm interprets the struct as UTC (unlike time.mktime which uses local time).
    import calendar
    return calendar.timegm(time.strptime(value, "%Y-%m-%d %H:%M:%S"))


def _to_trade_type(market_type: str) -> str:
    mt = market_type.lower()
    if mt == "spot":
        return "SPOT"
    if mt == "futures":
        return "FUTURES"
    raise ValueError("market_type must be 'spot' or 'futures'")


def fetch_kucoin_candles_chunk(symbol, market_type="spot", timeframe="1day", start_time=None, end_time=None):
    time.sleep(0.2)
    url = "https://api.kucoin.com/api/ua/v1/market/kline"
    params = {
        "tradeType": _to_trade_type(market_type),
        "symbol": symbol.upper(),
        "interval": timeframe,
    }
    if start_time:
        params["startAt"] = _parse_ts(start_time)
    if end_time:
        params["endAt"] = _parse_ts(end_time)

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != "200000":
        raise RuntimeError(f"KuCoin API error: {data}")
    payload = data.get("data", [])
    if isinstance(payload, dict):
        return payload.get("list", [])
    return payload


def fetch_all_kucoin_candles(symbol, market_type="spot", timeframe="1day", start_time=None, end_time=None):
    if not (start_time and end_time):
        raise ValueError("start_time and end_time are required")

    chunks = []
    current_end = end_time
    start_ts = _parse_ts(start_time)
    end_ts = _parse_ts(end_time)

    while True:
        chunk = fetch_kucoin_candles_chunk(symbol, market_type, timeframe, start_time, current_end)
        if not chunk:
            break

        earliest_ts = int(chunk[-1][0])
        chunks.extend(chunk)

        if earliest_ts <= start_ts:
            break

        current_end = datetime.fromtimestamp(earliest_ts - 60, timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    if not chunks:
        return pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])

    candles = [c for c in chunks if start_ts <= int(c[0]) <= end_ts]
    candles.sort(key=lambda x: int(x[0]))

    # UTA kline format: [timestamp, open, high, low, close, volume, turnover]
    df = pd.DataFrame(candles, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume", "Turnover"])
    df["Date"] = pd.to_datetime(df["Timestamp"].astype(int), unit="s", utc=True)
    df = df.set_index("Date")
    df = df.astype({"Open": float, "High": float, "Low": float, "Close": float, "Volume": float})
    return df[["Open", "High", "Low", "Close", "Volume"]]


def get_kucoin_candles_df(
    symbol="BTC-USDT",
    market_type="spot",
    timeframe="1day",
    start_time="2026-02-01 00:00:00",
    end_time=None,
):
    if end_time is None:
        end_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return fetch_all_kucoin_candles(symbol, market_type, timeframe, start_time, end_time)


def get_kucoin_futures_candles_df(
    symbol="XBTUSDTM",
    timeframe="1day",
    start_time="2026-02-01 00:00:00",
    end_time=None,
):
    return get_kucoin_candles_df(
        symbol=symbol,
        market_type="futures",
        timeframe=timeframe,
        start_time=start_time,
        end_time=end_time,
    )


def get_kucoin_spot_candles_df(
    symbol="BTC-USDT",
    timeframe="1day",
    start_time="2026-02-01 00:00:00",
    end_time=None,
):
    return get_kucoin_candles_df(
        symbol=symbol,
        market_type="spot",
        timeframe=timeframe,
        start_time=start_time,
        end_time=end_time,
    )


def load_ohlcv_kucoin(
    symbol: str = "XBTUSDTM",
    market_type: str = "futures",
    timeframe: str = "1day",
    start_time: str = "2026-02-01 00:00:00",
    end_time: Optional[str] = None,
) -> pd.DataFrame:
    return get_kucoin_candles_df(
        symbol=symbol,
        market_type=market_type,
        timeframe=timeframe,
        start_time=start_time,
        end_time=end_time,
    )


if __name__ == "__main__":
    # Example: fetch futures data via function call (import-friendly API).
    df = get_kucoin_futures_candles_df()
    print(df.head())
    print(f"Loaded {len(df)} candles")


