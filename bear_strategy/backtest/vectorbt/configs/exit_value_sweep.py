"""Bear Strategy — exit value sweep config.

All exit indicators are swept on/off in combination while also sweeping the
numeric params that control each exit indicator level plus SL/TP multiples.

Use this after exit_isolation to explore whether tuning the thresholds improves
the best single exits, and whether any combinations add edge.

Run:
    python -m bear_strategy.backtest.vectorbt.run_grid --config exit_value_sweep
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
        # Stop / target multiples
        sl_mult_range=(1.5, 2.0, 2.5),
        tp_mult_range=(2.0, 3.0, 4.0),
        # Exit indicator numeric params
        exit_rsi_level_range=(45.0, 50.0, 55.0),
        rsi_oversold_level_range=(25.0, 30.0, 35.0),
        exit_ema_period_range=(14, 21, 34),
        macd_fast_range=(8, 12),
        macd_slow_range=(21, 26),
        output_dir=Path("bear_strategy/backtest/vectorbt/results/exit_value_sweep"),
    )
