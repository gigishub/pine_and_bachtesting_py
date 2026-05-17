"""Bear Strategy — full combination sweep config.

Full Cartesian product:
  - All exit flags swept on/off in every valid combination
  - SL/TP multiples swept
  - Key exit indicator levels swept

This is the widest search — run it last, after exit_isolation and
exit_value_sweep have identified which indicators are worth combining.
Expect a large grid; consider running on a subset of symbols first.

Run:
    python -m bear_strategy.backtest.vectorbt.run_grid --config full_combo
    python -m bear_strategy.backtest.vectorbt.run_grid --config full_combo --symbols BTCUSDT ETHUSDT
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

from bear_strategy.backtest.vectorbt.configs.default import build_config as _base


def build_config():
    return dataclasses.replace(
        _base(),
        boolean_filter_ranges={
            "use_vp_trigger":        (True,),
            "use_fixed_tp":          (False, True),
            "use_rsi_exit":          (False, True),
            "use_macd_exit":         (False, True),
            "use_rsi_oversold_exit": (False, True),
            "use_ema_reclaim_exit":  (False, True),
            "use_funding_exit":      (False, True),
            "use_vbt_sl":            (False,),
            "use_vbt_sl_trail":      (False,),
        },
        sl_mult_range=(1.5, 2.0, 2.5),
        tp_mult_range=(2.0, 3.0, 4.0),
        exit_rsi_level_range=(45.0, 50.0, 55.0),
        rsi_oversold_level_range=(25.0, 30.0),
        exit_ema_period_range=(14, 21),
        macd_fast_range=(8, 12),
        macd_slow_range=(21, 26),
        output_dir=Path("bear_strategy/backtest/vectorbt/results/full_combo"),
    )
