"""Entry signal package for the Bear Strategy vectorbt backtest.

Structure
---------
  regime.py    — always-on structural regime filter (RSI bear zone + funding guard).
                 Both conditions must hold for any entry to fire.
  triggers.py  — individual entry trigger functions (one per timing signal).
                 At least one active trigger must fire alongside the regime.

Adding a new trigger
--------------------
1.  Write compute_<name>() in triggers.py with signature:
      compute_<name>(df_1h, df_1d, funding_df, params) -> pd.Series[bool]
2.  Add a use_<name>_trigger: bool flag to bear_strategy/strategy/parameters.py.
3.  Register it in TRIGGER_REGISTRY in triggers.py.
4.  Add the flag to BearGridConfig.boolean_filter_ranges in bear_grid_config.py.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.strategy.parameters import Parameters

from .regime   import compute_regime_filter
from .triggers import TRIGGER_REGISTRY


def build_entry_signal(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,
    funding_df: pd.DataFrame,
    params:     Parameters,
) -> pd.Series:
    """Combine regime filter with all active triggers (OR logic across triggers).

    Returns a bool Series on df_1h.index.
    An entry fires when:  regime AND (any active trigger)
    """
    regime = compute_regime_filter(df_1h, df_1d, funding_df, params)

    # OR all active triggers — if none is active → no entries
    trigger = pd.Series(False, index=df_1h.index, dtype=bool)
    for flag, fn in TRIGGER_REGISTRY.items():
        if getattr(params, flag, False):
            trigger = trigger | fn(df_1h, df_1d, funding_df, params)

    return (regime & trigger).fillna(False)
