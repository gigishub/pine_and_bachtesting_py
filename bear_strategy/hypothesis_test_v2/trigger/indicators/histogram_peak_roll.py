"""
Histogram peak roll trigger: MACD histogram turns down while still positive.

Early warning — fires before MACD line crosses signal.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when histogram peaks (turns down while positive)."""
    try:
        import pandas_ta as pta
    except ImportError as exc:
        raise ImportError("pandas_ta is required for histogram_peak_roll; install with: pip install pandas-ta") from exc

    fast = int(params.get("fast_period", 12))
    slow = int(params.get("slow_period", 26))
    signal_period = int(params.get("signal_period", 9))
    
    macd_df = pta.macd(df["close"], fast=fast, slow=slow, signal=signal_period)
    
    hist_col = f"MACDh_{fast}_{slow}_{signal_period}"
    if hist_col not in macd_df.columns:
        raise ValueError(f"MACD histogram column '{hist_col}' not found")
    
    histogram = macd_df[hist_col]
    
    still_positive = histogram > 0
    turning_down = histogram < histogram.shift(1)
    
    return (still_positive & turning_down).fillna(False)
