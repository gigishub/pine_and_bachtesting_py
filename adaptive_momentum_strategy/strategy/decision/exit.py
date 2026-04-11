"""Exit decision logic.

The Chandelier SAR is the sole exit mechanism for this strategy.  Once the
trailing stop is set on entry it only ever moves up, so the trade stays open
as long as the trend continues and closes automatically when momentum fades.
"""

from __future__ import annotations


def should_sell(
    close: float,
    trail_stop: float | None,
    in_position: bool,
) -> bool:
    """Return True when close falls below the active trailing stop.

    Args:
        close:       Current bar's close price.
        trail_stop:  Active Chandelier stop level, or None if not yet set.
        in_position: True if a long trade is open.
    """
    if not in_position or trail_stop is None:
        return False
    return close < trail_stop
