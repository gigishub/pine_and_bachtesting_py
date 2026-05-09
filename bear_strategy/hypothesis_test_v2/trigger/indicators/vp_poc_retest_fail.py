"""
Volume Profile trigger: price fails to reclaim POC from below.

POC is a magnet but also resistance once broken. Failed retest = continuation signal.
"""
from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.trigger.indicators.volume_profile_utils import compute_volume_profile


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when price fails a retest of POC from below."""
    window = int(params.get("window", 168))
    price_bins = int(params.get("price_bins", 100))
    
    vp = compute_volume_profile(df, window=window, price_bins=price_bins)
    
    poc = vp["poc"]
    prev_poc = poc.shift(1)
    prev_close = df["close"].shift(1)
    
    # Only fire if POC is defined
    poc_defined = poc.notna()
    
    # Simple: price was below POC, now also closes below (no reclaim)
    # This catches the pattern where price dips to POC but can't break above
    below_poc_now = df["close"] < poc
    tested_poc = (prev_close >= poc) & (prev_close <= poc * 1.005)  # came within 0.5% of POC
    
    return (poc_defined & tested_poc & below_poc_now).fillna(False)
