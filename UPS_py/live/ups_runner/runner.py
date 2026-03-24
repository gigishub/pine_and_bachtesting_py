from __future__ import annotations

import argparse
import time
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

import pandas as pd

from ...SL_TP.sl import compute_long_stop, compute_short_stop
from ...SL_TP.tp import compute_long_target, compute_short_target
from ...SL_TP.trail_rules import (
    active_long_stop,
    active_short_stop,
    compute_long_trail_candidate,
    compute_short_trail_candidate,
    update_long_trail_stop,
    update_short_trail_stop,
)
from ...entry_exit.entry_rules import should_open_long, should_open_short
from ...strategy_logic import build_strategy_series
from ..bybit_client import (
    BybitPublicKlineStream,
    BybitV5Client,
    InstrumentSpec,
    floor_to_step,
    fmt_decimal,
    to_decimal,
)
from .config import LiveConfig, build_config_from_env, interval_to_ms, normalize_interval
from .market_data import LiveMarketDataService
from .trade_state import TradeState


class UPSLiveRunner:
    def __init__(self, cfg: LiveConfig) -> None:
        self.cfg = cfg
        self.client = BybitV5Client(
            cfg.api_key,
            cfg.api_secret,
            testnet=cfg.testnet,
        )
        self.interval = normalize_interval(cfg.timeframe)
        self.instrument: InstrumentSpec = self.client.get_instrument_spec(
            category=cfg.category,
            symbol=cfg.symbol,
        )
        self.last_processed_ts: int | None = None

        self.market_data = LiveMarketDataService(
            client=self.client,
            cfg=cfg,
            interval=self.interval,
            interval_ms=interval_to_ms(self.interval),
        )

        # Persisted order-management state for the currently open trade.
        self.state = TradeState()

    @property
    def interval_ms(self) -> int:
        return interval_to_ms(self.interval)

    def _log(self, msg: str) -> None:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now} UTC] {msg}", flush=True)

    def _compute_signals(self, ohlcv: pd.DataFrame) -> dict[str, pd.Series]:
        return build_strategy_series(
            df=ohlcv[["Open", "High", "Low", "Close", "Volume"]],
            ma_length=self.cfg.ma_length,
            max_candles_beyond_ma=self.cfg.max_candles_beyond_ma,
            ma_consolidation_lookback=self.cfg.ma_consolidation_lookback,
            ma_consolidation_count=self.cfg.ma_consolidation_count,
            ma_breach_lookback=self.cfg.ma_breach_lookback,
            use_iq_filter=self.cfg.use_iq_filter,
            iq_lookback=self.cfg.iq_lookback,
            iq_min_score=self.cfg.iq_min_score,
            iq_slope_atr_scale=self.cfg.iq_slope_atr_scale,
            iq_er_weight=self.cfg.iq_er_weight,
            iq_slope_weight=self.cfg.iq_slope_weight,
            iq_bias_weight=self.cfg.iq_bias_weight,
            use_sq_boost=self.cfg.use_sq_boost,
            sq_boost_weight=self.cfg.sq_boost_weight,
            sq_vol_lookback=self.cfg.sq_vol_lookback,
            long_trades=self.cfg.long_trades,
            short_trades=self.cfg.short_trades,
            enable_ec=self.cfg.enable_ec,
            enable_bullish_engulfing=self.cfg.enable_bullish_engulfing,
            enable_shooting_star=self.cfg.enable_shooting_star,
            ec_wick=self.cfg.ec_wick,
            enable_hammer=self.cfg.enable_hammer,
            atr_max_size=self.cfg.atr_max_size,
            rejection_wick_max_size=self.cfg.rejection_wick_max_size,
            hammer_fib=self.cfg.hammer_fib,
            hammer_size=self.cfg.hammer_size,
            stop_multiplier=self.cfg.stop_multiplier,
            risk_reward_multiplier=self.cfg.risk_reward_multiplier,
            minimum_rr=self.cfg.minimum_rr,
            pb_reference=self.cfg.pb_reference,
            sl_reference=self.cfg.sl_reference,
            trail_stop=self.cfg.trail_stop,
            trail_stop_size=self.cfg.trail_stop_size,
            trail_source=self.cfg.trail_source,
            lookback=self.cfg.lookback,
            atr_length=self.cfg.atr_length,
            point_allowance=self.cfg.point_allowance,
        )

    def _current_position(self) -> dict[str, Any] | None:
        rows = self.client.get_position(category=self.cfg.category, symbol=self.cfg.symbol)
        if not rows:
            return None
        for position in rows:
            side = str(position.get("side", ""))
            size = float(position.get("size") or 0)
            if side in {"Buy", "Sell"} and size > 0:
                return position
        return None

    def _compute_order_qty(self, entry: float, stop: float) -> Decimal:
        if self.cfg.fixed_order_qty > 0:
            qty = to_decimal(self.cfg.fixed_order_qty)
        else:
            risk_distance = abs(entry - stop)
            if risk_distance <= 0:
                return Decimal("0")
            units = self.cfg.risk_per_trade_usdt / risk_distance
            qty = to_decimal(units)

        qty = floor_to_step(qty, self.instrument.qty_step)
        qty = min(qty, self.instrument.max_order_qty)
        if qty < self.instrument.min_order_qty:
            return Decimal("0")

        if entry * float(qty) < self.cfg.min_notional_usdt:
            return Decimal("0")
        return qty

    def _place_market_order(self, side: str, qty: Decimal, *, reduce_only: bool) -> None:
        payload: dict[str, Any] = {
            "category": self.cfg.category,
            "symbol": self.cfg.symbol,
            "side": side,
            "orderType": "Market",
            "qty": fmt_decimal(qty),
            "positionIdx": self.cfg.position_idx,
        }
        if self.cfg.category in {"linear", "inverse"}:
            payload["reduceOnly"] = reduce_only
            if reduce_only and self.cfg.reduce_only_closes:
                payload["closeOnTrigger"] = True

        if self.cfg.dry_run:
            self._log(f"DRY-RUN ORDER {payload}")
            return

        resp = self.client.create_order(payload)
        result = resp.get("result", {})
        self._log(f"ORDER {side} qty={qty} orderId={result.get('orderId')}")

    def _set_trading_stop(self, *, stop_loss: float | None, take_profit: float | None) -> None:
        if self.cfg.category not in {"linear", "inverse"}:
            return

        payload: dict[str, Any] = {
            "category": self.cfg.category,
            "symbol": self.cfg.symbol,
            "positionIdx": self.cfg.position_idx,
            "tpslMode": "Full",
        }

        if stop_loss is not None:
            payload["stopLoss"] = str(stop_loss)
            payload["slTriggerBy"] = "MarkPrice"
        if take_profit is not None:
            payload["takeProfit"] = str(take_profit)
            payload["tpTriggerBy"] = "MarkPrice"

        if self.cfg.dry_run:
            self._log(f"DRY-RUN TP/SL {payload}")
            return

        self.client.set_trading_stop(payload)

    def _handle_entry(
        self,
        closed_df: pd.DataFrame,
        signals: dict[str, pd.Series],
        position: dict[str, Any] | None,
    ) -> None:
        if position is not None:
            return

        i = -1
        is_flat = True
        position_size = 0.0
        price_above_ma = bool(signals["price_above_ma"].iloc[i])

        open_long = should_open_long(
            position_size=position_size,
            is_flat=is_flat,
            price_above_ma=price_above_ma,
            long_conditions_met=bool(signals["long_conditions_met"].iloc[i]),
            bearish_pb=bool(signals["bearish_pb"].iloc[i]),
            long_entry_pattern=bool(signals["long_entry_pattern"].iloc[i]),
        )
        open_short = should_open_short(
            position_size=position_size,
            is_flat=is_flat,
            price_above_ma=price_above_ma,
            short_conditions_met=bool(signals["short_conditions_met"].iloc[i]),
            bullish_pb=bool(signals["bullish_pb"].iloc[i]),
            short_entry_pattern=bool(signals["short_entry_pattern"].iloc[i]),
        )

        if self.cfg.category == "spot" and open_short:
            self._log("Skipping short signal: spot category does not support short entries.")
            open_short = False

        if not open_long and not open_short:
            return

        close_now = float(closed_df["Close"].iloc[i])
        open_now = float(closed_df["Open"].iloc[i])
        low_now = float(closed_df["Low"].iloc[i])
        high_now = float(closed_df["High"].iloc[i])
        low_prev = float(closed_df["Low"].iloc[i - 1]) if len(closed_df) >= 2 else low_now
        high_prev = float(closed_df["High"].iloc[i - 1]) if len(closed_df) >= 2 else high_now
        atr_now = float(signals["atr_value"].iloc[i])

        if open_long:
            stop_price = compute_long_stop(
                sl_reference=self.cfg.sl_reference,
                low_now=low_now,
                low_prev=low_prev,
                open_now=open_now,
                close_now=close_now,
                atr_now=atr_now,
                stop_multiplier=self.cfg.stop_multiplier,
            )
            target_price = compute_long_target(
                entry_price=close_now,
                stop_price=stop_price,
                risk_reward_multiplier=self.cfg.risk_reward_multiplier,
            )
            qty = self._compute_order_qty(close_now, stop_price)
            if qty <= 0:
                self._log("Order size computed as zero; skipping long entry.")
                return
            self._place_market_order("Buy", qty, reduce_only=False)
        else:
            stop_price = compute_short_stop(
                sl_reference=self.cfg.sl_reference,
                high_now=high_now,
                high_prev=high_prev,
                open_now=open_now,
                close_now=close_now,
                atr_now=atr_now,
                stop_multiplier=self.cfg.stop_multiplier,
            )
            target_price = compute_short_target(
                entry_price=close_now,
                stop_price=stop_price,
                risk_reward_multiplier=self.cfg.risk_reward_multiplier,
            )
            qty = self._compute_order_qty(close_now, stop_price)
            if qty <= 0:
                self._log("Order size computed as zero; skipping short entry.")
                return
            self._place_market_order("Sell", qty, reduce_only=False)

        # Initialize local stop/target state right after entry order placement.
        self.state.trade_stop_price = stop_price
        self.state.trade_target_price = target_price
        self.state.trail_stop_price = None
        self.state.active_stop_price = stop_price
        self.state.look_for_exit = False
        self.state.last_stop_sent = None

        if not self.cfg.trail_stop:
            self._set_trading_stop(stop_loss=self.state.trade_stop_price, take_profit=self.state.trade_target_price)
        else:
            self._set_trading_stop(stop_loss=self.state.trade_stop_price, take_profit=None)

        self._log(
            f"Entry state: stop={self.state.trade_stop_price:.6f} target={self.state.trade_target_price:.6f} "
            f"trail={'on' if self.cfg.trail_stop else 'off'}"
        )

    def _handle_position_management(self, closed_df: pd.DataFrame, position: dict[str, Any] | None) -> None:
        if position is None:
            self.state.reset()
            return

        side = str(position.get("side", ""))
        if self.state.trade_stop_price is None:
            # Recovery path: if runner restarted while a position was already open.
            avg_price = float(position.get("avgPrice") or closed_df["Close"].iloc[-1])
            self.state.trade_stop_price = avg_price
            self.state.trade_target_price = avg_price
            self.state.active_stop_price = avg_price

        if side == "Buy":
            if (
                self.cfg.trail_stop
                and not self.state.look_for_exit
                and self.state.trade_target_price is not None
                and float(closed_df["High"].iloc[-1]) >= self.state.trade_target_price
            ):
                self.state.look_for_exit = True

            self.state.active_stop_price = active_long_stop(self.state.trade_stop_price, self.state.trail_stop_price)
        elif side == "Sell":
            if (
                self.cfg.trail_stop
                and not self.state.look_for_exit
                and self.state.trade_target_price is not None
                and float(closed_df["Low"].iloc[-1]) <= self.state.trade_target_price
            ):
                self.state.look_for_exit = True

            self.state.active_stop_price = active_short_stop(self.state.trade_stop_price, self.state.trail_stop_price)

    def _apply_trailing_from_signals(self, closed_df: pd.DataFrame, signals: dict[str, pd.Series], position: dict[str, Any]) -> None:
        if not self.cfg.trail_stop:
            return
        if self.state.trade_stop_price is None:
            return

        atr_now = float(signals["atr_value"].iloc[-1])
        side = str(position.get("side", ""))

        if side == "Buy" and self.state.look_for_exit:
            close_prev = float(closed_df["Close"].iloc[-2]) if len(closed_df) >= 2 else float(closed_df["Close"].iloc[-1])
            open_prev = float(closed_df["Open"].iloc[-2]) if len(closed_df) >= 2 else float(closed_df["Open"].iloc[-1])
            lookback_low = float(closed_df["Low"].tail(max(1, self.cfg.lookback)).min())
            candidate = compute_long_trail_candidate(
                trail_source=self.cfg.trail_source,
                close_prev=close_prev,
                open_prev=open_prev,
                lookback_low=lookback_low,
                atr_now=atr_now,
                trail_stop_size=self.cfg.trail_stop_size,
            )
            self.state.trail_stop_price = update_long_trail_stop(
                position_size=float(position.get("size") or 0),
                look_for_exit=self.state.look_for_exit,
                current_trail_stop=self.state.trail_stop_price,
                candidate_trail_stop=candidate,
            )
            self.state.active_stop_price = active_long_stop(self.state.trade_stop_price, self.state.trail_stop_price)

        if side == "Sell" and self.state.look_for_exit:
            close_prev = float(closed_df["Close"].iloc[-2]) if len(closed_df) >= 2 else float(closed_df["Close"].iloc[-1])
            open_prev = float(closed_df["Open"].iloc[-2]) if len(closed_df) >= 2 else float(closed_df["Open"].iloc[-1])
            lookback_high = float(closed_df["High"].tail(max(1, self.cfg.lookback)).max())
            candidate = compute_short_trail_candidate(
                trail_source=self.cfg.trail_source,
                close_prev=close_prev,
                open_prev=open_prev,
                lookback_high=lookback_high,
                atr_now=atr_now,
                trail_stop_size=self.cfg.trail_stop_size,
            )
            self.state.trail_stop_price = update_short_trail_stop(
                position_size=-float(position.get("size") or 0),
                look_for_exit=self.state.look_for_exit,
                current_trail_stop=self.state.trail_stop_price,
                candidate_trail_stop=candidate,
            )
            self.state.active_stop_price = active_short_stop(self.state.trade_stop_price, self.state.trail_stop_price)

    def _process_closed_bar(self, closed_df: pd.DataFrame, last_ts: int) -> None:
        signals = self._compute_signals(closed_df[["Open", "High", "Low", "Close", "Volume"]])
        if not bool(signals["is_ready"].iloc[-1]):
            self._log("Warmup not ready yet; skipping bar.")
            self.last_processed_ts = last_ts
            return

        position = self._current_position()
        self._handle_entry(closed_df, signals, position)

        # Re-sync position after potential entry order.
        time.sleep(0.2)
        position = self._current_position()

        self._handle_position_management(closed_df, position)
        if position is not None:
            self._apply_trailing_from_signals(closed_df, signals, position)
            if self.state.active_stop_price is not None:
                stop_changed = (
                    self.state.last_stop_sent is None
                    or abs(self.state.active_stop_price - self.state.last_stop_sent) >= float(self.instrument.tick_size)
                )
                if stop_changed:
                    take_profit = None if self.cfg.trail_stop else self.state.trade_target_price
                    self._set_trading_stop(stop_loss=self.state.active_stop_price, take_profit=take_profit)
                    self.state.last_stop_sent = self.state.active_stop_price

        self.last_processed_ts = last_ts
        self._log(
            f"Processed candle {datetime.fromtimestamp(last_ts / 1000, tz=timezone.utc)} "
            f"pos={'none' if position is None else position.get('side') + ':' + str(position.get('size'))}"
        )

    def _run_polling_loop(self) -> None:
        while True:
            try:
                self.market_data.sleep_until_next_close()
                raw_df = self.market_data.fetch_ohlcv()
                closed_df = self.market_data.closed_df(raw_df)

                last_ts = int(closed_df["Timestamp"].iloc[-1])
                if self.last_processed_ts is not None and last_ts <= self.last_processed_ts:
                    continue

                self._process_closed_bar(closed_df, last_ts)
            except KeyboardInterrupt:
                self._log("Stopped by user.")
                raise
            except Exception as exc:
                self._log(f"Loop error: {exc}")
                time.sleep(2.0)

    def _run_ws_loop(self) -> None:
        closed_history = self.market_data.bootstrap_closed_history()
        self.last_processed_ts = int(closed_history["Timestamp"].iloc[-1])
        self._log(
            f"WebSocket mode active. Warmup candles={len(closed_history)} last={datetime.fromtimestamp(self.last_processed_ts / 1000, tz=timezone.utc)}"
        )

        stream = BybitPublicKlineStream(
            ws_url=self.client.public_ws_url(self.cfg.category),
            symbol=self.cfg.symbol,
            interval=self.interval,
        )
        stream.start()

        try:
            while True:
                row = stream.get_next_closed_kline(timeout_s=self.cfg.ws_queue_timeout_s)
                if row is None:
                    self._log("WS timeout waiting for closed candle; keeping connection alive.")
                    continue

                start_ts = int(row.get("start") or 0)
                if start_ts <= 0:
                    continue

                if self.last_processed_ts is not None and start_ts <= self.last_processed_ts:
                    continue

                # If websocket dropped candles, rebuild history and process missed bars in order.
                if self.last_processed_ts is not None and start_ts > (self.last_processed_ts + self.interval_ms):
                    self._log("Detected kline gap; restoring history from REST.")
                    closed_history = self.market_data.bootstrap_closed_history()
                    missed = closed_history[closed_history["Timestamp"] > self.last_processed_ts]
                    for idx in missed.index:
                        ts = int(closed_history.loc[idx, "Timestamp"])
                        slice_df = closed_history.loc[:idx]
                        self._process_closed_bar(slice_df, ts)
                    continue

                closed_history = self.market_data.append_closed_ws_kline(closed_history, row)
                last_idx = closed_history.index[-1]
                last_ts = int(closed_history.loc[last_idx, "Timestamp"])
                if last_ts <= (self.last_processed_ts or 0):
                    continue
                self._process_closed_bar(closed_history, last_ts)
        except KeyboardInterrupt:
            self._log("Stopped by user.")
            raise
        finally:
            stream.stop()

    def run_forever(self) -> None:
        self._log(
            f"Starting live UPS runner symbol={self.cfg.symbol} category={self.cfg.category} "
            f"tf={self.cfg.timeframe} dry_run={self.cfg.dry_run} mode={'ws' if self.cfg.use_ws_kline else 'polling'}"
        )
        if self.cfg.use_ws_kline:
            self._run_ws_loop()
            return
        self._run_polling_loop()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run UPS strategy live on Bybit V5")
    parser.add_argument("--dry-run", action="store_true", help="Compute signals but do not place orders")
    args = parser.parse_args()

    cfg = build_config_from_env()
    if args.dry_run:
        cfg.dry_run = True

    runner = UPSLiveRunner(cfg)
    runner.run_forever()


if __name__ == "__main__":
    main()
