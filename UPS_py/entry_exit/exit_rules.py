"""Long exit rule for the UPS strategy (non-trailing path only).

In the trailing path, exits are managed by updating Trade.sl in next().
This function covers only the non-trailing case where we want to close early
(e.g. signal reversal before SL/TP is hit).

Pure function: no side effects, no order placement.
"""

from __future__ import annotations


def should_close_long(
    position_size: float,
    # Reserved for any early-exit signal needed in the future
) -> bool:
    """Return True when the long position should be closed early.

    The UPS strategy exits via SL/TP orders set at entry (non-trailing path)
    or via a ratcheting trail stop (trailing path).  There is no explicit
    signal-based early exit in the Pine source, so this always returns False
    for now.

    Step 6 implementation.

    UPS Pine logic does not define a separate signal-based close condition;
    exits are managed by stop/target orders (or trailing stop once activated).
    """
    _ = position_size
    return False


def should_close_short(
    position_size: float,
    # Reserved for any early-exit signal needed in the future
) -> bool:
    """Return True when the short position should be closed early."""
    _ = position_size
    return False
