"""ATR-based stop and target level helpers.

These are pure arithmetic helpers; they do not compute ATR themselves.
Pass in a pre-computed ATR value alongside the entry price.
"""

from __future__ import annotations


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
