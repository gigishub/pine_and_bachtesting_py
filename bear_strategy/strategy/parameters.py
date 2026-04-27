"""Strategy parameters for the Bear Strategy.

All tunable values live here. No logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Parameters:
    # ------------------------------------------------------------------ #
    # Regime — Layer 1
    # ------------------------------------------------------------------ #

    # EMA 200 slope: bearish when EMA 200 is declining.
    ema_slope_period: int = 200
    # How many daily bars back to compare when measuring the slope.
    ema_slope_lookback: int = 1

    # Close-below-EMA periods: bearish when daily close < EMA(period).
    ema_below_periods: list[int] = field(default_factory=lambda: [50, 100, 150])

    # ------------------------------------------------------------------ #
    # ATR (shared — used by exit and hypothesis test stops)
    # ------------------------------------------------------------------ #
    atr_period: int = 14
