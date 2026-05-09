"""
ATR expansion bearish turn trigger: range expands + closes below open + below prior close.

Momentum burst confirmation — selective signal with follow-through.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when bar expands + closes bearishly."""
    try:
        import pandas_ta as pta
    except ImportError as exc:
        raise ImportError("pandas_ta is required for atr_expansion_bearish; install with: pip install pandas-ta") from exc

    atr_length = int(params.get("atr_length", 14))
    expansion_factor = float(params.get("expansion_factor", 1.2))
    
    atr = pta.atr(high=df["high"], low=df["low"], close=df["close"], length=atr_length)
    
    current_range = df["high"] - df["low"]
    prior_atr = atr.shift(1)
    
    # Range expands beyond prior ATR * factor
    range_expands = current_range > (prior_atr * expansion_factor)
    
    # Closes bearishly
    close_below_open = df["close"] < df["open"]
    close_below_prior = df["close"] < df["close"].shift(1)
    
    return (range_expands & close_below_open & close_below_prior).fillna(False)
