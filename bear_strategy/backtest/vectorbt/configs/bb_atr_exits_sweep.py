"""Bear Strategy — BB & ATR exits sweep config.

Focused testing of the two newest exit indicators:
  use_bb_mean_reversion_exit  — Bollinger Bands mean reversion
  use_atr_reversal_exit       — ATR reversal (volatility compression)

Sweeps their numeric parameters extensively to find optimal configurations.
All older exits are pinned OFF to isolate signal quality.

Parameters swept:
  - bb_period:           15 / 20 / 25 / 30      (SMA lookback for BB)
  - bb_num_std:          1.2 / 1.5 / 2.0 / 2.5  (num of standard deviations)
  - atr_reversal_mult:   1.0 / 1.2 / 1.5 / 2.0  (ATR threshold multiplier)
  - atr_reversal_period: 10 / 14 / 20 / 28      (ATR period)
  - use_bb_mean_reversion_exit: off / on
  - use_atr_reversal_exit:      off / on
  - SL/TP:               varied to test across risk profiles

Run:
    python -m bear_strategy.backtest.vectorbt.run_grid --config bb_atr_exits_sweep
    python -m bear_strategy.backtest.vectorbt.run_grid --config bb_atr_exits_sweep --symbols BTCUSDT ETHUSDT
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
            # Old exits — all pinned off
            "use_fixed_tp":          (True,),          # baseline hard TP
            "use_rsi_exit":          (False,),
            "use_macd_exit":         (False,),
            "use_rsi_oversold_exit": (False,),
            "use_ema_reclaim_exit":  (False,),
            "use_funding_exit":      (False,),
            # Earlier new exits — pinned off
            "use_ema_above_exit":    (False,),
            "use_vwap_exit":         (False,),
            "use_vwma_exit":         (False,),
            "use_engulfing_exit":    (False,),
            "use_hammer_exit":       (False,),
            # New BB & ATR exits — swept
            "use_bb_mean_reversion_exit": (False, True),
            "use_atr_reversal_exit": (False, True),
            "use_vbt_sl":            (False,),
            "use_vbt_sl_trail":      (False,),
        },
        # Numeric sweeps: BB & ATR parameters extensively tested
        bb_period_range=(15, 20, 25, 30),             # SMA lookback for BB
        bb_num_std_range=(1.2, 1.5, 2.0, 2.5),        # num of std devs
        atr_reversal_mult_range=(1.0, 1.2, 1.5, 2.0), # ATR threshold multiplier
        atr_reversal_period_range=(10, 14, 20, 28),   # ATR period
        # Vary SL/TP to ensure the exits work across different risk profiles
        # sl_mult_range=(2.0),
        # tp_mult_range=(3.0 ),
        output_dir=Path("bear_strategy/backtest/vectorbt/results/bb_atr_exits_sweep"),
    )
