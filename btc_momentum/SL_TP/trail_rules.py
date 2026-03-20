from __future__ import annotations


def compute_long_trail_candidate(
    highest_trail_src_now: float,
    atr_now: float,
    trail_stop_multi: float,
    prev_caution: bool) -> float:

    """Compute the candidate trailing stop for the current bar."""
    atr_distance = atr_now * (trail_stop_multi if prev_caution else 1.0)
    return highest_trail_src_now - atr_distance


def update_long_trail_stop(
    position_size: float,
    current_trail_stop: float | None,
    candidate_trail_stop: float) -> float | None:
    
    """Only move the long trailing stop upward (never loosen it)."""
    if position_size <= 0:
        return current_trail_stop
    if current_trail_stop is None:
        return candidate_trail_stop
    # Never loosen the stop: only ratchet upward.
    return max(current_trail_stop, candidate_trail_stop)
