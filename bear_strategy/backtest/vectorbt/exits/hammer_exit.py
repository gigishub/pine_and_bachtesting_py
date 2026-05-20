"""Exit: hammer candle on 1h.

A hammer signals a bullish reversal — for a short position this is a
warning to exit before price bounces.

Definition
----------
  lower wick  = min(open, close) − low       (buying tail below body)
  upper wick  = high − max(open, close)
  body        = |close − open|

  lower_wick >= hammer_wick_ratio × body     (long tail required)
  upper_wick <= body                          (small top shadow)
  body        > 0                             (exclude dojis)

Raising hammer_wick_ratio (e.g. 3.0) demands a more prominent tail;
lowering it (e.g. 1.5) accepts shorter-tailed candles.

Parameters used
---------------
  params.hammer_wick_ratio : lower-wick / body minimum ratio (default 2.0)

Activated by
------------
  params.use_hammer_exit = True
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.strategy.parameters import Parameters

FLAG = "use_hammer_exit"


def compute(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,   # unused; kept for uniform signature
    funding_df: pd.DataFrame,   # unused; kept for uniform signature
    params:     Parameters,
) -> pd.Series:
    """Return True on 1h bars where a qualifying hammer candle fires."""
    op    = df_1h["open"].astype(float)
    hi    = df_1h["high"].astype(float)
    lo    = df_1h["low"].astype(float)
    cl    = df_1h["close"].astype(float)
    ratio = float(params.hammer_wick_ratio)

    body        = (cl - op).abs()
    lower_wick  = pd.concat([op, cl], axis=1).min(axis=1) - lo
    upper_wick  = hi - pd.concat([op, cl], axis=1).max(axis=1)

    has_body        = body > 0
    long_lower_wick = lower_wick >= ratio * body
    small_upper     = upper_wick <= body

    return (has_body & long_lower_wick & small_upper).fillna(False)
