"""
Falling tunnel trigger: both Bollinger Bands moving down together.

Entire price structure shifts down — more selective than single-band move.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when both BB bands are moving down."""
    try:
        import pandas_ta as pta
    except ImportError as exc:
        raise ImportError("pandas_ta is required for falling_tunnel; install with: pip install pandas-ta") from exc

    length = int(params.get("length", 20))
    std = float(params.get("std", 2.0))
    
    bb_df = pta.bbands(df["close"], length=length, std=std)
    
    # Find upper and lower band columns dynamically (pandas_ta naming varies)
    # Typically returns [middle, upper, lower] or similar
    bb_cols = sorted([c for c in bb_df.columns if c.startswith("BB")])
    
    if len(bb_cols) < 2:
        return pd.Series(False, index=df.index)
    
    # Usually upper is last, lower is first of BBands
    upper = bb_df[bb_cols[-1]]
    lower = bb_df[bb_cols[0]]
    
    upper_falling = upper < upper.shift(1)
    lower_falling = lower < lower.shift(1)
    
    return (upper_falling & lower_falling).fillna(False)
