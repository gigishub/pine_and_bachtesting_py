"""Configuration for the BB Widening Setup Edge Check.

Regime filter: ema_below_50 (Step 1 winner).
Setup filter: BB bands are widening (BB_width > BB_width[1]) — volatility is
  picking up, which in a bear regime often precedes or accompanies an
  accelerating move down.

Edit fields directly in this file to change timeframe or exit sizing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestConfig:
    # ------------------------------------------------------------------ #
    # Timeframe
    # All BB and ATR signals are computed on entry_tf bars.
    # No context_tf needed — this test is single-timeframe.
    # ------------------------------------------------------------------ #
    entry_tf: str = "4h"

    # ------------------------------------------------------------------ #
    # Bollinger Band parameters
    # ------------------------------------------------------------------ #
    bb_period: int = 20       # SMA and StdDev lookback
    bb_std_mult: float = 2.0  # standard deviations for upper/lower bands

    # ------------------------------------------------------------------ #
    # Exit parameters
    # ATR period = 5 per spec ("ATR(1H, 5)") — keep at 5 for comparability
    # ------------------------------------------------------------------ #
    stop_atr_mult: float = 2.0
    target_atr_mult: float = 3.0
    atr_period: int = 5  # ATR(entry_tf, 5) per revised spec

    # ------------------------------------------------------------------ #
    # Regime — fixed to Step 1 winner (ema_below_50)
    # See bear_strategy/backtest/hypothesis_tests_raw/results/step1_regime_check/
    # ------------------------------------------------------------------ #
    regime_col: str = "ema_below_50_regime"
    ema_slope_period: int = 200
    ema_slope_lookback: int = 1
    ema_below_periods: list[int] = field(default_factory=lambda: [50])

    # ------------------------------------------------------------------ #
    # Falsification thresholds
    # Spec: pass on ≥ 4 of 5 pairs (stricter than Step 1's 3/4)
    # ------------------------------------------------------------------ #
    significance_zscore: float = 2.5
    min_pf_diff_high_n: float = 0.02   # n > 50 000
    min_pf_diff_mid_n: float = 0.05    # 10 000 ≤ n ≤ 50 000
    min_pf_diff_low_n: float = 0.10    # n < 10 000
    min_trades_per_pair: int = 1000
    min_pairs_passing: int = 4         # ≥ 4 of 5 pairs per spec

    # Minimum fraction of regime bars that bb_widening must keep.
    # Widening occurs roughly half the time, so a 30% floor is appropriate.
    min_coverage_ratio: float = 0.30   # filter must keep ≥ 30% of regime bars

    # ------------------------------------------------------------------ #
    # Data — 5 pairs (same as Step 1; XRP added)
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
            "bear_strategy/backtest/hypothesis_tests_raw/results/step2_bb_check"
        )
    )
