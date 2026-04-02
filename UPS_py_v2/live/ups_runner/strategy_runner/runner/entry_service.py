from __future__ import annotations

import pandas as pd
from uuid import uuid4

from .....strategy.decision.entry import should_open_long, should_open_short
from .....strategy.risk.sl_tp import compute_long_stop, compute_long_target, compute_short_stop, compute_short_target
from ...common.live_logger import LiveLogger
from ...common.types import Position, StrategySignals
from ...config import LiveConfig
from ..position_manager import PositionManager
from ..session_state import RunnerSessionState
from ...order_manager.order_manager import OrderManager
from ...stats_logger import SignalLogger
from .pending_execution_service import PendingExecutionService


class EntryService:
    """Build and place entries, then attach initial protection when appropriate."""

    def __init__(self, cfg: LiveConfig, logger: LiveLogger) -> None:
        self.cfg = cfg
        self.logger = logger
        self.signal_logger = SignalLogger(cfg)

    def attach_stops_for_pending_fill(
        self,
        *,
        position: Position,
        state: RunnerSessionState,
        position_manager: PositionManager,
        pending_execution: PendingExecutionService,
        orders: OrderManager,
    ) -> None:
        """When pending limit entry fills, clear pending state.

        Initial protection is attached on the parent entry order at create time.
        """
        if state.pending_entry_stop_price is not None and state.pending_entry_target_price is not None:
            position_manager.on_entry(state.pending_entry_stop_price, state.pending_entry_target_price)
        self.logger.log("Pending limit entry filled; protection was attached on entry order.")
        state.clear_pending_entry()

    def attach_stops_for_pending_fill_if_needed(
        self,
        *,
        position: Position | None,
        state: RunnerSessionState,
        position_manager: PositionManager,
        pending_execution: PendingExecutionService,
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
        df: pd.DataFrame,
        signals: StrategySignals,
        bar_ts: int,
        orders: OrderManager,
        position_manager: PositionManager,
        state: RunnerSessionState,
        pending_execution: PendingExecutionService,
    ) -> None:
        open_long = should_open_long(
            position_size=0.0,
            is_flat=True,
            price_above_ma=signals.price_above_ma,
            long_conditions_met=signals.long_conditions_met,
            bearish_pb=signals.bearish_pb,
            long_entry_pattern=signals.long_entry_pattern,
        )
        open_short = should_open_short(
            position_size=0.0,
            is_flat=True,
            price_above_ma=signals.price_above_ma,
            short_conditions_met=signals.short_conditions_met,
            bullish_pb=signals.bullish_pb,
            short_entry_pattern=signals.short_entry_pattern,
        )
        self.logger.log(
            f"Signal details: price_above_ma={signals.price_above_ma} "
            f"long_conditions={signals.long_conditions_met} bearish_pb={signals.bearish_pb} "
            f"long_entry={signals.long_entry_pattern} open_long={open_long} "
            f"short_conditions={signals.short_conditions_met} bullish_pb={signals.bullish_pb} "
            f"short_entry={signals.short_entry_pattern} open_short={open_short}"
        )

        if self.cfg.category == "spot" and open_short:
            self.logger.log("Skipping short signal: spot does not support shorts.")
            open_short = False

        if not open_long and not open_short:
            return

        trade_id = str(uuid4())
        close_now = float(df["Close"].iloc[-1])
        open_now = float(df["Open"].iloc[-1])
        low_now = float(df["Low"].iloc[-1])
        high_now = float(df["High"].iloc[-1])
        low_prev = float(df["Low"].iloc[-2]) if len(df) >= 2 else low_now
        high_prev = float(df["High"].iloc[-2]) if len(df) >= 2 else high_now

        if open_long:
            stop_price = compute_long_stop(
                sl_reference=self.cfg.sl_reference,
                low_now=low_now,
                low_prev=low_prev,
                open_now=open_now,
                close_now=close_now,
                atr_now=signals.atr_value,
                stop_multiplier=self.cfg.stop_multiplier,
            )
            target_price = compute_long_target(
                entry_price=close_now,
                stop_price=stop_price,
                risk_reward_multiplier=self.cfg.risk_reward_multiplier,
            )
            if self.cfg.auto_leverage_by_stop:
                orders.maybe_apply_auto_leverage(close_now, stop_price)
            qty = orders.compute_qty(close_now, stop_price)
            self.logger.log(f"Computed order qty={qty} for long entry (close={close_now}, stop={stop_price})")
            if qty <= 0:
                self.logger.log("Order size zero or below min notional; skipping long entry.")
                return
            self.signal_logger.log_entry_signal(trade_id, {
                "symbol": self.cfg.symbol,
                "signal_type": "long",
                "bar_open": open_now,
                "bar_high": high_now,
                "bar_low": low_now,
                "bar_close": close_now,
                "bar_volume": float(df["Volume"].iloc[-1]),
                "bar_atr": signals.atr_value,
                "price_above_ma": signals.price_above_ma,
                "long_conditions_met": signals.long_conditions_met,
                "bearish_pb": signals.bearish_pb,
                "long_entry_pattern": signals.long_entry_pattern,
                "intended_entry_price": close_now,
                "intended_qty": float(qty),
                "order_type": self.cfg.order_type,
                "stop_price": stop_price,
                "target_price": target_price,
                "risk_distance": abs(close_now - stop_price),
                "auto_leverage_by_stop": self.cfg.auto_leverage_by_stop,
            })
            entry_order_id = orders.place_entry(
                "Buy",
                qty,
                close_now,
                stop_loss=stop_price,
                take_profit=(None if self.cfg.trail_stop else target_price),
                order_link_id=trade_id,
            )
        else:
            stop_price = compute_short_stop(
                sl_reference=self.cfg.sl_reference,
                high_now=high_now,
                high_prev=high_prev,
                open_now=open_now,
                close_now=close_now,
                atr_now=signals.atr_value,
                stop_multiplier=self.cfg.stop_multiplier,
            )
            target_price = compute_short_target(
                entry_price=close_now,
                stop_price=stop_price,
                risk_reward_multiplier=self.cfg.risk_reward_multiplier,
            )
            if self.cfg.auto_leverage_by_stop:
                orders.maybe_apply_auto_leverage(close_now, stop_price)
            qty = orders.compute_qty(close_now, stop_price)
            self.logger.log(f"Computed order qty={qty} for short entry (close={close_now}, stop={stop_price})")
            if qty <= 0:
                self.logger.log("Order size zero or below min notional; skipping short entry.")
                return
            self.signal_logger.log_entry_signal(trade_id, {
                "symbol": self.cfg.symbol,
                "signal_type": "short",
                "bar_open": open_now,
                "bar_high": high_now,
                "bar_low": low_now,
                "bar_close": close_now,
                "bar_volume": float(df["Volume"].iloc[-1]),
                "bar_atr": signals.atr_value,
                "price_above_ma": signals.price_above_ma,
                "short_conditions_met": signals.short_conditions_met,
                "bullish_pb": signals.bullish_pb,
                "short_entry_pattern": signals.short_entry_pattern,
                "intended_entry_price": close_now,
                "intended_qty": float(qty),
                "order_type": self.cfg.order_type,
                "stop_price": stop_price,
                "target_price": target_price,
                "risk_distance": abs(close_now - stop_price),
                "auto_leverage_by_stop": self.cfg.auto_leverage_by_stop,
            })
            entry_order_id = orders.place_entry(
                "Sell",
                qty,
                close_now,
                stop_loss=stop_price,
                take_profit=(None if self.cfg.trail_stop else target_price),
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
                take_profit=(None if self.cfg.trail_stop else target_price),
                position_size=float(qty),
                position_side=("Buy" if open_long else "Sell"),
            )
        self.logger.log(
            f"Entry: stop={stop_price:.6f} target={target_price:.6f} trail={'on' if self.cfg.trail_stop else 'off'}"
        )
