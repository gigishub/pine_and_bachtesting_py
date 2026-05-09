"""
close_below_ema_200_and_ema_dual_slope_down_50_200 — Composite bear regime indicator.

Combines close below EMA(200) with dual EMA slope down (50/200).
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.regime.indicators.ema.close_below_ema import signal as ema_signal
from bear_strategy.hypothesis_test_v2.regime.indicators.ema.ema_dual_slope_down import signal as dual_slope_signal


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    ema_params = {"period": int(params.get("ema_period", 200))}
    slope_params = {
        "fast_period": int(params.get("fast_period", 50)),
        "slow_period": int(params.get("slow_period", 200)),
    }

    return ema_signal(df, ema_params) & dual_slope_signal(df, slope_params)
