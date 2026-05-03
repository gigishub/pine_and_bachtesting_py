"""Configuration for Setup 2 – Trigger 4: positional filters (condition-based, not crossovers).

Baseline: regime AND kde_upper (4h KDE open > peak), promoted from Setup 1.

Tests six conditions held while True (not just on crossover). These are
positional filters — they qualify trades only when momentum structure is
bearish, NOT when momentum flips.

Entry TF  : configurable (default 1h — change to test 15m / 4h etc.)
KDE TF    : 4h  (structural gate)

Signals tested:

    rsi_below_50
        RSI(period) < rsi_threshold (default 50).
        Held state: RSI remains below 50 while baseline is active.
        Logic: Bulls have lost control; trade only when RSI is on bearish side.

    mfi_below_50
        MFI(period) < mfi_threshold (default 50).
        Held state: MFI remains below 50 while baseline is active.
        Logic: Smart money (volume-weighted) is distributing; prevents low-volume traps.

    rsi_ma_below_50
        RSI's moving average (EMA/SMA) < rsi_ma_threshold (default 50).
        Held state: RSI's trend (not just momentary dip) is bearish.
        Logic: Double-check that the average momentum over recent bars is bearish.

    rsi_and_mfi
        Both RSI(period) < rsi_threshold AND MFI(period) < mfi_threshold.
        Held state: Both price momentum AND volume momentum are bearish simultaneously.
        Logic: Confluence — double-confirmation that smart money + price are aligned.

    rsi_ma_declining
        RSI's MA < RSI's MA[1] — moving average slope declining.
        Logic: Momentum is not just low, but turning worse (accelerating downward).

    mfi_ma_declining
        MFI's MA < MFI's MA[1] — moving average slope declining.
        Logic: Volume-weighted momentum is not just low, but turning worse.
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
    # rsi_below_50  — RSI positional filter
    # rsi_period: RSI lookback
    # rsi_threshold: level below which RSI qualifies trades (default 50)
    # ------------------------------------------------------------------ #
    rsi_period: int = 14
    rsi_threshold: float = 40

    # ------------------------------------------------------------------ #
    # mfi_below_50  — MFI positional filter
    # mfi_period   : MFI lookback
    # mfi_threshold: level below which MFI qualifies trades (default 50)
    # ------------------------------------------------------------------ #
    mfi_period: int = 14
    mfi_threshold: float = 40

    # ------------------------------------------------------------------ #
    # rsi_ma_below_50  — RSI moving average positional filter
    # rsi_ma_period : MA lookback applied to the RSI series
    # rsi_ma_type   : "ema" or "sma"
    # rsi_ma_threshold: level below which RSI_MA qualifies (default 50)
    # ------------------------------------------------------------------ #
    rsi_ma_period: int = 5
    rsi_ma_type: str = "ema"
    rsi_ma_threshold: float = 40

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
            "bear_strategy/hypothesis_tests/setup_2_trigger_4_check/test_results"
        )
    )
