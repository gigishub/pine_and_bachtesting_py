"""
ema_dual_slope_up — Regime indicator.

What it measures
----------------
True when BOTH a fast EMA and a slow EMA are rising simultaneously.
Higher conviction than a single EMA slope: both the intermediate and macro
trends must be pointing up, filtering out short-lived bounces within a
broader downtrend.

Parameters
----------
fast_period : int
    Lookback for the faster EMA.  Default 50.
slow_period : int
    Lookback for the slower EMA.  Default 200.
    Should always be larger than fast_period.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = both EMAs are rising (slope > 0 on both).
False = either EMA is flat/falling, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when both EMA(fast_period) and EMA(slow_period) are rising."""
    fast: int = int(params["fast_period"])
    slow: int = int(params["slow_period"])

    ema_fast = df["close"].ewm(span=fast, adjust=False).mean()
    ema_slow = df["close"].ewm(span=slow, adjust=False).mean()

    fast_up = (ema_fast.diff() > 0).fillna(False)
    slow_up = (ema_slow.diff() > 0).fillna(False)

    return fast_up & slow_up
