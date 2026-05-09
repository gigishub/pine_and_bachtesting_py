"""
Rolling fixed-range Volume Profile trigger: price breaks below rolling HVN low.

HVN is computed from the prior `window` bars.  With a 168-bar rolling window the
high-volume node is a meaningful established support level — breaking it signals
sellers have overcome real structural resistance.
"""
from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.trigger.indicators.volume_profile_utils import compute_volume_profile


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """True when close breaks below the rolling HVN low with downside confirmation."""
    window     = int(params.get("window", 168))
    price_bins = int(params.get("price_bins", 50))

    vp = compute_volume_profile(df, window=window, price_bins=price_bins)

    hvn_low    = vp["hvn_low"]
    prev_close = df["close"].shift(1)

    hvn_defined  = hvn_low.notna()
    break_below  = (
        (prev_close >= hvn_low)
        & (df["close"] < hvn_low)
        & (df["close"] < prev_close)   # downside confirmation
    )

    return (hvn_defined & break_below).fillna(False)
