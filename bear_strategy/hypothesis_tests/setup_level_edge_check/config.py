"""Configuration for the setup level edge check (Step 2).

Regime filter fixed to the Step 1 winner: ``ema_below_50``.
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
    # Timeframes
    # entry_tf   = candle resolution for entries, stops, and targets.
    # context_tf = higher-TF for VPVR, AVWAP, and ATR context signals.
    #
    # Timeframe choice guide for bear shorts:
    #   "15m" entry + "4h" context → intraday scalp shorts (1–8 h holds)
    #   "1h"  entry + "4h" context → swing shorts (4–48 h holds)  ← default
    #   "4h"  entry + "1d" context → position shorts (days to weeks)
    #
    # To change: set entry_tf and context_tf, then ensure matching parquet
    # files exist under crypto_data/data/{PAIR}/{PAIR}_{tf}_*.parquet.
    # ------------------------------------------------------------------ #
    entry_tf: str = "1h"
    context_tf: str = "4h"

    # ------------------------------------------------------------------ #
    # Exit parameters (same as Step 1)
    # ------------------------------------------------------------------ #
    stop_atr_mult: float = 2.0
    target_atr_mult: float = 3.0
    atr_period: int = 14  # ATR period on entry_tf bars (stop/target sizing)

    # ------------------------------------------------------------------ #
    # Setup distance threshold
    # ------------------------------------------------------------------ #
    # Near-setup: price within setup_distance_atr × ATR_context of a level
    setup_distance_atr: float = 0.5

    # ------------------------------------------------------------------ #
    # Context-TF indicator parameters
    # ------------------------------------------------------------------ #
    atr_4h_period: int = 14
    vpvr_window: int = 200   # trailing context_tf bars for the volume profile
    vpvr_bins: int = 50      # price grid resolution
    swing_lookback: int = 5  # bars to left of candidate swing high
    swing_confirmation_bars: int = 3  # bars to right needed for confirmation

    # ------------------------------------------------------------------ #
    # Regime — fixed to Step 1 winner (ema_below_50)
    # See bear_strategy/backtest/hypothesis_tests_raw/results/step1_regime_check/step1_results.csv
    # ------------------------------------------------------------------ #
    regime_col: str = "ema_below_50_regime"
    ema_slope_period: int = 200
    ema_slope_lookback: int = 1
    ema_below_periods: list[int] = field(default_factory=lambda: [50])

    # ------------------------------------------------------------------ #
    # Falsification thresholds (identical to Step 1)
    # ------------------------------------------------------------------ #
    significance_zscore: float = 2.5
    min_pf_diff_high_n: float = 0.02   # n > 50 000
    min_pf_diff_mid_n: float = 0.05    # 10 000 ≤ n ≤ 50 000
    min_pf_diff_low_n: float = 0.10    # n < 10 000
    min_trades_per_pair: int = 1000
    min_pairs_passing: int = 3

    # ------------------------------------------------------------------ #
    # Data
    # ------------------------------------------------------------------ #
    data_dir: Path = field(default_factory=lambda: Path("crypto_data/data"))
    pairs: list[str] = field(
        default_factory=lambda: ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]
    )
    start_date: str = "2021-01-01"
    end_date: str = "2025-11-01"

    # ------------------------------------------------------------------ #
    # Output
    # ------------------------------------------------------------------ #
    results_dir: Path = field(
        default_factory=lambda: Path(
            "bear_strategy/backtest/hypothesis_tests_raw/results/step2_setup_check"
        )
    )

    # ------------------------------------------------------------------ #
    # Factory: build from shared ExperimentConfig
    # ------------------------------------------------------------------ #
    @classmethod
    def from_experiment(cls, exp: "ExperimentConfig") -> "TestConfig":
        """Create a TestConfig using shared TF and exit settings."""
        return cls(
            entry_tf=exp.entry_tf,
            context_tf=exp.context_tf,
            stop_atr_mult=exp.stop_atr_mult,
            target_atr_mult=exp.target_atr_mult,
            atr_period=exp.atr_period,
        )
