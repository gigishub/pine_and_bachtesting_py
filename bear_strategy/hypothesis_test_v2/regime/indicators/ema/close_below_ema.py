"""
close_below_ema — Regime indicator.

What it measures
----------------
Identifies bars where the closing price is below an Exponential Moving Average.
This is a classic bear-market regime gate: when price is beneath the EMA the
asset is considered to be in a downtrend structure suitable for short trades.

Why it matters
--------------
An EMA acts as a dynamic trend filter.  Entries taken only when close < EMA
tend to have directional tailwind — the trend is already pointing down.

Parameters
----------
period : int
    The EMA lookback in bars.  Common values: 50 (medium-term), 200 (long-term).
    - 50: captures intermediate-trend regime changes, faster to react.
    - 200: captures macro-regime only, slower to react but higher conviction.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = close is below the EMA → bear regime active.
False = close is above the EMA, or EMA is in warm-up (first `period` bars).
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True on bars where close < EMA(period).

    Parameters
    ----------
    df:     OHLCV DataFrame with a 'close' column.
    params: {"period": int}  — EMA lookback length.
    """
    period: int = params["period"]
    ema = df["close"].ewm(span=period, adjust=False).mean()
    # NaN during warm-up period → False (no signal until EMA is valid).
    return (df["close"] < ema).fillna(False)
