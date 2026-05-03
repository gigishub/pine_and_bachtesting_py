"""Configuration for Setup 2 – Trigger 2: momentum-flip crossover signals.

Baseline: regime AND kde_upper (4h KDE open > peak), promoted from Setup 1.

Tests five momentum-flip indicators to confirm that the rally into the KDE
upper zone is losing steam or reversing, timed by a specific crossover event.

Entry TF  : configurable (default 1h — change to test 15m / 4h etc.)
KDE TF    : 4h  (structural gate)

Signals tested:

    cmf_cross
        Chaikin Money Flow crosses below zero.
        CMF = sum(money_flow_volume, period) / sum(volume, period)
        where money_flow_multiplier = ((close - low) - (high - close)) / (high - low)
        Cross: cmf < 0 AND cmf.shift(1) >= 0
        Confirms "big money" distribution replacing accumulation at the level.

    willr_cross
        Williams %R crosses below willr_threshold (default -20).
        WR = -100 × (highest_high - close) / (highest_high - lowest_low)
        Range: 0 (overbought) to -100 (oversold).
        Cross below -20 means price is failing to hold near recent highs.

    roc_cross
        Rate-of-Change crosses below zero.
        ROC = (close - close.shift(period)) / close.shift(period) × 100
        Cross: roc < 0 AND roc.shift(1) >= 0
        Current price fell below where it was N bars ago — velocity turned negative.

    trix_cross
        TRIX (triple-smoothed EMA pct-change) crosses below its signal line
        while TRIX is still above zero (rolling over from a peak).
        trix = pct_change(ema3(close, period)) × 100
        signal = ema(trix, signal_period)
        Cross: (trix < signal AND trix.shift(1) >= signal.shift(1)) AND trix.shift(1) > 0
        Filters out noise — only structural trend rollover events fire.

    fisher_cross
        Fisher Transform drops below its prior-bar value from an extreme high.
        fisher = 0.5 × ln((1 + v) / (1 - v))
        where v = 2 × (hl2 - min_hl2) / (max_hl2 - min_hl2) - 1  (clipped ±0.999)
        Trigger = fisher.shift(1)
        Cross: fisher < trigger AND trigger > fisher_extreme (default 1.5)
        Statistically extreme price snap-back at resistance.

    ema_cross
        Price crosses below its EMA (default 20-period).
        ema = ewm(close, span=ema_cross_period)
        Cross: close < ema AND close.shift(1) >= ema.shift(1)
        Simple structural trigger — price giving up the moving average.
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
    # cmf_cross  — Chaikin Money Flow
    # cmf_period: rolling sum window
    # ------------------------------------------------------------------ #
    cmf_period: int = 20

    # ------------------------------------------------------------------ #
    # willr_cross  — Williams %R
    # willr_period     : lookback for highest-high / lowest-low
    # willr_threshold  : cross-below level (default -20 = exit overbought)
    # ------------------------------------------------------------------ #
    willr_period: int = 14
    willr_threshold: float = -20.0

    # ------------------------------------------------------------------ #
    # roc_cross  — Rate of Change
    # roc_period: n bars back for price comparison
    # ------------------------------------------------------------------ #
    roc_period: int = 12

    # ------------------------------------------------------------------ #
    # trix_cross  — TRIX signal-line cross
    # trix_period        : EMA period for each of the three smoothing passes
    # trix_signal_period : EMA period for the signal line
    # ------------------------------------------------------------------ #
    trix_period: int = 15
    trix_signal_period: int = 9

    # ------------------------------------------------------------------ #
    # fisher_cross  — Fisher Transform trigger cross
    # fisher_period   : lookback for highest/lowest hl2
    # fisher_extreme  : trigger line (Fisher.shift(1)) must exceed this
    #                   to qualify as "at extreme high" — default 1.5
    # ------------------------------------------------------------------ #
    fisher_period: int = 9
    fisher_extreme: float = 1.5

    # ------------------------------------------------------------------ #
    # ema_cross  — Price crosses below EMA
    # ema_cross_period : EMA lookback (default 20)
    # ------------------------------------------------------------------ #
    ema_cross_period: int = 20

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
            "bear_strategy/hypothesis_tests/setup_2_trigger_2_check/test_results"
        )
    )
