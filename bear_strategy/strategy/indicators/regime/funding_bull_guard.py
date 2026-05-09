"""Funding-rate bull guard for the bear strategy.

True when the EMA-smoothed funding rate is **above** the threshold, meaning
longs are paying shorts (bullish funding). Combined with a bearish RSI regime
this prevents entering shorts during periods where funding is negative or
absent — i.e. where carrying a short costs nothing (adverse carry scenario).

Lookahead note
--------------
Funding is settled at each 8h mark and already known at that timestamp.
We shift(1) so each entry bar only sees the *previously settled* rate.
"""

from __future__ import annotations

import pandas as pd


def _align_funding(funding_df: pd.DataFrame, target_index: pd.DatetimeIndex) -> pd.Series:
    """Forward-fill the 8-hour funding series onto *target_index*."""
    rate = funding_df["fundingrate"].copy()
    fund_idx = pd.to_datetime(rate.index)
    fund_idx = fund_idx.tz_localize("UTC") if fund_idx.tz is None else fund_idx.tz_convert("UTC")
    rate.index = fund_idx

    tgt_utc = target_index.tz_localize("UTC") if target_index.tz is None else target_index.tz_convert("UTC")

    combined = rate.reindex(rate.index.union(tgt_utc)).ffill()
    result = combined.reindex(tgt_utc)
    result.index = target_index
    return result


def compute_funding_bull_guard(
    df_entry: pd.DataFrame,
    funding_df: pd.DataFrame,
    threshold: float = 0.0,
    ma_period: int = 3,
) -> pd.Series:
    """True when EMA-smoothed (settled) funding rate > threshold.

    Args:
        df_entry:    Entry-timeframe OHLCV DataFrame (provides timestamp index).
        funding_df:  Funding rate DataFrame with a 'fundingrate' column.
        threshold:   Minimum funding rate for signal to be True.
        ma_period:   EMA smoothing span applied to the funding series.

    Returns:
        Boolean Series on df_entry.index.
    """
    rate = _align_funding(funding_df, df_entry.index)

    if ma_period > 1:
        rate = rate.ewm(span=ma_period, adjust=False).mean()

    # shift(1): use the previously settled funding rate — no lookahead.
    settled = rate.shift(1)
    return (settled > threshold).fillna(False)
