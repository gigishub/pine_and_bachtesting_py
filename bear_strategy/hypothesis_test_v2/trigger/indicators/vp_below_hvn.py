"""
Volume Profile trigger: price breaks below HVN (High Volume Node).

Signals that sellers have overcome an established support zone.
"""
from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.trigger.indicators.volume_profile_utils import compute_volume_profile


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when close breaks below the HVN low level."""
    window = int(params.get("window", 168))
    price_bins = int(params.get("price_bins", 100))
    
    vp = compute_volume_profile(df, window=window, price_bins=price_bins)
    
    hvn_low = vp["hvn_low"]
    prev_close = df["close"].shift(1)
    
    # Only fire if HVN zone is defined
    hvn_defined = hvn_low.notna()
    
    # Break below HVN: price was at or above, now closes below
    break_below_hvn = (prev_close >= hvn_low) & (df["close"] < hvn_low)
    
    return (hvn_defined & break_below_hvn).fillna(False)
