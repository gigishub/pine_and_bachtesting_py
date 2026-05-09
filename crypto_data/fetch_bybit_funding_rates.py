"""Low-level Bybit V5 funding rate fetcher.

Mirrors the structure of fetch_bybit_candles.py.
Endpoint: GET /v5/market/funding/history
  - Returns up to 200 records per call, newest-first.
  - startTime alone is not allowed; always pass both startTime and endTime.
"""
from __future__ import annotations

import logging
import time
from datetime import datetime, timezone

import pandas as pd
import requests

logger = logging.getLogger(__name__)

_BASE_URL = "https://api.bybit.com/v5/market/funding/history"
_RATE_LIMIT_CODE = 10006
_MAX_RETRIES = 5
_RETRY_BACKOFF_BASE = 2.0  # seconds; doubles each attempt


def _parse_ts(value: str) -> int:
    """Parse a UTC datetime string to a Unix timestamp in milliseconds."""
    import calendar

    return calendar.timegm(time.strptime(value, "%Y-%m-%d %H:%M:%S")) * 1000


def fetch_funding_rates_chunk(
    symbol: str,
    category: str = "linear",
    start_time_ms: int | None = None,
    end_time_ms: int | None = None,
    limit: int = 200,
) -> list[dict]:
    """Fetch a single page (up to 200 records) of funding rate history.

    The API returns records in descending timestamp order (newest first).

    Args:
        symbol:       Bybit symbol, e.g. 'BTCUSDT'.
        category:     'linear' or 'inverse'.
        start_time_ms: Start timestamp in milliseconds (inclusive).
        end_time_ms:   End timestamp in milliseconds (inclusive).
        limit:        Max records per page, 1–200.

    Returns:
        List of raw record dicts with keys: symbol, fundingRate, fundingRateTimestamp.
    """
    time.sleep(0.25)  # courtesy pause to respect Bybit rate limits

    params: dict[str, str | int] = {
        "category": category,
        "symbol": symbol.upper(),
        "limit": limit,
    }
    if start_time_ms is not None:
        params["startTime"] = start_time_ms
    if end_time_ms is not None:
        params["endTime"] = end_time_ms

    for attempt in range(_MAX_RETRIES):
        try:
            resp = requests.get(_BASE_URL, params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as exc:
            wait = _RETRY_BACKOFF_BASE * (2**attempt)
            logger.warning(
                "Network error for %s funding (attempt %d/%d): %s. Retrying in %.1fs.",
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
                "Bybit rate limit hit for %s funding (attempt %d/%d). Waiting %.1fs.",
                symbol,
                attempt + 1,
                _MAX_RETRIES,
                wait,
            )
            time.sleep(wait)
            continue

        if ret_code not in (0, None):
            raise RuntimeError(f"Bybit API error for {symbol} funding: {data}")

        result = data.get("result", {})
        return result.get("list", [])

    raise RuntimeError(
        f"Bybit API not resolved after {_MAX_RETRIES} retries for {symbol} funding"
    )


def fetch_all_funding_rates(
    symbol: str,
    category: str = "linear",
    start_time: str | None = None,
    end_time: str | None = None,
) -> pd.DataFrame:
    """Fetch the full funding rate history for *symbol* over the requested range.

    Paginates backwards in time: each call moves the end pointer to just before
    the oldest record in the previous batch, until coverage reaches start_time.

    Args:
        symbol:     Bybit symbol, e.g. 'BTCUSDT'.
        category:   'linear' or 'inverse'.
        start_time: UTC datetime string 'YYYY-MM-DD HH:MM:SS'.
        end_time:   UTC datetime string 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        DataFrame indexed by UTC datetime with a single 'fundingRate' float column.
    """
    if not (start_time and end_time):
        raise ValueError("start_time and end_time are required")

    start_ms = _parse_ts(start_time)
    end_ms = _parse_ts(end_time)

    records: list[dict] = []
    current_end_ms = end_ms

    while True:
        chunk = fetch_funding_rates_chunk(
            symbol=symbol,
            category=category,
            start_time_ms=start_ms,
            end_time_ms=current_end_ms,
            limit=200,
        )
        if not chunk:
            break

        records.extend(chunk)

        # Response is newest-first; oldest record is last in the list.
        oldest_ts = int(chunk[-1]["fundingRateTimestamp"])

        # Full range covered — stop.
        if oldest_ts <= start_ms:
            break

        # Move end pointer to just before the oldest record and fetch the next page.
        current_end_ms = oldest_ts - 1

        # A partial page means there is no more history before this point.
        if len(chunk) < 200:
            break

    if not records:
        return pd.DataFrame(columns=["fundingRate"])

    df = pd.DataFrame(records)
    df["fundingRateTimestamp"] = df["fundingRateTimestamp"].astype(int)
    df["fundingRate"] = df["fundingRate"].astype(float)
    df = df.drop_duplicates(subset=["fundingRateTimestamp"], keep="last")
    df = df.sort_values("fundingRateTimestamp")

    # Clip to the requested range (the last page may overshoot start_ms slightly).
    df = df[
        (df["fundingRateTimestamp"] >= start_ms)
        & (df["fundingRateTimestamp"] <= end_ms)
    ]

    df["Date"] = pd.to_datetime(df["fundingRateTimestamp"], unit="ms", utc=True)
    df = df.set_index("Date")
    return df[["fundingRate"]]
