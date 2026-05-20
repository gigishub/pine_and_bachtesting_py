"""Exit: 1h close is above VWMA (Volume Weighted Moving Average).

VWMA weights each bar's close by its volume, producing a moving average that
reacts faster during high-volume moves and slower during low-volume drift.
When price trades back above VWMA the short is considered neutralised — exit.

  VWMA(n) = sum(close[i] × volume[i], n) / sum(volume[i], n)

Parameters used
---------------
  params.vwma_period  — rolling lookback for VWMA (default: 20)

Activated by
------------
  params.use_vwma_exit = True
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.strategy.parameters import Parameters
from bear_strategy.backtest.vectorbt.indicators import compute_vwma

FLAG = "use_vwma_exit"


def compute(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,   # unused; kept for uniform signature
    funding_df: pd.DataFrame,   # unused; kept for uniform signature
    params:     Parameters,
) -> pd.Series:
    """Return True on 1h bars where close > VWMA(vwma_period)."""
    close = df_1h["close"].astype(float)
    vwma  = compute_vwma(df_1h, period=params.vwma_period)
    return (close > vwma).fillna(False)
