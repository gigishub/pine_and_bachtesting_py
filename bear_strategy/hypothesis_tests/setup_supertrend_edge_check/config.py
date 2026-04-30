"""Configuration for the SuperTrend Setup Edge Check.

Regime filter: ema_below_50 (Step 1 winner).

Setup filter: SuperTrend(st_length, st_multiplier) direction is bearish
  (direction = −1), meaning close is below the SuperTrend resistance line
  and the indicator confirms an active downtrend.

Two sub-populations decompose whether the edge comes from entries close to
the SuperTrend resistance line (acting as overhead supply) versus entries
that are already extended far below it:

    st_near_resistance  — close within  proximity_atr_mult × ATR of the ST line
    st_extended         — close more than proximity_atr_mult × ATR below the ST line

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
    entry_tf: str = "4h"

    # ------------------------------------------------------------------ #
    # SuperTrend parameters
    # Defaults match the widely-used settings for crypto swing trading.
    # ------------------------------------------------------------------ #
    st_length: int = 10        # ATR lookback for SuperTrend bands
    st_multiplier: float = 4 # band width in ATR multiples

    # How close (in ATR units) a bar's close must be to the ST resistance
    # line to be classified as "near resistance".
    proximity_atr_mult: float = 0.5

    # ------------------------------------------------------------------ #
    # Exit parameters
    # ------------------------------------------------------------------ #
    stop_atr_mult: float = 1
    target_atr_mult: float = 2
    atr_period: int = 7   # entry-TF ATR used for stop/target and proximity

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

    # st_bear must keep enough bars for a trigger layer to work on top.
    min_coverage_ratio: float = 0.30   # primary filter must keep ≥ 30% of regime bars

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
            "bear_strategy/backtest/hypothesis_tests_raw/results/step2_supertrend_check"
        )
    )

    # ------------------------------------------------------------------ #
    # Helpers for pandas_ta column name resolution
    # ------------------------------------------------------------------ #
    def st_col(self) -> str:
        """pandas_ta SuperTrend line column name."""
        return f"SUPERT_{self.st_length}_{self.st_multiplier}"

    def st_dir_col(self) -> str:
        """pandas_ta SuperTrend direction column name."""
        return f"SUPERTd_{self.st_length}_{self.st_multiplier}"
