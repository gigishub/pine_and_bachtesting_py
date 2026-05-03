"""Configuration for the KDE Price Cluster Edge Check.

Regime filter: ema_below_50 (Step 1 winner).

Hypothesis: within a bear regime, the KDE-derived Point of Control (POC)
acts as a significant price magnet.  Two structural setups are tested:

  kde_upper       — open > kde_peak:
      Price gaps above the most-traded level (resistance reclaim attempt).
      In a bear regime this is a mean-reversion short setup.

  kde_lower       — close < kde_peak (any duration):
      Price closes below the POC, signalling a momentum breakdown below
      the dominant volume cluster.

  kde_lower_fresh — close < kde_peak AND counter ≤ lower_duration:
      Only the first `lower_duration` bars after a fresh breach, capturing
      the early momentum window before the move exhausts.

KDE parameters:
  window         — rolling lookback (bars) for the price sample.
  bandwidth_mult — multiplier on Scott's rule bandwidth.
                   < 1.0 → tighter, more sensitive peaks.
                   > 1.0 → smoother, broader clusters.
  kde_n_points   — evaluation grid resolution (higher = more precise POC).
  value_area_pct — fraction of density to capture in the Value Area band.
  lower_duration — bars the lower filter stays active after a breach.

Edit fields directly in this file to change timeframe or parameters.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestConfig:
    # ------------------------------------------------------------------ #
    # Timeframe
    # ------------------------------------------------------------------ #
    entry_tf: str = "1h"
    kde_tf: str = "4h"

    # ------------------------------------------------------------------ #
    # KDE parameters
    # ------------------------------------------------------------------ #
    # Rolling lookback window (bars) for the price distribution sample.
    window: int = 200

    # Bandwidth multiplier applied on top of Scott's rule.
    # Scott's rule: h = n^(-1/5) × std(data) × bandwidth_mult
    bandwidth_mult: float = 0.8

    # Number of evenly-spaced price points to evaluate the KDE curve on.
    kde_n_points: int = 500

    # Fraction of total KDE density captured in the Value Area band.
    value_area_pct: float = 0.70

    # Maximum bars the lower filter stays active after a breach of the POC.
    # Counter resets to 0 whenever close returns above kde_peak.
    lower_duration: int = 5

    # ------------------------------------------------------------------ #
    # Exit parameters
    # ------------------------------------------------------------------ #
    stop_atr_mult: float = 2.0
    target_atr_mult: float = 3.0
    atr_period: int = 7

    # ------------------------------------------------------------------ #
    # Regime — fixed to Step 1 winner (ema_below_50)
    # ------------------------------------------------------------------ #
    regime_col: str = "ema_below_50_regime"
    ema_slope_period: int = 200
    ema_slope_lookback: int = 1
    ema_below_periods: list[int] = field(default_factory=lambda: [50])

    # ------------------------------------------------------------------ #
    # Falsification thresholds
    # ------------------------------------------------------------------ #
    significance_zscore: float = 2.5
    min_pf_diff_high_n: float = 0.02   # n > 50 000
    min_pf_diff_mid_n: float = 0.05    # 10 000 ≤ n ≤ 50 000
    min_pf_diff_low_n: float = 0.10    # n < 10 000
    min_pairs_passing: int = 4

    # KDE events are discrete (not every bar), so 5% floor is appropriate.
    min_coverage_ratio: float = 0.05

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
            "bear_strategy/hypothesis_tests/setup_kde_edge_check/test_results"
        )
    )
