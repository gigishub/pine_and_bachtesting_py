"""Trailing stop helpers: Chandelier SAR (long) and btc_momentum-style trail.

Chandelier Exit (Le Beau, 1992):
    long_stop  = rolling_max(high, N) - ATR(N) × mult
    short_stop = rolling_min(low,  N) + ATR(N) × mult

btc_momentum-style Simple Trailing Stop:
    long_stop  = rolling_max(low, N)  - ATR(N) × mult

Uses the rolling highest LOW as the trail source — tighter than Chandelier
because lows rise faster than highs during uptrends.  Ratcheted upward in
next() so profits are locked in progressively.
"""

from __future__ import annotations

import pandas as pd
import pandas_ta as pta


def compute_chandelier_stop_series(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    lookback: int = 22,
    atr_mult: float = 3.0,
) -> pd.Series:
    """Precompute the Chandelier stop level for every bar.

    This is the *candidate* stop — the runner ratchets it upward bar-by-bar
    while a position is open so it never moves lower.

    Returns:
        Float Series.  NaN during the ATR warm-up period.
    """
    atr = pta.atr(high, low, close, length=lookback)
    if atr is None:
        return pd.Series(float("nan"), index=close.index, dtype=float)
    rolling_high = high.rolling(lookback).max()
    return (rolling_high - atr * atr_mult).astype(float)


def compute_trailing_stop_series(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    lookback: int = 22,
    atr_mult: float = 2.0,
) -> pd.Series:
    """Precompute the btc_momentum-style trailing stop level for every bar.

    stop = rolling_max(low, N) - ATR(N) × mult

    Uses the rolling highest LOW as the trail source — tighter than the
    Chandelier exit (which uses rolling_max(high)).  During uptrends the lows
    are rising, so this tracks the ascending support structure more closely.

    Returns:
        Float Series.  NaN during ATR warm-up.
    """
    atr = pta.atr(high, low, close, length=lookback)
    if atr is None:
        return pd.Series(float("nan"), index=close.index, dtype=float)
    rolling_highest_low = low.rolling(lookback).max()
    return (rolling_highest_low - atr * atr_mult).astype(float)


def compute_trailing_stop_short_series(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    lookback: int = 22,
    atr_mult: float = 2.0,
) -> pd.Series:
    """btc_momentum-style trailing stop level for a short position.

    stop = rolling_min(high, N) + ATR(N) × mult

    Uses the rolling lowest HIGH as the trail source — tighter than the
    Chandelier short exit (which uses rolling_min(low)).  During downtrends
    the highs are falling, so this tracks the descending resistance structure
    more closely.

    For shorts: price must *rise above* this stop level to trigger a cover.

    Returns:
        Float Series.  NaN during ATR warm-up.
    """
    atr = pta.atr(high, low, close, length=lookback)
    if atr is None:
        return pd.Series(float("nan"), index=close.index, dtype=float)
    rolling_lowest_high = high.rolling(lookback).min()
    return (rolling_lowest_high + atr * atr_mult).astype(float)


def compute_entry_candle_sl_long(
    low: pd.Series,
    close: pd.Series,
    atr: pd.Series,
    n_atr_init: float = 0.5,
    min_frac: float = 0.005,
) -> pd.Series:
    """Initial SL fraction for longs: entry candle low minus ATR buffer.

    SL price = low[entry_bar] - n_atr_init × ATR[entry_bar]
    SL frac  = (close - sl_price) / close   (approximates entry_price ≈ close)

    VBT uses the actual fill price (c.init_price) inside adjust_sl_func_nb,
    so this fraction only matters for the first bar — close is a fine proxy.

    Args:
        low:         Bar low prices.
        close:       Bar close prices (proxy for entry price).
        atr:         ATR series (same length/index as low/close).
        n_atr_init:  ATR multiplier for buffer below the candle low.
        min_frac:    Floor fraction (default 0.5%) to avoid zero-distance SL.

    Returns:
        Float Series of SL fractions, clipped to [min_frac, 1.0].
    """
    sl_price = low - n_atr_init * atr
    return ((close - sl_price) / close).clip(lower=min_frac)


def compute_entry_candle_sl_short(
    high: pd.Series,
    close: pd.Series,
    atr: pd.Series,
    n_atr_init: float = 0.5,
    min_frac: float = 0.005,
) -> pd.Series:
    """Initial SL fraction for shorts: entry candle high plus ATR buffer.

    SL price = high[entry_bar] + n_atr_init × ATR[entry_bar]
    SL frac  = (sl_price - close) / close

    Args:
        high:        Bar high prices.
        close:       Bar close prices (proxy for entry price).
        atr:         ATR series.
        n_atr_init:  ATR multiplier for buffer above the candle high.
        min_frac:    Floor fraction (default 0.5%).

    Returns:
        Float Series of SL fractions, clipped to [min_frac, 1.0].
    """
    sl_price = high + n_atr_init * atr
    return ((sl_price - close) / close).clip(lower=min_frac)


def compute_entry_candle_sl(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    atr: pd.Series,
    n_atr_init: float = 0.5,
    min_frac: float = 0.005,
) -> tuple[pd.Series, pd.Series]:
    """Compute both long and short entry candle SL fractions.

    Convenience wrapper around compute_entry_candle_sl_long/short.

    Returns:
        (sl_frac_long, sl_frac_short) — both clipped to [min_frac, 1.0]
    """
    sl_frac_long = compute_entry_candle_sl_long(low, close, atr, n_atr_init, min_frac)
    sl_frac_short = compute_entry_candle_sl_short(high, close, atr, n_atr_init, min_frac)
    return sl_frac_long, sl_frac_short


def compute_chandelier_short_stop_series(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    lookback: int = 22,
    atr_mult: float = 2.5,
) -> pd.Series:
    """Chandelier stop level for a short position.

    stop = rolling_min(low, N) + ATR(N) × mult

    For shorts, price must *rise above* this stop to trigger a cover.
    The 2.5× multiplier is tighter than the long-side 3.0× because bearish
    retracements (short squeezes) are sharp and rapid.

    Returns:
        Float Series.  NaN during ATR warm-up.
    """
    atr = pta.atr(high, low, close, length=lookback)
    if atr is None:
        return pd.Series(float("nan"), index=close.index, dtype=float)
    rolling_low = low.rolling(lookback).min()
    return (rolling_low + atr * atr_mult).astype(float)


def ratchet_short_stop(
    current_stop: float | None,
    candidate_stop: float,
    position_size: float,
) -> float | None:
    """Ratchet the short trailing stop downward; never loosen it.

    For a short trade, the stop price only moves DOWN (locking in gains as
    price falls).  A rising candidate is ignored — that would loosen the stop.

    Args:
        current_stop:   The stop in effect from the previous bar, or None.
        candidate_stop: The freshly computed chandelier short level.
        position_size:  Current position size (negative for shorts).

    Returns:
        Updated stop price, or None when no short position is open.
    """
    if position_size >= 0:
        return None
    if current_stop is None:
        return float(candidate_stop)
    return float(min(current_stop, candidate_stop))


def ratchet_stop(
    current_stop: float | None,
    candidate_stop: float,
    position_size: float,
) -> float | None:
    """Ratchet the trailing stop upward; never loosen it.

    Args:
        current_stop:   The stop in effect from the previous bar, or None if
                        no position was open.
        candidate_stop: The freshly computed Chandelier level for this bar.
        position_size:  Current position size (units held).

    Returns:
        Updated stop price, or None when position_size == 0.
    """
    if position_size <= 0:
        return None
    if current_stop is None:
        return float(candidate_stop)
    return float(max(current_stop, candidate_stop))
