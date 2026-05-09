"""
rsi_bear_zone_or_slope_1d_and_close_below_ema_100_200 — Composite bear regime indicator.

Each RSI condition is paired separately with EMA bearish structure confirmation.
The signal is True when any of the following is true:
    - rsi_bear_zone_1d AND close below EMA 100
    - rsi_bear_slope_zone_1d AND close below EMA 100
    - rsi_bear_zone_1d AND close below EMA 200
    - rsi_bear_slope_zone_1d AND close below EMA 200
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.regime.indicators.rsi.rsi_bear_zone import signal as zone_signal
from bear_strategy.hypothesis_test_v2.regime.indicators.rsi.rsi_bear_slope_zone import signal as slope_signal
from bear_strategy.hypothesis_test_v2.regime.indicators.ema.close_below_ema import signal as ema_signal


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    rsi_params = {
        "rsi_period": int(params.get("rsi_period", 14)),
        "ma_period": int(params.get("ma_period", 9)),
        "lower": float(params.get("lower", 30)),
        "upper": float(params.get("upper", 50)),
    }
    ema_100_params = {"period": int(params.get("ema_period_100", 100))}
    ema_200_params = {"period": int(params.get("ema_period_200", 200))}

    zone = zone_signal(df, rsi_params)
    slope = slope_signal(df, rsi_params)
    ema_100 = ema_signal(df, ema_100_params)
    ema_200 = ema_signal(df, ema_200_params)

    zone_and_100 = zone & ema_100
    slope_and_100 = slope & ema_100
    zone_and_200 = zone & ema_200
    slope_and_200 = slope & ema_200

    return (zone_and_100 | slope_and_100 | zone_and_200 | slope_and_200)
