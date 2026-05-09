"""
CMF cross below zero trigger: Chaikin Money Flow crosses from positive to negative.

Signals volume-weighted money flow flipped to distribution.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when CMF crosses below zero."""
    try:
        import pandas_ta as pta
    except ImportError as exc:
        raise ImportError("pandas_ta is required for cmf_cross_zero; install with: pip install pandas-ta") from exc

    length = int(params.get("length", 20))
    
    cmf = pta.cmf(high=df["high"], low=df["low"], close=df["close"], volume=df["volume"], length=length)
    
    prev_cmf = cmf.shift(1)
    cross_below_zero = (prev_cmf >= 0) & (cmf < 0)
    
    return cross_below_zero.fillna(False)
