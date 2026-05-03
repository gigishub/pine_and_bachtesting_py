"""Configuration for Setup 2 – Trigger 8: rsi_ma_below_50 as reinforced baseline.

Baseline (two-layer): regime AND kde_upper AND rsi_ma < rsi_ma_threshold.

rsi_ma_below_50 was confirmed in Trigger 4 (avg PF 1.969, 3/5 pairs).
It is promoted here as a permanent gate before testing any additional condition.

Seven simple held-state conditions tested on top:

    rsi_below_50
        RSI(rsi_period) < rsi_threshold.
        Price momentum on the bearish side of centre.

    mfi_below_50
        MFI(mfi_period) < mfi_threshold.
        Volume-weighted momentum confirms distribution.

    rsi_and_mfi
        RSI < rsi_threshold AND MFI < mfi_threshold simultaneously.
        Dual-indicator confluence.

    close_below_ema
        Close < EMA(ema_slow).
        Price sits below the slow trend average — macro bearish structure.

    ema_bearish_order
        EMA(ema_fast) < EMA(ema_slow).
        Fast average below slow — uptrend has structurally reversed.

    macd_signal_wall
        MACD line < 0 AND MACD line < signal line.
        Both bearish macro position and cross-confirmed momentum.

    lower_bb_declining
        Lower Bollinger Band < lower_bb[1].
        The price floor is actively falling — directional bearish expansion.
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
    # RSI MA — baked into the new baseline
    # rsi_period      : RSI lookback
    # rsi_ma_period   : MA applied to the RSI series
    # rsi_ma_type     : "ema" or "sma"
    # rsi_ma_threshold: baseline gate (RSI_MA must stay below this)
    # ------------------------------------------------------------------ #
    rsi_period: int = 14
    rsi_ma_period: int = 5
    rsi_ma_type: str = "ema"
    rsi_ma_threshold: float = 50.0

    # ------------------------------------------------------------------ #
    # RSI / MFI positional filters (conditions 1–3)
    # ------------------------------------------------------------------ #
    rsi_threshold: float = 50.0
    mfi_period: int = 14
    mfi_threshold: float = 50.0

    # ------------------------------------------------------------------ #
    # EMA parameters (conditions 4–5)
    # ------------------------------------------------------------------ #
    ema_fast: int = 9
    ema_slow: int = 20

    # ------------------------------------------------------------------ #
    # MACD parameters (condition 6)
    # ------------------------------------------------------------------ #
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9

    # ------------------------------------------------------------------ #
    # Bollinger Band parameters (condition 7)
    # ------------------------------------------------------------------ #
    bb_period: int = 20
    bb_std: float = 2.0

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
            "bear_strategy/hypothesis_tests/setup_2_trigger_8_check/test_results"
        )
    )
