from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...bybit_client import BybitV5Client
    from ..common.live_logger import LiveLogger
    from ..config import LiveConfig


class TrailStopOps:
    """Trailing-stop specific exchange behavior.

    This module intentionally contains only trailing-related concerns, so
    generic TP/SL update logic stays separate in StopOps.
    """

    # Provided by OrderManager facade. Declared here for static type checkers.
    if TYPE_CHECKING:
        client: BybitV5Client
        cfg: LiveConfig
        logger: LiveLogger
        def cancel_open_take_profit_orders(self, *, position_side: str) -> int: ...

    def prepare_trailing_mode(self, *, position_side: str, clear_take_profit: bool) -> None:
        """Run trailing-specific pre-update steps before a stop update call."""
        if not clear_take_profit:
            return
        # Ensure no stale TP order can close the position while trailing is active.
        self.cancel_open_take_profit_orders(position_side=position_side)
