"""Strategy parameters for Adaptive Momentum.

Each layer (Regime / Setup / Trigger / Exit) is controlled by independent
boolean flags.  Enable multiple flags in a layer to AND them together for
entry conditions, or OR them for the exit (first stop hit exits the trade).

Excluded options (require external data unavailable from OHLCV):
  - regime: "mvrv"   — MVRV Z-Score (needs Glassnode on-chain API)
  - trigger: "cvd"   — CVD Breakout  (needs tick-level trade data)
  - setup: "relative_strength" — needs a benchmark OHLCV DataFrame
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Parameters:
    # ------------------------------------------------------------------ #
    # Boolean flag groups
    # At least one flag per group must be True; signals are AND'd within
    # each entry layer.  Exit uses OR (first stop hit).
    # ------------------------------------------------------------------ #

    # Regime layer — all enabled filters must agree (AND)
    use_adx: bool = True          # ADX(14) > threshold          [Option A]
    use_ema_ribbon: bool = False   # EMA(20) > EMA(50) > EMA(200) [Option C]

    # Setup layer — all enabled filters must agree (AND)
    use_donchian: bool = True          # Donchian channel breakout + squeeze [Option A]
    use_volume_profile: bool = False   # Rolling VAH breakout                [Option B]
    # use_relative_strength: excluded — needs benchmark_df

    # Trigger layer — all enabled filters must agree (AND)
    use_cmf: bool = True           # CMF(20) > threshold              [Option A]
    use_power_candle: bool = False  # Close > High(N) + high volume    [Option C]

    # Exit layer — first stop hit exits (OR / max-stop logic)
    use_chandelier: bool = True    # ATR trailing stop (ratcheted)     [Option A]
    use_psar: bool = False         # Parabolic SAR                     [Option B]
    use_bbands: bool = False       # Bollinger Band upper              [Option C]
    use_trailing_stop: bool = False  # btc_momentum-style: rolling_max(low,N)-ATR*mult [Option D]

    # ------------------------------------------------------------------ #
    # Regime A — ADX
    # ------------------------------------------------------------------ #
    adx_period: int = 14
    adx_threshold: float = 25.0

    # ------------------------------------------------------------------ #
    # Regime C — EMA Ribbon
    # ------------------------------------------------------------------ #
    ema_fast: int = 20
    ema_mid: int = 50
    ema_slow: int = 200

    # ------------------------------------------------------------------ #
    # Setup A — Donchian channel breakout + volatility squeeze
    # ------------------------------------------------------------------ #
    donchian_lookback: int = 20         # bars to form the channel
    donchian_tolerance: float = 0.01    # close must be within 1% of upper band
    squeeze_history: int = 240          # bars for percentile ranking (≈10 days at 1h)

    # ------------------------------------------------------------------ #
    # Setup B — Volume Profile VAH
    # ------------------------------------------------------------------ #
    vp_session_bars: int = 24           # bars per session (e.g. 24h at 1h)
    vp_lookback_sessions: int = 3       # sessions to include in the profile
    vp_n_bins: int = 20                 # price bins for the volume histogram
    vp_value_area_pct: float = 0.70     # fraction of volume defining the Value Area
    vp_consecutive_bars: int = 2        # consecutive closes above VAH required

    # ------------------------------------------------------------------ #
    # Setup C — Relative Strength vs benchmark (e.g. BTC)
    # ------------------------------------------------------------------ #
    rs_period: int = 24                 # look-back bars for return comparison
    rs_multiplier: float = 1.5          # token return must exceed bench × this
    rs_ratio_sma_period: int = 20       # SMA period for token/benchmark ratio

    # ------------------------------------------------------------------ #
    # Trigger A — Chaikin Money Flow
    # ------------------------------------------------------------------ #
    cmf_period: int = 20
    cmf_threshold: float = 0.05

    # ------------------------------------------------------------------ #
    # Trigger C — Power Candle
    # ------------------------------------------------------------------ #
    power_candle_lookback: int = 15     # rolling-high lookback (bars)
    power_candle_vol_period: int = 20   # SMA period for baseline volume
    power_candle_vol_mult: float = 1.5  # volume must exceed SMA × this

    # ------------------------------------------------------------------ #
    # Exit A — Chandelier SAR (ratcheted trailing stop)
    # ------------------------------------------------------------------ #
    chandelier_lookback: int = 22
    chandelier_atr_mult: float = 3.0

    # ------------------------------------------------------------------ #
    # Exit B — Parabolic SAR
    # ------------------------------------------------------------------ #
    psar_af_initial: float = 0.02
    psar_af_step: float = 0.02
    psar_af_max: float = 0.20

    # ------------------------------------------------------------------ #
    # Exit C — Bollinger Band upper
    # ------------------------------------------------------------------ #
    bb_period: int = 20
    bb_std: float = 2.0

    # ------------------------------------------------------------------ #
    # Exit D — Simple Trailing Stop (btc_momentum-style)
    # stop = rolling_max(low, N) - ATR(N) × mult
    # Uses the rolling highest LOW as trail source (tighter than Chandelier).
    # Always ratcheted upward (same as chandelier).
    # ------------------------------------------------------------------ #
    trail_lookback: int = 22
    trail_atr_mult: float = 2.0

    # ------------------------------------------------------------------ #
    # Position sizing (shared)
    # ------------------------------------------------------------------ #
    risk_pct: float = 1.0               # % of equity risked per trade

    # ------------------------------------------------------------------ #
    # Direction toggles
    # ------------------------------------------------------------------ #
    use_long:  bool = True    # Enable long entries and exits
    use_short: bool = False   # Enable short entries and exits

    # ------------------------------------------------------------------ #
    # Short Regime layer
    # ADX (use_adx) is shared — non-directional, reused as-is
    # ------------------------------------------------------------------ #
    use_ema_ribbon_short: bool = False  # EMA(20) < EMA(50) < EMA(200) [bearish stacking]

    # ------------------------------------------------------------------ #
    # Short Setup layer
    # ------------------------------------------------------------------ #
    use_donchian_short:       bool = False  # close < Donchian lower band
    use_volume_profile_short: bool = False  # close below Value Area Low (VAL)

    # ------------------------------------------------------------------ #
    # Short Trigger layer
    # ------------------------------------------------------------------ #
    use_cmf_short:          bool = False  # CMF < -threshold (distribution confirmed)
    use_power_candle_short: bool = False  # bearish power candle (close at N-bar low + vol)

    # ------------------------------------------------------------------ #
    # Short Exit layer
    # ------------------------------------------------------------------ #
    use_chandelier_short:     bool = False  # lowest_low(N) + ATR*mult (ratcheted downward)
    use_psar_short:           bool = False  # Parabolic SAR (handles direction internally)
    use_bbands_short:         bool = False  # BB lower band re-entry
    use_trailing_stop_short:  bool = False  # rolling_min(high,N)+ATR*mult (ratcheted downward)

    # ------------------------------------------------------------------ #
    # Short Setup A — Donchian (short-specific lookback, shorter for crash speed)
    # ------------------------------------------------------------------ #
    short_donchian_lookback:   int   = 15    # 10-15 bars recommended for shorts
    short_donchian_tolerance:  float = 0.01  # within 1% of lower band

    # ------------------------------------------------------------------ #
    # Short Trigger A — CMF threshold (absolute; applied as cmf < -this)
    # ------------------------------------------------------------------ #
    short_cmf_threshold: float = 0.05

    # ------------------------------------------------------------------ #
    # Short Exit A — Chandelier short
    # ------------------------------------------------------------------ #
    short_chandelier_lookback:  int   = 22
    short_chandelier_atr_mult:  float = 2.5  # tighter than long 3.0

    # ------------------------------------------------------------------ #
    # VBT-native SL (entry candle + optional swing trailing)
    # use_vbt_sl=True  → entry-candle hard stop is registered with VBT.
    # use_vbt_sl_trail=True → additionally ratchets the stop inward each bar
    #                         using the rolling swing low/high + ATR buffer.
    #                         Requires use_vbt_sl=True to have any effect.
    # ------------------------------------------------------------------ #
    use_vbt_sl: bool = False            # Enable VBT-native entry-candle SL
    use_vbt_sl_trail: bool = False      # Enable swing trailing ratchet on top of SL
    sl_atr_period: int = 14             # ATR lookback for SL computation
    sl_n_atr_init: float = 0.5         # ATR buffer below entry candle low/above high
    sl_n_atr_trail: float = 0.5        # ATR buffer below trailing swing low/above high
    sl_swing_lookback: int = 10        # Bars for rolling swing low/high
