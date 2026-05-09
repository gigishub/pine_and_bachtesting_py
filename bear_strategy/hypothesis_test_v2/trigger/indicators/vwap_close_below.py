"""
Volume-weighted close below daily VWAP trigger.

Fires when close is below the current session VWAP.
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
    """Return True when close is below daily VWAP."""
    if "volume" not in df.columns:
        raise ValueError("VWAP trigger requires a volume column in the input DataFrame")

    vwap = _daily_vwap(df)
    return (df["close"] < vwap).fillna(False)
