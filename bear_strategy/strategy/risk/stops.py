"""ATR-based stop and target level helpers.

Two families:

1. atr_stop_level / atr_target_level — simple price-level helpers used by
   the hypothesis-test outcome engine and the backtesting.py runner.

2. compute_entry_candle_sl_* — pandas Series helpers for the VBT runner.
   These compute the initial SL fraction (relative to close) from the entry
   candle's high/low plus an ATR buffer.  The VBT trailing callback in
   stops_numba.py then ratchets the stop inward bar-by-bar.
"""

from __future__ import annotations

import pandas as pd


def atr_stop_level(entry_price: float, atr: float, atr_mult: float) -> float:
    """Return the short-side stop loss level (above entry).

    For a short trade, the stop is placed *above* entry at:
        entry + atr_mult × atr

    If price returns to this level the thesis is invalidated.

    Args:
        entry_price: Entry price of the short trade.
        atr:         Current ATR value.
        atr_mult:    Multiplier applied to ATR (e.g. 2.0 for 2×ATR stop).

    Returns:
        Stop price level (float).
    """
    return entry_price + atr_mult * atr


def atr_target_level(entry_price: float, atr: float, atr_mult: float) -> float:
    """Return the short-side profit target level (below entry).

    For a short trade, the target is placed *below* entry at:
        entry - atr_mult × atr

    Args:
        entry_price: Entry price of the short trade.
        atr:         Current ATR value.
        atr_mult:    Multiplier applied to ATR (e.g. 3.0 for 3×ATR target).

    Returns:
        Target price level (float).
    """
    return entry_price - atr_mult * atr


# ── VBT entry-candle SL fractions ────────────────────────────────────────────
# These functions compute the initial SL fraction at the signal bar.
# Pass a pre-computed ATR Series; no pandas_ta dependency.

def compute_entry_candle_sl_short(
    high: pd.Series,
    close: pd.Series,
    atr: pd.Series,
    n_atr_init: float = 0.5,
    min_frac: float = 0.005,
) -> pd.Series:
    """Initial SL fraction for shorts: entry candle high plus ATR buffer.

    SL price = high[entry_bar] + n_atr_init × ATR[entry_bar]
    SL frac  = (sl_price - close) / close   (close ≈ entry price proxy)

    VBT uses the actual fill price (c.init_price) inside the Numba callback,
    so this fraction only governs the first bar — close is an adequate proxy.

    Args:
        high:        Bar high prices.
        close:       Bar close prices.
        atr:         ATR series (same length/index).
        n_atr_init:  ATR buffer above the candle high (default 0.5).
        min_frac:    Floor fraction to prevent zero-distance SL (default 0.5%).

    Returns:
        Float Series of SL fractions, clipped to [min_frac, 1.0].
    """
    sl_price = high + n_atr_init * atr
    return ((sl_price - close) / close.where(close > 0)).clip(lower=min_frac).fillna(min_frac)
