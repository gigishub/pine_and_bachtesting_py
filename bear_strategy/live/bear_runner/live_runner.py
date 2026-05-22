from __future__ import annotations

import pandas as pd

from UPS_py_v2.live.bybit_client import BybitV5Client, InstrumentSpec
from UPS_py_v2.live.ups_runner.common.live_logger import LiveLogger
from UPS_py_v2.live.ups_runner.common.types import Position
from UPS_py_v2.live.ups_runner.order_manager.order_manager import OrderManager
from .config import BearLiveConfig
from .strategy_runner.market_data import BearMarketDataService
from .strategy_runner.position_manager import BearPositionManager
from .strategy_runner.session_state import RunnerSessionState
from .strategy_runner.strategy_executor import BearStrategyExecutor
from .strategy_runner.runner.bar_processor import BearBarProcessor
from .strategy_runner.runner.entry_service import BearEntryService
from .strategy_runner.runner.loop_runner import BearLoopRunner
from .strategy_runner.runner.pending_execution_service import BearPendingExecutionService


class BearLiveRunner:
    """Orchestrator for the bear strategy live runner.

    Wires all components together and exposes ``run_forever()`` as the main
    entry point.  Mirrors the structure of UPS ``LiveRunner``.
    """

    def __init__(self, cfg: BearLiveConfig) -> None:
        self.cfg = cfg
        self.logger = LiveLogger()
        self.client = BybitV5Client(cfg.api_key, cfg.api_secret, testnet=cfg.testnet)
        self.instrument: InstrumentSpec = self.client.get_instrument_spec(
            category=cfg.category,
            symbol=cfg.symbol,
        )
        self.market_data = BearMarketDataService(client=self.client, cfg=cfg)
        self.strategy = BearStrategyExecutor(cfg)
        self.orders = OrderManager(self.client, cfg, self.instrument, self.logger)
        self.position = BearPositionManager()
        self.state = RunnerSessionState()
        self.entry_service = BearEntryService(cfg, self.logger)
        self.pending_execution = BearPendingExecutionService(cfg, self.logger)
        self.bar_processor = BearBarProcessor(cfg, self.logger)
        self.loop_runner = BearLoopRunner(
            cfg=cfg,
            logger=self.logger,
            client=self.client,
            market_data=self.market_data,
        )

    @property
    def last_processed_ts(self) -> int | None:
        return self.loop_runner.last_processed_ts

    @last_processed_ts.setter
    def last_processed_ts(self, value: int | None) -> None:
        self.loop_runner.last_processed_ts = value

    def _attach_stops_for_pending_fill_if_needed(self, position: Position | None) -> bool:
        return self.entry_service.attach_stops_for_pending_fill_if_needed(
            position=position,
            state=self.state,
            position_manager=self.position,
            pending_execution=self.pending_execution,
            orders=self.orders,
        )

    def _retry_pending_stop_update_if_needed(self, position: Position | None) -> None:
        self.pending_execution.retry_pending_stop_update_if_needed(
            position=position,
            state=self.state,
            orders=self.orders,
        )

    def _process_closed_bar(
        self,
        df_1h: pd.DataFrame,
        df_1d: pd.DataFrame,
        funding_df: pd.DataFrame,
        last_ts: int,
    ) -> None:
        self.loop_runner.last_processed_ts = self.bar_processor.process_closed_bar(
            df_1h=df_1h,
            df_1d=df_1d,
            funding_df=funding_df,
            last_ts=last_ts,
            strategy=self.strategy,
            orders=self.orders,
            position_manager=self.position,
            state=self.state,
            entry_service=self.entry_service,
            pending_execution=self.pending_execution,
        )

    def run_forever(self) -> None:
        self.logger.log(
            f"Starting bear live runner  symbol={self.cfg.symbol}  "
            f"category={self.cfg.category}  tf={self.cfg.timeframe}  "
            f"dry_run={self.cfg.dry_run}  "
            f"mode={'ws' if self.cfg.use_ws_kline else 'polling'}"
        )
        self.orders.apply_leverage_if_configured()
        if self.cfg.use_ws_kline:
            self.loop_runner.run_ws_loop(
                process_closed_bar=self._process_closed_bar,
                state=self.state,
                orders=self.orders,
                attach_stops_for_pending_fill_if_needed=self._attach_stops_for_pending_fill_if_needed,
                retry_pending_stop_update_if_needed=self._retry_pending_stop_update_if_needed,
            )
        else:
            self.loop_runner.run_polling_loop(self._process_closed_bar)
