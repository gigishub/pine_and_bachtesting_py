"""
rsi_bear_slope_zone_and_close_below_ema — Composite bear regime indicator.

Combines RSI bear slope zone with close below EMA. Both signals must be true on
the same timeframe.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.regime.indicators.rsi.rsi_bear_slope_zone import signal as rsi_signal
from bear_strategy.hypothesis_test_v2.regime.indicators.ema.close_below_ema import signal as ema_signal


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    rsi_params = {
        "rsi_period": int(params.get("rsi_period", 14)),
        "ma_period": int(params.get("ma_period", 9)),
        "lower": float(params.get("lower", 30)),
        "upper": float(params.get("upper", 50)),
    }
    ema_params = {"period": int(params.get("ema_period", 200))}

    return rsi_signal(df, rsi_params) & ema_signal(df, ema_params)
