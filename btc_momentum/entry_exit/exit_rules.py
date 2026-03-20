from __future__ import annotations


def should_close_long(
    position_size: float,
    close_now: float,
    trail_stop: float | None,
    htf_ema_now: float,
    ) -> bool:
    
    """Close long when price breaks trailing stop or falls below HTF EMA."""
    if position_size <= 0 or trail_stop is None:
        return False
    return (close_now < trail_stop) or (close_now < htf_ema_now)
