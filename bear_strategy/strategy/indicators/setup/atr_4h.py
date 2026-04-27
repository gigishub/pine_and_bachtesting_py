"""4H ATR indicator.

Computes ATR(period) on 4H OHLCV data using an EWM approximation consistent
with the rest of the project.  No shift is applied here — the 1-bar shift
that prevents lookahead onto the 15-minute grid is applied once in the
runner's alignment step.
"""

from __future__ import annotations

import pandas as pd


def compute_atr_4h(df_4h: pd.DataFrame, period: int = 14) -> pd.Series:
    """Return ATR(period) on 4H data, unshifted.

    The shift-by-1 guard is applied in the runner before merge_asof so that
    all 4H-derived signals are shifted consistently in one place.

    Args:
        df_4h: 4H OHLCV DataFrame.
        period: ATR lookback period.

    Returns:
        pd.Series of ATR values indexed like df_4h, named ``atr_4h``.
    """
    high = df_4h["High"]
    low = df_4h["Low"]
    prev_close = df_4h["Close"].shift(1)

    tr = pd.concat(
        [high - low, (high - prev_close).abs(), (low - prev_close).abs()],
        axis=1,
    ).max(axis=1)

    return tr.ewm(span=period, adjust=False).mean().rename("atr_4h")
