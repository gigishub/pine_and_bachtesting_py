"""Bear Strategy — VP trigger tuning with new exits config.

Sweeps VP trigger parameters alongside the 6 new exit indicators.
Tests whether different VP configurations work better with specific exits.

Parameters swept:
  - vp_price_bins:               50 / 75 / 100       (VP resolution)
  - use_fixed_tp:                off / on             (new exits alone vs. + hard TP)
  - use_ema_above_exit:          off / on
  - use_vwap_exit:               off / on
  - use_vwma_exit:               off / on
  - use_engulfing_exit:          off / on
  - use_hammer_exit:             off / on
  - use_bb_mean_reversion_exit:  off / on
  - use_atr_reversal_exit:       off / on
  - entry_regime_offset:         1 / 2 / 3 / 4       (throttle position)
  - ema_above_period:            14 / 20 / 34
  - vwap_anchor_hours:           24 / 48 / 168       (daily / 2-day / weekly)
  - vwma_period:                 10 / 20 / 34 / 55   (short / med / long / slow)
  - engulfing_ratio:             0.8 / 1.0 / 1.2
  - hammer_wick_ratio:           1.5 / 2.0 / 3.0
  - bb_period:                   15 / 20 / 30
  - bb_num_std:                  1.5 / 2.0 / 2.5
  - atr_reversal_mult:           1.2 / 1.5 / 2.0
  - atr_reversal_period:         10 / 14 / 20

Run:
    python -m bear_strategy.backtest.vectorbt.run_grid --config vp_with_new_exits
    python -m bear_strategy.backtest.vectorbt.run_grid --config vp_with_new_exits --symbols BTCUSDT ETHUSDT
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
            # Old exits — swept to test new exits with/without hard TP
            "use_fixed_tp":          (False, True),   # sweep: new exits alone vs. + hard TP
            "use_rsi_exit":          (False,),        # pinned off
            "use_macd_exit":         (False,),        # pinned off
            "use_rsi_oversold_exit": (False,),        # pinned off
            "use_ema_reclaim_exit":  (False,),        # pinned off
            "use_funding_exit":      (False,),        # pinned off
            # New exits — sweep on/off
            "use_ema_above_exit":    (False, True),
            "use_vwap_exit":         (False, True),
            "use_vwma_exit":         (False, True),
            "use_engulfing_exit":    (False, True),
            "use_hammer_exit":       (False, True),
            "use_bb_mean_reversion_exit": (False, True),
            "use_atr_reversal_exit": (False, True),
            "use_vbt_sl":            (False,),
            "use_vbt_sl_trail":      (False,),
        },
        # Numeric sweeps: VP trigger + new exit params
        entry_regime_offset_range=(1, 2, 3, 4),
        vp_price_bins_range=(50, 75, 100),           # VP resolution sweep
        ema_above_period_range=(14, 20, 34),
        vwap_anchor_hours_range=(24, 48, 168),       # daily / 2-day / weekly
        vwma_period_range=(10, 20, 34, 55),          # short / medium / long / slow
        engulfing_ratio_range=(0.8, 1.0, 1.2),
        hammer_wick_ratio_range=(1.5, 2.0, 3.0),
        bb_period_range=(15, 20, 30),                # SMA lookback for BB
        bb_num_std_range=(1.5, 2.0, 2.5),            # num of std devs
        atr_reversal_mult_range=(1.2, 1.5, 2.0),     # ATR threshold multiplier
        atr_reversal_period_range=(10, 14, 20),      # ATR period
        # Pinned SL/TP (use new_exits_sweep config to vary these)
        sl_mult_range=(2.0,),
        tp_mult_range=(3.0,),
        output_dir=Path("bear_strategy/backtest/vectorbt/results/vp_with_new_exits"),
    )
