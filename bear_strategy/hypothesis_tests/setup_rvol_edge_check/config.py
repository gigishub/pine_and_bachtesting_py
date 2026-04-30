"""Configuration for the RVOL Setup Edge Check.

Regime filter: ema_below_50 (Step 1 winner).

Setup filter: Relative Volume spike — current bar volume is ≥ rvol_threshold
  times its own rolling average over the last vol_ma_len bars.

Three populations are tested as bear setup conditions:

    rvol_spike         — RVOL ≥ threshold for min_bars_active consecutive bars.
                         Tests whether raw volume participation adds edge.

    rvol_spike_bearish — rvol_spike + bearish candle (close < open).
                         Tests whether high-volume bearish candles confirm short.

    rvol_spike_down    — rvol_spike + price declined (close < prev close).
                         Tests whether high-volume price decline confirms short.

Key parameter — min_bars_active:
    1 (default)  → single spike bar qualifies.  Good for 4h / daily.
    2            → two consecutive spike bars required.  Better for 1h.
    3            → three consecutive spike bars required.  Better for 15m / 5m.

    On lower timeframes a one-bar spike can be noise.  Requiring N consecutive
    bars above the threshold filters out brief bursts that reverse immediately.

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
    # RVOL parameters
    # ------------------------------------------------------------------ #
    vol_ma_len: int = 20            # rolling window for average volume
    rvol_threshold: float = 1.2    # spike when volume / avg >= this value

    # How many consecutive bars must satisfy the threshold.
    # Set to 1 for a single-bar spike (higher TF).
    # Set to 2–3 on lower TF to filter noise.
    min_bars_active: int = 1

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

    # RVOL spikes cover roughly 20–30% of bars on crypto (more volatile than
    # equities), so 0.20 is a realistic floor.
    min_coverage_ratio: float = 0.20

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
            "bear_strategy/backtest/hypothesis_tests_raw/results/step2_rvol_check"
        )
    )
