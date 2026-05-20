"""Exit: bullish engulfing candle on 1h.

For a short position, a bullish engulfing is a reversal warning — exit
before the move turns against us.

Definition (body-only, no wicks)
---------------------------------
  previous bar : bearish  (prev_close < prev_open)
  current bar  : bullish  (close > open)
  current body >= engulfing_ratio × previous body

  body  = |close − open|   (wicks deliberately excluded)

A ratio of 1.0 (default) requires the current body to fully cover the
previous body.  Raise it (e.g. 1.2) to demand a larger engulf margin;
lower it (e.g. 0.8) to allow partial engulfs.

Parameters used
---------------
  params.engulfing_ratio : body-size multiplier threshold (default 1.0)

Activated by
------------
  params.use_engulfing_exit = True
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.strategy.parameters import Parameters

FLAG = "use_engulfing_exit"


def compute(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,   # unused; kept for uniform signature
    funding_df: pd.DataFrame,   # unused; kept for uniform signature
    params:     Parameters,
) -> pd.Series:
    """Return True on 1h bars where a qualifying bullish engulfing fires."""
    op    = df_1h["open"].astype(float)
    cl    = df_1h["close"].astype(float)
    ratio = float(params.engulfing_ratio)

    curr_body = (cl - op).abs()
    prev_body = (cl.shift(1) - op.shift(1)).abs()

    prev_bearish = cl.shift(1) < op.shift(1)
    curr_bullish = cl > op
    engulfs      = curr_body >= ratio * prev_body

    return (prev_bearish & curr_bullish & engulfs).fillna(False)
