"""Parabolic SAR trailing stop (Exit Option B).

The Parabolic SAR uses an acceleration factor (α) that increases as the
trend continues, moving the stop progressively closer to price.  This ensures
profits are captured when momentum slows, providing a purely mathematical,
objective exit point that removes emotional interference during parabolic moves.

Mathematical rule:
    SAR(t+1) = SAR(t) + α × (EP - SAR(t))
    α starts at af_initial and increments by af_step up to af_max.

Unlike the Chandelier exit, PSAR self-manages its own dynamics and should
NOT be ratcheted by the runner — the runner should apply the current PSAR
stop value directly to the open trade each bar.

Reference: Wilder, J. W. (1978). New Concepts in Technical Trading Systems.
"""

from __future__ import annotations

import pandas as pd
import pandas_ta as pta


def compute_psar_stop_series(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    af_initial: float = 0.02,
    af_step: float = 0.02,
    af_max: float = 0.20,
) -> pd.Series:
    """Return the Parabolic SAR long-stop level for each bar.

    When in a long trade, the SAR stop is the value of the *long* SAR series
    (below price).  NaN is returned for bars where PSAR has not yet
    established a long-side stop (e.g., during initial warmup).

    Args:
        af_initial: Starting acceleration factor (default 0.02).
        af_step:    Increment added to AF each time a new extreme point is set.
        af_max:     Maximum acceleration factor (default 0.20).
    """
    result = pta.psar(high, low, close, af0=af_initial, af=af_step, max_af=af_max)
    if result is None or result.empty:
        return pd.Series(float("nan"), index=close.index, dtype=float)

    # pandas_ta names the long SAR column PSARl_<af>_<max_af>
    long_col = [c for c in result.columns if c.startswith("PSARl")]
    if not long_col:
        return pd.Series(float("nan"), index=close.index, dtype=float)

    return result[long_col[0]].astype(float)
