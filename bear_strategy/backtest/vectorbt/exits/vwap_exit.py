"""Exit: 1h close is above anchor-period VWAP.

VWAP resets every ``vwap_anchor_hours`` hours (default: 24 = daily).  When
price trades back above the session VWAP the intraday bearish bias is
neutralised — exit the short.

Parameters used
---------------
  params.vwap_anchor_hours  — window size for VWAP anchor:
    24  = daily-anchored (default)
    48  = 2-day rolling window
    168 = weekly-anchored

Activated by
------------
  params.use_vwap_exit = True
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.strategy.parameters import Parameters
from bear_strategy.backtest.vectorbt.indicators import compute_vwap

FLAG = "use_vwap_exit"


def compute(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,   # unused; kept for uniform signature
    funding_df: pd.DataFrame,   # unused; kept for uniform signature
    params:     Parameters,
) -> pd.Series:
    """Return True on 1h bars where close > anchor-period VWAP."""
    close = df_1h["close"].astype(float)
    vwap  = compute_vwap(df_1h, anchor_hours=params.vwap_anchor_hours)
    return (close > vwap).fillna(False)
