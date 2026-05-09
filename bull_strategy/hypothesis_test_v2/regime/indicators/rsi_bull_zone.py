"""
rsi_bull_zone — Regime indicator.

What it measures
----------------
Checks that BOTH the raw RSI and a smoothed MA of RSI are inside the
bullish zone (50–70).

Intuition
---------
RSI in (50, 70) means the instrument is above neutral (> 50) — confirming
bullish momentum — but not yet overbought (< 70), so there is still room
to run. Adding RSI MA confirmation requires the smoothed trend to agree,
filtering single-bar pops into the zone.

Parameters
----------
rsi_period : int   — RSI lookback. Default 14.
ma_period  : int   — EMA smoothing period applied to the RSI. Default 9.
lower      : float — Lower bound of the zone (exclusive). Default 50.
upper      : float — Upper bound of the zone (exclusive). Default 70.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = RSI and RSI_MA both inside (lower, upper).
False = outside zone or warm-up bars.
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
    True when RSI and its EMA are both inside (lower, upper).

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

    return (in_zone_rsi & in_zone_rsi_ma).fillna(False)
