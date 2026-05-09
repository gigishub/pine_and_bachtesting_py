"""
Lower high formation trigger: current high < prior high, close < open.

Signals failed rally attempt within a pullback context.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when lower high forms and close is bearish."""
    prev_high = df["high"].shift(1)
    lower_high = df["high"] < prev_high
    bearish_close = df["close"] < df["open"]
    return (lower_high & bearish_close).fillna(False)
