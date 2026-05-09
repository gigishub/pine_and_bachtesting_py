"""Session VP POC/HVN break trigger for the bear strategy.

Fires True when either:
  - The prior session POC failed-reclaim pattern triggers (3-bar: was below,
    retested, then closed back below), or
  - Price crosses below the prior session HVN low with downside confirmation.

This is the exact logic promoted in the OSS test as
bear_rsi_vp_session_poc_or_hvn_break.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.trigger.indicators.vp_session_utils import (
    compute_session_volume_profile,
)


def compute_vp_signal(
    df: pd.DataFrame,
    price_bins: int = 50,
) -> pd.Series:
    """True when the session POC-failed-reclaim or HVN-break pattern fires.

    Args:
        df:         Entry-TF OHLCV DataFrame with 'open', 'high', 'low', 'close'.
        price_bins: Number of price bins for the volume profile histogram.

    Returns:
        Boolean Series on df.index.
    """
    vp = compute_session_volume_profile(df, price_bins=price_bins)

    poc     = vp["poc"]
    hvn_low = vp["hvn_low"]

    prev_close = df["close"].shift(1)
    close_2ago = df["close"].shift(2)

    # POC failed-reclaim (3-bar pattern)
    poc_signal = (
        poc.notna()
        & (close_2ago < poc)
        & (prev_close >= poc)
        & (df["close"] < poc)
    )

    # HVN cross-below with downside confirmation
    hvn_signal = (
        hvn_low.notna()
        & (prev_close >= hvn_low)
        & (df["close"] < hvn_low)
        & (df["close"] < prev_close)
    )

    return (poc_signal | hvn_signal).fillna(False)
