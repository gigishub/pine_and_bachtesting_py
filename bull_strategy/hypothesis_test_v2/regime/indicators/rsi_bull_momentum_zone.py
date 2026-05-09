"""
rsi_bull_momentum_zone — Regime indicator.

What it measures
----------------
RSI in bullish zone (50–70) AND the RSI value is higher than the previous bar
(RSI momentum is positive — the indicator itself is moving up).

Intuition
---------
A rising RSI inside the bull zone means buying pressure is building, not
stalling. This gives an early momentum-based confirmation that the regime
is actively strengthening rather than just hovering.

Parameters
----------
rsi_period : int   — RSI lookback. Default 14.
lower      : float — Zone lower bound. Default 50.
upper      : float — Zone upper bound. Default 70.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = RSI ∈ zone AND RSI > RSI[prev bar] (RSI rising).
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
    True when RSI ∈ zone AND current RSI > previous RSI (rising momentum).

    Parameters
    ----------
    df:     OHLCV DataFrame with a 'close' column.
    params: {"rsi_period": int, "lower": float, "upper": float}
    """
    rsi_period: int   = int(params.get("rsi_period", 14))
    lower:      float = float(params.get("lower", 50))
    upper:      float = float(params.get("upper", 70))

    rsi         = _compute_rsi(df["close"], rsi_period)
    in_zone     = (rsi > lower) & (rsi < upper)
    rsi_rising  = rsi > rsi.shift(1)   # current RSI higher than previous bar

    return (in_zone & rsi_rising).fillna(False)
