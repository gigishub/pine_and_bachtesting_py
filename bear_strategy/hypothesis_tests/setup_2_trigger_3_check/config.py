"""Configuration for Setup 2 – Trigger 3: oscillator-level and band-expansion signals.

Baseline: regime AND kde_upper (4h KDE open > peak), promoted from Setup 1.

Tests four signals that fire when momentum or volatility structure confirms
a bearish turn at the KDE upper zone.

Entry TF  : configurable (default 1h — change to test 15m / 4h etc.)
KDE TF    : 4h  (structural gate)

Signals tested:

    rsi_cross_50
        RSI(period) crosses below 50 (from above to below on this bar).
        Confirms momentum is tipping from bullish to neutral/bearish.

    mfi_cross_50
        Money Flow Index(period) crosses below 50.
        MFI uses both price and volume — cross below 50 means selling
        money flow now dominates buying flow.

    rsi_cross_ma
        RSI crosses below its own moving average (EMA or SMA).
        More sensitive than a fixed level — adapts to the current RSI range.
        rsi_ma_type: "ema" (default) or "sma"

    bb_expand_down
        Bollinger Band lower boundary moves further below the prior bar's
        lower boundary, while price closes below the midband AND the bar
        is bearish (close < open).
        Captures directional volatility expansion toward the downside.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestConfig:
    # ------------------------------------------------------------------ #
    # Timeframes
    # ------------------------------------------------------------------ #
    entry_tf: str = "15m"
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
    # rsi_cross_50  — RSI crosses below 50
    # rsi_period: RSI lookback
    # rsi_threshold: level to cross (default 50)
    # ------------------------------------------------------------------ #
    rsi_period: int = 14
    rsi_threshold: float = 50.0

    # ------------------------------------------------------------------ #
    # mfi_cross_50  — Money Flow Index crosses below 50
    # mfi_period   : MFI lookback
    # mfi_threshold: level to cross (default 50)
    # ------------------------------------------------------------------ #
    mfi_period: int = 14
    mfi_threshold: float = 50.0

    # ------------------------------------------------------------------ #
    # rsi_cross_ma  — RSI crosses below its own MA
    # rsi_ma_period : MA lookback applied to the RSI series
    # rsi_ma_type   : "ema" or "sma"
    # ------------------------------------------------------------------ #
    rsi_ma_period: int = 9
    rsi_ma_type: str = "ema"

    # ------------------------------------------------------------------ #
    # bb_expand_down  — Bollinger Bands expand downward
    # bb_period : SMA / std lookback for the bands
    # bb_std    : number of standard deviations for band width
    # ------------------------------------------------------------------ #
    bb_period: int = 20
    bb_std: float = 2.0

    # ------------------------------------------------------------------ #
    # ema_rvol_cross  — EMA cross confirmed by elevated relative volume
    # ema_rvol_period   : EMA period for price cross (default 20)
    # ema_rvol_lookback : rolling window for RVOL denominator (default 20)
    # ema_rvol_threshold: RVOL must exceed this to qualify (default 1.1)
    # ------------------------------------------------------------------ #
    ema_rvol_period: int = 20
    ema_rvol_lookback: int = 20
    ema_rvol_threshold: float = 1.1

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
            "bear_strategy/hypothesis_tests/setup_2_trigger_3_check/test_results"
        )
    )
