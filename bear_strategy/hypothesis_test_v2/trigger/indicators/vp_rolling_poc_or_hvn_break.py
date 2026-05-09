"""
Rolling fixed-range Volume Profile trigger: OR of POC-failed-reclaim and HVN break.

VP is computed once from the prior `window` bars and both conditions evaluated,
so there is no redundant computation.
"""
from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.trigger.indicators.volume_profile_utils import compute_volume_profile


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """True when either the rolling POC-failed-reclaim or HVN-break fires."""
    window     = int(params.get("window", 168))
    price_bins = int(params.get("price_bins", 50))

    vp = compute_volume_profile(df, window=window, price_bins=price_bins)

    poc     = vp["poc"]
    hvn_low = vp["hvn_low"]

    prev_close = df["close"].shift(1)
    close_2ago = df["close"].shift(2)

    # ── Rolling POC failed-reclaim ─────────────────────────────────────────────
    poc_defined    = poc.notna()
    was_below_poc  = close_2ago < poc
    retested_poc   = prev_close >= poc
    failed_reclaim = df["close"] < poc
    poc_signal = poc_defined & was_below_poc & retested_poc & failed_reclaim

    # ── Rolling HVN cross-below ────────────────────────────────────────────────
    hvn_defined = hvn_low.notna()
    break_hvn   = (prev_close >= hvn_low) & (df["close"] < hvn_low) & (df["close"] < prev_close)
    hvn_signal  = hvn_defined & break_hvn

    return (poc_signal | hvn_signal).fillna(False)
