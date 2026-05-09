"""
rsi_bear_momentum_zone — Regime indicator.

What it measures
----------------
RSI in bearish zone (30–50) AND the RSI value is lower than the previous bar
(RSI momentum is negative — the indicator itself is moving down).

Intuition
---------
A declining RSI inside the bear zone means selling pressure is building, not
stabilising. This gives an early momentum-based confirmation that the regime
is actively deteriorating rather than just hovering.

Parameters
----------
rsi_period : int   — RSI lookback. Default 14.
lower      : float — Zone lower bound. Default 30.
upper      : float — Zone upper bound. Default 50.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = RSI ∈ zone AND RSI < RSI[prev bar] (RSI falling).
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
    True when RSI ∈ zone AND current RSI < previous RSI (falling momentum).

    Parameters
    ----------
    df:     OHLCV DataFrame with a 'close' column.
    params: {"rsi_period": int, "lower": float, "upper": float}
    """
    rsi_period: int   = int(params.get("rsi_period", 14))
    lower:      float = float(params.get("lower", 30))
    upper:      float = float(params.get("upper", 50))

    rsi           = _compute_rsi(df["close"], rsi_period)
    in_zone       = (rsi > lower) & (rsi < upper)
    rsi_declining = rsi < rsi.shift(1)   # current RSI lower than previous bar

    return (in_zone & rsi_declining).fillna(False)
