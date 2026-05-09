"""
RSI Cross Below 40 Trigger: Detects when RSI crosses below the 40 level.

Signals stronger momentum shift — entry into potential oversold territory.
"""
import pandas as pd
import pandas_ta as pta


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True on bars where RSI crosses below 40.
    
    Args:
        df: OHLCV DataFrame with 'close' column
        params: dict with optional keys:
            - rsi_period: RSI lookback (default 14)
    
    Returns:
        Boolean Series where True = RSI crosses below 40
    """
    rsi_period = int(params.get("rsi_period", 14))
    
    # Calculate RSI
    rsi = pta.rsi(df["close"], length=rsi_period)
    
    # Detect cross below 40: RSI was >= 40 yesterday, now < 40
    prev_rsi = rsi.shift(1)
    cross_below_40 = (prev_rsi >= 40) & (rsi < 40)
    
    return cross_below_40.fillna(False)
