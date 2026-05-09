"""
macd — Trigger indicator.

What it measures
----------------
Basic MACD histogram signal: returns True when the MACD histogram is positive,
indicating that MACD line (fast exponential average) is above the signal line
(slow exponential average), suggesting bullish momentum.  Used as a secondary
confirmation filter within a confirmed regime + setup.

Parameters
----------
fast_period : int
    MACD fast EMA period. Default 12.

slow_period : int
    MACD slow EMA period. Default 26.

signal_period : int
    Signal line (EMA of MACD). Default 9.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = MACD histogram is positive (MACD > Signal).
False = histogram is negative or zero, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True on bars where MACD histogram is positive.

    Parameters
    ----------
    df:     OHLCV DataFrame with a 'close' column.
    params: {
        "fast_period": int (default 12),
        "slow_period": int (default 26),
        "signal_period": int (default 9),
    }
    """
    try:
        import pandas_ta as pta
    except ImportError as exc:
        raise ImportError("pandas_ta is required for macd indicator; install with: pip install pandas-ta") from exc

    fast_period: int = int(params.get("fast_period", 12))
    slow_period: int = int(params.get("slow_period", 26))
    signal_period: int = int(params.get("signal_period", 9))

    macd_df = pta.macd(df["close"], fast=fast_period, slow=slow_period, signal=signal_period)
    
    # Extract histogram column
    hist_col = f"MACDh_{fast_period}_{slow_period}_{signal_period}"
    if hist_col not in macd_df.columns:
        raise ValueError(f"MACD histogram column '{hist_col}' not found in computed MACD dataframe")
    
    hist = macd_df[hist_col]
    return (hist > 0).fillna(False)
