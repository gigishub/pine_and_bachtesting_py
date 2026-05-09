"""Strategy parameters for the Bear Strategy.

All tunable values live here. No logic.
These match the validated configuration from hypothesis_test_v2/oss_test/config.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Parameters:
    # ── Regime: RSI bear zone (computed on 1d bars) ───────────────────────────
    rsi_period:    int   = 14
    rsi_ma_period: int   = 9
    rsi_lower:     float = 30.0
    rsi_upper:     float = 50.0

    # ── Regime: Funding rate bull guard (computed on entry TF from 8h data) ───
    # True when EMA-smoothed funding > threshold → market is paying longs.
    # Combined with RSI bear zone this guards against shorting into extreme
    # positive funding where shorts pay longs (adverse carry).
    funding_threshold:  float = 0.0
    funding_ma_period:  int   = 3

    # ── Trigger: Session Volume Profile POC / HVN break (entry TF) ───────────
    vp_price_bins: int = 50

    # ── Risk: ATR-based stop and target ──────────────────────────────────────
    atr_period:      int   = 7
    stop_atr_mult:   float = 2.0
    target_atr_mult: float = 3.0

    # ── Data ─────────────────────────────────────────────────────────────────
    data_dir: str = "crypto_data/data"

    # ── Legacy EMA-based regime fields (hypothesis_tests/ backward compat) ───
    ema_slope_period:   int       = 200
    ema_slope_lookback: int       = 1
    ema_below_periods:  list[int] = field(default_factory=lambda: [50, 100, 150])
