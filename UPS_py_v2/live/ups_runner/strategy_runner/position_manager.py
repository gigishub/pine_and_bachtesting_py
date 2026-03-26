from __future__ import annotations

from decimal import Decimal

import pandas as pd

from ....strategy.risk.trailing import (
    active_long_stop,
    active_short_stop,
    compute_long_trail_candidate,
    compute_short_trail_candidate,
    update_long_trail_stop,
    update_short_trail_stop,
)
from ..config import LiveConfig
from ..common.live_logger import LiveLogger
from ..trade_state import TradeState
from ..common.types import Position, PositionUpdate, StrategySignals


class PositionManager:
    """Manages open trade state including trailing stop advancement."""

    def __init__(self, cfg: LiveConfig, tick_size: Decimal, logger: LiveLogger) -> None:
        self.cfg = cfg
        self.tick_size = tick_size
        self.logger = logger
        self.state = TradeState()

    def on_entry(self, stop_price: float, target_price: float) -> None:
        """Initialise state immediately after an entry order is placed."""
        self.state.trade_stop_price = stop_price
        self.state.trade_target_price = target_price
        self.state.trail_stop_price = None
        self.state.active_stop_price = stop_price
        self.state.look_for_exit = False
        self.state.last_stop_sent = None

    def on_flat(self) -> None:
        """Clear state when no open position exists."""
        self.state.reset()

    def update_for_closed_bar(
        self,
        df: pd.DataFrame,
        signals: StrategySignals,
        position: Position,
    ) -> PositionUpdate:
        """Process one closed bar: advance trailing logic, return stop-update instructions."""
        side = position.side

        # Recovery path: runner restarted while a position was already open.
        if self.state.trade_stop_price is None:
            avg = position.avg_price or float(df["Close"].iloc[-1])
            self.state.trade_stop_price = avg
            self.state.trade_target_price = avg
            self.state.active_stop_price = avg

        # Activate trailing exit mode once the target price is breached.
        if self.cfg.trail_stop and not self.state.look_for_exit and self.state.trade_target_price is not None:
            if side == "Buy" and float(df["High"].iloc[-1]) >= self.state.trade_target_price:
                self.state.look_for_exit = True
            elif side == "Sell" and float(df["Low"].iloc[-1]) <= self.state.trade_target_price:
                self.state.look_for_exit = True

        # Compute active stop as the best (highest/lowest) of trade stop and trail stop.
        if side == "Buy":
            self.state.active_stop_price = active_long_stop(self.state.trade_stop_price, self.state.trail_stop_price)
        else:
            self.state.active_stop_price = active_short_stop(self.state.trade_stop_price, self.state.trail_stop_price)

        # Advance the trailing stop once look_for_exit is active.
        if self.cfg.trail_stop and self.state.look_for_exit:
            self._advance_trail(df, signals, position)

        return self._build_update()

    def _advance_trail(self, df: pd.DataFrame, signals: StrategySignals, position: Position) -> None:
        atr = signals.atr_value
        side = position.side
        prev_idx = -2 if len(df) >= 2 else -1

        if side == "Buy":
            candidate = compute_long_trail_candidate(
                trail_source=self.cfg.trail_source,
                close_prev=float(df["Close"].iloc[prev_idx]),
                open_prev=float(df["Open"].iloc[prev_idx]),
                lookback_low=float(df["Low"].tail(max(1, self.cfg.lookback)).min()),
                atr_now=atr,
                trail_stop_size=self.cfg.trail_stop_size,
            )
            self.state.trail_stop_price = update_long_trail_stop(
                position_size=position.size,
                look_for_exit=self.state.look_for_exit,
                current_trail_stop=self.state.trail_stop_price,
                candidate_trail_stop=candidate,
            )
            self.state.active_stop_price = active_long_stop(self.state.trade_stop_price, self.state.trail_stop_price)

        elif side == "Sell":
            candidate = compute_short_trail_candidate(
                trail_source=self.cfg.trail_source,
                close_prev=float(df["Close"].iloc[prev_idx]),
                open_prev=float(df["Open"].iloc[prev_idx]),
                lookback_high=float(df["High"].tail(max(1, self.cfg.lookback)).max()),
                atr_now=atr,
                trail_stop_size=self.cfg.trail_stop_size,
            )
            self.state.trail_stop_price = update_short_trail_stop(
                position_size=-position.size,
                look_for_exit=self.state.look_for_exit,
                current_trail_stop=self.state.trail_stop_price,
                candidate_trail_stop=candidate,
            )
            self.state.active_stop_price = active_short_stop(self.state.trade_stop_price, self.state.trail_stop_price)

    def _build_update(self) -> PositionUpdate:
        if self.state.active_stop_price is None:
            return PositionUpdate(should_update_stops=False)

        stop_changed = (
            self.state.last_stop_sent is None
            or abs(self.state.active_stop_price - self.state.last_stop_sent) >= float(self.tick_size)
        )
        if not stop_changed:
            return PositionUpdate(should_update_stops=False)

        self.state.last_stop_sent = self.state.active_stop_price
        take_profit = None if self.cfg.trail_stop else self.state.trade_target_price
        return PositionUpdate(
            should_update_stops=True,
            new_stop_price=self.state.active_stop_price,
            new_take_profit=take_profit,
        )
