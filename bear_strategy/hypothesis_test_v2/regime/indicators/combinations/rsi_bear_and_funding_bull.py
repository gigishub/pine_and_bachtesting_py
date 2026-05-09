"""
rsi_bear_and_funding_bull — Composite regime indicator.

Combines one 1d RSI bear signal with a bullish funding-rate filter.
The RSI signal is computed on 1d bars and aligned to the entry timeframe,
while the funding signal is evaluated on the entry timeframe itself.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.engine.alignment import align_htf_to_ltf
from bear_strategy.hypothesis_test_v2.engine.data_loader import load_ohlcv
from bear_strategy.hypothesis_test_v2.regime.indicators.funding_rate.funding_rate import (
    signal as funding_signal,
)
from bear_strategy.hypothesis_test_v2.regime.indicators.rsi.rsi_bear_slope_zone import (
    signal as slope_signal,
)
from bear_strategy.hypothesis_test_v2.regime.indicators.rsi.rsi_bear_zone import (
    signal as zone_signal,
)


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Combine a 1d RSI bear regime signal with a bullish funding signal.

    Parameters
    ----------
    df: OHLCV DataFrame for the entry timeframe.
    params: {
        "rsi_type": "zone" or "slope_zone",
        "rsi_period": int,
        "ma_period": int,
        "lower": float,
        "upper": float,
        "funding_threshold": float,
        "funding_ma_period": int,
        "funding_direction": str,
        "_symbol": str,
        "_data_dir": str,
    }
    """
    symbol = str(params["_symbol"])
    data_dir = str(params.get("_data_dir", "crypto_data/data"))

    rsi_type = str(params.get("rsi_type", "zone"))
    rsi_params = {
        "rsi_period": int(params.get("rsi_period", 14)),
        "ma_period": int(params.get("ma_period", 9)),
        "lower": float(params.get("lower", 30)),
        "upper": float(params.get("upper", 50)),
    }
    funding_params = {
        "threshold": float(params.get("funding_threshold", 0.0)),
        "ma_period": int(params.get("funding_ma_period", 1)),
        "direction": str(params.get("funding_direction", "bull")),
        "_symbol": params["_symbol"],
        "_data_dir": params.get("_data_dir", "crypto_data/data"),
    }

    htf_df = load_ohlcv(symbol, "1d", str(df.index[0].date()), str(df.index[-1].date()), data_dir)

    if rsi_type == "zone":
        rsi_signal = zone_signal(htf_df, rsi_params)
    elif rsi_type == "slope_zone":
        rsi_signal = slope_signal(htf_df, rsi_params)
    else:
        raise ValueError(f"Unknown rsi_type: {rsi_type!r}")

    aligned_rsi = align_htf_to_ltf(htf_df, rsi_signal, df, shift=True)
    funding = funding_signal(df, funding_params)

    return (aligned_rsi & funding).fillna(False)
