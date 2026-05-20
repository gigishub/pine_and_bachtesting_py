"""Bear Strategy — IS sweep with 200d EMA regime filter.

Adds a third regime condition: daily close must be below the 200-period
daily EMA (bearish macro structure) before any entry fires.

Sweeps:
    stop_atr_mult   : 1.0 / 1.5 / 2.0 / 2.5 / 3.0 / 3.5 / 4.0 / 5.0
    target_atr_mult : 1.0 / 1.5 / 2.0 / 2.5 / 3.0 / 3.5 / 4.0 / 5.0

Exits pinned:
    use_fixed_tp = True   (ATR-based take-profit — the only exit)
    all other exits = False

Regime:
    RSI bear zone (1d)     — always on
    Funding bull guard     — always on
    Price < EMA(200) 1d    — enabled via use_ema_200_regime = True

Symbols: all 22 pairs with sufficient data history
Period:  2021-01-01 → 2023-11-01  (in-sample)
         NaN bars before 200d EMA warms up are handled by fillna(False)
         in the regime filter — those bars simply produce no entries.

Run:
    python -m bear_strategy.backtest.vectorbt.run_grid --config is_ema200
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
        start_date="2021-01-01",
        end_date="2023-11-01",
        boolean_filter_ranges={
            # Regime flag — pinned ON to activate the 200d EMA filter
            "use_ema_200_regime":          (True,),
            # Trigger
            "use_vp_trigger":              (True,),
            # Exits: fixed TP only, everything else off
            "use_fixed_tp":                (True,),
            "use_rsi_exit":                (False,),
            "use_macd_exit":               (False,),
            "use_rsi_oversold_exit":       (False,),
            "use_ema_reclaim_exit":        (False,),
            "use_funding_exit":            (False,),
            "use_ema_above_exit":          (False,),
            "use_vwap_exit":               (False,),
            "use_vwma_exit":               (False,),
            "use_engulfing_exit":          (False,),
            "use_hammer_exit":             (False,),
            "use_bb_mean_reversion_exit":  (False,),
            "use_atr_reversal_exit":       (False,),
            "use_vbt_sl":                  (False,),
            "use_vbt_sl_trail":            (False,),
        },
        # sl_mult_range=(1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0),
        # tp_mult_range=(1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0),
        sl_mult_range=(2.0,3.0),
        tp_mult_range=(5.0,6.0),
        output_dir=Path("bear_strategy/backtest/vectorbt/results/is_ema200"),
    )
