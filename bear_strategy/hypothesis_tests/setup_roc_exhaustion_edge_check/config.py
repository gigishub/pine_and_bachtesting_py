"""Configuration for the ROC Exhaustion Setup Edge Check.

Regime filter: ema_below_50 (Step 1 winner).

Setup filter: ROC-based exhaustion zones translated from the
  "ROC Exhaustion Zones" Pine Script indicator.

Three populations are tested as bear setup conditions:

    roc_post_bull   — bullExhaustionActive = True (red zone).
                      ROC had been rising for drift_bars bars above
                      accel_thresh, but the trend has now ended.
                      Hypothesis: post-bull exhaustion in a bear regime
                      predicts continuation downward.

    roc_bear_trend  — isBearTrend = True (bear prediction zone).
                      ROC is actively falling for drift_bars bars and
                      is below -accel_thresh.
                      Hypothesis: momentum confirmation of the bear move.

    roc_post_bear   — bearExhaustionActive = True (green zone).
                      ROC had been falling for drift_bars bars below
                      -accel_thresh, but the trend has now ended.
                      Hypothesis: local bounces inside a bear regime
                      still offer short edge (bear-in-bear exhaustion).

Edit fields directly in this file to change timeframe or parameters.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestConfig:
    # ------------------------------------------------------------------ #
    # Timeframe — single-TF, no context_tf needed.
    # ------------------------------------------------------------------ #
    entry_tf: str = "4h"

    # ------------------------------------------------------------------ #
    # ROC Exhaustion parameters (mirror Pine Script defaults)
    # ------------------------------------------------------------------ #
    roc_len: int = 10           # ROC lookback period (ta.roc bars)
    drift_bars: int = 3         # consecutive bars ROC must be rising/falling
    accel_thresh: float = 0.5   # ROC must exceed ±this % to qualify as a trend

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
    min_trades_per_pair: int = 500
    min_pairs_passing: int = 4         # ≥ 4 of 5 pairs

    # Exhaustion zones are narrower than the full regime, so a lower floor
    # is appropriate — but the filter must still leave room for a trigger.
    min_coverage_ratio: float = 0.15   # primary filters must keep ≥ 15% of regime bars

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
            "bear_strategy/backtest/hypothesis_tests_raw/results/step2_roc_exhaustion_check"
        )
    )
