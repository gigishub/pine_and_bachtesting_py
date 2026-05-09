"""
Stochastic cross below threshold trigger.

Fires when %K crosses below a threshold, typically 50 or 80.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when %K crosses below a threshold."""
    try:
        import pandas_ta as pta
    except ImportError as exc:
        raise ImportError("pandas_ta is required for stoch_cross_below; install with: pip install pandas-ta") from exc

    k_period = int(params.get("k_period", 14))
    d_period = int(params.get("d_period", 3))
    smooth_k = int(params.get("smooth_k", 3))
    threshold = float(params.get("threshold", 50.0))

    stoch = pta.stoch(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        k=k_period,
        d=d_period,
        smooth_k=smooth_k,
    )

    k_col = f"STOCHk_{k_period}_{d_period}_{smooth_k}"
    if k_col not in stoch.columns:
        raise ValueError(f"Expected stochastic %K column '{k_col}' not found")

    k_line = stoch[k_col]
    prev_k = k_line.shift(1)
    cross_below = (prev_k >= threshold) & (k_line < threshold)

    return cross_below.fillna(False)
