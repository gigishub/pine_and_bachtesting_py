from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_DOWN
from typing import Any


@dataclass
class InstrumentSpec:
    """Exchange precision and order limits for one symbol/category."""

    symbol: str
    category: str
    tick_size: Decimal
    qty_step: Decimal
    min_order_qty: Decimal
    max_order_qty: Decimal


def to_decimal(value: Any) -> Decimal:
    return Decimal(str(value))


def floor_to_step(value: Decimal, step: Decimal) -> Decimal:
    if step <= 0:
        return value
    units = (value / step).to_integral_value(rounding=ROUND_DOWN)
    return units * step


def fmt_decimal(value: Decimal) -> str:
    s = format(value.normalize(), "f")
    return s.rstrip("0").rstrip(".") if "." in s else s
