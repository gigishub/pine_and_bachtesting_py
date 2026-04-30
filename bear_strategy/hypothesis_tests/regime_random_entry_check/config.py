"""Configuration for the regime random-entry falsification test (Step 1).

Adjust ``pairs`` and ``date_range`` to match your available parquet data.
Edit fields directly in this dataclass to change timeframe or exit sizing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestConfig:
    # ------------------------------------------------------------------ #
    # Timeframe
    # Candle resolution for entries, ATR, stops, and targets.
    # regime_tf is always "1d" and is not configurable here.
    # ------------------------------------------------------------------ #
    entry_tf: str = "1h"

    # ------------------------------------------------------------------ #
    # Exit parameters for the random short entries
    # ------------------------------------------------------------------ #
    stop_atr_mult: float = 2.0    # Stop placed at entry + stop_atr_mult × ATR
    target_atr_mult: float = 3.0  # Target placed at entry - target_atr_mult × ATR
    atr_period: int = 7           # ATR lookback on entry_tf bars

    # ------------------------------------------------------------------ #
    # Falsification thresholds
    # ------------------------------------------------------------------ #
    significance_zscore: float = 2.5   # statistical guardrail for win-rate lift
    min_pf_diff_high_n: float = 0.02   # PF lift floor when smaller population > 50k trades
    min_pf_diff_mid_n: float = 0.05    # PF lift floor when smaller population is 10k-50k
    min_pf_diff_low_n: float = 0.10    # PF lift floor when smaller population < 10k
    min_trades_per_pair: int = 1000    # minimum resolved trades per pair
    min_pairs_passing: int = 3         # filter must pass on this many pairs to survive

    # ------------------------------------------------------------------ #
    # Data
    # ------------------------------------------------------------------ #
    data_dir: Path = field(default_factory=lambda: Path("crypto_data/data"))

    pairs: list[str] = field(
        default_factory=lambda: [
            "BTCUSDT",
            "ETHUSDT",
            "SOLUSDT",
            "BNBUSDT",
            "XRPUSDT",
        ]
    )

    start_date: str = "2021-01-01"
    end_date: str = "2025-11-01"

    # ------------------------------------------------------------------ #
    # Regime indicator parameters
    # ------------------------------------------------------------------ #
    # Condition 1: EMA 200 slope pointing down
    ema_slope_period: int = 200
    ema_slope_lookback: int = 1

    # Condition 2: daily close below EMA 50
    ema_below_periods: list[int] = field(default_factory=lambda: [50])

    # ------------------------------------------------------------------ #
    # Output
    # ------------------------------------------------------------------ #
    results_dir: Path = field(
        default_factory=lambda: Path(
            "bear_strategy/backtest/hypothesis_tests_raw/results/step1_regime_check"
        )
    )
