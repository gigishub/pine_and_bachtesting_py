"""Low-level Bybit V5 open interest fetcher.

Mirrors the structure of fetch_bybit_funding_rates.py.
Endpoint: GET /v5/market/open-interest
  - Requires intervalTime: '5min', '15min', '30min', '1h', '4h', '1d'.
  - Returns up to 200 records per call, newest-first.
  - Uses cursor-based pagination via the nextPageCursor field.
"""
from __future__ import annotations

import logging
import time

import pandas as pd
import requests

logger = logging.getLogger(__name__)

_BASE_URL = "https://api.bybit.com/v5/market/open-interest"
_RATE_LIMIT_CODE = 10006
_MAX_RETRIES = 5
_RETRY_BACKOFF_BASE = 2.0  # seconds; doubles each attempt

# Maps common short-form aliases to Bybit's intervalTime strings
_INTERVAL_MAP: dict[str, str] = {
    "5m": "5min",
    "5min": "5min",
    "15m": "15min",
    "15min": "15min",
    "30m": "30min",
    "30min": "30min",
    "1h": "1h",
    "1hour": "1h",
    "4h": "4h",
    "4hour": "4h",
    "1d": "1d",
    "1day": "1d",
}


def _parse_ts(value: str) -> int:
    """Parse a UTC datetime string to a Unix timestamp in milliseconds."""
    import calendar

    return calendar.timegm(time.strptime(value, "%Y-%m-%d %H:%M:%S")) * 1000


def normalize_oi_interval(interval: str) -> str:
    """Normalise an interval alias to Bybit's intervalTime string, e.g. '1h' → '1h'."""
    key = interval.strip().lower()
    if key not in _INTERVAL_MAP:
        raise ValueError(
            f"Unsupported OI interval '{interval}'. "
            f"Choose from: {sorted(_INTERVAL_MAP)}"
        )
    return _INTERVAL_MAP[key]


def fetch_open_interest_chunk(
    symbol: str,
    interval: str = "1h",
    category: str = "linear",
    start_time_ms: int | None = None,
    end_time_ms: int | None = None,
    cursor: str = "",
    limit: int = 200,
) -> tuple[list[dict], str]:
    """Fetch a single page of open interest data.

    Args:
        symbol:       Bybit symbol, e.g. 'BTCUSDT'.
        interval:     Bybit intervalTime string, e.g. '1h'.
        category:     'linear' or 'inverse'.
        start_time_ms: Start timestamp in milliseconds.
        end_time_ms:   End timestamp in milliseconds.
        cursor:       Pagination cursor from previous response ('nextPageCursor').
        limit:        Records per page, 1–200.

    Returns:
        Tuple of (records list, next_cursor string).
        next_cursor is empty when there are no more pages.
    """
    time.sleep(0.25)  # courtesy pause to respect Bybit rate limits

    params: dict[str, str | int] = {
        "category": category,
        "symbol": symbol.upper(),
        "intervalTime": interval,
        "limit": limit,
    }
    if start_time_ms is not None:
        params["startTime"] = start_time_ms
    if end_time_ms is not None:
        params["endTime"] = end_time_ms
    if cursor:
        params["cursor"] = cursor

    for attempt in range(_MAX_RETRIES):
        try:
            resp = requests.get(_BASE_URL, params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as exc:
            wait = _RETRY_BACKOFF_BASE * (2**attempt)
            logger.warning(
                "Network error for %s OI (attempt %d/%d): %s. Retrying in %.1fs.",
                symbol,
                attempt + 1,
                _MAX_RETRIES,
                exc,
                wait,
            )
            if attempt < _MAX_RETRIES - 1:
                time.sleep(wait)
                continue
            raise

        ret_code = data.get("retCode") or data.get("ret_code")

        if ret_code == _RATE_LIMIT_CODE:
            wait = _RETRY_BACKOFF_BASE * (2**attempt)
            logger.warning(
                "Bybit rate limit hit for %s OI (attempt %d/%d). Waiting %.1fs.",
                symbol,
                attempt + 1,
                _MAX_RETRIES,
                wait,
            )
            time.sleep(wait)
            continue

        if ret_code not in (0, None):
            raise RuntimeError(f"Bybit API error for {symbol} OI: {data}")

        result = data.get("result", {})
        records = result.get("list", [])
        next_cursor = result.get("nextPageCursor", "")
        return records, next_cursor

    raise RuntimeError(
        f"Bybit API not resolved after {_MAX_RETRIES} retries for {symbol} OI"
    )


def fetch_all_open_interest(
    symbol: str,
    interval: str = "1h",
    category: str = "linear",
    start_time: str | None = None,
    end_time: str | None = None,
) -> pd.DataFrame:
    """Fetch the full open interest history for *symbol* over the requested range.

    Uses cursor-based pagination: each response provides a nextPageCursor that
    is passed into the following request until the cursor is exhausted.

    Args:
        symbol:     Bybit symbol, e.g. 'BTCUSDT'.
        interval:   Interval alias, e.g. '1h', '4h', '1d'.
        category:   'linear' or 'inverse'.
        start_time: UTC datetime string 'YYYY-MM-DD HH:MM:SS'.
        end_time:   UTC datetime string 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        DataFrame indexed by UTC datetime with a single 'openInterest' float column.
    """
    if not (start_time and end_time):
        raise ValueError("start_time and end_time are required")

    interval_norm = normalize_oi_interval(interval)
    start_ms = _parse_ts(start_time)
    end_ms = _parse_ts(end_time)

    records: list[dict] = []
    cursor = ""

    while True:
        chunk, next_cursor = fetch_open_interest_chunk(
            symbol=symbol,
            interval=interval_norm,
            category=category,
            start_time_ms=start_ms,
            end_time_ms=end_ms,
            cursor=cursor,
            limit=200,
        )
        if not chunk:
            break

        records.extend(chunk)

        # Stop when there are no more pages.
        if not next_cursor:
            break

        cursor = next_cursor

    if not records:
        return pd.DataFrame(columns=["openInterest"])

    df = pd.DataFrame(records)
    df["timestamp"] = df["timestamp"].astype(int)
    df["openInterest"] = df["openInterest"].astype(float)
    df = df.drop_duplicates(subset=["timestamp"], keep="last")
    df = df.sort_values("timestamp")

    # Clip to the requested range.
    df = df[
        (df["timestamp"] >= start_ms)
        & (df["timestamp"] <= end_ms)
    ]

    df["Date"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df = df.set_index("Date")
    return df[["openInterest"]]
