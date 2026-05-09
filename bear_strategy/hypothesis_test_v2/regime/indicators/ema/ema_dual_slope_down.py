"""
ema_dual_slope_down — Regime indicator.

What it measures
----------------
True when BOTH a fast EMA and a slow EMA are simultaneously declining
bar-over-bar.  This is a higher-conviction bearish regime signal than a
single-EMA slope: it requires the shorter-term trend AND the longer-term
trend to both be pointing down.

Why both slopes
---------------
A falling fast EMA alone can be a brief pullback inside a still-rising slow
trend (noise).  When the slow EMA also turns down, the macro trend has
confirmed the direction — regime is unambiguously bearish.

Parameters
----------
fast_period : int
    Fast EMA lookback (e.g. 50).
slow_period : int
    Slow EMA lookback (e.g. 200).  Must be > fast_period.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = BOTH fast EMA and slow EMA are declining (slope < 0 for both).
False = either EMA is flat/rising, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when both EMA(fast_period) and EMA(slow_period) are declining."""
    fast_period: int = int(params["fast_period"])
    slow_period: int = int(params["slow_period"])

    fast_ema = df["close"].ewm(span=fast_period, adjust=False).mean()
    slow_ema = df["close"].ewm(span=slow_period, adjust=False).mean()

    fast_slope_down = (fast_ema.diff() < 0).fillna(False)
    slow_slope_down = (slow_ema.diff() < 0).fillna(False)

    return fast_slope_down & slow_slope_down
