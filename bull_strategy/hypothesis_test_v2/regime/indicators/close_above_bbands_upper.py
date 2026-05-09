"""
close_above_bbands_upper — Regime indicator.

What it measures
----------------
True when the closing price breaks above the upper Bollinger Band.  A close
above the upper band indicates a volatility-driven breakout to the upside.
While statistically "overbought" in mean-reversion frameworks, in trending
markets this is a regime signal: momentum is strong enough to push into
expansion territory.

Parameters
----------
period : int
    Bollinger Band moving average period.  Default 20.
std_dev : float
    Number of standard deviations for the upper band.  Default 2.0.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = close > upper Bollinger Band.
False = close <= upper band, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when close is above the upper Bollinger Band."""
    period: int   = int(params.get("period", 20))
    std_dev: float = float(params.get("std_dev", 2.0))

    mid   = df["close"].rolling(period).mean()
    sigma = df["close"].rolling(period).std(ddof=0)
    upper = mid + std_dev * sigma

    return (df["close"] > upper).fillna(False)
