"""Donchian channel breakout setup.

Donchian Channels (Donchian, 1960) plot the highest high and lowest low over
a lookback window.  A close near or above the upper band signals that price
has exited a prior trading range — a structural breakout.

The 'volatility squeeze' overlay adds selectivity: we only act on breakouts
that emerge from a compressed channel (bottom 25th percentile of channel
width), because range contractions that precede expansions tend to produce
more decisive moves with lower retracement risk.
"""

from __future__ import annotations

import pandas as pd


def compute_donchian_upper(high: pd.Series, lookback: int = 20) -> pd.Series:
    """Highest high over the last `lookback` bars (inclusive of current bar).

    Includes the current bar — no shift — because the bar is closed when
    next() evaluates it.  The entry fills at the NEXT bar's open, so no
    lookahead occurs.
    """
    return high.rolling(lookback).max().astype(float)


def compute_donchian_lower(low: pd.Series, lookback: int = 20) -> pd.Series:
    """Lowest low over the last `lookback` bars."""
    return low.rolling(lookback).min().astype(float)


def compute_donchian_squeeze(
    high: pd.Series,
    low: pd.Series,
    lookback: int = 20,
    squeeze_history: int = 240,
) -> pd.Series:
    """True when the channel width is in the bottom 25th percentile.

    A compressed channel indicates a volatility contraction; breakouts from
    these phases are historically more reliable than breakouts in already-wide
    channels.

    Args:
        squeeze_history: Rolling window (bars) used to rank the channel width.
                         Default 240 ≈ 10 calendar days at 1h.
    """
    upper = compute_donchian_upper(high, lookback)
    lower = compute_donchian_lower(low, lookback)
    width = upper - lower

    # 25th-percentile threshold over the last squeeze_history bars.
    threshold_25th = width.rolling(squeeze_history).quantile(0.25)
    return (width <= threshold_25th).fillna(False)


def setup_is_active(
    close: pd.Series,
    donchian_upper: pd.Series,
    donchian_squeeze: pd.Series,
    tolerance: float = 0.01,
) -> pd.Series:
    """True when close is within `tolerance` of the upper band AND squeeze is active.

    Args:
        tolerance: Fraction below the upper band still considered 'near breakout'.
                   Default 0.01 = within 1% of the high.
    """
    near_upper = close >= donchian_upper * (1.0 - tolerance)
    return (near_upper & donchian_squeeze).fillna(False)


def setup_short_is_active(
    close: pd.Series,
    donchian_lower: pd.Series,
    donchian_squeeze: pd.Series,
    tolerance: float = 0.01,
) -> pd.Series:
    """True when close is within tolerance of the lower band AND squeeze is active.

    Short-side mirror of setup_is_active().  A close near or below the lower
    Donchian band signals a structural breakdown from a compressed range.

    Args:
        tolerance: Fraction above the lower band still considered 'near breakdown'.
                   Default 0.01 = within 1% of the low.
    """
    near_lower = close <= donchian_lower * (1.0 + tolerance)
    return (near_lower & donchian_squeeze).fillna(False)
