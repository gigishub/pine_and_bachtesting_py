from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..common.types import Position

if TYPE_CHECKING:
    from ...bybit_client import BybitV5Client
    from ..config import LiveConfig


class PositionOps:
    """Exchange position and order-history queries."""

    # Provided by OrderManager facade. Declared here for static type checkers.
    if TYPE_CHECKING:
        client: BybitV5Client
        cfg: LiveConfig

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
