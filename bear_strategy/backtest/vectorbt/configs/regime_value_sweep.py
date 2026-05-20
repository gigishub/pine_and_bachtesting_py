"""Bear Strategy — regime value sweep config.

Sweeps the numeric thresholds of the two always-active regime filters:
  - RSI bear zone: rsi_lower + rsi_upper on the daily RSI
  - Funding bull guard: funding_threshold on the EMA-smoothed 8h funding rate

Exit flags are all pinned off except use_fixed_tp (the simple baseline exit)
so regime sensitivity is isolated from exit-indicator noise.

Run:
    python -m bear_strategy.backtest.vectorbt.run_grid --config regime_value_sweep
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
            "use_fixed_tp":          (True,),   # simple exit to isolate regime signal
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
            "use_bb_mean_reversion_exit": (False,),
            "use_atr_reversal_exit": (False,),
            "use_vbt_sl":            (False,),
            "use_vbt_sl_trail":      (False,),
        },
        # Regime numeric sweeps
        rsi_lower_range=(25.0, 30.0, 35.0),
        rsi_upper_range=(45.0, 50.0, 55.0),
        funding_threshold_range=(-0.0001, 0.0, 0.0001),
        # Vary SL/TP to ensure regime sweep isn't confounded by stop placement
        sl_mult_range=(1.5, 2.0, 2.5),
        tp_mult_range=(2.0, 3.0, 4.0),
        output_dir=Path("bear_strategy/backtest/vectorbt/results/regime_value_sweep"),
    )
