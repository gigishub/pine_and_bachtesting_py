from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Callable, cast

import pandas as pd

from ....bybit_client import BybitPublicKlineStream, BybitV5Client
from ...common.live_logger import LiveLogger
from ...config import LiveConfig
from ..market_data import LiveMarketDataService
from ..session_state import RunnerSessionState
from ...common.types import Position
from ...order_manager.order_manager import OrderManager


class LoopRunner:
    """Transport-specific loops for polling and websocket execution."""

    def __init__(
        self,
        *,
        cfg: LiveConfig,
        logger: LiveLogger,
        client: BybitV5Client,
        market_data: LiveMarketDataService,
        interval: str,
        interval_ms: int,
    ) -> None:
        self.cfg = cfg
        self.logger = logger
        self.client = client
        self.market_data = market_data
        self.interval = interval
        self.interval_ms = interval_ms
        self.last_processed_ts: int | None = None

    def run_polling_loop(self, process_closed_bar: Callable[[pd.DataFrame, int], None]) -> None:
        while True:
            try:
                self.market_data.sleep_until_next_close()
                raw_df = self.market_data.fetch_ohlcv()
                closed_df = self.market_data.closed_df(raw_df)
                last_ts = int(closed_df["Timestamp"].iloc[-1])
                if self.last_processed_ts is not None and last_ts <= self.last_processed_ts:
                    continue
                process_closed_bar(closed_df, last_ts)
            except KeyboardInterrupt:
                self.logger.log("Stopped by user.")
                raise
            except Exception as exc:
                self.logger.log(f"Loop error: {exc}")
                time.sleep(2.0)

    def run_ws_loop(
        self,
        *,
        process_closed_bar: Callable[[pd.DataFrame, int], None],
        state: RunnerSessionState,
        orders: OrderManager,
        attach_stops_for_pending_fill_if_needed: Callable[[Position | None], bool],
        retry_pending_stop_update_if_needed: Callable[[Position | None], None],
    ) -> None:
        closed_history = self.market_data.bootstrap_closed_history()
        self.last_processed_ts = int(closed_history["Timestamp"].iloc[-1])
        self.logger.log(
            f"WebSocket mode active. Warmup candles={len(closed_history)} "
            f"last={datetime.fromtimestamp(self.last_processed_ts / 1000, tz=timezone.utc)}"
        )
        stream = BybitPublicKlineStream(
            ws_url=self.client.public_ws_url(self.cfg.category),
            symbol=self.cfg.symbol,
            interval=self.interval,
        )
        stream.start()
        try:
            while True:
                timeout_s = self.cfg.ws_queue_timeout_s
                if state.pending_entry_order_id is not None:
                    timeout_s = min(timeout_s, self.cfg.pending_fill_check_interval_s)
                if state.pending_stop_side is not None:
                    timeout_s = min(timeout_s, self.cfg.pending_stop_retry_interval_s)

                row = stream.get_next_closed_kline(timeout_s=timeout_s)
                if row is None:
                    if state.pending_entry_order_id is not None:
                        position = orders.get_current_position()
                        if attach_stops_for_pending_fill_if_needed(position):
                            continue
                    if state.pending_stop_side is not None:
                        position = orders.get_current_position()
                        retry_pending_stop_update_if_needed(position)
                        if state.pending_stop_side is None:
                            self.logger.log("Pending stop update retry succeeded.")
                            continue
                    self.logger.log("WS timeout; keeping alive.")
                    continue

                start_ts = int(row.get("start") or 0)
                if start_ts <= 0:
                    continue
                if self.last_processed_ts is not None and start_ts <= self.last_processed_ts:
                    continue

                if self.last_processed_ts is not None and start_ts > (self.last_processed_ts + self.interval_ms):
                    self.logger.log("Detected kline gap; restoring history from REST.")
                    closed_history = self.market_data.bootstrap_closed_history()
                    missed = closed_history[closed_history["Timestamp"] > self.last_processed_ts]
                    for idx in missed.index:
                        ts = int(cast(int, closed_history.loc[idx, "Timestamp"]))
                        process_closed_bar(closed_history.loc[:idx], ts)
                    continue

                closed_history = self.market_data.append_closed_ws_kline(closed_history, row)
                last_idx = closed_history.index[-1]
                last_ts = int(cast(int, closed_history.loc[last_idx, "Timestamp"]))
                if last_ts <= (self.last_processed_ts or 0):
                    continue
                process_closed_bar(closed_history, last_ts)
        except KeyboardInterrupt:
            self.logger.log("Stopped by user.")
            raise
        finally:
            stream.stop()
