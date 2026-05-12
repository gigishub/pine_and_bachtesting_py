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

    # ── Minimum SL distance filter ────────────────────────────────────────────
    # Skip entries where the stop distance (as a fraction of price) is below
    # this threshold.  Prevents trades where taker fees consume most of the R.
    # e.g. 0.005 = 0.5% — at 0.08% round-trip, that is ~16% of the risk premium.
    min_sl_pct: float = 0.005

    # ── Position sizing ───────────────────────────────────────────────────────
    # Fraction of equity risked per trade (e.g. 0.01 = 1%).
    # Size = risk_pct / sl_pct_fraction so each trade risks exactly risk_pct × equity.
    risk_pct: float = 0.01

    # ── Entry throttling (signal sampling) ───────────────────────────────────
    # Keep every Nth raw trigger. Useful when triggers are too dense.
    # entry_phase selects which hit in each N-sized cycle is tradable (1..N).
    # Examples:
    #   entry_every_n=2, entry_phase=1 -> 1st, 3rd, 5th ... trigger
    #   entry_every_n=2, entry_phase=2 -> 2nd, 4th, 6th ... trigger
    entry_every_n: int = 1
    entry_phase: int = 1

    # ── Exit mode (SL is always active) ──────────────────────────────────────
    # fixed_tp:                    SL + fixed ATR-based take-profit
    # rsi_cross_up:                SL + daily RSI crosses above exit_rsi_level
    # fixed_tp_or_rsi_cross_up:    SL + whichever fires first (TP or RSI cross)
    # macd_hist_cross_zero:        SL + 1h MACD histogram crosses from negative to ≥ 0
    #                              (bearish momentum fading — take profit early)
    # rsi_oversold:                SL + 1h RSI drops below rsi_oversold_level
    #                              (move is exhausted — take profit before bounce)
    # ema_reclaim:                 SL + 1h close crosses back above EMA(exit_ema_period)
    #                              (bearish structure broken — exit now)
    # funding_regime_shift:        SL + EMA-smoothed 8h funding rate drops at or below
    #                              funding_threshold (carry tailwind gone — exit now).
    #                              Keeps fixed TP as a safety net.
    use_exit_rsi: bool = False   # legacy flag; exit_mode alone controls behaviour
    exit_mode: str = "fixed_tp"
    exit_rsi_period: int = 14    # RSI period for rsi_cross_up and rsi_oversold exits
    exit_rsi_level: float = 50.0  # RSI level for rsi_cross_up (daily)
    rsi_oversold_level: float = 30.0  # RSI level for rsi_oversold (1h, below = oversold)

    # ── MACD exit parameters (macd_hist_cross_zero) ───────────────────────────
    macd_fast_period:   int = 12
    macd_slow_period:   int = 26
    macd_signal_period: int = 9

    # ── EMA reclaim exit parameters (ema_reclaim) ─────────────────────────────
    exit_ema_period: int = 21

    # ── Data ─────────────────────────────────────────────────────────────────
    data_dir: str = "crypto_data/data"

    # ── Legacy EMA-based regime fields (hypothesis_tests/ backward compat) ───
    ema_slope_period:   int       = 200
    ema_slope_lookback: int       = 1
    ema_below_periods:  list[int] = field(default_factory=lambda: [50, 100, 150])
