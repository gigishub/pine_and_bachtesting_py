"""Configuration for the VWAP Rejection Candle Setup Edge Check.

Regime filter: ema_below_50 (Step 1 winner).

Setup filters tested against the regime-only baseline:

    vwap_rejection       — open > VWAP AND close < VWAP.
                           The candle crossed through VWAP bearishly: it
                           opened above (buyers in control at the start) but
                           sellers pushed it through and closed below VWAP.

    vwap_rejection_clean — vwap_rejection + minimal wicks at both ends.
                           Both top wick ≤ max_wick_ratio × candle range
                           AND bottom wick ≤ max_wick_ratio × candle range.
                           A clean rejection body: sellers stepped in at or
                           near the open and drove price straight down to close,
                           with little noise above or below.

─── Wick definitions ────────────────────────────────────────────────────────

For a bearish rejection candle (open > close):

    top_wick    = High  − Open   (how far above the open price was tested)
    bottom_wick = Close − Low    (how far below the close price was tested)
    candle_range = High − Low

    top_wick_ratio    = top_wick    / candle_range
    bottom_wick_ratio = bottom_wick / candle_range

A "clean" candle has both ratios ≤ max_wick_ratio (default 0.2 = 20%).
This means ≥ 60% of the candle range is solid body.

─── VWAP anchor options (vwap_anchor) ───────────────────────────────────────

    "daily"    — resets at UTC midnight each day  ← default
                 Best for 1h / 15m intraday scalps.

    "weekly"   — resets Monday 00:00 UTC each week.
                 Best for 4h / 1h swing entries.

    "monthly"  — resets the 1st of each UTC month.
                 Best for 4h / daily position shorts.

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
    # VWAP parameters
    # ------------------------------------------------------------------ #
    # Reset period for VWAP.  Options: "daily", "weekly", "monthly".
    vwap_anchor: str = "daily"

    # ------------------------------------------------------------------ #
    # Clean candle filter
    # ------------------------------------------------------------------ #
    # Maximum allowed wick-to-range ratio at each end.
    # 0.20 → each wick may be at most 20% of the total candle range.
    # Lower = stricter (cleaner body).  Try 0.15 for very clean candles.
    max_wick_ratio: float = 0.20

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
    min_pf_diff_high_n: float = 0.02    # n > 50 000
    min_pf_diff_mid_n: float = 0.05     # 10 000 ≤ n ≤ 50 000
    min_pf_diff_low_n: float = 0.10     # n < 10 000
    min_trades_per_pair: int = 500
    min_pairs_passing: int = 4          # ≥ 4 of 5 pairs

    # VWAP rejections are discrete events — lower floor than always-on filters.
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
            "bear_strategy/backtest/hypothesis_tests_raw/results/step2_vwap_rejection_check"
        )
    )
