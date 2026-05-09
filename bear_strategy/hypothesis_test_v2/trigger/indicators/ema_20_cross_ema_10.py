"""
ema_20_cross_ema_10 — Trigger indicator.

What it measures
----------------
EMA 20 crossing below EMA 10 — momentum pullback after a rally, or 
confirmation of weakening uptrend.  Used as entry confirmation for 
short positions within a confirmed regime + setup.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = EMA 20 just crossed below EMA 10 on this bar.
False = no cross, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True on bars where EMA 20 crosses below EMA 10.

    Parameters
    ----------
    df:     OHLCV DataFrame with a 'close' column.
    params: {"fast_period": int, "slow_period": int}
    """
    fast_period: int = int(params.get("fast_period", 10))
    slow_period: int = int(params.get("slow_period", 20))

    ema_fast = df["close"].ewm(span=fast_period, adjust=False).mean()
    ema_slow = df["close"].ewm(span=slow_period, adjust=False).mean()

    # Cross below: previous bar had slow >= fast, current bar has slow < fast
    was_above = ema_slow.shift(1) >= ema_fast.shift(1)
    is_below = ema_slow < ema_fast

    return (was_above & is_below).fillna(False)
