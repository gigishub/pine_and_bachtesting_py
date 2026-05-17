"""Shared low-level indicator helpers for the bear_strategy vectorbt backtest.

Pure functions: no I/O, no side-effects, no lookahead at bar N.
Used by both the entry/ and exits/ packages so they don't duplicate math.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_rsi(close: pd.Series, period: int) -> pd.Series:
    """Wilder-smoothed RSI using EWM (alpha = 1/period)."""
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def compute_macd_histogram(
    close: pd.Series,
    fast: int,
    slow: int,
    signal: int,
) -> pd.Series:
    """MACD histogram = (fast EMA − slow EMA) − signal EMA of that difference.

    All EMAs are causal (adjust=False) — no lookahead at bar N.
    """
    ema_fast    = close.ewm(span=fast,   adjust=False).mean()
    ema_slow    = close.ewm(span=slow,   adjust=False).mean()
    macd_line   = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line - signal_line


def compute_ema(close: pd.Series, period: int) -> pd.Series:
    """Exponential Moving Average, causal (adjust=False)."""
    return close.ewm(span=period, adjust=False).mean()


def get_smoothed_funding(
    funding_df: pd.DataFrame,
    target_index: pd.DatetimeIndex,
    ma_period: int,
) -> pd.Series:
    """Align 8h funding settlements to target_index and apply EMA smoothing.

    Returns the smoothed series WITHOUT any shift — the caller must apply
    whichever shift is appropriate for their use-case (entry guard vs exit).
    """
    rate = funding_df["fundingrate"].copy()
    fund_idx = pd.to_datetime(rate.index)
    fund_idx = (
        fund_idx.tz_localize("UTC") if fund_idx.tz is None else fund_idx.tz_convert("UTC")
    )
    rate.index = fund_idx

    tgt_utc = (
        target_index.tz_localize("UTC")
        if target_index.tz is None
        else target_index.tz_convert("UTC")
    )
    combined = rate.reindex(rate.index.union(tgt_utc)).ffill()
    result = combined.reindex(tgt_utc)
    result.index = target_index

    if ma_period > 1:
        result = result.ewm(span=ma_period, adjust=False).mean()
    return result
