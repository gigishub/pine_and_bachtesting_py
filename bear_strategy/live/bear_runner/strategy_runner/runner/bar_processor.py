from __future__ import annotations

import time
from datetime import datetime, timezone

import pandas as pd

from UPS_py_v2.live.ups_runner.common.live_logger import LiveLogger
from UPS_py_v2.live.ups_runner.common.types import Position
from UPS_py_v2.live.ups_runner.order_manager.order_manager import OrderManager
from ...config import BearLiveConfig
from ...strategy_runner.position_manager import BearPositionManager
from ...strategy_runner.session_state import RunnerSessionState
from ...strategy_runner.strategy_executor import BearStrategyExecutor
from .entry_service import BearEntryService
from .pending_execution_service import BearPendingExecutionService

# 1h bar in milliseconds
_1H_MS = 3_600_000


class BearBarProcessor:
    """Apply bear strategy logic to one fully closed 1h bar."""

    def __init__(self, cfg: BearLiveConfig, logger: LiveLogger) -> None:
        self.cfg = cfg
        self.logger = logger

    def process_closed_bar(
        self,
        *,
        df_1h: pd.DataFrame,
        df_1d: pd.DataFrame,
        funding_df: pd.DataFrame,
        last_ts: int,
        strategy: BearStrategyExecutor,
        orders: OrderManager,
        position_manager: BearPositionManager,
        state: RunnerSessionState,
        entry_service: BearEntryService,
        pending_execution: BearPendingExecutionService,
    ) -> int:
        signals = strategy.compute(df_1h, df_1d, funding_df)
        if not signals.is_ready:
            self.logger.log("Warmup not complete; skipping bar.")
            return last_ts

        self.logger.log(
            f"Signals: entry={signals.entry_signal}  regime={signals.regime_active}"
            f"  atr={signals.atr_value:.6f}"
        )

        position = orders.get_current_position()

        pending_execution.cancel_stale_limit_entry_if_needed(
            last_ts=last_ts,
            position=position,
            state=state,
            interval_ms=_1H_MS,
            orders=orders,
            attach_stops_for_pending_fill_if_needed=lambda pos: (
                entry_service.attach_stops_for_pending_fill_if_needed(
                    position=pos,
                    state=state,
                    position_manager=position_manager,
                    pending_execution=pending_execution,
                    orders=orders,
                )
            ),
        )
        pending_execution.retry_pending_stop_update_if_needed(
            position=position, state=state, orders=orders
        )

        # Wait if a limit entry is still pending fill
        if position is None and state.pending_entry_order_id is not None:
            self.logger.log("Pending limit entry still unfilled; waiting.")
            return last_ts

        if position is None:
            entry_service.try_entry(
                df_1h=df_1h,
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

        # Sync position manager — bear has no trailing stop to advance
        position_manager.update_for_closed_bar(position)

        self.logger.log(
            f"Processed candle {datetime.fromtimestamp(last_ts / 1000, tz=timezone.utc)} "
            f"pos={'none' if position is None else position.side + ':' + str(position.size)}"
        )
        return last_ts
