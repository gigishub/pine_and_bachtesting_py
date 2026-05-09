"""
rsi_bull_zone_1d_and_close_above_ema_200 — Composite regime indicator.

What it measures
----------------
Combines TWO bullish signals with AND logic:
1. RSI in bullish zone (50–70) on 1d timeframe, RSI MA in zone (computed on 1d).
2. Close price is above EMA(200).

Both conditions must be true simultaneously. This creates a selective filter that
captures bars where 1d momentum AND entry-TF price location both confirm upside.

Rationale
---------
- RSI bull zone 1d: confirms bullish momentum at daily resolution (higher conviction).
- Close above EMA 200: confirms price is above the long-term average (support).
- AND: filters to bars where daily momentum and price location agree → higher bias.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = RSI ∈ zone & RSI_MA ∈ zone (computed on 1d) & close > EMA(200).
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
    - RSI ∈ zone AND RSI_MA ∈ zone (on entry-TF bars)
    - close > EMA(200)
    """
    rsi_period: int   = int(params.get("rsi_period", 14))
    ma_period:  int   = int(params.get("ma_period",   9))
    lower:      float = float(params.get("lower", 50))
    upper:      float = float(params.get("upper", 70))
    ema_period: int   = int(params.get("ema_period", 200))

    # ─── RSI bull zone signal ─────────────────────────────────────────────────
    rsi    = _compute_rsi(df["close"], rsi_period)
    rsi_ma = rsi.ewm(span=ma_period, adjust=False).mean()

    in_zone_rsi    = (rsi    > lower) & (rsi    < upper)
    in_zone_rsi_ma = (rsi_ma > lower) & (rsi_ma < upper)

    rsi_signal = (in_zone_rsi & in_zone_rsi_ma).fillna(False)

    # ─── Close above EMA signal ───────────────────────────────────────────────
    ema = df["close"].ewm(span=ema_period, adjust=False).mean()
    close_signal = df["close"] > ema

    # ─── Combined: AND logic ──────────────────────────────────────────────────
    return rsi_signal & close_signal
