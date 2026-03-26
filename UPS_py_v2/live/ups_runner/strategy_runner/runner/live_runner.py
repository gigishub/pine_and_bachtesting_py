from __future__ import annotations

import pandas as pd

from ....bybit_client import BybitV5Client, InstrumentSpec
from ...common.live_logger import LiveLogger
from ...common.types import Position
from ...config import LiveConfig, interval_to_ms, normalize_interval
from ...order_manager.order_manager import OrderManager
from ..market_data import LiveMarketDataService
from ..position_manager import PositionManager
from ..session_state import RunnerSessionState
from ..strategy_executor import StrategyExecutor
from .bar_processor import BarProcessor
from .entry_service import EntryService
from .loop_runner import LoopRunner
from .pending_execution_service import PendingExecutionService


class LiveRunner:
    def __init__(self, cfg: LiveConfig) -> None:
        self.cfg = cfg
        self.logger = LiveLogger()
        self.client = BybitV5Client(cfg.api_key, cfg.api_secret, testnet=cfg.testnet)
        self.interval = normalize_interval(cfg.timeframe)
        self.instrument: InstrumentSpec = self.client.get_instrument_spec(
            category=cfg.category,
            symbol=cfg.symbol,
        )
        self.market_data = LiveMarketDataService(
            client=self.client,
            cfg=cfg,
            interval=self.interval,
            interval_ms=interval_to_ms(self.interval),
        )
        self.strategy = StrategyExecutor(cfg)
        self.orders = OrderManager(self.client, cfg, self.instrument, self.logger)
        self.position = PositionManager(cfg, self.instrument.tick_size, self.logger)
        self.state = RunnerSessionState()
        self.entry_service = EntryService(cfg, self.logger)
        self.pending_execution = PendingExecutionService(cfg, self.logger)
        self.bar_processor = BarProcessor(cfg, self.logger, interval_to_ms(self.interval))
        self.loop_runner = LoopRunner(
            cfg=cfg,
            logger=self.logger,
            client=self.client,
            market_data=self.market_data,
            interval=self.interval,
            interval_ms=interval_to_ms(self.interval),
        )

    @property
    def interval_ms(self) -> int:
        return interval_to_ms(self.interval)

    @property
    def last_processed_ts(self) -> int | None:
        return self.loop_runner.last_processed_ts

    @last_processed_ts.setter
    def last_processed_ts(self, value: int | None) -> None:
        self.loop_runner.last_processed_ts = value

    # Backward-compatible attribute access for tests/scripts that reference
    # pending fields directly on runner.
    @property
    def pending_entry_order_id(self) -> str | None:
        return self.state.pending_entry_order_id

    @pending_entry_order_id.setter
    def pending_entry_order_id(self, value: str | None) -> None:
        self.state.pending_entry_order_id = value

    @property
    def pending_entry_bar_ts(self) -> int | None:
        return self.state.pending_entry_bar_ts

    @pending_entry_bar_ts.setter
    def pending_entry_bar_ts(self, value: int | None) -> None:
        self.state.pending_entry_bar_ts = value

    @property
    def pending_entry_stop_price(self) -> float | None:
        return self.state.pending_entry_stop_price

    @pending_entry_stop_price.setter
    def pending_entry_stop_price(self, value: float | None) -> None:
        self.state.pending_entry_stop_price = value

    @property
    def pending_entry_target_price(self) -> float | None:
        return self.state.pending_entry_target_price

    @pending_entry_target_price.setter
    def pending_entry_target_price(self, value: float | None) -> None:
        self.state.pending_entry_target_price = value

    @property
    def pending_stop_loss(self) -> float | None:
        return self.state.pending_stop_loss

    @pending_stop_loss.setter
    def pending_stop_loss(self, value: float | None) -> None:
        self.state.pending_stop_loss = value

    @property
    def pending_take_profit(self) -> float | None:
        return self.state.pending_take_profit

    @pending_take_profit.setter
    def pending_take_profit(self, value: float | None) -> None:
        self.state.pending_take_profit = value

    @property
    def pending_stop_side(self) -> str | None:
        return self.state.pending_stop_side

    @pending_stop_side.setter
    def pending_stop_side(self, value: str | None) -> None:
        self.state.pending_stop_side = value

    def _retry_pending_stop_update_if_needed(self, position: Position | None) -> None:
        self.pending_execution.retry_pending_stop_update_if_needed(
            position=position,
            state=self.state,
            orders=self.orders,
        )

    def _attach_stops_for_pending_fill_if_needed(self, position: Position | None) -> bool:
        return self.entry_service.attach_stops_for_pending_fill_if_needed(
            position=position,
            state=self.state,
            position_manager=self.position,
            pending_execution=self.pending_execution,
            orders=self.orders,
        )

    def _process_closed_bar(self, df: pd.DataFrame, last_ts: int) -> None:
        self.last_processed_ts = self.bar_processor.process_closed_bar(
            df=df,
            last_ts=last_ts,
            strategy=self.strategy,
            orders=self.orders,
            position_manager=self.position,
            state=self.state,
            entry_service=self.entry_service,
            pending_execution=self.pending_execution,
        )

    def _run_polling_loop(self) -> None:
        self.loop_runner.run_polling_loop(self._process_closed_bar)

    def _run_ws_loop(self) -> None:
        self.loop_runner.run_ws_loop(
            process_closed_bar=self._process_closed_bar,
            state=self.state,
            orders=self.orders,
            attach_stops_for_pending_fill_if_needed=self._attach_stops_for_pending_fill_if_needed,
            retry_pending_stop_update_if_needed=self._retry_pending_stop_update_if_needed,
        )

    def run_forever(self) -> None:
        self.logger.log(
            f"Starting live runner symbol={self.cfg.symbol} category={self.cfg.category} "
            f"tf={self.cfg.timeframe} dry_run={self.cfg.dry_run} mode={'ws' if self.cfg.use_ws_kline else 'polling'}"
        )
        self.orders.apply_leverage_if_configured()
        if self.cfg.use_ws_kline:
            self._run_ws_loop()
        else:
            self._run_polling_loop()


# Backward-compatibility alias.
UPSLiveRunner = LiveRunner
