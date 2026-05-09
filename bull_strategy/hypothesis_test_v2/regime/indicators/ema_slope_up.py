"""
ema_slope_up — Regime indicator.

What it measures
----------------
True when a single EMA is rising bar-over-bar (current value > previous value).
A rising EMA means the trend is accelerating upward — the regime is bullish
regardless of where price sits relative to the EMA level.

Why slope instead of price-above-EMA
--------------------------------------
Price-above-EMA identifies *location* (where price is relative to the average).
EMA slope identifies *direction* (whether the average itself is moving up).
Slope is more responsive at turning points and filters out sideways/choppy
markets where price oscillates around a flat EMA.

Parameters
----------
period : int
    EMA lookback.  Common values: 50 (medium), 100 (slow), 200 (macro).

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = EMA is rising (slope > 0).
False = EMA is flat or falling, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when EMA(period) is rising on this bar."""
    period: int = int(params["period"])
    ema = df["close"].ewm(span=period, adjust=False).mean()
    # slope > 0 → EMA is rising; NaN during warm-up → False
    return (ema.diff() > 0).fillna(False)
