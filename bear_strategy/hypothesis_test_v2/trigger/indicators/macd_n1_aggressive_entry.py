"""
MACD N1 (Aggressive Entry) Trigger: Histogram increased for 1+ bar, then decreases.

Signals immediate momentum reversal — fastest/most aggressive entry point.
"""
import pandas as pd
import pandas_ta as pta


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True when:
    - Histogram was higher previously: H[-2] < H[-1]
    - Current histogram decreases: H[0] < H[-1]
    
    Args:
        df: OHLCV DataFrame with 'close' column
        params: dict with optional keys:
            - fast_period: MACD fast period (default 12)
            - slow_period: MACD slow period (default 26)
            - signal_period: Signal line period (default 9)
    
    Returns:
        Boolean Series where True = 1-bar increase confirmed + current decrease
    """
    fast = int(params.get("fast_period", 12))
    slow = int(params.get("slow_period", 26))
    signal_period = int(params.get("signal_period", 9))
    
    macd_df = pta.macd(df["close"], fast=fast, slow=slow, signal=signal_period)
    
    # Extract histogram
    hist_col = f"MACDh_{fast}_{slow}_{signal_period}"
    histogram = macd_df[hist_col]
    
    # One-bar increase: H[-2] < H[-1] (histogram was going up)
    h_lag2 = histogram.shift(2)
    h_lag1 = histogram.shift(1)
    
    one_bar_increase = h_lag2 < h_lag1
    
    # Current decrease: H[0] < H[-1]
    current_decrease = histogram < h_lag1
    
    return (one_bar_increase & current_decrease).fillna(False)
