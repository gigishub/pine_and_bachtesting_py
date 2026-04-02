from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any

from ...bybit_client import floor_to_step, fmt_decimal, to_decimal
from .error_policy import bybit_ret_code, is_non_fatal_entry_error

if TYPE_CHECKING:
    from ...bybit_client import BybitV5Client, InstrumentSpec
    from ..common.live_logger import LiveLogger
    from ..config import LiveConfig


class ExecutionOps:
    """Entry sizing and order placement behavior."""

    # Provided by OrderManager facade. Declared here for static type checkers.
    if TYPE_CHECKING:
        client: BybitV5Client
        cfg: LiveConfig
        instrument: InstrumentSpec
        logger: LiveLogger

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

    def place_entry(
        self,
        side: str,
        qty: Decimal,
        ref_price: float,
        *,
        stop_loss: float | None = None,
        take_profit: float | None = None,
        order_link_id: str | None = None,
    ) -> str | None:
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
            # Attach protection on the parent entry order to minimize the
            # unprotected timing window between fill and a later TP/SL call.
            if stop_loss is not None:
                payload["stopLoss"] = str(stop_loss)
                payload["slOrderType"] = "Market"
            if take_profit is not None:
                payload["takeProfit"] = str(take_profit)
                payload["tpOrderType"] = "Market"
            if stop_loss is not None or take_profit is not None:
                payload["tpslMode"] = "Full"

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

