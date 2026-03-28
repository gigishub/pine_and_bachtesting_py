from __future__ import annotations

from decimal import Decimal
from typing import Any

from ...bybit_client import BybitV5Client, InstrumentSpec, floor_to_step, fmt_decimal, to_decimal
from ..config import LiveConfig
from .error_policy import (
    bybit_ret_code,
    is_non_fatal_cancel_error,
    is_non_fatal_entry_error,
    is_non_fatal_stop_error,
    is_unchanged_stop_error,
)
from ..common.live_logger import LiveLogger
from .tpsl_policy import build_trading_stop_plan
from ..common.types import Position


class OrderManager:
    """Handles all order placement and exchange position queries."""

    def __init__(
        self,
        client: BybitV5Client,
        cfg: LiveConfig,
        instrument: InstrumentSpec,
        logger: LiveLogger,
    ) -> None:
        self.client = client
        self.cfg = cfg
        self.instrument = instrument
        self.logger = logger

    def _set_leverage_with_fallback(self, target_leverage: float, *, reason: str) -> bool:
        """Try to set leverage and optionally soft-fail on known exchange constraints."""
        try:
            self.client.set_leverage(
                category=self.cfg.category,
                symbol=self.cfg.symbol,
                leverage=target_leverage,
            )
            self.logger.log(f"Leverage set to {target_leverage}x for {self.cfg.symbol} ({reason})")
            return True
        except RuntimeError as exc:
            msg = str(exc).lower()
            code = bybit_ret_code(exc)
            if "not modified" in msg:
                self.logger.log(f"Leverage already {target_leverage}x on exchange; continuing.")
                return True

            # 110012: not enough available balance to apply requested leverage.
            if self.cfg.leverage_fail_soft and code == "110012":
                self.logger.log(
                    "Leverage update rejected by Bybit (110012: insufficient balance for new leverage). "
                    "Continuing with current exchange leverage."
                )
                return False

            if self.cfg.leverage_fail_soft:
                self.logger.log(f"Leverage update failed; continuing due to leverage_fail_soft=True. Details: {exc}")
                return False
            raise

    def maybe_apply_auto_leverage(self, entry: float, stop: float) -> None:
        """Optionally set leverage from stop distance, capped by configured bounds.

        Heuristic: leverage ~= 1 / (stop_distance_pct + buffer_pct).
        This is an approximation and does not model full liquidation mechanics.
        """
        if self.cfg.dry_run:
            return
        if self.cfg.category not in {"linear", "inverse"}:
            return
        if not self.cfg.auto_leverage_by_stop:
            return
        if entry <= 0:
            return

        stop_distance_pct = abs(entry - stop) / entry
        safety_buffer_pct = max(0.0, self.cfg.auto_leverage_sl_buffer_pct) / 100.0
        min_liq_gap_pct = stop_distance_pct + safety_buffer_pct
        if min_liq_gap_pct <= 0:
            return

        target = 1.0 / min_liq_gap_pct
        target = max(self.cfg.auto_leverage_min, min(self.cfg.auto_leverage_max, target))
        target = round(target, 2)
        self._set_leverage_with_fallback(target, reason="auto-by-stop")

    def get_current_position(self) -> Position | None:
        """Query the exchange and return the open position, or None if flat."""
        if self.cfg.dry_run:
            # Dry-run should not depend on private REST endpoints.
            return None

        rows = self.client.get_position(category=self.cfg.category, symbol=self.cfg.symbol)
        if not rows:
            return None
        for pos in rows:
            side = str(pos.get("side", ""))
            size = float(pos.get("size") or 0)
            if side in {"Buy", "Sell"} and size > 0:
                return Position(
                    side=side,  # type: ignore[arg-type]
                    size=size,
                    avg_price=float(pos.get("avgPrice") or 0),
                )
        return None

    def get_order_history(self, order_id: str) -> list[dict[str, Any]]:
        """Return order history entries for a specific orderId."""
        if self.cfg.dry_run:
            return []

        return self.client.get_order_history(
            category=self.cfg.category,
            symbol=self.cfg.symbol,
            orderId=order_id,
            limit=10,
        )

    def get_order_status(self, order_id: str) -> str:
        """Return a normalized order status string from bybit order history."""
        items = self.get_order_history(order_id)
        if not items:
            return "not_found"

        status = str(items[0].get("orderStatus", "unknown"))
        if status not in {"Filled", "Cancelled", "Rejected", "New", "PartiallyFilled"}:
            return "unknown"
        return status

    def compute_qty(self, entry: float, stop: float) -> Decimal:
        """Compute order quantity using fixed size or risk-based sizing."""
        if self.cfg.fixed_order_qty > 0:
            qty = to_decimal(self.cfg.fixed_order_qty)
        elif self.cfg.dry_run:
            # In dry-run mode avoid wallet-balance requests and use a deterministic
            # notional-based size so signal/order logs remain meaningful.
            if entry <= 0:
                return Decimal("0")
            qty = to_decimal(self.cfg.min_notional_usdt / entry)
        else:
            risk_distance = abs(entry - stop)
            if risk_distance <= 0:
                return Decimal("0")
            balance = self.client.get_wallet_balance()
            risk_usdt = balance * (self.cfg.risk_per_trade_pct / 100.0)
            units = risk_usdt / risk_distance
            qty = to_decimal(units)

        qty = floor_to_step(qty, self.instrument.qty_step)
        qty = min(qty, self.instrument.max_order_qty)
        if qty < self.instrument.min_order_qty:
            self.logger.log(
                f"Computed qty {qty} below instrument min_order_qty {self.instrument.min_order_qty}; dropping to 0"
            )
            return Decimal("0")
        if entry * float(qty) < self.cfg.min_notional_usdt:
            self.logger.log(
                f"Computed notional {entry * float(qty):.2f} < min_notional_usdt {self.cfg.min_notional_usdt}; dropping to 0"
            )
            return Decimal("0")
        return qty

    def place_entry(self, side: str, qty: Decimal, ref_price: float, order_link_id: str | None = None) -> str | None:
        """Place an entry order using configured order type.

        Returns order ID when accepted by exchange (or a dry-run placeholder),
        or None when rejected with a known non-fatal exchange error.
        """
        order_type = self.cfg.order_type
        payload: dict[str, Any] = {
            "category": self.cfg.category,
            "symbol": self.cfg.symbol,
            "side": side,
            "orderType": order_type,
            "qty": fmt_decimal(qty),
            "positionIdx": self.cfg.position_idx,
        }
        if order_link_id:
            payload["orderLinkId"] = order_link_id
        if order_type == "Limit":
            payload["price"] = str(ref_price)
            payload["timeInForce"] = "GTC"
        if self.cfg.category in {"linear", "inverse"}:
            payload["reduceOnly"] = False

        if self.cfg.dry_run:
            self.logger.log(f"DRY-RUN ORDER {payload}")
            return "dry-run-entry"

        try:
            resp = self.client.create_order(payload)
        except RuntimeError as exc:
            if is_non_fatal_entry_error(exc):
                code = bybit_ret_code(exc) or "unknown"
                self.logger.log(
                    f"Entry order rejected by exchange (non-fatal, retCode {code}); skipping bar. Details: {exc}"
                )
                return None
            raise

        result = resp.get("result", {})
        order_id = str(result.get("orderId") or "")
        self.logger.log(f"ORDER {order_type} {side} qty={qty} orderId={order_id}")
        return order_id or None

    def cancel_order_if_open(self, order_id: str) -> bool:
        """Cancel an order by ID when still open.

        Returns True when cancellation was accepted or when the order is already
        not open (filled/canceled), False for non-fatal cancellation failures.
        """
        if self.cfg.dry_run:
            self.logger.log(f"DRY-RUN CANCEL orderId={order_id}")
            return True

        if not order_id:
            return True

        try:
            self.client.cancel_order(
                {
                    "category": self.cfg.category,
                    "symbol": self.cfg.symbol,
                    "orderId": order_id,
                }
            )
            self.logger.log(f"Canceled stale entry order orderId={order_id}")
            return True
        except RuntimeError as exc:
            if is_non_fatal_cancel_error(exc):
                self.logger.log(f"Entry order already not open orderId={order_id}; continuing.")
                return True
            self.logger.log(f"Cancel order failed (non-fatal) orderId={order_id}: {exc}")
            return False

    def apply_leverage_if_configured(self) -> None:
        """Set symbol leverage for derivatives categories when configured."""
        if self.cfg.dry_run:
            return
        if self.cfg.category not in {"linear", "inverse"}:
            return

        target_leverage = 1.0 if self.cfg.force_no_leverage else self.cfg.leverage
        if target_leverage <= 0:
            return

        reason = "force-no-leverage" if self.cfg.force_no_leverage else "fixed"
        self._set_leverage_with_fallback(target_leverage, reason=reason)

    @staticmethod
    def _as_bool(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in {"1", "true", "yes", "y", "on"}
        return bool(value)

    @staticmethod
    def _close_side_for_position(position_side: str) -> str:
        return "Sell" if position_side == "Buy" else "Buy"

    def _is_tp_close_order(self, order: dict[str, Any], *, close_side: str) -> bool:
        """Return True for open reduce-only TP orders that can close this position side."""
        if str(order.get("side", "")) != close_side:
            return False
        if not self._as_bool(order.get("reduceOnly")):
            return False

        stop_order_type = str(order.get("stopOrderType", ""))
        create_type = str(order.get("createType", ""))
        return ("TakeProfit" in stop_order_type) or ("TakeProfit" in create_type)

    def cancel_open_take_profit_orders(self, *, position_side: str) -> int:
        """Cancel currently-open TP child orders so trailing stop remains the only exit path."""
        if self.cfg.dry_run:
            return 0

        close_side = self._close_side_for_position(position_side)
        open_orders = self.client.get_open_orders(
            category=self.cfg.category,
            symbol=self.cfg.symbol,
            open_only=0,
        )

        canceled = 0
        for order in open_orders:
            if not self._is_tp_close_order(order, close_side=close_side):
                continue

            order_id = str(order.get("orderId") or "")
            if not order_id:
                continue

            try:
                self.client.cancel_order(
                    {
                        "category": self.cfg.category,
                        "symbol": self.cfg.symbol,
                        "orderId": order_id,
                    }
                )
                canceled += 1
            except RuntimeError as exc:
                if is_non_fatal_cancel_error(exc):
                    self.logger.log(f"TP order already closed orderId={order_id}; continuing.")
                    continue
                self.logger.log(f"TP order cancel failed (non-fatal) orderId={order_id}: {exc}")

        if canceled > 0:
            self.logger.log(f"Canceled {canceled} open TP close order(s) before trailing stop sync.")
        return canceled

    def _attempt_single_side_update(
        self,
        payload: dict[str, Any],
        *,
        start_log: str,
        success_log: str,
        unchanged_log: str,
        nonfatal_log_prefix: str,
        retry_after_success: bool,
        retry_after_unchanged: bool,
    ) -> str:
        self.logger.log(start_log)
        try:
            self.client.set_trading_stop(payload)
            self.logger.log(success_log)
            return "retry" if retry_after_success else "success"
        except RuntimeError as exc:
            code = bybit_ret_code(exc)
            if code == "34040":
                self.logger.log(unchanged_log)
                return "retry" if retry_after_unchanged else "success"
            if code in {"10001", "110007"}:
                self.logger.log(f"{nonfatal_log_prefix} (non-fatal, retCode {code}); continuing.")
                return "next"
            raise

    def _attempt_emergency_updates(
        self,
        *,
        sl_only_payload: dict[str, Any] | None,
        tp_only_payload: dict[str, Any] | None,
        prefix: str,
    ) -> bool:
        if sl_only_payload is not None:
            status = self._attempt_single_side_update(
                sl_only_payload,
                start_log=f"{prefix}attempting emergency SL-only update.",
                success_log="Emergency SL-only update succeeded.",
                unchanged_log="SL unchanged on exchange (retCode 34040); continuing.",
                nonfatal_log_prefix="Emergency SL-only update rejected",
                retry_after_success=False,
                retry_after_unchanged=False,
            )
            if status == "success":
                return True
            if tp_only_payload is None:
                return False

        if tp_only_payload is None:
            return False

        sl_still_missing = sl_only_payload is not None
        status = self._attempt_single_side_update(
            tp_only_payload,
            start_log=f"{prefix}attempting emergency TP-only update.",
            success_log=(
                "WARNING: Emergency TP-only update succeeded but SL was not set; queuing retry to set SL."
                if sl_still_missing
                else "Emergency TP-only update succeeded."
            ),
            unchanged_log=(
                "TP already set (retCode 34040) but SL not set; queuing retry to set SL."
                if sl_still_missing
                else "TP unchanged on exchange (retCode 34040); continuing."
            ),
            nonfatal_log_prefix="Emergency TP-only update rejected",
            retry_after_success=sl_still_missing,
            retry_after_unchanged=sl_still_missing,
        )
        return status == "success"

    def update_stops(
        self,
        stop_loss: float | None,
        take_profit: float | None,
        *,
        position_size: float,
        position_side: str,
    ) -> bool:
        """Set stop-loss and/or take-profit on the exchange. No-op for spot."""
        if self.cfg.category not in {"linear", "inverse"}:
            return True

        plan = build_trading_stop_plan(
            self.cfg,
            self.instrument,
            stop_loss=stop_loss,
            take_profit=take_profit,
            position_size=position_size,
            position_side=position_side,
        )

        if self.cfg.dry_run:
            self.logger.log(f"DRY-RUN TP/SL {plan.payload}")
            return True

        if plan.clear_take_profit:
            # Ensure no stale TP order can close the position while trailing is active.
            self.cancel_open_take_profit_orders(position_side=position_side)

        try:
            self.client.set_trading_stop(plan.payload)
            return True
        except RuntimeError as exc:
            # Bybit returns retCode 34040 when submitted TP/SL is unchanged.
            # This is not an execution failure and should not stop the runner loop.
            code = bybit_ret_code(exc)
            if is_unchanged_stop_error(exc):
                self.logger.log("TP/SL unchanged on exchange (retCode 34040); continuing.")
                return True

            # TP/SL may become invalid momentarily as mark price moves.
            # For partial TP/SL, invalid parameter (10001) may happen due API checks.
            # Retry once in Full TP/SL mode to ensure we still have protective exits.
            if code == "10001" and plan.use_partial_tp_limit:
                self.logger.log(
                    "TP/SL update rejected with 10001 in partial mode; retrying with Full mode fallback."
                )
                try:
                    self.client.set_trading_stop(plan.full_payload)
                    self.logger.log("TP/SL update succeeded after Full mode fallback.")
                    return True
                except RuntimeError as exc2:
                    code2 = bybit_ret_code(exc2)
                    if code2 == "34040":
                        self.logger.log("TP/SL unchanged on exchange (retCode 34040); continuing.")
                        return True
                    if code2 == "10001":
                        return self._attempt_emergency_updates(
                            sl_only_payload=plan.sl_only_payload,
                            tp_only_payload=plan.tp_only_payload,
                            prefix="Fallback TP/SL still invalid; ",
                        )
                    if is_non_fatal_stop_error(exc2):
                        self.logger.log(
                            f"TP/SL update rejected on fallback (non-fatal, retCode {code2}); continuing."
                        )
                        return False
                    raise

            if code == "10001":
                return self._attempt_emergency_updates(
                    sl_only_payload=plan.sl_only_payload,
                    tp_only_payload=plan.tp_only_payload,
                    prefix="TP/SL update invalid; ",
                )

            if is_non_fatal_stop_error(exc):
                self.logger.log(f"TP/SL update rejected by exchange (non-fatal, retCode {code}); continuing.")
                return False
            raise
