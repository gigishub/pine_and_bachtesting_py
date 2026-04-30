"""Configuration for the EMA Cross-Below Setup Edge Check.

Regime filter: ema_below_50 (Step 1 winner).

Setup filters tested against the regime-only baseline:

    ema_cross_below           — close < EMA(ema_period) on this bar AND
                                close was above EMA on the previous bar.
                                Any downward EMA cross, regardless of how
                                long price was above before.

    ema_cross_below_sustained — same cross, but price must have been above
                                EMA for at least min_bars_above consecutive
                                bars immediately before crossing.
                                The idea: a longer consolidation above EMA
                                builds more energy for the breakdown.

─── Why this matters ────────────────────────────────────────────────────────

Simply being below EMA20 is a continuous condition — in a bear regime most
bars will satisfy it.  The EMA cross captures the specific moment of
breakdown: the first bar that closes below EMA after sustained time above.

This has two interpretations:

1.  Bear regime pullback ended — price rallied back above EMA, then failed.
    The cross-below marks the failure of the counter-trend bounce.

2.  Momentum shift — the sustained-above requirement filters for genuine
    rallies (not just one bounce bar), making the breakdown more meaningful.

─── Tuning min_bars_above by timeframe ──────────────────────────────────────

    4h / daily   →  min_bars_above = 3–5  (3 bars = 12–20 hours of rally)
    1h           →  min_bars_above = 4–8  (4 bars = 4 hours of rally)
    15m          →  min_bars_above = 8–16 (8 bars = 2 hours of rally)

Edit fields directly in this file to change timeframe or parameters.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestConfig:
    # ------------------------------------------------------------------ #
    # Timeframe — single-TF, no context_tf needed.
    # ------------------------------------------------------------------ #
    entry_tf: str = "15m"

    # ------------------------------------------------------------------ #
    # EMA parameters
    # ------------------------------------------------------------------ #
    ema_period: int = 20    # EMA lookback period

    # Minimum consecutive bars that must have been above EMA immediately
    # before the cross.  Set higher on lower timeframes to filter noise.
    min_bars_above: int = 3

    # ------------------------------------------------------------------ #
    # Exit parameters
    # ------------------------------------------------------------------ #
    stop_atr_mult: float = 2.0
    target_atr_mult: float = 3.0
    atr_period: int = 7

    # ------------------------------------------------------------------ #
    # Regime — fixed to Step 1 winner (ema_below_50)
    # ------------------------------------------------------------------ #
    regime_col: str = "ema_below_50_regime"
    ema_slope_period: int = 200
    ema_slope_lookback: int = 1
    ema_below_periods: list[int] = field(default_factory=lambda: [50])

    # ------------------------------------------------------------------ #
    # Falsification thresholds
    # ------------------------------------------------------------------ #
    significance_zscore: float = 2.5
    min_pf_diff_high_n: float = 0.02    # n > 50 000
    min_pf_diff_mid_n: float = 0.05     # 10 000 ≤ n ≤ 50 000
    min_pf_diff_low_n: float = 0.10     # n < 10 000
    min_trades_per_pair: int = 500
    min_pairs_passing: int = 4          # ≥ 4 of 5 pairs

    # EMA crosses are discrete events — expect fewer bars than continuous filters.
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
            "bear_strategy/backtest/hypothesis_tests_raw/results/step2_ema_cross_below_check"
        )
    )
