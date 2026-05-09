"""
Price action trigger: close below prior bar low.

Fires when current bar closes below the previous bar's low.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when close is below prior bar low."""
    prev_low = df["low"].shift(1)
    return (df["close"] < prev_low).fillna(False)
