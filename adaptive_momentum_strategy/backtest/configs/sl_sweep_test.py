"""SL Sweep Test — smoke test for the VBT-native entry-candle + trailing SL.

Purpose
-------
Validate that use_vbt_sl=True runs end-to-end without errors across multiple
timeframes and coins, and that the SL numeric params (sl_n_atr_init,
sl_n_atr_trail, sl_swing_lookback) produce meaningfully different results.

Scope
-----
- 3 symbols  × 2 timeframes = 6 conditions
- 6-month date range (fast fetch, enough trades for stats)
- Indicators pinned to a single minimal combo:
    Regime  : ADX on
    Setup   : Donchian on
    Trigger : CMF on
    Exit    : Chandelier on (precomputed exit kept active alongside VBT SL)
- Grid: use_vbt_sl swept (False/True), plus 3×3×3 SL numeric values
    use_vbt_sl=False: 1 combo (SL params collapse via feature_dependencies)
    use_vbt_sl=True : 3 × 3 × 3 = 27 combos
    Total: 28 unique combos per condition → 168 total runs

What to look for
----------------
- Zero errors in the log (all 168 combos complete).
- use_vbt_sl=True combos have higher Sharpe / lower max_dd than use_vbt_sl=False
  (hard stops cut the tail losses).
- Smaller sl_n_atr_init / sl_n_atr_trail values produce fewer trades and
  higher win-rate (tighter stops shake out more noise).
- Results are consistent across BTCUSDT, ETHUSDT, SOLUSDT and across 1h/4h.

Usage
-----
    source .venv/bin/activate
    python -m adaptive_momentum_strategy.backtest.vectorbt.run --config sl_sweep_test
"""

from __future__ import annotations

from pathlib import Path

from adaptive_momentum_strategy.backtest.config import MomentumGridConfig


def build_config(output_dir: Path | None = None) -> MomentumGridConfig:
    return MomentumGridConfig(
        source="bybit",
        market_type="linear",
        symbols=["BTCUSDT", "ETHUSDT", "SOLUSDT"],
        timeframes=["1h", "4h"],
        start_time="2024-01-01 00:00:00",
        end_time="2024-07-01 00:00:00",
        boolean_filter_ranges={
            # ── Regime: ADX only (pinned on for a consistent signal)
            "use_adx":            (True,),
            "use_ema_ribbon":     (False,),
            # ── Setup: Donchian only
            "use_donchian":       (True,),
            "use_volume_profile": (False,),
            # ── Trigger: CMF only
            "use_cmf":            (True,),
            "use_power_candle":   (False,),
            # ── Exit: Chandelier pinned on (precomputed fallback always active)
            "use_chandelier":     (True,),
            "use_psar":           (False,),
            "use_bbands":         (False,),
            "use_trailing_stop":  (False,),
            # ── VBT-native SL: sweep off vs on
            "use_vbt_sl":         (False, True),
            # ── Trailing ratchet: sweep off vs on (deduplicated when use_vbt_sl=False)
            "use_vbt_sl_trail":   (False, True),
            # ── Short flags: all pinned off (long-only test)
            "use_ema_ribbon_short":     (False,),
            "use_donchian_short":       (False,),
            "use_volume_profile_short": (False,),
            "use_cmf_short":            (False,),
            "use_power_candle_short":   (False,),
            "use_chandelier_short":     (False,),
            "use_psar_short":           (False,),
            "use_bbands_short":         (False,),
            "use_trailing_stop_short":  (False,),
        },
        # ── SL numeric sweep (deduplicated when use_vbt_sl=False)
        sl_n_atr_init_range=(0.25, 0.5, 1.0),
        sl_n_atr_trail_range=(0.25, 0.5, 1.0),
        sl_swing_lookback_range=(5, 10, 20),
        # ── All other numeric params pinned at baseline
        adx_threshold_range=(25.0,),
        chandelier_atr_mult_range=(3.0,),
        cmf_threshold_range=(0.05,),
        trail_atr_mult_range=(2.0,),
        ema_fast_range=(20,),
        ema_mid_range=(50,),
        ema_slow_range=(200,),
        # ── Direction
        enable_long=True,
        enable_short=False,
        # ── No exclusive mode — single combo per indicator layer anyway
        regime_exclusive=False,
        setup_exclusive=False,
        trigger_exclusive=False,
        exit_exclusive=False,
        # ── Execution
        initial_cash=10_000.0,
        fees=0.001,
        n_jobs=-1,
        min_bars=300,
        # ── Output
        output_dir=output_dir or Path(
            "adaptive_momentum_strategy/backtest/results/results_vbt"
        ),
        consistency_top_n=10,
        save_trade_logs=True,
        trade_logs_top_n=5,
    )
