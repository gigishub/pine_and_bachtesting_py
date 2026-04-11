"""Entry decision logic.

Combines the three independent filters (regime / setup / trigger) with a
single AND gate.  All conditions must be True simultaneously for a buy signal.
The `in_position` guard prevents pyramiding — one trade at a time.
"""

from __future__ import annotations


def should_buy(
    regime_ok: bool,
    setup_ok: bool,
    trigger_ok: bool,
    in_position: bool,
) -> bool:
    """Return True when all filters align and no position is currently open.

    Args:
        regime_ok:   ADX > threshold (trending market).
        setup_ok:    Price near Donchian upper AND channel was squeezed.
        trigger_ok:  CMF > threshold (volume confirms the move).
        in_position: True if already holding a long trade.
    """
    return regime_ok and setup_ok and trigger_ok and not in_position
