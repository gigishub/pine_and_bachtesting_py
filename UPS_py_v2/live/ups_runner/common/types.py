from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class StrategySignals:
    """Scalar signal values extracted from the most recent closed bar."""

    is_ready: bool
    price_above_ma: bool
    long_conditions_met: bool
    bearish_pb: bool
    long_entry_pattern: bool
    short_conditions_met: bool
    bullish_pb: bool
    short_entry_pattern: bool
    atr_value: float


@dataclass
class Position:
    """Exchange position snapshot parsed from the Bybit API response."""

    side: Literal["Buy", "Sell"]
    size: float
    avg_price: float


@dataclass
class PositionUpdate:
    """Instructions returned by PositionManager after processing one closed bar."""

    should_update_stops: bool
    new_stop_price: float | None = None
    new_take_profit: float | None = None
