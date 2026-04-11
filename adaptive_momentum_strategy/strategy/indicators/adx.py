"""ADX regime filter.

Average Directional Index (Wilder, 1978).
Quantifies trend strength on a 0–100 scale.  A rising ADX above 25 indicates
the market is in a directional phase; momentum strategies achieve their best
Sharpe ratios under this condition.  Keeping ADX below threshold means we sit
out choppy, range-bound markets where trend-following incurs 'death by a
thousand cuts'.
"""

from __future__ import annotations

import pandas as pd
import pandas_ta as pta


def compute_adx(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int = 14,
) -> pd.Series:
    """Return the ADX series (0–100, higher = stronger trend).

    Args:
        period: Smoothing window.  14 is Wilder's original default; range 10–21.

    Returns:
        Float Series aligned to the input index.  NaN for the first `period`
        bars while the indicator warms up.
    """
    adx_df = pta.adx(high, low, close, length=period)
    col = f"ADX_{period}"
    if adx_df is None or col not in adx_df.columns:
        return pd.Series(float("nan"), index=close.index, dtype=float)
    return adx_df[col].astype(float)


def regime_is_trending(adx: pd.Series, threshold: float = 25.0) -> pd.Series:
    """Return boolean Series: True when ADX > threshold (market is trending)."""
    return (adx > threshold).fillna(False)
