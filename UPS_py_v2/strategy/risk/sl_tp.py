"""Stop-loss and take-profit helpers for the UPS strategy.

Pure functions: receive bar-snapshot values, return a price level.
No side effects, no order placement.

Pine ATR stop model (long):
    longPriceSource = slReference == "High/Low" ? min(low, low[1])
                    : slReference == "Open"     ? open
                    :                             close
    longStopPrice   = longPriceSource - atr * stopMultiplier

Pine target model:
    longStopDistance  = close - longStopPrice
    tradeTargetPrice  = close + longStopDistance * riskRewardMultiplier
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Stop-loss
# ---------------------------------------------------------------------------

def compute_long_stop(
    sl_reference: str,
    low_now: float,
    low_prev: float,
    open_now: float,
    close_now: float,
    atr_now: float,
    stop_multiplier: float,
) -> float:
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
    ref = sl_reference.strip().lower()
    if ref == "high/low":
        src = max(high_now, high_prev)
    elif ref == "open":
        src = open_now
    else:
        src = close_now
    return float(src + (atr_now * stop_multiplier))


# ---------------------------------------------------------------------------
# Take-profit
# ---------------------------------------------------------------------------

def compute_long_target(
    entry_price: float,
    stop_price: float,
    risk_reward_multiplier: float,
) -> float:
    """Fixed-RR take-profit for a long entry."""
    risk = entry_price - stop_price
    return float(entry_price + (risk * risk_reward_multiplier))


def compute_short_target(
    entry_price: float,
    stop_price: float,
    risk_reward_multiplier: float,
) -> float:
    """Fixed-RR take-profit for a short entry."""
    risk = stop_price - entry_price
    return float(entry_price - (risk * risk_reward_multiplier))
