from __future__ import annotations

import logging
from uuid import uuid4

import pandas as pd

from UPS_py_v2.live.ups_runner.common.live_logger import LiveLogger
from UPS_py_v2.live.ups_runner.order_manager.order_manager import OrderManager
from ...common.types import BearSignals, Position
from ...config import BearLiveConfig
from ...stats_logger import BearSignalLogger
from ...strategy_runner.position_manager import BearPositionManager
from ...strategy_runner.session_state import RunnerSessionState
from .pending_execution_service import BearPendingExecutionService

logger = logging.getLogger(__name__)


class BearEntryService:
    """Build and place short entries for the bear strategy.

    Stop:   close + stop_atr_mult × ATR  (above entry → exits on rise)
    Target: close − target_atr_mult × ATR (below entry → exits on drop)
    """

    def __init__(self, cfg: BearLiveConfig, live_logger: LiveLogger) -> None:
        self.cfg = cfg
        self.logger = live_logger
        self.signal_logger = BearSignalLogger(cfg)

    def attach_stops_for_pending_fill(
        self,
        *,
        position: Position,
        state: RunnerSessionState,
        position_manager: BearPositionManager,
        pending_execution: BearPendingExecutionService,
        orders: OrderManager,
    ) -> None:
        """Reconcile state after a pending limit entry fills."""
        if (
            state.pending_entry_stop_price is not None
            and state.pending_entry_target_price is not None
        ):
            position_manager.on_entry(
                state.pending_entry_stop_price,
                state.pending_entry_target_price,
            )
        self.logger.log("Pending limit entry filled; protection was attached on entry order.")
        state.clear_pending_entry()

    def attach_stops_for_pending_fill_if_needed(
        self,
        *,
        position: Position | None,
        state: RunnerSessionState,
        position_manager: BearPositionManager,
        pending_execution: BearPendingExecutionService,
        orders: OrderManager,
    ) -> bool:
        if position is None or state.pending_entry_order_id is None:
            return False
        self.attach_stops_for_pending_fill(
            position=position,
            state=state,
            position_manager=position_manager,
            pending_execution=pending_execution,
            orders=orders,
        )
        return True

    def try_entry(
        self,
        *,
        df_1h: pd.DataFrame,
        signals: BearSignals,
        bar_ts: int,
        orders: OrderManager,
        position_manager: BearPositionManager,
        state: RunnerSessionState,
        pending_execution: BearPendingExecutionService,
    ) -> None:
        """Place a short entry if all signal conditions are met."""
        if not signals.entry_signal:
            return

        trade_id = str(uuid4())
        close_now = float(df_1h["close"].iloc[-1])
        atr_now = signals.atr_value

        # SL above entry (short stops on price rise)
        stop_price = close_now + self.cfg.stop_atr_mult * atr_now
        # TP below entry (short profits on price drop)
        target_price = close_now - self.cfg.target_atr_mult * atr_now

        # Guard: SL distance sanity check
        sl_pct = (stop_price - close_now) / close_now
        if sl_pct < self.cfg.min_sl_pct:
            self.logger.log(
                f"SL distance {sl_pct:.4%} < min_sl_pct {self.cfg.min_sl_pct:.4%}; skipping entry."
            )
            return

        if self.cfg.auto_leverage_by_stop:
            orders.maybe_apply_auto_leverage(close_now, stop_price)

        qty = orders.compute_qty(close_now, stop_price)
        self.logger.log(
            f"Short entry signal: close={close_now:.6f}  atr={atr_now:.6f}  "
            f"stop={stop_price:.6f}  target={target_price:.6f}  qty={qty}"
        )
        if qty <= 0:
            self.logger.log("Order size zero or below min notional; skipping short entry.")
            return

        self.signal_logger.log_entry_signal(
            trade_id,
            {
                "symbol": self.cfg.symbol,
                "signal_type": "short",
                "bar_open": float(df_1h["open"].iloc[-1]),
                "bar_high": float(df_1h["high"].iloc[-1]),
                "bar_low": float(df_1h["low"].iloc[-1]),
                "bar_close": close_now,
                "bar_volume": float(df_1h["volume"].iloc[-1]),
                "bar_atr": atr_now,
                "regime_active": signals.regime_active,
                "entry_signal": signals.entry_signal,
                "intended_entry_price": close_now,
                "intended_qty": float(qty),
                "order_type": self.cfg.order_type,
                "stop_price": stop_price,
                "target_price": target_price,
                "sl_pct": sl_pct,
                "auto_leverage_by_stop": self.cfg.auto_leverage_by_stop,
            },
        )

        entry_order_id = orders.place_entry(
            "Sell",
            qty,
            close_now,
            stop_loss=stop_price,
            take_profit=target_price,
            order_link_id=trade_id,
        )

        if not entry_order_id:
            return

        self.signal_logger.save_entry_order_id(trade_id, entry_order_id)

        if self.cfg.order_type == "Limit":
            state.set_pending_entry(
                order_id=entry_order_id,
                bar_ts=bar_ts,
                stop_price=stop_price,
                target_price=target_price,
            )

        position_manager.on_entry(stop_price, target_price)
        if self.cfg.dry_run:
            orders.update_stops(
                stop_loss=stop_price,
                take_profit=target_price,
                position_size=float(qty),
                position_side="Sell",
            )
        self.logger.log(
            f"Entry placed: stop={stop_price:.6f}  target={target_price:.6f}"
        )
