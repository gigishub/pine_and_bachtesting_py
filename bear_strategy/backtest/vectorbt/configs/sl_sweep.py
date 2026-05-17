"""Bear Strategy — VBT trailing stop sweep config.

Isolates the effect of the entry-candle SL and optional swing-high trailing
ratchet.  Sweeps:
  - use_vbt_sl: off (classic ATR-fraction SL) vs on (entry-candle SL)
  - use_vbt_sl_trail: off vs on  (meaningful only when use_vbt_sl=True; invalid
    combos are filtered by pipeline.py)
  - sl_n_atr_init: ATR buffer above entry-candle high
  - sl_n_atr_trail: ATR buffer above trailing swing high
  - sl_swing_lookback: rolling window for swing-high ratchet

All exits are pinned off to isolate SL mechanics from exit logic.
use_fixed_tp is on so there is always a closing condition.

Run:
    python -m bear_strategy.backtest.vectorbt.run_grid --config sl_sweep
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

from bear_strategy.backtest.vectorbt.configs.default import build_config as _base


def build_config():
    return dataclasses.replace(
        _base(),
        boolean_filter_ranges={
            "use_vp_trigger":        (False,),
            "use_fixed_tp":          (False,),    # always on — need some close condition
            "use_rsi_exit":          (False,),
            "use_macd_exit":         (False,),
            "use_rsi_oversold_exit": (False,),
            "use_ema_reclaim_exit":  (False,),
            "use_funding_exit":      (False,),
            "use_vbt_sl":            (False, True),   # key sweep
            "use_vbt_sl_trail":      (False, True),   # key sweep
        },
        sl_mult_range=(2.0,),          # baseline SL (used when use_vbt_sl=False)
        tp_mult_range=(3.0,),
        sl_n_atr_init_range=(0.3, 0.5, 0.8),
        sl_n_atr_trail_range=(0.3, 0.5, 0.8),
        sl_swing_lookback_range=(5, 10, 20),
        output_dir=Path("bear_strategy/backtest/vectorbt/results/sl_sweep"),
    )
