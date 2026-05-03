"""Configuration for Setup 2 Candle Trigger: KDE Upper (4h) + 15m bar quality.

Baseline: regime AND kde_upper (4h KDE, promoted from Setup 1).
Tests whether bearish bar-quality signals on 15m add edge on top of the
confirmed structural gate.

Entry TF  : 15m
KDE TF    : 4h  (structural gate)
Reference : 1d  (regime context)

Signals tested:
    bearish_rvol         -- bearish bar with volume spike
    upper_wick_rejection -- large upper wick relative to total bar range
    breakdown_bar        -- bearish close in lower portion of range
    roc_negative         -- rate-of-change negative over N bars
    bearish_engulf       -- bearish engulfing pattern
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestConfig:
    # ------------------------------------------------------------------ #
    # Timeframes
    # ------------------------------------------------------------------ #
    entry_tf: str = "4h"
    kde_tf: str = "4h"
    context_tf: str = "1d"

    # ------------------------------------------------------------------ #
    # Exit parameters (15m ATR)
    # ------------------------------------------------------------------ #
    stop_atr_mult: float = 2.0
    target_atr_mult: float = 3.0
    atr_period: int = 7

    # ------------------------------------------------------------------ #
    # KDE parameters (must match Setup 1 confirmed values)
    # ------------------------------------------------------------------ #
    kde_window: int = 200
    kde_bandwidth_mult: float = 1.0
    kde_n_points: int = 500
    kde_value_area_pct: float = 0.70
    kde_lower_duration: int = 2    # kept for _compute_kde_signals signature

    # ------------------------------------------------------------------ #
    # bearish_rvol
    # Bearish bar (close < open) AND volume > threshold × rolling mean
    # ------------------------------------------------------------------ #
    rvol_window: int = 20         # 24h rolling baseline at 15m
    rvol_threshold: float = 1.4

    # ------------------------------------------------------------------ #
    # upper_wick_rejection
    # upper_wick / bar_range > wick_ratio_threshold
    # Does NOT require a bearish bar — measures seller rejection at the top
    # ------------------------------------------------------------------ #
    wick_ratio_threshold: float = 0.5    # upper wick > 50% of total range

    # ------------------------------------------------------------------ #
    # breakdown_bar
    # Bearish bar (close < open) that closes in the bottom N% of its range
    # ------------------------------------------------------------------ #
    breakdown_close_pct: float = 0.25   # close in bottom 25% of bar range

    # ------------------------------------------------------------------ #
    # roc_negative
    # (close - close[N]) / close[N] < 0
    # ------------------------------------------------------------------ #
    roc_period: int = 3                 # lookback in 15m bars

    # ------------------------------------------------------------------ #
    # bearish_engulf
    # No extra parameters — standard definition:
    #   curr bar bearish, prev bar bullish, curr body fully engulfs prev body
    # ------------------------------------------------------------------ #

    # ------------------------------------------------------------------ #
    # Regime
    # ------------------------------------------------------------------ #
    regime_col: str = "ema_below_50_regime"
    ema_slope_period: int = 200
    ema_slope_lookback: int = 1
    ema_below_periods: list[int] = field(default_factory=lambda: [50])

    # ------------------------------------------------------------------ #
    # Verdict thresholds
    # ------------------------------------------------------------------ #
    min_pairs_passing: int = 3

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
            "bear_strategy/hypothesis_tests/setup_2_candle_trigger_check/test_results"
        )
    )
