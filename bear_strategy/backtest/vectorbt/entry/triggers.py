"""Entry trigger functions for the Bear Strategy vectorbt backtest.

A trigger is an aggressive timing signal that fires WITHIN an established
regime.  At least one active trigger must fire for an entry to occur.

Current triggers
----------------
  use_vp_trigger    Session Volume-Profile POC / HVN breakout (1h bars).
                    Wired to compute_vp_trigger() below.

Adding a new trigger
--------------------
1.  Write a compute_<name>() function below with the standard signature:
      compute_<name>(df_1h, df_1d, funding_df, params) -> pd.Series[bool]
2.  Add  use_<name>_trigger: bool = False  to Parameters
    in bear_strategy/strategy/parameters.py.
3.  Add the flag → function mapping to TRIGGER_REGISTRY below.
4.  Add the flag to BearGridConfig.boolean_filter_ranges
    in bear_strategy/backtest/vectorbt/bear_grid_config.py.

Notes
-----
- All triggers receive the full (df_1h, df_1d, funding_df, params) tuple even
  if they don't use all three DataFrames — uniform signature keeps the registry
  loop in __init__.py simple.
- No trigger should look ahead: use only data available at the END of bar N;
  build_vbt_arrays() in signals.py will shift everything +1 to fill at open[N+1].
"""

from __future__ import annotations

from typing import Callable

import pandas as pd

from bear_strategy.strategy.indicators.trigger.vp_session_poc_or_hvn_break import (
    compute_vp_signal,
)
from bear_strategy.strategy.parameters import Parameters

# ── Type alias for the uniform trigger signature ──────────────────────────────

TriggerFn = Callable[
    [pd.DataFrame, pd.DataFrame, pd.DataFrame, Parameters],
    pd.Series,
]


# ── Individual trigger functions ──────────────────────────────────────────────

def compute_vp_trigger(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,   # not used; kept for uniform signature
    funding_df: pd.DataFrame,   # not used; kept for uniform signature
    params:     Parameters,
) -> pd.Series:
    """Session VP POC / HVN downside breakout on 1h bars.

    Returns True on bars where price breaks below the session Value-Profile
    Point-of-Control or a High-Volume-Node — a high-probability short entry.
    """
    return compute_vp_signal(df_1h, params.vp_price_bins)


# ── Registry — maps Parameters flag → trigger function ───────────────────────
# To disable a trigger entirely: set its boolean_filter_ranges value to (False,)
# in the grid config (it will be pinned off and never enter the grid).

TRIGGER_REGISTRY: dict[str, TriggerFn] = {
    "use_vp_trigger": compute_vp_trigger,
    # Add new triggers here:
    # "use_<name>_trigger": compute_<name>_trigger,
}
