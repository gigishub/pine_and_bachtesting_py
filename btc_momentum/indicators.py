"""Indicator utilities for backtesting strategies."""

from __future__ import annotations

import pandas as pd
import pandas_ta as pta


def ind_ema(close: pd.Series, length: int) -> pd.Series:
    return pta.ema(close, length=length)


def ind_atr(high: pd.Series, low: pd.Series, close: pd.Series, length: int) -> pd.Series:
    return pta.atr(high, low, close, length=length)


def ind_bbands(close: pd.Series, length: int, std: float) -> tuple[pd.Series, pd.Series]:
    bb = pta.bbands(close, length=length, std=std)
    basis_col = next((c for c in bb.columns if c.startswith("BBM_")), None)
    lower_col = next((c for c in bb.columns if c.startswith("BBL_")), None)
    if basis_col is None or lower_col is None:
        raise ValueError(f"Unexpected pandas_ta bbands columns: {list(bb.columns)}")
    return bb[basis_col], bb[lower_col]


def map_timeframe_to_rule(tf: str) -> str:
    mapping = {
        "W": "W",
        "D": "D",
        "1D": "D",
        "4H": "4H",
        "1H": "1H",
    }
    return mapping.get(tf.upper(), tf)


def non_repainting_htf_ema(close: pd.Series, htf: str, length: int) -> pd.Series:
    rule = map_timeframe_to_rule(htf)
    htf_close = close.resample(rule).last().dropna()

    if htf_close.empty:
        return pd.Series(index=close.index, dtype=float)

    htf_ema = ind_ema(htf_close, length)
    if htf_ema is None:
        return pd.Series(index=close.index, dtype=float)

    htf_ema = htf_ema.reindex(close.index, method="ffill")
    return htf_ema.shift(1).astype(float)
