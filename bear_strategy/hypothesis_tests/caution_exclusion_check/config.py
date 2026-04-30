"""Configuration for Step 2b — Caution Exclusion Filter.

Hypothesis: Within the EMA-50 bear regime, excluding bars where price
reclaims the 1H EMA(20) OR where the 7-bar swing exceeds 1.5× ATR should
improve short-entry quality by removing noise/reversal bars.

To sweep timeframes or exit sizing across all steps, edit
``bear_strategy/hypothesis_tests/experiment_config.py`` and use
``TestConfig.from_experiment(ExperimentConfig())``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bear_strategy.hypothesis_tests.experiment_config import ExperimentConfig


@dataclass
class TestConfig:
    # ------------------------------------------------------------------ #
    # Timeframe — all signals computed on entry_tf bars.
    # No context_tf needed; this test is single-timeframe.
    # ------------------------------------------------------------------ #
    entry_tf: str = "1h"

    # ------------------------------------------------------------------ #
    # Caution filter parameters
    # ------------------------------------------------------------------ #
    # EMA period for local trend reference (is_caution condition 1)
    ema20_period: int = 20
    # Rolling window for 7-bar swing range (is_caution condition 2)
    range_period: int = 7
    # Multiplier: range > range_atr_mult × ATR is flagged as choppy
    range_atr_mult: float = 1.5

    # ------------------------------------------------------------------ #
    # Exit parameters — ATR(7) per spec, same period used for range filter
    # ------------------------------------------------------------------ #
    stop_atr_mult: float = 2.0
    target_atr_mult: float = 3.0
    atr_period: int = 7  # ATR(entry_tf, 7) per spec; matches ExperimentConfig default

    # ------------------------------------------------------------------ #
    # Regime — fixed to Step 1 winner (ema_below_50)
    # See bear_strategy/backtest/hypothesis_tests_raw/results/step1_regime_check/
    # ------------------------------------------------------------------ #
    regime_col: str = "ema_below_50_regime"
    ema_slope_period: int = 200
    ema_slope_lookback: int = 1
    ema_below_periods: list[int] = field(default_factory=lambda: [50])

    # ------------------------------------------------------------------ #
    # Falsification thresholds — ≥ 4 of 5 pairs must pass
    # ------------------------------------------------------------------ #
    significance_zscore: float = 2.5
    min_pf_diff_high_n: float = 0.02   # n > 50 000
    min_pf_diff_mid_n: float = 0.05    # 10 000 ≤ n ≤ 50 000
    min_pf_diff_low_n: float = 0.10    # n < 10 000
    min_trades_per_pair: int = 1000
    min_pairs_passing: int = 4

    # no_caution must keep ≥ this fraction of eligible regime bars.
    # Unlike BB (6–8%), caution bars are the minority in a clean bear trend
    # so this should pass easily. Hard-fail if it doesn't.
    min_coverage_ratio: float = 0.40

    # ------------------------------------------------------------------ #
    # Data — 5 pairs (same as Step 2a)
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
            "bear_strategy/backtest/hypothesis_tests_raw/results/step2b_caution_check"
        )
    )

    # ------------------------------------------------------------------ #
    # Factory: build from shared ExperimentConfig
    # ------------------------------------------------------------------ #
    @classmethod
    def from_experiment(cls, exp: "ExperimentConfig") -> "TestConfig":
        """Create a TestConfig using shared TF and exit settings.

        atr_period defaults to 7 in both TestConfig and ExperimentConfig,
        so no override is needed for this step's spec.
        """
        return cls(
            entry_tf=exp.entry_tf,
            stop_atr_mult=exp.stop_atr_mult,
            target_atr_mult=exp.target_atr_mult,
            atr_period=exp.atr_period,
        )
