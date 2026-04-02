from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .error_policy import is_non_fatal_cancel_error

if TYPE_CHECKING:
    from ...bybit_client import BybitV5Client
    from ..common.live_logger import LiveLogger
    from ..config import LiveConfig


class CancellationOps:
    """Order cancellation concerns (generic + TP child cleanup)."""

    # Provided by OrderManager facade. Declared here for static type checkers.
    if TYPE_CHECKING:
        client: BybitV5Client
        cfg: LiveConfig
        logger: LiveLogger

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

    def cancel_open_take_profit_orders(self, *, position_side: str) -> int:
        """Cancel open TP child orders so trailing stop remains the only exit path."""
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
