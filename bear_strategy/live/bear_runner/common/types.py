from __future__ import annotations

from dataclasses import dataclass

# Re-export Position and PositionUpdate from UPS so bear runner code imports
# from one place.
from UPS_py_v2.live.ups_runner.common.types import Position, PositionUpdate  # noqa: F401


@dataclass
class BearSignals:
    """Computed strategy signals for one 1h bar."""

    is_ready: bool
    """False during ATR/RSI warmup — skip bar."""

    entry_signal: bool
    """True when regime + funding guard + VP trigger + throttle all pass."""

    atr_value: float
    """ATR(atr_period) at the last closed bar."""

    regime_active: bool
    """True when RSI bear zone + funding guard are both True."""
