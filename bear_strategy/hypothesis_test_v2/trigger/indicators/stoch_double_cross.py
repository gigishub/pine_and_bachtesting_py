"""
Stochastic %K and %D double cross trigger: %K crosses below %D, both below 50.

Confirms bearish momentum while staying in bearish zone.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when %K crosses %D from above while both below 50."""
    try:
        import pandas_ta as pta
    except ImportError as exc:
        raise ImportError("pandas_ta is required for stoch_double_cross; install with: pip install pandas-ta") from exc

    k_period = int(params.get("k_period", 14))
    d_period = int(params.get("d_period", 3))
    smooth_k = int(params.get("smooth_k", 3))
    
    stoch = pta.stoch(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        k=k_period,
        d=d_period,
        smooth_k=smooth_k,
    )
    
    k_col = f"STOCHk_{k_period}_{d_period}_{smooth_k}"
    d_col = f"STOCHd_{k_period}_{d_period}_{smooth_k}"
    
    if k_col not in stoch.columns or d_col not in stoch.columns:
        raise ValueError(f"Stoch columns not found: {k_col}, {d_col}")
    
    k = stoch[k_col]
    d = stoch[d_col]
    
    # Both below 50
    both_below_50 = (k < 50) & (d < 50)
    
    # %K crosses below %D
    prev_k = k.shift(1)
    prev_d = d.shift(1)
    k_cross_d = (prev_k >= prev_d) & (k < d)
    
    return (both_below_50 & k_cross_d).fillna(False)
