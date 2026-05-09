"""
Rolling fixed-range Volume Profile trigger: price fails to reclaim rolling POC.

POC is computed from the prior `window` bars (no look-ahead).  Unlike the session VP
(6 bars on 4h), a 168-bar rolling window covers ~28 days on 4h — a much richer,
more stable profile that changes slowly and captures real market structure.
"""
from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.trigger.indicators.volume_profile_utils import compute_volume_profile


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """True when price fails a retest of the rolling POC (3-bar pattern)."""
    window     = int(params.get("window", 168))
    price_bins = int(params.get("price_bins", 50))

    vp = compute_volume_profile(df, window=window, price_bins=price_bins)

    poc        = vp["poc"]
    prev_close = df["close"].shift(1)
    close_2ago = df["close"].shift(2)

    poc_defined    = poc.notna()
    was_below_poc  = close_2ago < poc
    retested_poc   = prev_close >= poc
    failed_reclaim = df["close"] < poc

    return (poc_defined & was_below_poc & retested_poc & failed_reclaim).fillna(False)
