"""Exit: 1h close reclaims the EMA (crosses back above).

When the 1h close crosses back above EMA(exit_ema_period) the bearish
price structure is broken — exit now before a larger reversal.

Parameters used
---------------
  params.exit_ema_period : EMA lookback period (default 21)

Activated by
------------
  params.use_ema_reclaim_exit = True
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.strategy.parameters import Parameters

from bear_strategy.backtest.vectorbt.indicators import compute_ema

FLAG = "use_ema_reclaim_exit"


def compute(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,   # not used; kept for uniform signature
    funding_df: pd.DataFrame,   # not used; kept for uniform signature
    params:     Parameters,
) -> pd.Series:
    """Return True on 1h bars where price reclaims EMA(exit_ema_period)."""
    close = df_1h["close"].astype(float)
    ema   = compute_ema(close, int(params.exit_ema_period))

    # cross up: previous bar below EMA, current bar ≥ EMA
    return (
        (close.shift(1) < ema.shift(1)) & (close >= ema)
    ).fillna(False)
