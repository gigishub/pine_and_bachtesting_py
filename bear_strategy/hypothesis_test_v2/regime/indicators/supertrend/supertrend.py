"""
supertrend — Regime indicator.

What it measures
----------------
Supertrend direction based on ATR bands.
For bear regime, the signal is True when the close is below the Supertrend line.

Parameters
----------
atr_period : int
    ATR lookback period. Default 10.
multiplier : float
    ATR multiplier for the Supertrend band. Default 3.0.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = close < Supertrend line.
False = close >= Supertrend line, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd


def _atr(df: pd.DataFrame, period: int) -> pd.Series:
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift(1)).abs()
    low_close = (df["low"] - df["close"].shift(1)).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return true_range.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    atr_period: int = int(params.get("atr_period", 10))
    multiplier: float = float(params.get("multiplier", 3.0))

    hl2 = (df["high"] + df["low"]) / 2
    atr = _atr(df, atr_period)

    basic_upper = hl2 + multiplier * atr
    basic_lower = hl2 - multiplier * atr

    final_upper = basic_upper.copy()
    final_lower = basic_lower.copy()
    trend = pd.Series(index=df.index, dtype=bool)
    supertrend = pd.Series(index=df.index, dtype=float)

    for i in range(1, len(df)):
        if basic_upper.iat[i] < final_upper.iat[i - 1] or df["close"].iat[i - 1] > final_upper.iat[i - 1]:
            final_upper.iat[i] = basic_upper.iat[i]
        else:
            final_upper.iat[i] = max(basic_upper.iat[i], final_upper.iat[i - 1])

        if basic_lower.iat[i] > final_lower.iat[i - 1] or df["close"].iat[i - 1] < final_lower.iat[i - 1]:
            final_lower.iat[i] = basic_lower.iat[i]
        else:
            final_lower.iat[i] = min(basic_lower.iat[i], final_lower.iat[i - 1])

        if df["close"].iat[i] > final_upper.iat[i - 1]:
            trend.iat[i] = True
        elif df["close"].iat[i] < final_lower.iat[i - 1]:
            trend.iat[i] = False
        else:
            trend.iat[i] = trend.iat[i - 1]

        supertrend.iat[i] = final_upper.iat[i] if not trend.iat[i] else final_lower.iat[i]

    return (df["close"] < supertrend).fillna(False)
