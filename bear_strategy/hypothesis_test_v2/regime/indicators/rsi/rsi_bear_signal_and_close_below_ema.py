"""
rsi_bear_signal_and_close_below_ema — Composite bear regime indicator.

Combines one 1d RSI bear signal with a close-below-EMA condition.
Each idea using this module runs a single RSI condition paired with one EMA period.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.regime.indicators.rsi.rsi_bear_zone import signal as zone_signal
from bear_strategy.hypothesis_test_v2.regime.indicators.rsi.rsi_bear_slope_zone import signal as slope_signal
from bear_strategy.hypothesis_test_v2.regime.indicators.ema.close_below_ema import signal as ema_signal


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    rsi_type = str(params.get("rsi_type", "zone"))
    rsi_params = {
        "rsi_period": int(params.get("rsi_period", 14)),
        "ma_period": int(params.get("ma_period", 9)),
        "lower": float(params.get("lower", 30)),
        "upper": float(params.get("upper", 50)),
    }
    ema_params = {"period": int(params.get("ema_period", 200))}

    if rsi_type == "zone":
        rsi_signal = zone_signal(df, rsi_params)
    elif rsi_type == "slope_zone":
        rsi_signal = slope_signal(df, rsi_params)
    else:
        raise ValueError(f"Unknown rsi_type: {rsi_type!r}")

    return (rsi_signal & ema_signal(df, ema_params))
