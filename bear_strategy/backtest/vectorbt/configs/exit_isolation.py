"""Bear Strategy — exit isolation config.

Tests each exit indicator in isolation (exit_exclusive=True), so exactly one
exit is active per combo.  Use this to rank exit indicators individually before
combining them.

Exits swept (4 conditions):
  use_fixed_tp          ATR-based hard take-profit
  use_rsi_exit          Daily RSI crosses above exit level
  use_rsi_oversold_exit 1h RSI drops below oversold level
  use_vbt_sl_trail      Swing-high trailing SL ratchet

Run:
    python -m bear_strategy.backtest.vectorbt.run_grid --config exit_isolation
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
            # Sweep these 4 exit conditions — all combinations are valid
            # because the hard SL always closes the trade as a backstop.
            "use_fixed_tp":          (False, True),
            "use_rsi_exit":          (False, True),
            "use_macd_exit":         (False,),
            "use_rsi_oversold_exit": (False, True),
            "use_ema_reclaim_exit":  (False,),
            "use_funding_exit":      (False,),
            "use_ema_above_exit":    (False, True),
            "use_vwap_exit":         (False, True),
            "use_vwma_exit":         (False, True),
            "use_engulfing_exit":    (False, True),
            "use_hammer_exit":       (False, True),
            "use_bb_mean_reversion_exit": (False, True),
            "use_atr_reversal_exit": (False, True),
            "use_vbt_sl":            (False,),
            "use_vbt_sl_trail":      (False, True),
        },
        sl_mult_range=(1.5, 2.0, 2.5),
        exit_exclusive=False,
        output_dir=Path("bear_strategy/backtest/vectorbt/results/exit_isolation_3"),
    )
