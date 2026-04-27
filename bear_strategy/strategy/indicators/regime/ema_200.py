"""EMA indicator for regime detection.

Computes an exponential moving average of the closing price.
"""

from __future__ import annotations

import pandas as pd


def compute_ema(df: pd.DataFrame, period: int) -> pd.Series:
    """Return EMA of ``df['Close']`` over ``period`` bars.

    The first (period - 1) values are NaN while the EMA warms up.

    Args:
        df: OHLCV DataFrame with a 'Close' column.
        period: EMA lookback (e.g. 200 for the 200-day EMA).

    Returns:
        pd.Series aligned to df's index, dtype float64.
    """
    return df["Close"].ewm(span=period, adjust=False).mean()
