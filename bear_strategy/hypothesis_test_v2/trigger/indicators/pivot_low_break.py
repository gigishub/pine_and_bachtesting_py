"""
Pivot low break trigger: price breaks below recent swing low.

Highest confidence structure-based entry.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when close breaks below recent swing low (pivot)."""
    lookback = int(params.get("lookback", 5))
    
    # Find pivot low: lowest low in prior lookback bars (no look-ahead)
    pivot_low = df["low"].shift(1).rolling(window=lookback).min()
    
    # Break: close below the pivot
    break_below = df["close"] < pivot_low
    
    return break_below.fillna(False)
