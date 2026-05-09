"""
Rolling fixed-range Volume Profile trigger: price drops into rolling LVN zone.

LVN (Low Volume Node) is thin-air in the profile — price typically accelerates
through it.  Entering from above is a bear continuation signal.
LVN is computed from the prior `window` bars (no look-ahead).
"""
from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.trigger.indicators.volume_profile_utils import compute_volume_profile


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """True when price drops into the rolling LVN zone from above."""
    window     = int(params.get("window", 168))
    price_bins = int(params.get("price_bins", 50))

    vp = compute_volume_profile(df, window=window, price_bins=price_bins)

    lvn_high   = vp["lvn_high"]
    lvn_low    = vp["lvn_low"]
    prev_close = df["close"].shift(1)

    lvn_defined  = lvn_high.notna() & lvn_low.notna()
    was_above    = prev_close > lvn_high
    # Enter AT the LVN zone — not far below it (allow 0.5% slippage through zone)
    entered_zone = (df["close"] <= lvn_high) & (df["close"] >= lvn_low * 0.995)

    return (lvn_defined & was_above & entered_zone).fillna(False)
