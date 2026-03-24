"""ATR primitives for the UPS strategy.

Pure pandas functions — no side effects.
"""

from __future__ import annotations

import pandas as pd


def ind_rma(series: pd.Series, length: int) -> pd.Series:
    """Pine-compatible RMA smoothing (used by ta.atr)."""
    return series.ewm(alpha=1.0 / float(length), adjust=False, min_periods=length).mean()


def ind_atr(high: pd.Series, low: pd.Series, close: pd.Series, length: int) -> pd.Series:
    """Pine-compatible ATR using True Range + RMA."""
    prev_close = close.shift(1)
    tr = pd.concat(
        [
            (high - low),
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return ind_rma(tr, length)
