"""EMA Ribbon regime filter (Regime Option C).

A 'ribbon' of three exponential moving averages confirms that momentum is
consistent across multiple time scales.  When fast > mid > slow the market
structure is unambiguously bullish; this alignment filters out counter-trend
entries and reduces whipsaw trades in sideways conditions.

Reference: Kaufman, P. J. (2013). Trading Systems and Methods.
"""

from __future__ import annotations

import pandas as pd


def compute_ema(close: pd.Series, period: int) -> pd.Series:
    """Exponential moving average with standard (Wilder-adjusted) span."""
    return close.ewm(span=period, adjust=False).mean().astype(float)


def compute_ema_ribbon(
    close: pd.Series,
    fast: int = 20,
    mid: int = 50,
    slow: int = 200,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Return (ema_fast, ema_mid, ema_slow) as a triple of float Series."""
    return compute_ema(close, fast), compute_ema(close, mid), compute_ema(close, slow)


def regime_is_aligned(
    ema_fast: pd.Series,
    ema_mid: pd.Series,
    ema_slow: pd.Series,
) -> pd.Series:
    """True when EMA(fast) > EMA(mid) > EMA(slow).

    This stacking confirms bullish momentum at multiple time scales and acts
    as a filter: trades are only initiated when all three layers agree.
    """
    return (ema_fast > ema_mid) & (ema_mid > ema_slow)


def regime_is_bearish(
    ema_fast: pd.Series,
    ema_mid: pd.Series,
    ema_slow: pd.Series,
) -> pd.Series:
    """True when EMA(fast) < EMA(mid) < EMA(slow) (bearish stacking).

    Flipped hierarchy confirms multi-scale downward momentum — the short-side
    mirror of regime_is_aligned().
    """
    return (ema_fast < ema_mid) & (ema_mid < ema_slow)
