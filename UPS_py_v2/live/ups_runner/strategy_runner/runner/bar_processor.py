from __future__ import annotations

import time
from datetime import datetime, timezone

import pandas as pd

from ...common.live_logger import LiveLogger
from ...config import LiveConfig
from ..position_manager import PositionManager
from ..session_state import RunnerSessionState
from ..strategy_executor import StrategyExecutor
from ...common.types import Position
from ...order_manager.order_manager import OrderManager
from .entry_service import EntryService
from .pending_execution_service import PendingExecutionService


class BarProcessor:
    """Apply strategy logic to one fully closed bar."""

    def __init__(self, cfg: LiveConfig, logger: LiveLogger, interval_ms: int) -> None:
        self.cfg = cfg
        self.logger = logger
        self.interval_ms = interval_ms

    def process_closed_bar(
        self,
        *,
        df: pd.DataFrame,
        last_ts: int,
        strategy: StrategyExecutor,
        orders: OrderManager,
        position_manager: PositionManager,
        state: RunnerSessionState,
        entry_service: EntryService,
        pending_execution: PendingExecutionService,
    ) -> int:
        signals = strategy.compute(df)
        if not signals.is_ready:
            self.logger.log("Warmup not ready; skipping bar.")
            return last_ts

        position = orders.get_current_position()
        pending_execution.cancel_stale_limit_entry_if_needed(
            last_ts=last_ts,
            position=position,
            state=state,
            interval_ms=self.interval_ms,
            orders=orders,
            attach_stops_for_pending_fill_if_needed=lambda current_position: entry_service.attach_stops_for_pending_fill_if_needed(
                position=current_position,
                state=state,
                position_manager=position_manager,
                pending_execution=pending_execution,
                orders=orders,
            ),
        )
        pending_execution.retry_pending_stop_update_if_needed(position=position, state=state, orders=orders)
        if position is None and state.pending_entry_order_id is not None:
            self.logger.log("Pending limit entry still unfilled; waiting before issuing a new signal order.")
            return last_ts

        if position is None:
            entry_service.try_entry(
                df=df,
                signals=signals,
                bar_ts=last_ts,
                orders=orders,
                position_manager=position_manager,
                state=state,
                pending_execution=pending_execution,
            )
            time.sleep(0.2)
            position = orders.get_current_position()
            entry_service.attach_stops_for_pending_fill_if_needed(
                position=position,
                state=state,
                position_manager=position_manager,
                pending_execution=pending_execution,
                orders=orders,
            )

        if position is None:
            position_manager.on_flat()
        else:
            update = position_manager.update_for_closed_bar(df, signals, position)
            if update.should_update_stops:
                pending_execution.apply_or_queue_stops(
                    stop_loss=update.new_stop_price,
                    take_profit=update.new_take_profit,
                    position=position,
                    state=state,
                    orders=orders,
                )

        self.logger.log(
            f"Processed candle {datetime.fromtimestamp(last_ts / 1000, tz=timezone.utc)} "
            f"pos={'none' if position is None else position.side + ':' + str(position.size)}"
        )
        return last_ts
