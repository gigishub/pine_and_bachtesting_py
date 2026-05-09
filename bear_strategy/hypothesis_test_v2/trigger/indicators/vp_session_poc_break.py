"""
Session-based Volume Profile trigger: price breaks below the daily session POC.

POC (Point of Control) is the price level with highest volume in the session.
Breaking below it means sellers have overcome the most-traded level.
"""
from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.trigger.indicators.vp_session_utils import compute_session_volume_profile


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when price fails to reclaim session POC from below."""
    price_bins = int(params.get("price_bins", 50))
    
    vp = compute_session_volume_profile(df, price_bins=price_bins)
    
    poc = vp["poc"]
    prev_close = df["close"].shift(1)
    
    # Only fire if POC is defined for this session
    poc_defined = poc.notna()
    
    # Failed reclaim event:
    # 1) two bars ago was below POC,
    # 2) previous bar retested/rose to at-or-above POC,
    # 3) current bar closes back below POC.
    close_2ago = df["close"].shift(2)
    was_below = close_2ago < poc
    retested = prev_close >= poc
    failed_reclaim = df["close"] < poc

    return (poc_defined & was_below & retested & failed_reclaim).fillna(False)
