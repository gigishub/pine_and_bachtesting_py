"""Unified OHLCV fetch interface.

Supported sources: 'kucoin', 'bybit'.
Both return a DataFrame with columns: Open, High, Low, Close, Volume
and a DatetimeIndex named 'Date'.
"""

from __future__ import annotations

import pandas as pd

from .fetch_kucoin_candles import load_ohlcv_kucoin
from .fetch_bybit_candles import load_ohlcv_bybit


def load_ohlcv(
    source: str = "kucoin",
    *,
    symbol: str,
    market_type: str = "futures",
    timeframe: str = "1day",
    start_time: str = "2020-03-25 00:00:00",
    end_time: str | None = None,
) -> pd.DataFrame:
    """Fetch OHLCV candles from the specified exchange source.

    Args:
        source:      'kucoin' or 'bybit'
        symbol:      e.g. 'XBTUSDTM' (KuCoin) or 'BTCUSDT' (Bybit)
        market_type: 'spot', 'futures', 'linear', 'inverse'
        timeframe:   e.g. '1day', '4hour', '1h'
        start_time:  UTC string 'YYYY-MM-DD HH:MM:SS'
        end_time:    UTC string or None (→ now)

    Returns:
        DataFrame with DatetimeIndex and OHLCV columns.
    """
    src = source.lower().strip()

    if not isinstance(start_time, str):
        raise ValueError("start_time must be a string")

    if src == "kucoin":
        return load_ohlcv_kucoin(
            symbol=symbol,
            market_type=market_type,
            timeframe=timeframe,
            start_time=start_time,
            end_time=end_time,
        )
    elif src == "bybit":
        return load_ohlcv_bybit(
            symbol=symbol,
            market_type=market_type,
            timeframe=timeframe,
            start_time=start_time,
            end_time=end_time,
        )
    else:
        raise ValueError(f"Unknown source: {source!r}. Choose 'kucoin' or 'bybit'.")
