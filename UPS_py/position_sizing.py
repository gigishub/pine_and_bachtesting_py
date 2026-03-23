from __future__ import annotations


def compute_long_size_fraction(
    entry_price: float,
    stop_price: float,
    equity: float,
    risk_per_trade: float,
) -> float:
    """Return order size as fraction of current equity based on risk-per-trade.

    risk_cash = equity * (risk_per_trade / 100)
    units = risk_cash / (entry_price - stop_price)
    notional = units * entry_price
    size_fraction = notional / equity

    backtesting.py interprets size in (0.0, 1.0) as a fraction of available liquidity.
    """
    stop_distance = entry_price - stop_price
    if stop_distance <= 0 or equity <= 0 or risk_per_trade <= 0:
        return 0.0

    risk_cash = equity * (risk_per_trade / 100.0)
    if risk_cash <= 0:
        return 0.0

    units = risk_cash / stop_distance
    notional = units * entry_price
    if notional <= 0:
        return 0.0

    return max(0.0, min(notional / equity, 0.9999))


def compute_short_size_fraction(
    entry_price: float,
    stop_price: float,
    equity: float,
    risk_per_trade: float,
) -> float:
    """Return short order size as fraction of current equity based on risk-per-trade."""
    stop_distance = stop_price - entry_price
    if stop_distance <= 0 or equity <= 0 or risk_per_trade <= 0:
        return 0.0

    risk_cash = equity * (risk_per_trade / 100.0)
    if risk_cash <= 0:
        return 0.0

    units = risk_cash / stop_distance
    notional = units * entry_price
    if notional <= 0:
        return 0.0

    return max(0.0, min(notional / equity, 0.9999))
