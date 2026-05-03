"""Configuration for Setup 2 – Trigger 6: MACD signals.

Baseline: regime AND kde_upper (4h KDE open > peak), promoted from Setup 1.

Tests six MACD-based conditions on top of baseline. All focus on momentum
divergence, rate-of-change, and trend exhaustion signals.

Entry TF  : configurable (default 1h — change to test 15m / 4h etc.)
KDE TF    : 4h  (structural gate)

Signals tested:

    zero_line_rejection
        MACD approaches 0 from below, touches/nears, then turns lower without crossing.
        Logic: Failed relief rally at neutral point; bears still control macro trend.

    histogram_peak_roll
        Histogram[1] > Histogram while Histogram is still positive.
        Logic: Early warning — bullish impulse exhausting before price drops.

    rapid_separation
        (MACD_Line - Signal_Line) increasing in value (widening gap below zero).
        Logic: Downward momentum accelerating; equivalent to BB expansion.

    signal_line_wall
        Signal_Line < 0 AND MACD_Line < Signal_Line (positional filter).
        Logic: Confirms average momentum of recent bars is bearish regime.

    histogram_twin_peaks
        Price makes Higher High but MACD Histogram makes Lower High.
        Logic: Bearish divergence — latest push done on weaker momentum.

    cross_velocity
        MACD_Line crosses below Signal_Line with steep slope (high rate of change).
        Logic: Not all crosses equal — steep cross = violent sentiment shift.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestConfig:
    # ------------------------------------------------------------------ #
    # Timeframes
    # ------------------------------------------------------------------ #
    entry_tf: str = "4h"
    kde_tf: str = "4h"
    context_tf: str = "1d"

    # ------------------------------------------------------------------ #
    # Exit parameters
    # ------------------------------------------------------------------ #
    stop_atr_mult: float = 2.0
    target_atr_mult: float = 3.0
    atr_period: int = 7

    # ------------------------------------------------------------------ #
    # KDE parameters (must match Setup 1 confirmed values)
    # ------------------------------------------------------------------ #
    kde_window: int = 200
    kde_bandwidth_mult: float = 1.0
    kde_n_points: int = 500
    kde_value_area_pct: float = 0.70
    kde_lower_duration: int = 2

    # ------------------------------------------------------------------ #
    # MACD parameters
    # macd_fast         : fast EMA period (default 12)
    # macd_slow         : slow EMA period (default 26)
    # macd_signal       : signal line EMA period (default 9)
    # histogram_lookback: lookback for peak_roll and twin_peaks (default 20)
    # cross_velocity_slope_threshold: min slope for steep cross (default 0.05)
    # zero_line_margin  : how close to 0 for rejection (default 0.01, 1% of normalized scale)
    # ------------------------------------------------------------------ #
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    histogram_lookback: int = 20
    cross_velocity_slope_threshold: float = 0.05
    zero_line_margin: float = 0.01

    # ------------------------------------------------------------------ #
    # Regime
    # ------------------------------------------------------------------ #
    regime_col: str = "ema_below_50_regime"
    ema_slope_period: int = 200
    ema_slope_lookback: int = 1
    ema_below_periods: list[int] = field(default_factory=lambda: [50])

    # ------------------------------------------------------------------ #
    # Verdict thresholds
    # ------------------------------------------------------------------ #
    min_pairs_passing: int = 3

    # ------------------------------------------------------------------ #
    # Data
    # ------------------------------------------------------------------ #
    data_dir: Path = field(default_factory=lambda: Path("crypto_data/data"))
    pairs: list[str] = field(
        default_factory=lambda: ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
    )
    start_date: str = "2021-01-01"
    end_date: str = "2025-11-01"

    # ------------------------------------------------------------------ #
    # Output
    # ------------------------------------------------------------------ #
    results_dir: Path = field(
        default_factory=lambda: Path(
            "bear_strategy/hypothesis_tests/setup_2_trigger_6_check/test_results"
        )
    )
