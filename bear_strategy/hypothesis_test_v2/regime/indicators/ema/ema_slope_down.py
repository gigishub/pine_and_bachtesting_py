"""
ema_slope_down — Regime indicator.

What it measures
----------------
True when a single EMA is declining bar-over-bar (current value < previous
value).  A falling EMA means the trend is accelerating downward — the regime
is bearish regardless of where price sits relative to the EMA level.

Why slope instead of price-below-EMA
--------------------------------------
Price-below-EMA identifies *location* (where price is relative to the average).
EMA slope identifies *direction* (whether the average itself is moving down).
Slope is more responsive at turning points and filters out sideways/choppy
markets where price oscillates around a flat EMA.

Parameters
----------
period : int
    EMA lookback.  Common values: 50 (medium), 100 (slow), 200 (macro).

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = EMA is declining (slope < 0).
False = EMA is flat or rising, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when EMA(period) is declining on this bar."""
    period: int = int(params["period"])
    ema = df["close"].ewm(span=period, adjust=False).mean()
    # slope < 0 → EMA is falling; NaN during warm-up → False
    return (ema.diff() < 0).fillna(False)
