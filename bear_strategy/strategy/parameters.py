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

    # ── Entry throttle: regime-aware position within each regime window ───────
    # Starting position for entries in each new regime window:
    #   1 = take 1st trigger onwards (accept every trigger)
    #   2 = take 2nd trigger onwards (skip 1st)  ← default, skips crowded entry
    #   3 = take 3rd trigger onwards (skip 1st & 2nd)
    entry_regime_offset: int = 4

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

    # ── EMA-above exit parameters (ema_above) ─────────────────────────────────
    ema_above_period: int = 20

    # ── VWAP exit parameters (vwap_above) ────────────────────────────────────
    # vwap_anchor_hours: size of each VWAP anchor window in hours.
    #   24  = daily-anchored (resets every 24h)
    #   48  = 2-day rolling window
    #   168 = weekly-anchored (resets every 7 days)
    # Larger windows produce a smoother VWAP that lags more but gives fewer
    # false exits; smaller windows are more reactive.
    vwap_anchor_hours: int = 24

    # ── VWMA exit parameters (vwma_above) ─────────────────────────────────────
    # vwma_period: rolling lookback in bars for the volume-weighted MA.
    # Shorter = faster, more responsive; longer = smoother, fewer signals.
    vwma_period: int = 20

    # ── Engulfing candle exit parameters ──────────────────────────────────────
    # engulfing_ratio: current bullish body must be >= ratio × prev bearish body.
    # Values < 1.0 allow partial engulfs; > 1.0 require full+buffer engulf.
    engulfing_ratio: float = 1.0

    # ── Hammer candle exit parameters ─────────────────────────────────────────
    # hammer_wick_ratio: lower wick must be >= ratio × body size.
    # Higher = only strong hammers trigger the exit.
    hammer_wick_ratio: float = 2.0

    # ── Data ─────────────────────────────────────────────────────────────────
    data_dir: str = "crypto_data/data"

    # ── Trigger flags ─────────────────────────────────────────────────────────
    # At least one trigger flag must be True for an entry to fire.
    # New triggers can be added here and wired in backtest/vectorbt/signals.py.
    use_vp_trigger: bool = True   # Session VP POC/HVN break

    # ── Exit flags ────────────────────────────────────────────────────────────
    # At least one exit flag must be True.  Multiple active flags → OR logic:
    # the trade closes on whichever signal fires first.
    # use_fixed_tp=True keeps the ATR-based VBT tp_stop;
    # setting it False zeros tp_pct (indicator-only exit).
    use_fixed_tp:          bool = True   # ATR-based take-profit stop
    use_rsi_exit:          bool = False  # daily RSI crosses above exit_rsi_level
    use_macd_exit:         bool = False  # 1h MACD histogram negative→≥0
    use_rsi_oversold_exit: bool = False  # 1h RSI drops below rsi_oversold_level
    use_ema_reclaim_exit:  bool = False  # 1h close crosses back above EMA
    use_funding_exit:      bool = False  # EMA-smoothed funding drops ≤ threshold
    use_ema_above_exit:    bool = False  # 1h close is above EMA(ema_above_period)
    use_vwap_exit:         bool = False  # 1h close is above anchor-period VWAP
    use_vwma_exit:         bool = False  # 1h close is above VWMA(vwma_period)
    use_engulfing_exit:    bool = False  # bullish engulfing candle on 1h
    use_hammer_exit:       bool = False  # hammer candle on 1h
    use_bb_mean_reversion_exit: bool = False  # Bollinger Bands mean reversion exit
    use_atr_reversal_exit: bool = False  # ATR reversal exit

    # ── Bollinger Bands exit parameters ───────────────────────────────────────
    bb_period: int = 20      # SMA lookback for BB
    bb_num_std: float = 2.0  # Number of standard deviations

    # ── ATR reversal exit parameters ──────────────────────────────────────────
    atr_reversal_mult: float = 1.5  # ATR threshold multiplier for reversal
    atr_reversal_period: int = 14   # ATR period for reversal calculation
    # ── VBT-native trailing stop ──────────────────────────────────────────────
    # Two-step: (1) entry-candle SL replaces the ATR-fraction SL when use_vbt_sl=True.
    #           (2) swing-high ratchet tightens the stop as price falls when
    #               use_vbt_sl_trail=True (requires use_vbt_sl=True).
    #
    # use_vbt_sl=False  → classic ATR-fraction SL from stop_atr_mult (no change)
    # use_vbt_sl=True   → SL set at candle high + sl_n_atr_init × ATR(sl_atr_period)
    # use_vbt_sl_trail=True → above + ratchet via rolling swing_high(sl_swing_lookback)
    use_vbt_sl:       bool  = False   # enable entry-candle SL
    use_vbt_sl_trail: bool  = False   # enable swing-high trailing ratchet
    sl_atr_period:    int   = 14      # ATR period for entry-candle SL
    sl_n_atr_init:    float = 0.5     # ATR buffer above entry candle high
    sl_n_atr_trail:   float = 0.5     # ATR buffer above trailing swing high
    sl_swing_lookback: int  = 10      # rolling window (bars) for swing high

    # ── Regime: 200d EMA below filter (optional, off by default) ────────────────
    # When True, entries are only allowed when the daily close is BELOW the
    # 200-period daily EMA — confirming bearish macro structure.
    use_ema_200_regime: bool = False

    # ── Legacy EMA-based regime fields (hypothesis_tests/ backward compat) ───
    ema_slope_period:   int       = 200
    ema_slope_lookback: int       = 1
    ema_below_periods:  list[int] = field(default_factory=lambda: [50, 100, 150])
