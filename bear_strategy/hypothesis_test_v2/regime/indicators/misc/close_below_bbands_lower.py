"""
close_below_bbands_lower — Regime indicator.

What it measures
----------------
Identifies bars where price closes below the lower Bollinger Band.
This is a strong bearish regime signal because it indicates volatility
and price pressure are both biased lower.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = close is below the lower BB.
False = close is above the lower BB or the band is still warming up.
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    period = int(params.get("period", 20))
    std_dev = float(params.get("std_dev", 2.0))

    rolling_mean = df["close"].rolling(window=period, min_periods=period).mean()
    rolling_std = df["close"].rolling(window=period, min_periods=period).std()
    lower_band = rolling_mean - std_dev * rolling_std

    return (df["close"] < lower_band).fillna(False)
