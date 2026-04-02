from __future__ import annotations

from ...bybit_client import BybitV5Client, InstrumentSpec
from ..common.live_logger import LiveLogger
from ..config import LiveConfig
from .cancellation_ops import CancellationOps
from .execution_ops import ExecutionOps
from .leverage_ops import LeverageOps
from .position_ops import PositionOps
from .stop_ops import StopOps
from .trail_stop_ops import TrailStopOps


class OrderManager(LeverageOps, PositionOps, ExecutionOps, CancellationOps, TrailStopOps, StopOps):
    """Thin facade that groups exchange concerns into focused mixins.

    Public API remains unchanged for runner callers, while implementation is
    separated by concern in dedicated modules.
    """

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
