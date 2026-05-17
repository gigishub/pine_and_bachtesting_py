"""Exit: EMA-smoothed funding rate drops at or below funding_threshold.

When the carry tailwind disappears (funding no longer positive) there is
less edge in holding the short — exit now.  use_fixed_tp can remain active
as a safety-net hard TP alongside this exit.

Parameters used
---------------
  params.funding_ma_period  : EMA smoothing window for funding rate (default 3)
  params.funding_threshold  : level that must be crossed down (default 0.0)

Activated by
------------
  params.use_funding_exit = True
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.strategy.parameters import Parameters

from bear_strategy.backtest.vectorbt.indicators import get_smoothed_funding

FLAG = "use_funding_exit"


def compute(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,   # not used; kept for uniform signature
    funding_df: pd.DataFrame,
    params:     Parameters,
) -> pd.Series:
    """Return True on 1h bars where smoothed funding crosses down through threshold."""
    smoothed = get_smoothed_funding(
        funding_df, df_1h.index, int(params.funding_ma_period)
    )
    # 'settled' replicates the entry-guard logic: one extra shift so the exit
    # fires on the bar AFTER the cross, consistent with fill_at_next_open.
    settled = smoothed.shift(1)
    thr     = float(params.funding_threshold)

    # cross down: previous settled > thr, current settled ≤ thr
    return ((settled.shift(1) > thr) & (settled <= thr)).fillna(False)
