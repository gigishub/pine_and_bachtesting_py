"""
Session-based Volume Profile trigger: price enters session LVN (Low Volume Node).

LVN zones are thin air — minimal trading occurred here. Price moves through them fast.
Entering an LVN from above signals potential acceleration downward.
"""
from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.trigger.indicators.vp_session_utils import compute_session_volume_profile


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when price drops into the session LVN from above.

    Entry logic:
    - Previous bar was above the LVN zone top (lvn_high)
    - Current bar drops into or through the LVN zone (close <= lvn_high)
    - Close is not far below lvn_low — want entries AT the LVN, not after it
      (allow close >= lvn_low * 0.995 to catch bars that slice through the zone)
    """
    price_bins = int(params.get("price_bins", 50))

    vp = compute_session_volume_profile(df, price_bins=price_bins)

    lvn_high = vp["lvn_high"]
    lvn_low = vp["lvn_low"]
    prev_close = df["close"].shift(1)

    lvn_defined = lvn_high.notna() & lvn_low.notna()

    was_above = prev_close > lvn_high
    entered_zone = (df["close"] <= lvn_high) & (df["close"] >= lvn_low * 0.995)

    return (lvn_defined & was_above & entered_zone).fillna(False)
