"""Unified OHLCV fetch interface.

Supported sources: 'kucoin', 'bybit'.
Both return a DataFrame with columns: Open, High, Low, Close, Volume
and a DatetimeIndex named 'Date'.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd

# Allow the underlying fetch modules (which still live in UPS_py) to be
# imported by adding the old package to sys.path if needed.
_UPS_PY_ROOT = Path(__file__).parents[2] / "UPS_py"


def _ensure_ups_py_on_path() -> None:
    entry = str(_UPS_PY_ROOT)
    if entry not in sys.path:
        sys.path.insert(0, entry)


def load_ohlcv(
    source: str = "kucoin",
    *,
    symbol: str,
    market_type: str = "futures",
    timeframe: str = "1day",
    start_time: str | None = "2020-03-25 00:00:00",
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
    _ensure_ups_py_on_path()
    src = source.lower().strip()

    if src == "kucoin":
        from fetch_data.fetch_kucoin_candles import load_ohlcv_kucoin
        return load_ohlcv_kucoin(
            symbol=symbol,
            market_type=market_type,
            timeframe=timeframe,
            start_time=start_time,
            end_time=end_time,
        )
    elif src == "bybit":
        from fetch_data.fetch_bybit_candles import load_ohlcv_bybit
        return load_ohlcv_bybit(
            symbol=symbol,
            market_type=market_type,
            timeframe=timeframe,
            start_time=start_time,
            end_time=end_time,
        )
    else:
        raise ValueError(f"Unknown source: {source!r}. Choose 'kucoin' or 'bybit'.")
