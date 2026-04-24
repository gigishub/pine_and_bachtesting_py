from __future__ import annotations

import pandas as pd

from .fetch_bybit_candles import fetch_all_bybit_candles

# Map user-friendly aliases to the canonical short form expected by fetch_bybit_candles
_TF_ALIASES: dict[str, str] = {
    "1min": "1m",
    "5min": "5m",
    "15min": "15m",
    "30min": "30m",
    "1hour": "1h",
    "4hour": "4h",
    "1day": "1d",
    "3day": "3d",
    "1week": "1w",
}


def normalize_timeframe(tf: str) -> str:
    """Normalise a timeframe string to the canonical short form (e.g. '15min' → '15m')."""
    return _TF_ALIASES.get(tf.strip().lower(), tf.strip().lower())


def fetch_ohlcv(
    symbol: str,
    tf: str,
    start_time: str,
    end_time: str,
    market_type: str = "linear",
) -> pd.DataFrame:
    """Fetch OHLCV candles for a single symbol + timeframe from Bybit."""
    return fetch_all_bybit_candles(
        symbol=symbol,
        market_type=market_type,
        timeframe=normalize_timeframe(tf),
        start_time=start_time,
        end_time=end_time,
    )
