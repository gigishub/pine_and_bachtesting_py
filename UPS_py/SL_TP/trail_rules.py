"""Trailing-stop helpers for the UPS strategy.

Pure functions: receive bar-snapshot values, return updated trailing state.
No side effects, no order placement.

Pine trailing model:
    - Trail is OFF until high >= tradeTargetPrice  (lookForExit flag).
    - Once activated: trailStopPrice ratchets up each bar (never loosens).
    - Effective stop = max(tradeStopPrice, trailStopPrice).
    - While trailing is active, TP is disabled (limit=na in Pine).

See also:
    sl.py — ATR stop-loss computation
    tp.py — fixed RR target computation
"""

from __future__ import annotations


def compute_long_trail_candidate(
    trail_source: str,
    close_prev: float,
    open_prev: float,
    lookback_low: float,
    atr_now: float,
    trail_stop_size: float,
) -> float:
    """Compute the trailing-stop candidate for the current bar (long side).

    Mirrors Pine:
        trailSrcLong  = trailSource == "Close" ? close[1]
                      : trailSource == "Open"  ? open[1]
                      :                          ta.lowest(low, lookback)
        trailCandidate = trailSrcLong - atr * trailStopSize

    Step 5 implementation.
    """
    src_key = trail_source.strip().lower()
    if src_key == "close":
        src = close_prev
    elif src_key == "open":
        src = open_prev
    else:
        src = lookback_low
    return float(src - (atr_now * trail_stop_size))


def compute_short_trail_candidate(
    trail_source: str,
    close_prev: float,
    open_prev: float,
    lookback_high: float,
    atr_now: float,
    trail_stop_size: float,
) -> float:
    """Compute the trailing-stop candidate for the current bar (short side)."""
    src_key = trail_source.strip().lower()
    if src_key == "close":
        src = close_prev
    elif src_key == "open":
        src = open_prev
    else:
        src = lookback_high
    return float(src + (atr_now * trail_stop_size))


def update_long_trail_stop(
    position_size: float,
    look_for_exit: bool,
    current_trail_stop: float | None,
    candidate_trail_stop: float,
) -> float | None:
    """Ratchet the trailing stop upward; only runs after target is reached.

    Returns None when trailing has not yet been activated (look_for_exit=False).

    Mirrors Pine:
        if (trailStop and lookForExit and barstate.isconfirmed)
            trailStopPrice := na(trailStopPrice) ? trailCandidate
                            : math.max(trailStopPrice, trailCandidate)

    Step 5 implementation.
    """
    if position_size <= 0:
        return current_trail_stop
    if not look_for_exit:
        return current_trail_stop
    if current_trail_stop is None:
        return float(candidate_trail_stop)
    return float(max(current_trail_stop, candidate_trail_stop))


def update_short_trail_stop(
    position_size: float,
    look_for_exit: bool,
    current_trail_stop: float | None,
    candidate_trail_stop: float,
) -> float | None:
    """Ratchet the trailing stop downward for a short trade."""
    if position_size >= 0:
        return current_trail_stop
    if not look_for_exit:
        return current_trail_stop
    if current_trail_stop is None:
        return float(candidate_trail_stop)
    return float(min(current_trail_stop, candidate_trail_stop))


def active_long_stop(
    trade_stop_price: float,
    trail_stop_price: float | None,
) -> float:
    """Return the effective stop to write to Trade.sl each bar.

    When trail is active  : max(trade_stop_price, trail_stop_price).
    When trail not active : trade_stop_price only.

    Mirrors Pine:
        activeStop = trailStop and not na(trailStopPrice)
                   ? math.max(tradeStopPrice, trailStopPrice)
                   : tradeStopPrice

    Step 5 implementation.
    """
    if trail_stop_price is None:
        return float(trade_stop_price)
    return float(max(trade_stop_price, trail_stop_price))


def active_short_stop(
    trade_stop_price: float,
    trail_stop_price: float | None,
) -> float:
    """Return the effective stop to write to Trade.sl each bar for a short trade."""
    if trail_stop_price is None:
        return float(trade_stop_price)
    return float(min(trade_stop_price, trail_stop_price))
