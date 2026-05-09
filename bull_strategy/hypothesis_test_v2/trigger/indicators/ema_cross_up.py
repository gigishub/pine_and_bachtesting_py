"""
ema_cross_up — Trigger indicator.

What it measures
----------------
A fast EMA crossing above a slow EMA signals that short-term momentum has
turned bullish.  This is a classic entry trigger: after the regime (trend) and
setup (structure) conditions are met, the EMA cross provides a specific bar to
enter the long trade with a defined momentum shift.

Why a cross rather than position
---------------------------------
Simply "fast above slow" can mean price is already well into a move — the edge
may already be spent.  A *cross event* (the bar the cross occurs on) captures
the inflection point, giving both a precise entry timing and a cleaner stop
placement (just below the cross bar's low).

Parameters
----------
fast_period : int
    Lookback for the fast EMA.  Default 8.
    Lower → more sensitive, more crosses; higher → fewer, higher conviction.

slow_period : int
    Lookback for the slow EMA.  Default 21.
    Should always be larger than fast_period.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = on THIS bar the fast EMA crossed above the slow EMA (cross event only).
False = no cross, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True only on bars where the fast EMA crosses above the slow EMA.

    Parameters
    ----------
    df:     OHLCV DataFrame with a 'close' column.
    params: {"fast_period": int, "slow_period": int}
    """
    fast: int = params["fast_period"]
    slow: int = params["slow_period"]

    ema_fast = df["close"].ewm(span=fast, adjust=False).mean()
    ema_slow = df["close"].ewm(span=slow, adjust=False).mean()

    # Cross event: fast was <= slow on previous bar, now fast > slow.
    was_below_or_equal = (ema_fast.shift(1) <= ema_slow.shift(1))
    now_above          = (ema_fast > ema_slow)

    return (was_below_or_equal & now_above).fillna(False)
