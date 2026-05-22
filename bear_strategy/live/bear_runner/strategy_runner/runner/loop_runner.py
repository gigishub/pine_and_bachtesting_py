from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Callable, cast

import pandas as pd

from UPS_py_v2.live.bybit_client import BybitPublicKlineStream, BybitV5Client
from UPS_py_v2.live.ups_runner.common.live_logger import LiveLogger
from UPS_py_v2.live.ups_runner.common.types import Position
from UPS_py_v2.live.ups_runner.order_manager.order_manager import OrderManager
from ...config import BearLiveConfig
from ...strategy_runner.market_data import BearMarketDataService
from ...strategy_runner.session_state import RunnerSessionState

_1H_MS = 3_600_000


class BearLoopRunner:
    """Transport-specific loops (polling and WebSocket) for the bear runner.

    Key difference from UPS: on every closed 1h bar the loop *also* refreshes
    the 1d OHLCV and funding history via REST (two quick calls).  This keeps
    the regime and funding guard data fresh without a separate scheduler.

    The callback signature is:
        process_closed_bar(df_1h, df_1d, funding_df, last_ts)
    """

    def __init__(
        self,
        *,
        cfg: BearLiveConfig,
        logger: LiveLogger,
        client: BybitV5Client,
        market_data: BearMarketDataService,
    ) -> None:
        self.cfg = cfg
        self.logger = logger
        self.client = client
        self.market_data = market_data
        self.last_processed_ts: int | None = None

    # ── Polling loop ──────────────────────────────────────────────────────────

    def run_polling_loop(
        self,
        process_closed_bar: Callable[[pd.DataFrame, pd.DataFrame, pd.DataFrame, int], None],
    ) -> None:
        """REST-polling fallback: wait for each 1h close then fetch all data."""
        while True:
            try:
                self.market_data.sleep_until_next_1h_close()
                raw_1h = self.market_data.fetch_ohlcv_1h()
                df_1h = self.market_data.closed_df(raw_1h)
                last_ts = int(df_1h["Timestamp"].iloc[-1])
                if self.last_processed_ts is not None and last_ts <= self.last_processed_ts:
                    continue
                df_1d = self.market_data.fetch_ohlcv_1d()
                funding_df = self.market_data.fetch_funding_history()
                process_closed_bar(df_1h, df_1d, funding_df, last_ts)
                self.last_processed_ts = last_ts
            except KeyboardInterrupt:
                self.logger.log("Stopped by user.")
                raise
            except Exception as exc:
                self.logger.log(f"Polling loop error: {exc}")
                time.sleep(2.0)

    # ── WebSocket loop ────────────────────────────────────────────────────────

    def run_ws_loop(
        self,
        *,
        process_closed_bar: Callable[[pd.DataFrame, pd.DataFrame, pd.DataFrame, int], None],
        state: RunnerSessionState,
        orders: OrderManager,
        attach_stops_for_pending_fill_if_needed: Callable[[Position | None], bool],
        retry_pending_stop_update_if_needed: Callable[[Position | None], None],
    ) -> None:
        """WebSocket mode: bootstrap history then process each closed 1h kline."""
        closed_1h, df_1d, funding_df = self.market_data.bootstrap_closed_history()
        self.last_processed_ts = int(closed_1h["Timestamp"].iloc[-1])
        self.logger.log(
            f"WS mode active. Warmup bars={len(closed_1h)} "
            f"last={datetime.fromtimestamp(self.last_processed_ts / 1000, tz=timezone.utc)}"
        )

        stream = BybitPublicKlineStream(
            ws_url=self.client.public_ws_url(self.cfg.category),
            symbol=self.cfg.symbol,
            interval="60",  # 1h interval
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
                    # Timeout: handle pending state, then keep alive
                    if state.pending_entry_order_id is not None:
                        position = orders.get_current_position()
                        if attach_stops_for_pending_fill_if_needed(position):
                            continue
                    if state.pending_stop_side is not None:
                        position = orders.get_current_position()
                        retry_pending_stop_update_if_needed(position)
                        if state.pending_stop_side is None:
                            self.logger.log("Pending stop retry succeeded.")
                            continue
                    self.logger.log("WS timeout; keeping alive.")
                    continue

                start_ts = int(row.get("start") or 0)
                if start_ts <= 0:
                    continue
                if self.last_processed_ts is not None and start_ts <= self.last_processed_ts:
                    continue

                # Gap detection: re-bootstrap history from REST
                if (
                    self.last_processed_ts is not None
                    and start_ts > (self.last_processed_ts + _1H_MS)
                ):
                    self.logger.log("Kline gap detected; restoring history from REST.")
                    closed_1h, df_1d, funding_df = self.market_data.bootstrap_closed_history()
                    missed = closed_1h[closed_1h["Timestamp"] > self.last_processed_ts]
                    for idx in missed.index:
                        ts = int(cast(int, closed_1h.loc[idx, "Timestamp"]))
                        # Re-fetch 1d / funding once per missed bar is acceptable
                        try:
                            df_1d = self.market_data.fetch_ohlcv_1d()
                            funding_df = self.market_data.fetch_funding_history()
                        except Exception as exc:
                            self.logger.log(f"Gap fill: secondary data fetch error: {exc}")
                        process_closed_bar(closed_1h.loc[:idx], df_1d, funding_df, ts)
                    self.last_processed_ts = int(closed_1h["Timestamp"].iloc[-1])
                    continue

                # Normal path: append new bar, refresh secondary data, process
                closed_1h = self.market_data.append_closed_ws_kline(closed_1h, row)
                last_ts = int(cast(int, closed_1h["Timestamp"].iloc[-1]))
                if last_ts <= (self.last_processed_ts or 0):
                    continue

                try:
                    df_1d = self.market_data.fetch_ohlcv_1d()
                    funding_df = self.market_data.fetch_funding_history()
                except Exception as exc:
                    self.logger.log(f"Secondary data fetch error: {exc}; using cached data.")

                process_closed_bar(closed_1h, df_1d, funding_df, last_ts)
                self.last_processed_ts = last_ts

        except KeyboardInterrupt:
            self.logger.log("Stopped by user.")
            raise
        finally:
            stream.stop()
