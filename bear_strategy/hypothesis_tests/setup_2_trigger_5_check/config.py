"""Configuration for Setup 2 – Trigger 5: Bollinger Band + Keltner Channel signals.

Baseline: regime AND kde_upper (4h KDE open > peak), promoted from Setup 1.

Tests six advanced volatility and expansion signals based on Bollinger Bands
and Keltner Channel structures.

Entry TF  : configurable (default 1h — change to test 15m / 4h etc.)
KDE TF    : 4h  (structural gate)

Signals tested:

    momentum_close
        Close finishes below the lower Bollinger Band.
        Logic: Confirms price acceptance at lower levels (not just a wick).

    falling_tunnel
        Both lower and upper BB move downward together.
        Lower_Band < Lower_Band[1] AND Upper_Band < Upper_Band[1].
        Logic: Entire price structure shifting lower — dominant selling.

    volatility_velocity
        BB width expansion rate exceeds rolling average.
        (BB_Width - BB_Width[1]) > Average_Width_Delta.
        Logic: Detects "panic" or "climax" high-momentum breakouts.

    squeeze_snap
        BB width is at 20-bar low, then lower band moves down.
        Identifies contraction-then-expansion volatility coiling.

    lower_expansion
        Lower band falls below prior bar's level.
        Lower_Band < Lower_Band[1].
        Logic: Broadest trigger — floor is dropping out.

    keltner_squeeze_release
        Lower BB drops below lower Keltner Channel.
        Compares std-dev (BB) vs ATR (Keltner) — statistically extraordinary.
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
    # Bollinger Band parameters
    # bb_period: SMA/std lookback
    # bb_std: standard deviations for band width
    # ------------------------------------------------------------------ #
    bb_period: int = 20
    bb_std: float = 2.0

    # ------------------------------------------------------------------ #
    # Keltner Channel parameters
    # kc_period: ATR lookback
    # kc_atr_mult: ATR multiplier for channel width
    # ------------------------------------------------------------------ #
    kc_period: int = 20
    kc_atr_mult: float = 2.0

    # ------------------------------------------------------------------ #
    # volatility_velocity parameters
    # vol_vel_lookback: rolling average of BB width delta
    # ------------------------------------------------------------------ #
    vol_vel_lookback: int = 20

    # ------------------------------------------------------------------ #
    # squeeze_snap parameters
    # squeeze_lookback: lookback for BB width minimum
    # ------------------------------------------------------------------ #
    squeeze_lookback: int = 20

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
            "bear_strategy/hypothesis_tests/setup_2_trigger_5_check/test_results"
        )
    )
