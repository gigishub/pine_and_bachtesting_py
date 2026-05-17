"""Bear Strategy — entry trigger throttle config.

Tests whether acting only on every Nth entry signal (default: 2nd) improves
performance by skipping signals in the middle of crowded zones.

Parameters swept:
  - entry_every_n: 1 (every signal) vs 2 (every 2nd signal)
  - entry_phase:   1 (1st, 3rd, 5th…) vs 2 (2nd, 4th, 6th…)
    Varying phase shows whether the 1st or 2nd occurrence is more reliable.

Exits are kept at the default (only use_fixed_tp pinned on) to isolate the
entry throttle effect cleanly.

Run:
    python -m bear_strategy.backtest.vectorbt.run_grid --config trigger_throttle
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

from bear_strategy.backtest.vectorbt.configs.default import build_config as _base


def build_config():
    return dataclasses.replace(
        _base(),
        # ===== BOOLEAN FLAGS: trigger + exit on/off toggles =====
        boolean_filter_ranges={
            # TRIGGER
            "use_vp_trigger":        (True,),
            
            # EXITS
            "use_fixed_tp":          (False,),        # Fixed take profit (off)
            "use_rsi_exit":          (False,),        # RSI-based exit (off)
            # "use_rsi_exit":        (False, True),   # Uncomment to sweep: off vs on
            "use_macd_exit":         (False,),        # MACD exit signal (off)
            # "use_macd_exit":       (False, True),   # Uncomment to sweep: off vs on
            "use_rsi_oversold_exit": (False,),        # RSI oversold exit (off)
            # "use_rsi_oversold_exit": (False, True), # Uncomment to sweep: off vs on
            "use_ema_reclaim_exit":  (False,),        # EMA reclaim exit (off)
            # "use_ema_reclaim_exit": (False, True),  # Uncomment to sweep: off vs on
            "use_funding_exit":      (False,),        # Funding rate exit (off)
            # "use_funding_exit":    (False, True),   # Uncomment to sweep: off vs on
            
            # VBT-NATIVE STOP LOSS (only used when True)
            "use_vbt_sl":            (False, True),      # Fixed VBT stop loss (off)
            # "use_vbt_sl":          (False, True),   # Uncomment to sweep: off vs on
            "use_vbt_sl_trail":      (False, True),   # VBT trailing stop (off)
            # "use_vbt_sl_trail":    (False, True),   # Uncomment to sweep: off vs on
        },
        
        # ===== NUMERIC SWEEPS: Stop / Target =====
        # When use_vbt_sl=False (currently): these multipliers define stop & target
        # When use_vbt_sl=True: ignore these; use sl_n_atr_init_range instead
        sl_mult_range=(2.0, 2.5, 3.0),               # Stop loss = ATR × this value
        # tp_mult_range=(2.0, 3.0, 4.0),               # Take profit = ATR × this value
        # atr_period_range=(7,),                     # ATR lookback period (currently 7)
        
        # ===== EXIT INDICATOR NUMERIC PARAMS (only active when respective exit is on) =====
        # exit_rsi_level_range=(50.0,),              # RSI threshold for RSI exit (currently off)
        # rsi_oversold_level_range=(30.0,),          # RSI threshold for oversold exit (currently off)
        # exit_ema_period_range=(21,),               # EMA period for EMA reclaim (currently off)
        # macd_fast_range=(12,),                     # MACD fast period (currently off)
        # macd_slow_range=(26,),                     # MACD slow period (currently off)
        
        # ===== REGIME NUMERIC PARAMS (always active) =====
        # rsi_lower_range=(30.0,),                   # RSI bear zone lower bound (currently 30)
        # rsi_upper_range=(50.0,),                   # RSI bear zone upper bound (currently 50)
        # funding_threshold_range=(0.0,),            # Funding threshold for bull guard (currently 0)
        
        # ===== VBT TRAILING STOP PARAMS (only active when use_vbt_sl=True) =====
        # IMPORTANT: These are ONLY used when use_vbt_sl=True.
        # Currently use_vbt_sl=(False,), so sl_n_atr_init/trail are IGNORED.
        # sl_n_atr_init_range=(1, 1.5),              # Initial ATR width for VBT stop (inactive now)
        # sl_n_atr_trail_range=(1, 1.5, 2),          # Trailing ATR width for VBT stop (inactive now)
        # sl_swing_lookback_range=(10,),             # Lookback for swing stop (inactive now)
        
        # ===== ENTRY THROTTLE: skip every Nth signal =====
        # Core sweep: 1st-vs-2nd signal
        entry_every_n_range=(1, 2),                  # 1=every signal, 2=every 2nd signal
        # entry_phase_range=(1, 2),                    # 1=odd signals, 2=even signals
        
        # ===== OUTPUT =====
        output_dir=Path("bear_strategy/backtest/vectorbt/results/trigger_throttle"),
    )
