"""OLS regression of SQN on toggle columns to identify statistically significant filters.

Answers the question: *"Is this toggle's effect on SQN real, or could it be random noise?"*

A toggle with p < 0.05 has a statistically significant effect.
The coefficient tells you the average change in SQN when that toggle is switched on.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
import pandas as pd

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.importance import _NON_TOGGLE_COLS

_log = logging.getLogger(__name__)

_SIGNIFICANCE_THRESHOLD = 0.05


@dataclass
class OLSResult:
    """Per-toggle OLS regression results."""

    table: pd.DataFrame
    """DataFrame with columns: toggle, coefficient, std_err, t_stat, p_value, significant."""
    target_col: str
    n_combos: int
    r_squared: float


def compute_ols_significance(
    df: pd.DataFrame,
    cfg: RobustnessConfig,  # noqa: ARG001
    target_col: str = "SQN",
    significance_threshold: float = _SIGNIFICANCE_THRESHOLD,
) -> OLSResult | None:
    """Run OLS regression *target_col* ~ toggle columns.

    Returns ``None`` if statsmodels is not installed or data is insufficient.

    Parameters
    ----------
    df:
        Annotated backtest DataFrame from ``annotate_dataframe()``.
    cfg:
        ``RobustnessConfig`` (kept for API consistency).
    target_col:
        Metric to regress; typically ``"SQN"``.
    significance_threshold:
        p-value below which a toggle is flagged as significant (default 0.05).
    """
    try:
        import statsmodels.api as sm
    except ImportError:
        _log.warning("statsmodels not installed — skipping OLS significance analysis.")
        return None

    toggle_cols = [c for c in df.columns if c not in _NON_TOGGLE_COLS]
    if not toggle_cols:
        _log.warning("No toggle columns found — skipping OLS analysis.")
        return None

    if target_col not in df.columns:
        _log.warning("Target column '%s' not in DataFrame.", target_col)
        return None

    working = df[toggle_cols + [target_col]].dropna()
    if len(working) < 20:
        _log.warning("Too few rows (%d) for OLS analysis.", len(working))
        return None

    X_raw = working[toggle_cols].astype(float)

    # Drop one column from each perfectly collinear pair (|correlation| >= 0.999).
    # This happens when toggles are mutually exclusive alternatives in the backtest
    # design (e.g. use_adx is always the inverse of use_ema_ribbon).
    dropped: set[str] = set()
    corr_matrix = X_raw.corr().abs()
    for i, col_i in enumerate(toggle_cols):
        if col_i in dropped:
            continue
        for col_j in toggle_cols[i + 1 :]:
            if col_j in dropped:
                continue
            if corr_matrix.loc[col_i, col_j] >= 0.999:
                dropped.add(col_j)
                _log.info("Dropped collinear toggle '%s' (|corr| with '%s' ≥ 0.999).", col_j, col_i)

    fit_cols = [c for c in toggle_cols if c not in dropped]
    if not fit_cols:
        _log.warning("All toggle columns are collinear — skipping OLS analysis.")
        return None

    X = sm.add_constant(X_raw[fit_cols])
    y = working[target_col].astype(float)

    try:
        model = sm.OLS(y, X).fit()
    except Exception:
        _log.exception("OLS fitting failed.")
        return None

    rows = []
    for col in fit_cols:
        if col not in model.params.index:
            continue
        p = float(model.pvalues[col])
        rows.append(
            {
                "toggle": col,
                "coefficient": float(model.params[col]),
                "std_err": float(model.bse[col]),
                "t_stat": float(model.tvalues[col]),
                "p_value": p,
                "significant": p < significance_threshold,
            }
        )

    table = pd.DataFrame(rows).sort_values("p_value")

    return OLSResult(
        table=table,
        target_col=target_col,
        n_combos=len(working),
        r_squared=float(model.rsquared),
    )
