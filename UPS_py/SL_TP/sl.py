"""Stop-loss helpers for the UPS strategy.

Pure functions: receive bar-snapshot values, return a stop price.
No side effects, no order placement.

Pine ATR stop model:
    longPriceSource = slReference == "High/Low" ? (low < low[1] ? low : low[1])
                    : slReference == "Open"     ? open
                    :                             close
    longStopPrice   = longPriceSource - atr * stopMultiplier
"""

from __future__ import annotations


def compute_long_stop(
    sl_reference: str,
    low_now: float,
    low_prev: float,
    open_now: float,
    close_now: float,
    atr_now: float,
    stop_multiplier: float,
) -> float:
    """Compute the initial ATR-based stop price for a long entry.

    Mirrors Pine:
        longPriceSource = slReference == "High/Low" ? (low < low[1] ? low : low[1])
                        : slReference == "Open"     ? open
                        :                             close
        longStopPrice = longPriceSource - atr * stopMultiplier

    Step 5 implementation.
    """
    ref = sl_reference.strip().lower()
    if ref == "high/low":
        src = min(low_now, low_prev)
    elif ref == "open":
        src = open_now
    else:
        src = close_now
    return float(src - (atr_now * stop_multiplier))


def compute_short_stop(
    sl_reference: str,
    high_now: float,
    high_prev: float,
    open_now: float,
    close_now: float,
    atr_now: float,
    stop_multiplier: float,
) -> float:
    """Compute the initial ATR-based stop price for a short entry."""
    ref = sl_reference.strip().lower()
    if ref == "high/low":
        src = max(high_now, high_prev)
    elif ref == "open":
        src = open_now
    else:
        src = close_now
    return float(src + (atr_now * stop_multiplier))
