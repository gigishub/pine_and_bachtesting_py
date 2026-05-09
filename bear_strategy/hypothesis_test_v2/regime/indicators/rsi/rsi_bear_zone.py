"""
rsi_bear_zone — Regime indicator.

What it measures
----------------
Checks that BOTH the raw RSI and a smoothed MA of RSI are inside the
bearish zone (30–50).

Intuition
---------
RSI in (30, 50) means the instrument is not in collapse (> 30) but is
clearly below neutral (< 50) — the typical range where a bear regime
holds steady without extreme oversold readings.

Adding the RSI MA confirmation filters out single-bar spikes into the zone;
both the raw reading and the smoothed trend must be bearish-zone aligned.

Parameters
----------
rsi_period : int   — RSI lookback. Default 14.
ma_period  : int   — EMA smoothing period applied to the RSI. Default 9.
lower      : float — Lower bound of the zone (inclusive). Default 30.
upper      : float — Upper bound of the zone (exclusive). Default 50.

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
    lower:      float = float(params.get("lower", 30))
    upper:      float = float(params.get("upper", 50))

    rsi    = _compute_rsi(df["close"], rsi_period)
    rsi_ma = rsi.ewm(span=ma_period, adjust=False).mean()

    in_zone_rsi    = (rsi    > lower) & (rsi    < upper)
    in_zone_rsi_ma = (rsi_ma > lower) & (rsi_ma < upper)

    return (in_zone_rsi & in_zone_rsi_ma).fillna(False)
