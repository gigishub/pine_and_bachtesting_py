from __future__ import annotations

import logging

from ..common.types import Position

logger = logging.getLogger(__name__)


class BearPositionManager:
    """Track open short position state for the bear live runner.

    The bear strategy uses fixed SL/TP attached to the entry order on Bybit.
    No trailing stop logic is needed — Bybit manages SL/TP natively after entry.
    This manager simply tracks whether we are in a position and records entry
    levels for logging and recovery purposes.
    """

    def __init__(self) -> None:
        self._in_position: bool = False
        self._stop_price: float | None = None
        self._target_price: float | None = None

    @property
    def in_position(self) -> bool:
        return self._in_position

    def on_entry(self, stop_price: float, target_price: float) -> None:
        """Record state immediately after a short entry order is placed."""
        self._in_position = True
        self._stop_price = stop_price
        self._target_price = target_price
        logger.info(
            "Position entered: stop=%.6f  target=%.6f",
            stop_price,
            target_price,
        )

    def on_flat(self) -> None:
        """Clear state when no open position exists."""
        if self._in_position:
            logger.info("Position closed (flat).")
        self._in_position = False
        self._stop_price = None
        self._target_price = None

    def update_for_closed_bar(self, position: Position | None) -> None:
        """Sync internal state with the live position from the exchange.

        Bear strategy SL/TP are native Bybit orders, so no stop advancement
        is needed.  This method only updates the flat/in-position flag.
        """
        if position is None:
            self.on_flat()
