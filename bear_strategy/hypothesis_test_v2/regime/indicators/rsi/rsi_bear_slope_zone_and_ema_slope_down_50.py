"""
rsi_bear_slope_zone_and_ema_slope_down_50 — Composite regime indicator.

What it measures
----------------
Combines TWO bearish signals with AND logic:
1. RSI in bearish zone (30–50), RSI MA in zone, AND RSI MA slope is negative.
2. EMA(50) is declining bar-over-bar (slope < 0).

Both conditions must be true simultaneously. This creates a tighter filter that
captures bars where RSI momentum AND price trend momentum both confirm downside.

Rationale
---------
- RSI slope zone: confirms sustained bearish pressure (not just a dip).
- EMA slope down: confirms trend acceleration downward.
- AND: filters to bars where both momentum and trend agree → higher conviction.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = RSI in zone & RSI MA in zone & RSI MA declining & EMA(50) declining.
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
    True when BOTH:
    - RSI ∈ zone AND RSI_MA ∈ zone AND RSI_MA slope < 0
    - EMA(50) slope < 0
    """
    rsi_period: int   = int(params.get("rsi_period", 14))
    ma_period:  int   = int(params.get("ma_period",   9))
    lower:      float = float(params.get("lower", 30))
    upper:      float = float(params.get("upper", 50))
    ema_period: int   = int(params.get("ema_period", 50))

    # ─── RSI bear slope zone signal ───────────────────────────────────────────
    rsi    = _compute_rsi(df["close"], rsi_period)
    rsi_ma = rsi.ewm(span=ma_period, adjust=False).mean()

    in_zone_rsi    = (rsi    > lower) & (rsi    < upper)
    in_zone_rsi_ma = (rsi_ma > lower) & (rsi_ma < upper)
    rsi_slope_down = rsi_ma.diff() < 0

    rsi_signal = (in_zone_rsi & in_zone_rsi_ma & rsi_slope_down).fillna(False)

    # ─── EMA slope down signal ────────────────────────────────────────────────
    ema = df["close"].ewm(span=ema_period, adjust=False).mean()
    ema_signal = (ema.diff() < 0).fillna(False)

    # ─── Combined: AND logic ──────────────────────────────────────────────────
    return rsi_signal & ema_signal
