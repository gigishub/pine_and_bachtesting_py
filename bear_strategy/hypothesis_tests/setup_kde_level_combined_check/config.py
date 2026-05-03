"""Configuration for the KDE + Level Proximity Combined Check.

Tests whether the KDE gate (kde_upper OR kde_lower_fresh) combined with
price proximity to daily VWAP or VPVR HVN creates stronger short edge than
either signal class alone.

Entry TF : 1h
Reference : 1d  (daily VWAP resets at midnight; VPVR from trailing daily bars)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestConfig:
    # ------------------------------------------------------------------ #
    # Timeframes
    # entry_tf  — candle resolution for entries, stops, and targets
    # kde_tf    — higher TF for KDE structural signal (shifted 1 bar before 1h alignment)
    # context_tf — reference TF for VPVR volume profile
    # ------------------------------------------------------------------ #
    entry_tf: str = "1h"
    kde_tf: str = "4h"
    context_tf: str = "1d"

    # ------------------------------------------------------------------ #
    # Exit parameters
    # ------------------------------------------------------------------ #
    stop_atr_mult: float = 2.0
    target_atr_mult: float = 3.0
    atr_period: int = 7        # 1h ATR for stop/target sizing

    # ------------------------------------------------------------------ #
    # KDE parameters (mirrors setup_kde_edge_check)
    # ------------------------------------------------------------------ #
    kde_window: int = 200          # trailing 1h bars for KDE
    kde_bandwidth_mult: float = 1.0
    kde_n_points: int = 500
    kde_value_area_pct: float = 0.70
    kde_lower_duration: int = 2    # max bars for lower_fresh to stay active

    # ------------------------------------------------------------------ #
    # Daily VWAP
    # ------------------------------------------------------------------ #
    vwap_anchor: str = "daily"     # resets at UTC midnight each day

    # ------------------------------------------------------------------ #
    # VPVR (1d reference)
    # ------------------------------------------------------------------ #
    vpvr_window: int = 50          # trailing 1d bars for volume profile
    vpvr_n_bins: int = 50

    # ------------------------------------------------------------------ #
    # Level proximity threshold
    # near = price within setup_distance_atr × ATR_1h of the level
    # ------------------------------------------------------------------ #
    setup_distance_atr: float = 1.0

    # ------------------------------------------------------------------ #
    # Regime — fixed to Step 1 winner (ema_below_50)
    # ------------------------------------------------------------------ #
    regime_col: str = "ema_below_50_regime"
    ema_slope_period: int = 200
    ema_slope_lookback: int = 1
    ema_below_periods: list[int] = field(default_factory=lambda: [50])

    # ------------------------------------------------------------------ #
    # Verdict thresholds
    # ------------------------------------------------------------------ #
    pf_base: float = 1.0
    min_pf_lift_high_n: float = 0.02
    min_pf_lift_mid_n: float = 0.05
    min_pf_lift_low_n: float = 0.10
    min_win_rate: float = 0.40
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
            "bear_strategy/hypothesis_tests/setup_kde_level_combined_check/test_results"
        )
    )
