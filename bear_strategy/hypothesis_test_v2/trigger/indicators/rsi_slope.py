"""
RSI slope trigger: RSI declining for 2+ consecutive bars while below 50.

Continuous momentum confirmation in bearish context.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when RSI is declining and below 50."""
    try:
        import pandas_ta as pta
    except ImportError as exc:
        raise ImportError("pandas_ta is required for rsi_slope; install with: pip install pandas-ta") from exc

    rsi_period = int(params.get("rsi_period", 14))
    
    rsi = pta.rsi(df["close"], length=rsi_period)
    
    # RSI below 50
    below_50 = rsi < 50
    
    # RSI declining for at least 2 bars
    rsi_declining = (rsi < rsi.shift(1)) & (rsi.shift(1) < rsi.shift(2))
    
    return (below_50 & rsi_declining).fillna(False)
