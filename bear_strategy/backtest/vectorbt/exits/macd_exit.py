"""Exit: 1h MACD histogram crosses from negative to ≥ 0.

When the MACD histogram transitions from negative to flat/positive the
short-side momentum is fading — take profit early before a full reversal.

Parameters used
---------------
  params.macd_fast_period   : fast EMA period (default 12)
  params.macd_slow_period   : slow EMA period (default 26)
  params.macd_signal_period : signal EMA period (default 9)

Activated by
------------
  params.use_macd_exit = True
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.strategy.parameters import Parameters

from bear_strategy.backtest.vectorbt.indicators import compute_macd_histogram

FLAG = "use_macd_exit"


def compute(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,   # not used; kept for uniform signature
    funding_df: pd.DataFrame,   # not used; kept for uniform signature
    params:     Parameters,
) -> pd.Series:
    """Return True on 1h bars where the MACD histogram crosses negative → ≥ 0."""
    hist = compute_macd_histogram(
        df_1h["close"].astype(float),
        fast=int(params.macd_fast_period),
        slow=int(params.macd_slow_period),
        signal=int(params.macd_signal_period),
    )
    # previous bar negative, current bar ≥ 0
    return ((hist.shift(1) < 0) & (hist >= 0)).fillna(False)
