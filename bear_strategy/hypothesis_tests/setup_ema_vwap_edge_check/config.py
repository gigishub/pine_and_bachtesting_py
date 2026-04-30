"""Configuration for the EMA20 / VWAP Setup Edge Check.

Regime filter: ema_below_50 (Step 1 winner).

Setup filters tested against the regime-only baseline:

    below_ema20        — close < EMA(ema_period) at bar close.
    below_vwap         — close < anchored VWAP at bar close.
    below_both         — close < EMA AND close < VWAP simultaneously.
    below_vwap_1std    — close < VWAP − 1 standard deviation band.

VWAP anchor options (vwap_anchor):

    "daily"    — resets at UTC midnight each day  ← default
                 Best for 1h / 15m / 5m intraday scalps.

    "weekly"   — resets at the start of each UTC week (Monday 00:00).
                 Best for 4h / 1h swing entries.

    "monthly"  — resets at the start of each UTC month.
                 Best for 4h / daily position shorts.

VWAP standard deviation bands (vwap_std_mult):

    The standard deviation of the typical price (volume-weighted) within
    the current anchor window is computed alongside the VWAP.  Bands:

        upper_band = VWAP + vwap_std_mult × std
        lower_band = VWAP − vwap_std_mult × std

    Setting vwap_std_mult = 1.0 gives the ±1σ band (common default).
    The `below_vwap_1std` population fires when close < lower_band,
    meaning price is more than 1σ below VWAP — a deeper bearish position.

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
    # Indicator parameters
    # ------------------------------------------------------------------ #
    ema_period: int = 20   # EMA lookback period

    # ── VWAP anchor ──────────────────────────────────────────────────── #
    # Controls when VWAP resets.  Options: "daily", "weekly", "monthly".
    # Use "daily" for intraday TFs (15m/1h), "weekly" for 4h/1h swing,
    # "monthly" for position-level entries.
    vwap_anchor: str = "daily"

    # ── VWAP standard deviation band multiplier ───────────────────────  #
    # The lower_band = VWAP − vwap_std_mult × rolling_std.
    # 1.0 = ±1σ band  (default, covers ~68% of typical price distribution)
    # 2.0 = ±2σ band  (stricter — price deep below VWAP)
    vwap_std_mult: float = 2

    # ------------------------------------------------------------------ #
    # Exit parameters
    # ------------------------------------------------------------------ #
    stop_atr_mult: float = 2.0
    target_atr_mult: float = 3.0
    atr_period: int = 14

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

    # In a bear regime most bars trade below EMA20 — expect high coverage.
    min_coverage_ratio: float = 0.30

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
            "bear_strategy/backtest/hypothesis_tests_raw/results/step2_ema_vwap_check"
        )
    )
