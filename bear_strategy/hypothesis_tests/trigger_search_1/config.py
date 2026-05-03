"""Configuration for Trigger Search 2: optimized entry timing on close_below_bb baseline.

Purpose
-------
Previous testing (trigger_search_1) confirmed close_below_bb as a strong event trigger
(avg PF 1.885, 4/5 pairs). This test refines entry timing by adding momentum confirmation.

Baseline (two-layer, both confirmed):
    regime AND kde_upper (4h) AND RSI_MA(rsi_ma_type, rsi_ma_period) < rsi_ma_threshold

Three entry timing conditions tested:

    close_below_bb
        Close < lower Bollinger Band.
        Base trigger — price accepts value below the 2σ band on the close.
        (Previously confirmed: avg PF 1.885, 4/5 pairs)

    bearish_candle_size
        Bar range falls within 0.7–1.2 × ATR (medium-sized bearish candle).
        Confirms momentum without over-expansion or compression (avoids extremes).

    ema_cross_price
        Price crosses below EMA(n, default 10) on this bar.
        Event signal: the first bar where price rolls under the short-term moving average.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestConfig:
    # ------------------------------------------------------------------ #
    # Timeframes
    # ------------------------------------------------------------------ #
    entry_tf: str = "1h"
    kde_tf: str = "4h"
    context_tf: str = "1d"

    # ------------------------------------------------------------------ #
    # Exit parameters
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
    kde_lower_duration: int = 2

    # ------------------------------------------------------------------ #
    # RSI MA — baked into the baseline
    # ------------------------------------------------------------------ #
    rsi_period: int = 14
    rsi_ma_period: int = 5
    rsi_ma_type: str = "ema"
    rsi_ma_threshold: float = 50.0

    # ------------------------------------------------------------------ #
    # bearish_engulfing  (no extra params)
    # break_prior_low    (no extra params)
    # ------------------------------------------------------------------ #

    # ------------------------------------------------------------------ #
    # close_below_bb — close below lower Bollinger Band (BASE CONFIRMED TRIGGER)
    # ------------------------------------------------------------------ #
    bb_period: int = 10
    bb_std: float = 2.0

    # ------------------------------------------------------------------ #
    # bearish_candle_size — bar range in 0.7–1.2 × ATR range (medium size)
    # ------------------------------------------------------------------ #
    atr_candle_min: float = 0.5
    atr_candle_max: float = 1

    # ------------------------------------------------------------------ #
    # ema_cross_price — price crosses below EMA(n, default 10)
    # ------------------------------------------------------------------ #
    ema_cross_period: int = 15

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
            "bear_strategy/hypothesis_tests/trigger_search_1/test_results"
        )
    )
