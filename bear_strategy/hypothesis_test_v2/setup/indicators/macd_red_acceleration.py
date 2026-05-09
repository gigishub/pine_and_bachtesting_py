"""
MACD Red Acceleration Setup: Histogram loses n% of previous magnitude while remaining negative.
Signals deceleration in bearish momentum (histogram getting less negative).
"""
import pandas as pd
import pandas_ta as pta


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    MACD histogram magnitude shrinks by n% (default 50%) while both current and prior are negative.
    Example: prior = -100, current = -50 (loses 50% magnitude) → activation.
    
    Args:
        df: OHLCV DataFrame with 'close' column
        params: dict with optional keys:
            - fast_period: MACD fast period (default 12)
            - slow_period: MACD slow period (default 26)
            - signal_period: Signal line period (default 9)
            - drop_pct: Percentage magnitude loss required (default 0.50 = 50%)
    
    Returns:
        Boolean Series where True = histogram shrinks by drop_pct while both red
    """
    fast = int(params.get("fast_period", 12))
    slow = int(params.get("slow_period", 26))
    signal_period = int(params.get("signal_period", 9))
    drop_pct = float(params.get("drop_pct", 0.50))
    
    macd_df = pta.macd(df["close"], fast=fast, slow=slow, signal=signal_period)
    
    # Extract histogram
    hist_col = f"MACDh_{fast}_{slow}_{signal_period}"
    hist = macd_df[hist_col]
    
    # Both current and prior histogram negative (red)
    both_negative = (hist < 0) & (hist.shift(1) < 0)
    
    # Histogram loses drop_pct of previous magnitude (gets less negative)
    # Example: prior = -100, drop_pct = 0.50 → require abs(hist) <= 50
    hist_reduction = abs(hist) <= drop_pct * abs(hist.shift(1))
    
    return (both_negative & hist_reduction).fillna(False)
