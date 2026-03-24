"""Long/short exit gates for the UPS strategy.

UPS exits are managed via SL/TP orders set at entry (non-trailing path) or a
ratcheting trail stop (trailing path).  There is no explicit signal-based
early exit in the Pine source, so these return False for now.

Pure functions: no side effects, no order placement.
"""

from __future__ import annotations


def should_close_long(position_size: float) -> bool:
    """Return True when the long position should be closed early."""
    _ = position_size
    return False


def should_close_short(position_size: float) -> bool:
    """Return True when the short position should be closed early."""
    _ = position_size
    return False
