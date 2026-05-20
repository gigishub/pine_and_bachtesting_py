"""Bear Strategy — entry throttle position sweep config.

Tests which trigger position within each regime window produces the best results.

Parameters swept:
  - entry_regime_offset: 1 / 2 / 3 / 4
    1 = take all triggers (no filtering)
    2 = skip 1st, take 2nd+ (default, avoids crowded entry zones)
    3 = skip 1st & 2nd, take 3rd+
    4 = skip first 3, take 4th+

Run:
    python -m bear_strategy.backtest.vectorbt.run_grid --config throttle_offset_sweep
    python -m bear_strategy.backtest.vectorbt.run_grid --config throttle_offset_sweep --symbols BTCUSDT ETHUSDT
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
            # Keep exits minimal to isolate throttle effect
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
            "use_bb_mean_reversion_exit": (False,),
            "use_atr_reversal_exit": (False,),
            "use_vbt_sl":            (False,),
            "use_vbt_sl_trail":      (False,),
        },
        # Throttle position sweep
        entry_regime_offset_range=(3,4,5),
        vp_price_bins_range=(10,25,50,),           # VP resolution sweep
        # Pinned SL/TP to isolate throttle effect
        sl_mult_range=(2.0,),
        tp_mult_range=(3.0,),
        output_dir=Path("bear_strategy/backtest/vectorbt/results/throttle_offset_sweep_2"),
    )
