"""Configuration for the RSI Setup Edge Check.

Regime filter: ema_below_50 (Step 1 winner).
Setup filter: RSI(rsi_period) strictly between rsi_lower and rsi_upper —
  bearish momentum confirmed but not yet oversold, so there is still room
  to fall rather than bouncing from an exhausted dip.

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
    entry_tf: str = "1h"

    # ------------------------------------------------------------------ #
    # RSI parameters
    # ------------------------------------------------------------------ #
    rsi_period: int = 7
    rsi_lower: float = 20  # exclude oversold bars (likely to bounce)
    rsi_upper: float = 40   # exclude bars above midline (bearish zone entry only)

    # ------------------------------------------------------------------ #
    # Exit parameters (consistent with other steps)
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

    # RSI [30, 50] is a narrower zone than full-regime, so the coverage
    # floor is lower — but the filter still must not be too selective to
    # leave room for a trigger layer on top.
    min_coverage_ratio: float = 0.20   # primary filter must keep ≥ 20% of regime bars

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
            "bear_strategy/hypothesis_tests/setup_rsi_edge_check/test_results"
        )
    )


