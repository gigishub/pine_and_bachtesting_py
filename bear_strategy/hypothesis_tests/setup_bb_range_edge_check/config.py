"""Configuration for the BB Range Setup Edge Check.

Regime filter: ema_below_50 (Step 1 winner).
Setup filter: close price is WITHIN the Bollinger Bands
  (BB_lower ≤ close ≤ BB_upper) — price has not yet broken out below the
  lower band, so there is still downside range available before the market
  becomes statistically overextended.

This complements setup_bb_edge_check which tests bars that have BROKEN
below the lower band.  Together they answer: is the edge in extended
momentum (outside lower) or in the pre-breakdown zone (inside bands)?

Edit fields directly in this file to change timeframe or exit sizing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestConfig:
    # ------------------------------------------------------------------ #
    # Timeframe — single-TF, no context_tf needed.
    # ------------------------------------------------------------------ #
    entry_tf: str = "1d"

    # ------------------------------------------------------------------ #
    # Bollinger Band parameters (same defaults as setup_bb_edge_check)
    # ------------------------------------------------------------------ #
    bb_period: int = 20
    bb_std_mult: float = 2.0

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
    min_trades_per_pair: int = 1000
    min_pairs_passing: int = 4         # ≥ 4 of 5 pairs

    # Price is inside the bands the majority of the time, so a 40% floor
    # is reasonable — a much lower number would indicate something wrong.
    min_coverage_ratio: float = 0.40   # primary filter must keep ≥ 40% of regime bars

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
            "bear_strategy/backtest/hypothesis_tests_raw/results/step2_bb_range_check"
        )
    )


