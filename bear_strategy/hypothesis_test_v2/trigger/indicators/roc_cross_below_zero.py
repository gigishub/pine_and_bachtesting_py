"""
ROC cross below zero trigger: Rate of Change crosses from positive to negative.

Signals velocity has turned negative — move has started.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when ROC crosses below zero."""
    try:
        import pandas_ta as pta
    except ImportError as exc:
        raise ImportError("pandas_ta is required for roc_cross_zero; install with: pip install pandas-ta") from exc

    length = int(params.get("length", 12))
    
    roc = pta.roc(df["close"], length=length)
    
    prev_roc = roc.shift(1)
    cross_below_zero = (prev_roc >= 0) & (roc < 0)
    
    return cross_below_zero.fillna(False)
