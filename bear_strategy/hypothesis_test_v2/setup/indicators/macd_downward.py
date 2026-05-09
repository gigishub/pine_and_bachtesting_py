"""
MACD Downward Setup: Both MACD and Signal lines above 0 and both sloping downward.
Signals potential bearish momentum loss (deceleration).
"""
import pandas as pd
import pandas_ta as pta


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Both MACD and Signal line > 0, and both are sloping downward.
    
    Args:
        df: OHLCV DataFrame with 'close' column
        params: dict with optional keys:
            - fast_period: MACD fast period (default 12)
            - slow_period: MACD slow period (default 26)
            - signal_period: Signal line period (default 9)
    
    Returns:
        Boolean Series where True = both lines > 0 and both downward
    """
    fast = int(params.get("fast_period", 12))
    slow = int(params.get("slow_period", 26))
    signal_period = int(params.get("signal_period", 9))
    
    macd_df = pta.macd(df["close"], fast=fast, slow=slow, signal=signal_period)
    
    # Extract MACD and Signal line
    macd_col = f"MACD_{fast}_{slow}_{signal_period}"
    signal_col = f"MACDs_{fast}_{slow}_{signal_period}"
    
    macd = macd_df[macd_col]
    signal_line = macd_df[signal_col]
    
    # Both lines positive
    both_positive = (macd > 0) & (signal_line > 0)
    
    # Both lines sloping downward
    macd_downward = macd < macd.shift(1)
    signal_downward = signal_line < signal_line.shift(1)
    both_sloping_down = macd_downward & signal_downward
    
    return (both_positive & both_sloping_down).fillna(False)
