"""
N-bar low break trigger: close below lowest close of last N bars.

Signals new lower level acceptance.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when close breaks below the N-bar low."""
    n = int(params.get("n", 5))
    lowest_close = df["close"].rolling(window=n).min()
    return (df["close"] < lowest_close.shift(1)).fillna(False)
