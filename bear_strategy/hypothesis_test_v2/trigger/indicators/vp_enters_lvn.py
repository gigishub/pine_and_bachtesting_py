"""
Volume Profile trigger: price enters LVN (Low Volume Node) from above.

LVN is thin air — price accelerates through it. Entry signal for acceleration phase.
"""
from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.trigger.indicators.volume_profile_utils import compute_volume_profile


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when close enters a thin volume zone from above."""
    window = int(params.get("window", 168))
    price_bins = int(params.get("price_bins", 100))
    
    vp = compute_volume_profile(df, window=window, price_bins=price_bins)
    
    lvn_high = vp["lvn_high"]
    lvn_low = vp["lvn_low"]
    prev_close = df["close"].shift(1)
    
    # Only fire if LVN zone is defined (not NaN)
    lvn_defined = lvn_high.notna() & lvn_low.notna()
    
    # Enter LVN from above: was above LVN, now inside or below
    in_lvn_now = (df["close"] >= lvn_low) & (df["close"] <= lvn_high)
    was_above = prev_close > lvn_high
    
    return (lvn_defined & in_lvn_now & was_above).fillna(False)
