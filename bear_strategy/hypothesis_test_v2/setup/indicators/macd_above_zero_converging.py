"""
MACD Above Zero & Converging Setup: MACD (blue) > Signal (orange), both > 0, histogram shrinking.

Signals momentum deceleration while still positive — pre-reversal condition.
"""
import pandas as pd
import pandas_ta as pta


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True when:
    - MACD line (blue) > Signal line (orange)
    - Both lines > 0
    - Histogram is shrinking (lines converging)
    
    Args:
        df: OHLCV DataFrame with 'close' column
        params: dict with optional keys:
            - fast_period: MACD fast period (default 12)
            - slow_period: MACD slow period (default 26)
            - signal_period: Signal line period (default 9)
    
    Returns:
        Boolean Series where True = MACD > Signal, both > 0, histogram shrinking
    """
    fast = int(params.get("fast_period", 12))
    slow = int(params.get("slow_period", 26))
    signal_period = int(params.get("signal_period", 9))
    
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
    
    # Both lines > 0
    both_positive = (macd > 0) & (signal_line > 0)
    
    # Histogram shrinking (absolute value decreasing)
    hist_shrinking = histogram.abs() < histogram.shift(1).abs()
    
    return (macd_above_signal & both_positive & hist_shrinking).fillna(False)
