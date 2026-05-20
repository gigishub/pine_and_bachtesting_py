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

_ALL_SYMBOLS = [
    "AAVEUSDT", "ADAUSDT",  "ALGOUSDT", "ATOMUSDT", "AVAXUSDT",
    "BATUSDT",  "BCHUSDT",  "BNBUSDT",  "BTCUSDT",  "DOGEUSDT",
    "DOTUSDT",  "ETHUSDT",  "LINKUSDT", "LTCUSDT",  "NEARUSDT",
    "SOLUSDT",  "TRXUSDT",  "UNIUSDT",  "XLMUSDT",  "XMRUSDT",
    "XRPUSDT",  "ZECUSDT",
]

def build_config():
    return dataclasses.replace(
        _base(),
        symbols=_ALL_SYMBOLS,
        boolean_filter_ranges={
            "use_ema_200_regime":          (False,),  # pinned OFF — not part of this config
            "use_vp_trigger":        (True,),     # pinned on — required for entries
            "use_fixed_tp":          (True,),     
            "use_rsi_exit":          (False,),
            "use_macd_exit":         (False,),
            "use_rsi_oversold_exit": (False,),
            "use_ema_reclaim_exit":  (False,),
            "use_funding_exit":      (False,),
            "use_ema_above_exit":    (False,),
            "use_vwap_exit":         (False,),
            "use_vwma_exit":         (False,),
            "use_engulfing_exit":    (False,),
            "use_hammer_exit":       (False,),
            "use_vbt_sl":            (False, ),   
            "use_vbt_sl_trail":      (False, ),   
            "use_bb_mean_reversion_exit": (False, ),
            "use_atr_reversal_exit": (False, ),
        },
        sl_mult_range=(2,3,5),          # baseline SL (used when use_vbt_sl=False)
        tp_mult_range=(5,6),
        # sl_n_atr_init_range=(2,3,4,5),
        # sl_n_atr_trail_range=( 3,4,5),
        # sl_swing_lookback_range=(7),
        output_dir=Path("bear_strategy/backtest/vectorbt/results/sl_sweep2"),
    )
