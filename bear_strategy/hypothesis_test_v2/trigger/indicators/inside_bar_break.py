"""
Inside bar break trigger: price breaks below the low of an inside bar.

Fires when a compressed bar's low is violated downward.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when bar breaks below a prior inside bar's low."""
    high_prev = df["high"].shift(1)
    low_prev = df["low"].shift(1)
    high_2ago = df["high"].shift(2)
    low_2ago = df["low"].shift(2)
    
    # Inside bar pattern: bar N-1 is inside bar N-2
    prev_is_inside = (high_prev <= high_2ago) & (low_prev >= low_2ago)
    
    # Break: current close breaks below the inside bar's low
    break_below = df["close"] < low_prev
    
    return (prev_is_inside & break_below).fillna(False)
