"""Risk-based position sizing.

Size each trade so that if the initial stop is hit, the loss equals exactly
`risk_pct`% of current equity.  Clipped to 99.99% of equity to avoid
margin issues in backtesting.py.
"""

from __future__ import annotations


def compute_position_size(
    entry_price: float,
    stop_price: float,
    equity: float,
    risk_pct: float = 1.0,
) -> float:
    """Return order size as a fraction of equity (0.0 – 0.9999).

    Formula:
        risk_cash     = equity × (risk_pct / 100)
        units         = risk_cash / (entry_price - stop_price)
        notional      = units × entry_price
        size_fraction = notional / equity

    Args:
        entry_price:  Expected fill price (next-bar open approximation).
        stop_price:   Initial Chandelier stop at entry bar.
        equity:       Current account equity.
        risk_pct:     Percentage of equity to risk.  Default 1.0 = 1%.

    Returns:
        Fraction in (0.0, 0.9999], or 0.0 if inputs are invalid.
    """
    stop_distance = entry_price - stop_price
    if stop_distance <= 0 or equity <= 0 or risk_pct <= 0:
        return 0.0
    risk_cash = equity * (risk_pct / 100.0)
    units = risk_cash / stop_distance
    notional = units * entry_price
    return float(max(0.0, min(notional / equity, 0.9999)))
