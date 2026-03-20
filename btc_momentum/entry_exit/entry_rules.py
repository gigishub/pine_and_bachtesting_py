from __future__ import annotations


def should_open_long(
    long_trades_enabled: bool,
    is_bullish: bool,
    is_caution: bool,
    position_size: float,
    ) -> bool:
    
    """Return True when the strategy should open a new long position."""
    return long_trades_enabled and is_bullish and (position_size == 0) and (not is_caution)
