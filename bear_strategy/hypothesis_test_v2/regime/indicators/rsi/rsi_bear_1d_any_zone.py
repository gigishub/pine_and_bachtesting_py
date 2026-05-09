"""
rsi_bear_1d_any_zone — Composite bear regime indicator.

Combines the three 1d RSI bear signals with OR logic. The composite is True
when any 1d RSI bearish zone condition is satisfied.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.regime.indicators.rsi.rsi_bear_zone import signal as zone_signal
from bear_strategy.hypothesis_test_v2.regime.indicators.rsi.rsi_bear_slope_zone import signal as slope_signal
from bear_strategy.hypothesis_test_v2.regime.indicators.rsi.rsi_bear_momentum_zone import signal as momentum_signal


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    rsi_params = {
        "rsi_period": int(params.get("rsi_period", 14)),
        "ma_period": int(params.get("ma_period", 9)),
        "lower": float(params.get("lower", 30)),
        "upper": float(params.get("upper", 50)),
    }

    return (
        zone_signal(df, rsi_params)
        | slope_signal(df, rsi_params)
        | momentum_signal(df, rsi_params)
    )
