"""
MACD N3 (Deep Pullback) Trigger: Histogram increased for 3+ bars, then decreases.

Signals peak of uptrend in histogram — strongest momentum confirmation before reversal.
"""
import pandas as pd
import pandas_ta as pta


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True when:
    - Histogram increased for at least 3 bars: H[-3] < H[-2] < H[-1]
    - Current histogram decreases: H[0] < H[-1]
    
    Args:
        df: OHLCV DataFrame with 'close' column
        params: dict with optional keys:
            - fast_period: MACD fast period (default 12)
            - slow_period: MACD slow period (default 26)
            - signal_period: Signal line period (default 9)
    
    Returns:
        Boolean Series where True = 3-bar increase confirmed + current decrease
    """
    fast = int(params.get("fast_period", 12))
    slow = int(params.get("slow_period", 26))
    signal_period = int(params.get("signal_period", 9))
    
    macd_df = pta.macd(df["close"], fast=fast, slow=slow, signal=signal_period)
    
    # Extract histogram
    hist_col = f"MACDh_{fast}_{slow}_{signal_period}"
    histogram = macd_df[hist_col]
    
    # Three-bar increase: H[-3] < H[-2] < H[-1]
    h_lag3 = histogram.shift(3)
    h_lag2 = histogram.shift(2)
    h_lag1 = histogram.shift(1)
    
    three_bar_increase = (h_lag3 < h_lag2) & (h_lag2 < h_lag1)
    
    # Current decrease: H[0] < H[-1]
    current_decrease = histogram < h_lag1
    
    return (three_bar_increase & current_decrease).fillna(False)
