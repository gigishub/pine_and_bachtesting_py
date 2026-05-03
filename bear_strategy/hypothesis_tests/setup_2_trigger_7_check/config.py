"""Configuration for Setup 2 – Trigger 7: exhaustion / momentum-fade signals.

Baseline: regime AND kde_upper (4h KDE open > peak), promoted from Setup 1.

Tests four exhaustion signals on top of the baseline. All focus on detecting
when an upswing is "hollow" — price pushed higher but underlying energy fading.

Entry TF  : configurable (default 1h)
KDE TF    : 4h  (structural gate)

Signals tested:

    price_rsi_divergence
        Price makes a Higher High over lookback, but RSI makes a Lower High.
        Logic: Latest push done on weaker relative strength — hollow move.

    shrinking_impulse
        The gain from the previous high to the current high is smaller than
        the prior high-to-high gain (impulse is shrinking) AND the bar has
        a long upper wick (top wick > wick_ratio * bar range).
        Logic: Buyers struggling to extend; sellers immediately reject each push.

    bb_rounding
        Price was near the upper Bollinger Band bb_lookback bars ago, but has
        since pulled toward the midline, AND the upper band itself is flattening
        (upper_bb <= upper_bb[1]).
        Logic: Volatility driving the move is dying; "rounding top" forming.

    ema_tightening
        The absolute gap between a fast EMA and a slow EMA is narrowing
        (current |fast-slow| < prior |fast-slow|) while fast EMA < slow EMA.
        Logic: EMAs fan out in strong moves; convergence signals momentum loss.
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
    # price_rsi_divergence
    # divergence_lookback : bars back to find previous swing high (default 20)
    # rsi_period          : RSI period for divergence check (default 14)
    # ------------------------------------------------------------------ #
    divergence_lookback: int = 20
    rsi_period: int = 14

    # ------------------------------------------------------------------ #
    # shrinking_impulse
    # impulse_lookback   : bars back to find previous high-to-high gain (default 20)
    # wick_ratio         : upper wick must exceed this fraction of bar range (default 0.5)
    # ------------------------------------------------------------------ #
    impulse_lookback: int = 20
    wick_ratio: float = 0.5

    # ------------------------------------------------------------------ #
    # bb_rounding
    # bb_period          : Bollinger Band SMA period (default 20)
    # bb_std             : Bollinger Band standard deviation multiplier (default 2.0)
    # bb_proximity_pct   : how close to upper band counts as "walking" (default 0.01)
    # bb_lookback        : bars ago price must have been near upper band (default 10)
    # ------------------------------------------------------------------ #
    bb_period: int = 20
    bb_std: float = 2.0
    bb_proximity_pct: float = 0.01
    bb_lookback: int = 10

    # ------------------------------------------------------------------ #
    # ema_tightening
    # ema_fast           : fast EMA period (default 9)
    # ema_slow           : slow EMA period (default 20)
    # ------------------------------------------------------------------ #
    ema_fast: int = 9
    ema_slow: int = 20

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
    end_date: str = "2023-11-01"

    # ------------------------------------------------------------------ #
    # Output
    # ------------------------------------------------------------------ #
    results_dir: Path = field(
        default_factory=lambda: Path(
            "bear_strategy/hypothesis_tests/setup_2_trigger_7_check/test_results"
        )
    )
