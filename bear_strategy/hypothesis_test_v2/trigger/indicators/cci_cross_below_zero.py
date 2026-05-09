"""
CCI cross below zero trigger: CCI crosses from positive to negative.

Signals transition from above-average to below-average momentum.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when CCI crosses below zero from positive."""
    try:
        import pandas_ta as pta
    except ImportError as exc:
        raise ImportError("pandas_ta is required for cci_cross_zero; install with: pip install pandas-ta") from exc

    length = int(params.get("length", 20))
    
    cci_df = pta.cci(high=df["high"], low=df["low"], close=df["close"], length=length)
    
    # Extract CCI column (usually named CCI_<length>)
    if isinstance(cci_df, pd.DataFrame):
        cci_cols = [c for c in cci_df.columns if c.startswith("CCI_")]
        if not cci_cols:
            return pd.Series(False, index=df.index)
        cci = cci_df[cci_cols[0]]
    else:
        cci = cci_df
    
    prev_cci = cci.shift(1)
    cross_below_zero = (prev_cci >= 0) & (cci < 0)
    
    return cross_below_zero.fillna(False)
