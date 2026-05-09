"""
RSI MA Dynamic Band Setup: RSI MA between 65-75, RSI maintains dynamic distance from MA.

Signals recovery mode with managed momentum — RSI distance decreases as MA grows.
"""
import pandas as pd
import pandas_ta as pta


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True when:
    - RSI MA (simple MA of RSI) is between 65 and 75
    - RSI stays above: RSI_MA + (RSI_MA * dynamic_distance_pct)
    - Dynamic distance decreases as RSI_MA grows:
      * At RSI_MA = 65: distance = 10%
      * At RSI_MA = 75: distance = 5%
    
    Args:
        df: OHLCV DataFrame with 'close' column
        params: dict with optional keys:
            - rsi_period: RSI lookback (default 14)
            - ma_period: MA period over RSI values (default 9)
            - ma_lower: lower bound of RSI_MA band (default 65)
            - ma_upper: upper bound of RSI_MA band (default 75)
            - distance_at_lower: distance % at lower bound (default 0.10)
            - distance_at_upper: distance % at upper bound (default 0.05)
    
    Returns:
        Boolean Series where True = RSI MA in band and RSI maintains dynamic distance
    """
    rsi_period = int(params.get("rsi_period", 14))
    ma_period = int(params.get("ma_period", 9))
    ma_lower = float(params.get("ma_lower", 65))
    ma_upper = float(params.get("ma_upper", 75))
    distance_at_lower = float(params.get("distance_at_lower", 0.10))
    distance_at_upper = float(params.get("distance_at_upper", 0.05))
    
    # Calculate RSI
    rsi = pta.rsi(df["close"], length=rsi_period)
    
    # Calculate MA of RSI
    rsi_ma = rsi.rolling(window=ma_period).mean()
    
    # RSI_MA in band [ma_lower, ma_upper]
    ma_in_band = (rsi_ma >= ma_lower) & (rsi_ma <= ma_upper)
    
    # Linear interpolation of distance requirement based on RSI_MA position
    # As RSI_MA grows from ma_lower to ma_upper, distance shrinks
    norm_position = (rsi_ma - ma_lower) / (ma_upper - ma_lower)  # 0 to 1
    dynamic_distance = distance_at_lower - norm_position * (distance_at_lower - distance_at_upper)
    
    # Minimum RSI value = RSI_MA * (1 + dynamic_distance)
    min_rsi = rsi_ma * (1 + dynamic_distance)
    
    rsi_above_min = rsi >= min_rsi
    
    return (ma_in_band & rsi_above_min).fillna(False)
