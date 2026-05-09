"""
Session-based Volume Profile trigger: price breaks below session HVN (High Volume Node).

HVN zones are where the most trading happened. Breaking below means overcoming resistance.
"""
from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.trigger.indicators.vp_session_utils import compute_session_volume_profile


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when close breaks below session HVN low."""
    price_bins = int(params.get("price_bins", 50))
    
    vp = compute_session_volume_profile(df, price_bins=price_bins)
    
    hvn_low = vp["hvn_low"]
    prev_close = df["close"].shift(1)
    
    # Only fire if HVN is defined for this session
    hvn_defined = hvn_low.notna()
    
    # Break: cross below HVN low with downside continuation confirmation.
    break_below_hvn = (
        (prev_close >= hvn_low)
        & (df["close"] < hvn_low)
        & (df["close"] < df["close"].shift(1))
    )
    
    return (hvn_defined & break_below_hvn).fillna(False)
