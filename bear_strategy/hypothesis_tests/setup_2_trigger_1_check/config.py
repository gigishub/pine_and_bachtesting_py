"""Configuration for Setup 2 – Trigger 1: zone-sequence signals after KDE upper touch.

Baseline: regime AND kde_upper (4h KDE open > peak), promoted from Setup 1.

All trigger signals fire AFTER price has tagged the KDE upper zone on the
entry TF (high >= kde_peak).  They measure structural follow-through:
expansion, consecutive closes, lower-high formation, low violation, or a
failed retest.

Entry TF  : configurable (default 1h — change to test 15m / 4h)
KDE TF    : 4h  (structural gate and peak price level)

Triggers tested:

    trigger_1  ATR expansion bearish turn
        After zone touch: bar range > atr_expansion_mult × short ATR,
        bar closes below its open AND below the prior bar's close.
        Confirms momentum expansion in the bearish direction away from zone.

    trigger_2  Consecutive bearish closes
        After zone touch: N consecutive bars (consec_bearish_n) each
        closing strictly below the prior close.  Pure price commitment,
        no range or volume filter.

    trigger_3  Lower high formation
        After zone touch: the highest high seen between the touch bar and
        the current bar is strictly below the touch bar's high (lower high
        confirmed), AND the current bar closes bearishly (close < open)
        AND below the open of the bar that formed the lower high.

    trigger_4  Zone-touch bar low violation
        After zone touch: current bar closes strictly below the low of the
        zone-touch bar, putting all buyers who entered on the touch bar
        underwater and confirming structural rejection.

    trigger_5  Failed retest
        After zone touch and initial pullback: price returns to within
        retest_proximity_atr ATRs of the kde_peak from below.  The retest
        bar closes below its midpoint AND below the prior close AND on a
        smaller range than the original zone-touch bar.  Confirms supply
        is still organised at the level on diminishing buying pressure.

    trigger_6  RSI below threshold (momentum fade)
        RSI(rsi_period) < rsi_threshold on the entry TF — same confirmed
        signal from the prior kde_zone_trigger test.  Included here as a
        standalone reference so confirmed momentum filter can be seen
        alongside the new structural triggers.
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
    # Zone-touch lookbacks
    # For triggers 1–3: how many bars after a zone touch the signal is valid.
    # For trigger 4: low-violation lookback (slightly wider).
    # For trigger 5: retest lookback (needs pullback + return time).
    # ------------------------------------------------------------------ #
    zone_touch_lookback: int = 10
    zone_touch_low_lookback: int = 15
    retest_lookback: int = 25

    # ------------------------------------------------------------------ #
    # trigger_1  ATR expansion bearish turn
    # Short ATR uses atr_short_period bars (Wilder EMA).
    # Signal fires when bar_range > atr_expansion_mult × atr_short (prior bar).
    # ------------------------------------------------------------------ #
    atr_short_period: int = 5
    atr_expansion_mult: float = 1.2

    # ------------------------------------------------------------------ #
    # trigger_2  Consecutive bearish closes
    # consec_bearish_n: number of bars required (2 or 3, counting backwards
    # from the current bar inclusive).
    # ------------------------------------------------------------------ #
    consec_bearish_n: int = 1

    # ------------------------------------------------------------------ #
    # trigger_3  Lower high formation
    # No extra parameters; uses zone_touch_lookback.
    # ------------------------------------------------------------------ #

    # ------------------------------------------------------------------ #
    # trigger_4  Zone-touch bar low violation
    # Uses zone_touch_low_lookback.
    # ------------------------------------------------------------------ #

    # ------------------------------------------------------------------ #
    # trigger_5  Failed retest
    # retest_proximity_atr: how close (in ATR units) high must be to kde_peak.
    # Uses retest_lookback.
    # ------------------------------------------------------------------ #
    retest_proximity_atr: float = 0.5

    # ------------------------------------------------------------------ #
    # trigger_6  RSI below threshold
    # ------------------------------------------------------------------ #
    rsi_period: int = 14
    rsi_threshold: float = 50.0

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
            "bear_strategy/hypothesis_tests/setup_2_trigger_1_check/test_results"
        )
    )
