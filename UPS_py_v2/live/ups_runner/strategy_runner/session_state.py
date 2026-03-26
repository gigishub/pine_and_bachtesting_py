from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RunnerSessionState:
    """Ephemeral runtime state for one live runner process."""

    pending_entry_order_id: str | None = None
    pending_entry_bar_ts: int | None = None
    pending_entry_stop_price: float | None = None
    pending_entry_target_price: float | None = None

    pending_stop_loss: float | None = None
    pending_take_profit: float | None = None
    pending_stop_side: str | None = None

    def set_pending_entry(self, *, order_id: str, bar_ts: int, stop_price: float, target_price: float) -> None:
        self.pending_entry_order_id = order_id
        self.pending_entry_bar_ts = bar_ts
        self.pending_entry_stop_price = stop_price
        self.pending_entry_target_price = target_price

    def clear_pending_entry(self) -> None:
        self.pending_entry_order_id = None
        self.pending_entry_bar_ts = None
        self.pending_entry_stop_price = None
        self.pending_entry_target_price = None

    def queue_pending_stop_update(self, *, stop_loss: float | None, take_profit: float | None, side: str) -> None:
        self.pending_stop_loss = stop_loss
        self.pending_take_profit = take_profit
        self.pending_stop_side = side

    def clear_pending_stop_update(self) -> None:
        self.pending_stop_loss = None
        self.pending_take_profit = None
        self.pending_stop_side = None
