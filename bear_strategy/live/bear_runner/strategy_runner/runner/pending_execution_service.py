from __future__ import annotations

from typing import Callable

from UPS_py_v2.live.ups_runner.common.live_logger import LiveLogger
from UPS_py_v2.live.ups_runner.common.types import Position
from UPS_py_v2.live.ups_runner.order_manager.order_manager import OrderManager
from ...config import BearLiveConfig
from ...strategy_runner.session_state import RunnerSessionState


class BearPendingExecutionService:
    """Manage pending fills, stale limit entries, and deferred stop updates.

    Functionally identical to UPS PendingExecutionService but typed for
    BearLiveConfig so bear-specific interval_ms (1h = 3_600_000ms) is used
    correctly.
    """

    def __init__(self, cfg: BearLiveConfig, logger: LiveLogger) -> None:
        self.cfg = cfg
        self.logger = logger

    def apply_or_queue_stops(
        self,
        *,
        stop_loss: float | None,
        take_profit: float | None,
        position: Position,
        state: RunnerSessionState,
        orders: OrderManager,
    ) -> None:
        ok = orders.update_stops(
            stop_loss=stop_loss,
            take_profit=take_profit,
            position_size=position.size,
            position_side=position.side,
        )
        if ok:
            state.clear_pending_stop_update()
            return
        state.queue_pending_stop_update(stop_loss=stop_loss, take_profit=take_profit, side=position.side)
        self.logger.log("Stop update rejected; queued retry until exchange accepts it.")

    def retry_pending_stop_update_if_needed(
        self,
        *,
        position: Position | None,
        state: RunnerSessionState,
        orders: OrderManager,
    ) -> None:
        if state.pending_stop_side is None:
            return
        if position is None:
            state.clear_pending_stop_update()
            return
        if position.side != state.pending_stop_side:
            self.logger.log("Pending stop update side mismatch; dropping stale retry.")
            state.clear_pending_stop_update()
            return
        self.apply_or_queue_stops(
            stop_loss=state.pending_stop_loss,
            take_profit=state.pending_take_profit,
            position=position,
            state=state,
            orders=orders,
        )

    def cancel_stale_limit_entry_if_needed(
        self,
        *,
        last_ts: int,
        position: Position | None,
        state: RunnerSessionState,
        interval_ms: int,
        orders: OrderManager,
        attach_stops_for_pending_fill_if_needed: Callable[[Position | None], bool],
    ) -> None:
        if not self.cfg.cancel_unfilled_limit_entry:
            return
        if self.cfg.order_type != "Limit":
            return
        if state.pending_entry_order_id is None or state.pending_entry_bar_ts is None:
            return
        if attach_stops_for_pending_fill_if_needed(position):
            return
        bars_waited = int((last_ts - state.pending_entry_bar_ts) // interval_ms)
        if bars_waited < max(1, self.cfg.cancel_unfilled_limit_entry_after_bars):
            return
        orders.cancel_order_if_open(state.pending_entry_order_id)
        state.clear_pending_entry()
