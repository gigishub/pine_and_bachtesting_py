"""Configuration for Setup 2 Trigger: KDE Upper (4h) + Level/RVOL on 15m.

Baseline: regime AND kde_upper (4h KDE, promoted from Setup 1).
Trigger signals (VWAP proximity, VPVR proximity, RVOL) are evaluated on
15-minute bars to find a tighter entry trigger within the structural gate.

Entry TF  : 15m
KDE TF    : 4h  (structural gate, shifted 1 bar, aligned to 15m)
Reference : 1d  (VPVR from trailing daily bars; daily VWAP resets at midnight)
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
    atr_period: int = 7        # 15m ATR for stop/target sizing

    # ------------------------------------------------------------------ #
    # KDE parameters (must match Setup 1 confirmed values)
    # ------------------------------------------------------------------ #
    kde_window: int = 200
    kde_bandwidth_mult: float = 1.0
    kde_n_points: int = 500
    kde_value_area_pct: float = 0.70
    kde_lower_duration: int = 2    # kept for _compute_kde_signals signature

    # ------------------------------------------------------------------ #
    # Daily VWAP
    # ------------------------------------------------------------------ #
    vwap_anchor: str = "weekly"     # resets at UTC midnight each day

    # ------------------------------------------------------------------ #
    # VPVR (1d reference)
    # ------------------------------------------------------------------ #
    vpvr_window: int = 50
    vpvr_n_bins: int = 50

    # ------------------------------------------------------------------ #
    # Level proximity threshold (15m ATR units)
    # ------------------------------------------------------------------ #
    setup_distance_atr: float = 1.0

    # ------------------------------------------------------------------ #
    # Relative volume (RVOL) on 15m bars
    # 96 bars = 24h rolling baseline at 15m resolution
    # rvol_above when current_volume / rolling_mean > rvol_threshold
    # ------------------------------------------------------------------ #
    rvol_window: int = 20
    rvol_threshold: float = 1.4

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
            "bear_strategy/hypothesis_tests/setup_2_trigger_check/test_results"
        )
    )
