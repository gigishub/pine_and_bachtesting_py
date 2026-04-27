"""EMA slope regime indicator.

Regime is confirmed bearish when the EMA is sloping downward — i.e. the
current EMA value is below its value ``slope_lookback`` bars ago.
Flat or rising EMAs are treated as non-bearish.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.strategy.indicators.regime.ema_200 import compute_ema


def compute_ema_slope_regime(
    df: pd.DataFrame,
    ema_period: int,
    slope_lookback: int = 1,
) -> pd.Series:
    """Return a boolean Series: True where EMA(ema_period) slope is negative.

    A negative slope means ema[i] < ema[i - slope_lookback], i.e. the EMA
    is declining — downtrend confirmed.  Flat (zero diff) is treated as
    non-bearish because it signals indecision, not distribution.

    Args:
        df: Daily OHLCV DataFrame with a 'Close' column.
        ema_period: EMA lookback in bars (e.g. 200, 150, 100).
        slope_lookback: Number of bars to look back when measuring slope.
            Default 1 is sufficient for long-period EMAs which are already
            heavily smoothed; increase for shorter EMAs if noise is a concern.

    Returns:
        Boolean pd.Series aligned to df's index.
        True = EMA is pointing down (bearish); False = flat or rising.
    """
    ema = compute_ema(df, ema_period)
    slope = ema.diff(slope_lookback)
    return (slope < 0).rename(f"ema_{ema_period}_slope_regime")
