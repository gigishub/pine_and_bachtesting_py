from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TradeState:
    """Mutable state that persists while one position is open."""

    trade_stop_price: float | None = None
    trade_target_price: float | None = None
    trail_stop_price: float | None = None
    active_stop_price: float | None = None
    look_for_exit: bool = False
    last_stop_sent: float | None = None

    def reset(self) -> None:
        self.trade_stop_price = None
        self.trade_target_price = None
        self.trail_stop_price = None
        self.active_stop_price = None
        self.look_for_exit = False
        self.last_stop_sent = None
