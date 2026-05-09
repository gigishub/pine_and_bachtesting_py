"""
Session-based Volume Profile trigger: OR combination of POC break and HVN break.

Fires when either:
  - Price fails to reclaim the session POC (3-bar pattern), OR
  - Price crosses below the session HVN low with downside confirmation.

Computing the VP once and evaluating both conditions avoids double computation.
"""
from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.trigger.indicators.vp_session_utils import compute_session_volume_profile


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """True when either the POC-failed-reclaim or HVN-break condition is met."""
    price_bins = int(params.get("price_bins", 50))

    vp = compute_session_volume_profile(df, price_bins=price_bins)

    poc     = vp["poc"]
    hvn_low = vp["hvn_low"]

    prev_close  = df["close"].shift(1)
    close_2ago  = df["close"].shift(2)

    # ── POC failed-reclaim (3-bar pattern) ────────────────────────────────────
    poc_defined     = poc.notna()
    was_below_poc   = close_2ago < poc
    retested_poc    = prev_close >= poc
    failed_reclaim  = df["close"] < poc
    poc_signal = poc_defined & was_below_poc & retested_poc & failed_reclaim

    # ── HVN cross-below ────────────────────────────────────────────────────────
    hvn_defined    = hvn_low.notna()
    break_hvn      = (prev_close >= hvn_low) & (df["close"] < hvn_low) & (df["close"] < prev_close)
    hvn_signal     = hvn_defined & break_hvn

    return (poc_signal | hvn_signal).fillna(False)
