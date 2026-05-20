"""Bear Strategy — OOS test for combo #1: stop_atr_mult=2, target_atr_mult=5.

In-sample period : 2021-01-01 → 2023-11-01  (sl_sweep config)
Out-of-sample    : 2023-11-01 → 2026-04-22  (this config)

Symbols passing IS gates (6 of 9):
    ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT

Pinned exactly as the IS winner:
    use_vp_trigger = True  (only trigger)
    use_fixed_tp   = True  (only exit)
    stop_atr_mult  = 2.0
    target_atr_mult = 5.0
    All other flags = False

Run:
    python -m bear_strategy.backtest.vectorbt.run_grid --config oos_sl2_tp5
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

from bear_strategy.backtest.vectorbt.configs.default import build_config as _base


def build_config():
    return dataclasses.replace(
        _base(),
        symbols=['AAVEUSDT', 'ADAUSDT', 'ALGOUSDT', 'ATOMUSDT', 'AVAXUSDT', 'BATUSDT', 'BCHUSDT', 'BNBUSDT', 'DOGEUSDT', 'DOTUSDT', 'XLMUSDT', 'XRPUSDT']
,
        start_date="2023-11-01",
        end_date="2026-04-22",
        boolean_filter_ranges={
            "use_ema_200_regime":          (False,),  
            "use_vp_trigger":             (True,),
            "use_fixed_tp":               (True,),
            "use_rsi_exit":               (False,),
            "use_macd_exit":              (False,),
            "use_rsi_oversold_exit":      (False,),
            "use_ema_reclaim_exit":       (False,),
            "use_funding_exit":           (False,),
            "use_ema_above_exit":         (False,),
            "use_vwap_exit":              (False,),
            "use_vwma_exit":              (False,),
            "use_engulfing_exit":         (False,),
            "use_hammer_exit":            (False,),
            "use_bb_mean_reversion_exit": (False,),
            "use_atr_reversal_exit":      (False,),
            "use_vbt_sl":                 (False,),
            "use_vbt_sl_trail":           (False,),
        },
        sl_mult_range=(3.0,),
        tp_mult_range=(6.0,),
        output_dir=Path("bear_strategy/backtest/vectorbt/results/oos_sl3_tp6"),
    )
