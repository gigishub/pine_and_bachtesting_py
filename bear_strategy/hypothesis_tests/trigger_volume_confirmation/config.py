"""Configuration for the trigger volume confirmation test (Step 3).

Regime filter: ema_below_50 (Step 1 winner).
Step 2 falsified setup-level proximity — this test operates directly on
the regime population with no setup gate.

Edit fields directly in this dataclass to change timeframe or exit sizing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestConfig:
    # ------------------------------------------------------------------ #
    # Timeframe
    # entry_tf = candle resolution for entries, stops, targets, and the
    # volume rolling average. No higher-TF alignment needed for this test.
    #
    # Timeframe choice guide for bear shorts:
    #   "15m" → intraday scalp shorts (holds 15 min – 4 h)
    #   "1h"  → swing shorts (holds 1 – 48 h)  ← default
    #   "4h"  → position shorts (holds days to weeks)
    #
    # To change: set entry_tf, ensure matching parquet files exist under
    # crypto_data/data/{PAIR}/{PAIR}_{entry_tf}_*.parquet.
    # ------------------------------------------------------------------ #
    entry_tf: str = "15m"

    # ------------------------------------------------------------------ #
    # Exit parameters (same as Steps 1 and 2)
    # ------------------------------------------------------------------ #
    stop_atr_mult: float = 2.0
    target_atr_mult: float = 3.0
    atr_period: int = 7   # ATR period on entry_tf bars

    # ------------------------------------------------------------------ #
    # Volume trigger
    # ------------------------------------------------------------------ #
    volume_window: int = 20      # Rolling window for average volume
    volume_mult: float = 1.2     # Trigger when volume > volume_mult × rolling_avg

    # ------------------------------------------------------------------ #
    # Regime — fixed to Step 1 winner (ema_below_50)
    # See bear_strategy/backtest/hypothesis_tests_raw/results/step1_regime_check/step1_results.csv
    # ------------------------------------------------------------------ #
    regime_col: str = "ema_below_50_regime"
    ema_slope_period: int = 200
    ema_slope_lookback: int = 1
    ema_below_periods: list[int] = field(default_factory=lambda: [50])

    # ------------------------------------------------------------------ #
    # Falsification thresholds (identical to Steps 1 and 2)
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
        default_factory=lambda: ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT","XRPUSDT"]
    )
    start_date: str = "2021-01-01"
    end_date: str = "2025-11-01"

    # ------------------------------------------------------------------ #
    # Output
    # ------------------------------------------------------------------ #
    results_dir: Path = field(
        default_factory=lambda: Path(
            "bear_strategy/hypothesis_tests/trigger_volume_confirmation/test_results"
        )
    )
