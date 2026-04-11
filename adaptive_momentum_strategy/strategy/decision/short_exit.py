"""Short exit (cover) decision logic.

A short trade is covered when price rises above the active short trailing stop.
This is the inverse of the long exit: for longs, close < stop triggers exit;
for shorts, close > stop triggers cover.
"""

from __future__ import annotations


def should_cover(
    close: float,
    trail_stop: float | None,
    in_short: bool,
) -> bool:
    """Return True when close rises above the active short trailing stop.

    Args:
        close:       Current bar's close price.
        trail_stop:  Active short stop level (price above which we cover),
                     or None if not yet set.
        in_short:    True if a short trade is currently open.
    """
    if not in_short or trail_stop is None:
        return False
    return close > trail_stop
