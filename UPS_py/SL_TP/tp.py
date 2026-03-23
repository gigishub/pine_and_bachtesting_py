"""Take-profit target helpers for the UPS strategy.

Pure functions: receive entry/stop prices, return target price.
No side effects, no order placement.

Pine target model:
    longStopDistance  = close - longStopPrice
    tradeTargetPrice  = close + longStopDistance * riskRewardMultiplier

When trailing is active the TP is disabled in Pine (limit=na), so
the target price returned here is used in two ways:
  1. As the fixed TP when trail_stop=False  → passed to Trade.tp.
  2. As the activation threshold for the trail when trail_stop=True
     → compared against high each bar; Trade.tp is set to None once active.
"""

from __future__ import annotations


def compute_long_target(
    entry_price: float,
    stop_price: float,
    risk_reward_multiplier: float,
) -> float:
    """Compute the fixed-RR take-profit price for a long entry.

    Mirrors Pine:
        longStopDistance = close - longStopPrice
        tradeTargetPrice = close + longStopDistance * riskRewardMultiplier

    Step 5 implementation.
    """
    risk = entry_price - stop_price
    return float(entry_price + (risk * risk_reward_multiplier))


def compute_short_target(
    entry_price: float,
    stop_price: float,
    risk_reward_multiplier: float,
) -> float:
    """Compute the fixed-RR take-profit price for a short entry."""
    risk = stop_price - entry_price
    return float(entry_price - (risk * risk_reward_multiplier))
