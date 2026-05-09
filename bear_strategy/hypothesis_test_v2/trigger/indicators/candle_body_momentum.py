"""
Candle body momentum trigger: close in weak half of prior bar's range.

Signals continuation of downward pressure within pullback.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when close is below midpoint of prior bar's range."""
    high_prev = df["high"].shift(1)
    low_prev = df["low"].shift(1)
    midpoint = (high_prev + low_prev) / 2
    return (df["close"] < midpoint).fillna(False)
