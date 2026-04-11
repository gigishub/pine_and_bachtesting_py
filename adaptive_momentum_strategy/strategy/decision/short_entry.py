"""Short entry decision logic.

Combines the three short filters (regime / setup / trigger) with an AND gate.
All conditions must be True simultaneously for a short (sell) signal.
The `in_short` guard prevents pyramiding — one short trade at a time.
"""

from __future__ import annotations


def should_short(
    regime_ok: bool,
    setup_ok: bool,
    trigger_ok: bool,
    in_short: bool,
) -> bool:
    """Return True when all short filters align and no short position is open.

    Args:
        regime_ok:  Bearish regime confirmed (EMA ribbon down and/or ADX trending).
        setup_ok:   Price near Donchian lower band or below VAL.
        trigger_ok: CMF < -threshold or bearish power candle confirms distribution.
        in_short:   True if already holding a short trade.
    """
    return regime_ok and setup_ok and trigger_ok and not in_short
