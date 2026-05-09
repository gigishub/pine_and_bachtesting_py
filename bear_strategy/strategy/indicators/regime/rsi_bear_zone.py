"""RSI bear-zone regime computation.

True when both the raw RSI and its EMA are inside (lower, upper).
This mirrors the hypothesis_test_v2 rsi_bear_zone indicator exactly.
"""

from __future__ import annotations

import pandas as pd


def _compute_rsi(close: pd.Series, period: int) -> pd.Series:
    delta = close.diff()
    gain  = delta.clip(lower=0).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    loss  = (-delta.clip(upper=0)).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs    = gain / loss.replace(0, float("nan"))
    return 100 - (100 / (1 + rs))


def compute_rsi_bear_zone(
    df: pd.DataFrame,
    rsi_period: int = 14,
    ma_period: int = 9,
    lower: float = 30.0,
    upper: float = 50.0,
) -> pd.Series:
    """Return True when RSI and its EMA are both inside (lower, upper).

    Args:
        df:         OHLCV DataFrame with a 'close' column.
        rsi_period: RSI lookback period.
        ma_period:  EMA smoothing period applied to the RSI.
        lower:      Lower bound of the bearish zone (exclusive).
        upper:      Upper bound of the bearish zone (exclusive).

    Returns:
        Boolean Series on df.index.
    """
    rsi    = _compute_rsi(df["close"], rsi_period)
    rsi_ma = rsi.ewm(span=ma_period, adjust=False).mean()

    in_zone = (rsi > lower) & (rsi < upper) & (rsi_ma > lower) & (rsi_ma < upper)
    return in_zone.fillna(False)
