"""
rsi_bull_slope_zone — Regime indicator.

What it measures
----------------
RSI in bullish zone (50–70) AND RSI MA in zone AND RSI MA slope is positive
(rising smoothed RSI confirms sustained bullish pressure, not a dead-cat bounce).

The slope filter removes bars where RSI MA is in the zone but drifting downward —
those may be early weakening signals, not confirmed bull regimes.

Parameters
----------
rsi_period : int   — RSI lookback. Default 14.
ma_period  : int   — EMA period applied to RSI. Default 9.
lower      : float — Zone lower bound. Default 50.
upper      : float — Zone upper bound. Default 70.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = RSI ∈ zone AND RSI_MA ∈ zone AND RSI_MA is rising.
False = any condition not met, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd


def _compute_rsi(close: pd.Series, period: int) -> pd.Series:
    delta = close.diff()
    gain  = delta.clip(lower=0).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    loss  = (-delta.clip(upper=0)).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs    = gain / loss.replace(0, float("nan"))
    return 100 - (100 / (1 + rs))


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    True when RSI ∈ zone AND RSI_MA ∈ zone AND RSI_MA slope > 0.

    Parameters
    ----------
    df:     OHLCV DataFrame with a 'close' column.
    params: {"rsi_period": int, "ma_period": int, "lower": float, "upper": float}
    """
    rsi_period: int   = int(params.get("rsi_period", 14))
    ma_period:  int   = int(params.get("ma_period",   9))
    lower:      float = float(params.get("lower", 50))
    upper:      float = float(params.get("upper", 70))

    rsi    = _compute_rsi(df["close"], rsi_period)
    rsi_ma = rsi.ewm(span=ma_period, adjust=False).mean()

    in_zone_rsi    = (rsi    > lower) & (rsi    < upper)
    in_zone_rsi_ma = (rsi_ma > lower) & (rsi_ma < upper)
    slope_up       = rsi_ma.diff() > 0   # RSI MA is rising

    return (in_zone_rsi & in_zone_rsi_ma & slope_up).fillna(False)
