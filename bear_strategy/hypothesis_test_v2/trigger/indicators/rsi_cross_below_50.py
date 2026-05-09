"""
RSI Cross Below 50 Trigger: Detects when RSI crosses below the 50 level.

Signals potential momentum shift from neutral to bearish.
"""
import pandas as pd
import pandas_ta as pta


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True on bars where RSI crosses below 50.
    
    Args:
        df: OHLCV DataFrame with 'close' column
        params: dict with optional keys:
            - rsi_period: RSI lookback (default 14)
    
    Returns:
        Boolean Series where True = RSI crosses below 50
    """
    rsi_period = int(params.get("rsi_period", 14))
    
    # Calculate RSI
    rsi = pta.rsi(df["close"], length=rsi_period)
    
    # Detect cross below 50: RSI was >= 50 yesterday, now < 50
    prev_rsi = rsi.shift(1)
    cross_below_50 = (prev_rsi >= 50) & (rsi < 50)
    
    return cross_below_50.fillna(False)
