"""
MACD Above Threshold & Converging Setup: MACD (blue) > Signal (orange), 
both > threshold level, histogram shrinking.

Signals momentum deceleration at sustained positive level — more selective setup.
"""
import pandas as pd
import pandas_ta as pta


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True when:
    - MACD line (blue) > Signal line (orange)
    - Both lines > threshold (not just 0)
    - Histogram is shrinking (lines converging)
    
    Args:
        df: OHLCV DataFrame with 'close' column
        params: dict with optional keys:
            - fast_period: MACD fast period (default 12)
            - slow_period: MACD slow period (default 26)
            - signal_period: Signal line period (default 9)
            - threshold: minimum MACD/Signal level (default 0.0005 — reasonable middle ground)
    
    Returns:
        Boolean Series where True = MACD > Signal, both > threshold, histogram shrinking
    """
    fast = int(params.get("fast_period", 12))
    slow = int(params.get("slow_period", 26))
    signal_period = int(params.get("signal_period", 9))
    threshold = float(params.get("threshold", 0.0005))  # mid-range threshold
    
    macd_df = pta.macd(df["close"], fast=fast, slow=slow, signal=signal_period)
    
    # Extract MACD, Signal line, and histogram
    macd_col = f"MACD_{fast}_{slow}_{signal_period}"
    signal_col = f"MACDs_{fast}_{slow}_{signal_period}"
    hist_col = f"MACDh_{fast}_{slow}_{signal_period}"
    
    macd = macd_df[macd_col]
    signal_line = macd_df[signal_col]
    histogram = macd_df[hist_col]
    
    # MACD > Signal (blue above orange)
    macd_above_signal = macd > signal_line
    
    # Both lines > threshold
    both_above_threshold = (macd > threshold) & (signal_line > threshold)
    
    # Histogram shrinking (absolute value decreasing)
    hist_shrinking = histogram.abs() < histogram.shift(1).abs()
    
    return (macd_above_signal & both_above_threshold & hist_shrinking).fillna(False)
