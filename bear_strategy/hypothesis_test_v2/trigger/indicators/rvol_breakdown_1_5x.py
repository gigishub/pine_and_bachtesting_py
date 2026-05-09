"""
rvol_breakdown_1.5x — Trigger indicator.

What it measures
----------------
Relative volume (RVOL) breakdown: flags bars where the current volume is
1.5× the rolling average — indicating a surge of selling activity that 
could accelerate a breakdown within a confirmed regime + setup.

Parameters
----------
period : int
    Rolling average lookback for volume. Default 20 bars.

threshold : float
    Multiplier above average. E.g. 1.5 means "volume is 1.5× the average".

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = current volume > threshold × rolling_avg_volume.
False = volume is normal, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True on bars where volume exceeds threshold × rolling average.

    Parameters
    ----------
    df:     OHLCV DataFrame with a 'volume' column.
    params: {"period": int, "threshold": float}
    """
    period: int = params.get("period", 20)
    threshold: float = params.get("threshold", 1.5)

    avg_vol = df["volume"].rolling(period, min_periods=period).mean()
    return (df["volume"] > threshold * avg_vol).fillna(False)
