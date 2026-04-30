"""Configuration for the EMA Cross-Below Setup Edge Check.

Regime filter: ema_below_50 (Step 1 winner).

Hypothesis: within a bear regime, a bar where price crosses below EMA(ema_period)
after having been above it for at least min_bars_above consecutive bars signals
a meaningful momentum shift — one that predicts short continuation.

Setup filters tested against the regime-only baseline:

    ema_cross_below       — close crossed below EMA on this bar
                            (close[t] < EMA[t] AND close[t-1] > EMA[t-1]).
                            Any cross, regardless of how long price was above.

    ema_cross_below_N     — ema_cross_below AND price was above EMA for
                            at least min_bars_above consecutive bars before
                            the cross.
                            The sustained setup: the longer price holds above
                            EMA before breaking, the more significant the break.

Key parameter — min_bars_above:

    Controls how "sustained" the prior move above EMA must be before the
    cross is considered a valid setup.

    Lower TF (15m / 5m) → price can be above EMA for many bars before a
    meaningful break; try min_bars_above = 5–8.

    Mid TF (1h / 4h)    → try min_bars_above = 3–5.

    Higher TF (daily)   → try min_bars_above = 2–3.

    The test compares ema_cross_below vs ema_cross_below_N to show whether
    the sustained qualifier actually adds edge beyond a raw cross.

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
    entry_tf: str = "1h"

    # ------------------------------------------------------------------ #
    # Indicator parameters
    # ------------------------------------------------------------------ #
    ema_period: int = 20        # EMA lookback period

    # Minimum consecutive bars price must be above EMA before the cross.
    # Set to 1 to accept any single bar above before crossing down.
    # Increase for stricter "sustained above" requirement.
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

    # EMA crosses are discrete events — lower floor than always-on filters.
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
            "bear_strategy/backtest/hypothesis_tests_raw/results/step2_ema_cross_check"
        )
    )
