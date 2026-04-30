"""Configuration for the VWAP Cross-Below Setup Edge Check.

Regime filter: ema_below_50 (Step 1 winner).

Hypothesis: within a bear regime, a bar where price crosses below VWAP
after holding above it for at least min_bars_above consecutive bars
signals a meaningful session-level momentum shift.

Setup filters tested against the regime-only baseline:

    vwap_cross_below       — close crossed below VWAP on this bar
                             (close[t] < VWAP[t] AND close[t-1] > VWAP[t-1]).

    vwap_cross_below_N     — vwap_cross_below AND price was above VWAP for
                             at least min_bars_above consecutive bars before.

Key parameter — min_bars_above:

    Identical logic to the EMA cross test.  VWAP resets each session, so
    "sustained above VWAP" within a session means the session started with
    buyers in control before the sell-off took over.

    1h  data → try min_bars_above = 2–4
    15m data → try min_bars_above = 4–8
    4h  data → try min_bars_above = 1–2

VWAP anchor options (vwap_anchor):

    "daily"   → resets UTC midnight  ← default
    "weekly"  → resets Monday 00:00 UTC
    "monthly" → resets 1st of each month

Edit fields directly in this file to change timeframe or parameters.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestConfig:
    # ------------------------------------------------------------------ #
    # Timeframe
    # ------------------------------------------------------------------ #
    entry_tf: str = "1h"

    # ------------------------------------------------------------------ #
    # VWAP parameters
    # ------------------------------------------------------------------ #
    vwap_anchor: str = "daily"      # "daily" | "weekly" | "monthly"

    # ------------------------------------------------------------------ #
    # Sustained-above qualifier
    # ------------------------------------------------------------------ #
    min_bars_above: int = 3         # consecutive bars above VWAP before cross

    # ------------------------------------------------------------------ #
    # Exit parameters
    # ------------------------------------------------------------------ #
    stop_atr_mult: float = 2.0
    target_atr_mult: float = 3.0
    atr_period: int = 7

    # ------------------------------------------------------------------ #
    # Regime
    # ------------------------------------------------------------------ #
    regime_col: str = "ema_below_50_regime"
    ema_slope_period: int = 200
    ema_slope_lookback: int = 1
    ema_below_periods: list[int] = field(default_factory=lambda: [50])

    # ------------------------------------------------------------------ #
    # Falsification thresholds
    # ------------------------------------------------------------------ #
    significance_zscore: float = 2.5
    min_pf_diff_high_n: float = 0.02
    min_pf_diff_mid_n: float = 0.05
    min_pf_diff_low_n: float = 0.10
    min_trades_per_pair: int = 500
    min_pairs_passing: int = 4

    # VWAP crosses are discrete events.
    min_coverage_ratio: float = 0.05

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
            "bear_strategy/backtest/hypothesis_tests_raw/results/step2_vwap_cross_check"
        )
    )
