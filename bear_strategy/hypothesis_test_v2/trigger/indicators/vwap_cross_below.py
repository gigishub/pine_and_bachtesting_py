"""
VWAP cross trigger: price crosses below daily VWAP (instead of just being below).

Tighter entry signal — catches the break rather than the sustained state.
"""
from __future__ import annotations

import pandas as pd


def _daily_vwap(df: pd.DataFrame) -> pd.Series:
    typical_price = (df["high"] + df["low"] + df["close"]) / 3
    tp_vol = typical_price * df["volume"]
    anchor = df.index.normalize()
    cum_tp_vol = tp_vol.groupby(anchor).cumsum()
    cum_vol = df["volume"].groupby(anchor).cumsum()
    return (cum_tp_vol / cum_vol).rename("daily_vwap")


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when close crosses below daily VWAP."""
    if "volume" not in df.columns:
        raise ValueError("VWAP trigger requires a volume column in the input DataFrame")

    vwap = _daily_vwap(df)
    prev_close = df["close"].shift(1)
    cross_below = (prev_close >= vwap.shift(1)) & (df["close"] < vwap)
    
    return cross_below.fillna(False)
