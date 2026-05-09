"""
TRIX cross trigger: TRIX crosses below signal line while TRIX still positive.

Catches rollover from a peak — exhaustion signal.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when TRIX crosses below signal while TRIX > 0."""
    try:
        import pandas_ta as pta
    except ImportError as exc:
        raise ImportError("pandas_ta is required for trix_cross; install with: pip install pandas-ta") from exc

    length = int(params.get("length", 15))
    signal_length = int(params.get("signal_length", 9))
    
    trix_df = pta.trix(df["close"], length=length, signal=signal_length)
    
    # Find TRIX and Signal columns dynamically (pandas_ta naming varies)
    trix_cols = [c for c in trix_df.columns if c.startswith("TRIX_")]
    signal_cols = [c for c in trix_df.columns if c.startswith("TRIXs_")]
    
    if not trix_cols or not signal_cols:
        return pd.Series(False, index=df.index)
    
    trix_line = trix_df[trix_cols[0]]
    signal_line = trix_df[signal_cols[0]]
    
    trix_positive = trix_line > 0
    prev_trix = trix_line.shift(1)
    prev_signal = signal_line.shift(1)
    cross_below = (prev_trix >= prev_signal) & (trix_line < signal_line)
    
    return (trix_positive & cross_below).fillna(False)
