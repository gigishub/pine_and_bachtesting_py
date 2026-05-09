"""
close_above_ema — Regime indicator.

What it measures
----------------
True when the closing price is above a given EMA.  A close above the EMA
indicates that price is in a bullish position relative to the average — the
regime is supportive of long trades.

Parameters
----------
period : int
    EMA lookback.  Common values: 50, 100, 200.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = close > EMA(period).
False = close <= EMA, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when close > EMA(period)."""
    period: int = int(params["period"])
    ema = df["close"].ewm(span=period, adjust=False).mean()
    return (df["close"] > ema).fillna(False)
