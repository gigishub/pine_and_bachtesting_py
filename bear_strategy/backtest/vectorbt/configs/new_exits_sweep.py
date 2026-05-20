"""Bear Strategy — new exit indicators sweep config.

Tests the 4 newly-added exits in isolation and combination:
  use_ema_above_exit    — 1h close above EMA(n)
  use_vwap_exit         — 1h close above daily-anchored VWAP
  use_engulfing_exit    — bullish engulfing candle
  use_hammer_exit       — hammer candle

The old exits are pinned OFF to focus cleanly on the new ones.
use_fixed_tp is ON as a baseline closing condition (SL always active).

Run:
    python -m bear_strategy.backtest.vectorbt.run_grid --config new_exits_sweep
    python -m bear_strategy.backtest.vectorbt.run_grid --config new_exits_sweep --symbols BTCUSDT ETHUSDT
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

from bear_strategy.backtest.vectorbt.configs.default import build_config as _base


def build_config():
    return dataclasses.replace(
        _base(),
        boolean_filter_ranges={
            "use_ema_200_regime":          (False,),  # pinned OFF — not part of this config
            "use_vp_trigger":        (True,),
            # New exits — all combinations tested
            "use_fixed_tp":          (True,False,),         # baseline hard TP
            "use_rsi_exit":          (False,),        # pinned off
            "use_macd_exit":         (False,),        # pinned off
            "use_rsi_oversold_exit": (False,),        # pinned off
            "use_ema_reclaim_exit":  (False,),        # pinned off
            "use_funding_exit":      (False,),        # pinned off
            # New exits — sweep on/off
            "use_ema_above_exit":    (False, True),
            "use_vwap_exit":         (False, True),
            "use_engulfing_exit":    (False, True),
            "use_hammer_exit":       (False, True),
            "use_vbt_sl":            (False,),
            "use_vbt_sl_trail":      (False,),
        },
        # Numeric sweeps for new exits
        ema_above_period_range=(10,14, 20, 34),
        engulfing_ratio_range=(0.8, 1.0, 1.2),
        hammer_wick_ratio_range=(1.5, 2.0, 3.0),
        # Vary SL/TP to ensure the exits work across different risk profiles
        sl_mult_range=(1.5, 2.0, 2.5),
        tp_mult_range=(2.0, 3.0, 4.0),
        output_dir=Path("bear_strategy/backtest/vectorbt/results/new_exits_sweep"),
    )
