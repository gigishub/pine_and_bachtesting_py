"""Unified OHLCV fetch interface.

Supported sources: 'kucoin', 'bybit'.
Both return a DataFrame with columns: Open, High, Low, Close, Volume
and a DatetimeIndex named 'Date'.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

import pandas as pd

from .fetch_kucoin_candles import load_ohlcv_kucoin
from .fetch_bybit_candles import load_ohlcv_bybit

logger = logging.getLogger(__name__)

# Cache lives next to this file: UPS_py_v2/data/cache/
_CACHE_DIR = Path(__file__).parent / "cache"


def _cache_path(source: str, symbol: str, market_type: str, timeframe: str,
                start_time: str, end_time: str | None) -> Path:
    """Deterministic parquet filename from fetch parameters."""
    key = f"{source}_{symbol}_{market_type}_{timeframe}_{start_time}_{end_time}"
    digest = hashlib.md5(key.encode()).hexdigest()[:12]
    safe_name = f"{source}_{symbol}_{timeframe}_{digest}.parquet"
    return _CACHE_DIR / safe_name


def load_ohlcv(
    source: str = "bybit",
    *,
    symbol: str,
    market_type: str = "futures",
    timeframe: str = "1day",
    start_time: str = "2020-03-25 00:00:00",
    end_time: str | None = None,
    use_cache: bool = True,
) -> pd.DataFrame:
    """Fetch OHLCV candles from the specified exchange source.

    Results are cached to disk as parquet on first fetch and reused on
    subsequent calls with identical parameters — no re-download needed.
    Pass use_cache=False to force a fresh download.

    Args:
        source:      'kucoin' or 'bybit'
        symbol:      e.g. 'XBTUSDTM' (KuCoin) or 'BTCUSDT' (Bybit)
        market_type: 'spot', 'futures', 'linear', 'inverse'
        timeframe:   e.g. '1day', '4hour', '1h'
        start_time:  UTC string 'YYYY-MM-DD HH:MM:SS'
        end_time:    UTC string or None (→ now)
        use_cache:   Load from disk if available; save after fresh download.

    Returns:
        DataFrame with DatetimeIndex and OHLCV columns.
    """
    src = source.lower().strip()

    if not isinstance(start_time, str):
        raise ValueError("start_time must be a string")

    cache_file = _cache_path(src, symbol, market_type, timeframe, start_time, end_time)

    if use_cache and cache_file.exists():
        logger.info("Cache hit: %s", cache_file.name)
        df = pd.read_parquet(cache_file)
        return df

    logger.info("Fetching %s %s %s from %s (no cache)...", symbol, timeframe, src, start_time)

    if src == "kucoin":
        df = load_ohlcv_kucoin(
            symbol=symbol,
            market_type=market_type,
            timeframe=timeframe,
            start_time=start_time,
            end_time=end_time,
        )
    elif src == "bybit":
        df = load_ohlcv_bybit(
            symbol=symbol,
            market_type=market_type,
            timeframe=timeframe,
            start_time=start_time,
            end_time=end_time,
        )
    else:
        raise ValueError(f"Unknown source: {source!r}. Choose 'kucoin' or 'bybit'.")

    if use_cache:
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        df.to_parquet(cache_file)
        logger.info("Cached to: %s", cache_file.name)

    return df
