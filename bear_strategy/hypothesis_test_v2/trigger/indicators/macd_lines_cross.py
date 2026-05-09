"""
macd_lines_cross — Trigger indicator.

What it measures
----------------
MACD line crossing below its signal line — a reversal signal that can 
confirm momentum loss or trend change.  In a confirmed regime + setup,
this acts as a precise entry trigger.

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
True  = MACD line just crossed below signal line on this bar.
False = no cross, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True on bars where MACD crosses below signal line.

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
    
    macd_col = f"MACD_{fast_period}_{slow_period}_{signal_period}"
    signal_col = f"MACDs_{fast_period}_{slow_period}_{signal_period}"
    
    if macd_col not in macd_df.columns or signal_col not in macd_df.columns:
        raise ValueError(f"MACD columns not found: {macd_col}, {signal_col}")
    
    macd = macd_df[macd_col]
    signal_line = macd_df[signal_col]

    # Cross below: previous bar had macd >= signal, current bar has macd < signal
    was_above = macd.shift(1) >= signal_line.shift(1)
    is_below = macd < signal_line

    return (was_above & is_below).fillna(False)
