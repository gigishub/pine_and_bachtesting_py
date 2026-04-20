"""Toggle importance analysis using RandomForestRegressor and SHAP.

Two complementary analyses:
- ``compute_toggle_importance`` — RandomForest feature importance (magnitude only).
- ``compute_shap_importance`` — SHAP TreeExplainer (magnitude + direction: does enabling
  a toggle raise or lower SQN?).

Rather than simply counting how often a toggle appears in top-ranked combos,
these functions measure how much each toggle *drives* the target metric by
training a RandomForest on the full combo space.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from strategy_evaluation.config import RobustnessConfig

_log = logging.getLogger(__name__)




@dataclass
class ImportanceResult:
    """Feature importances from the RandomForest model."""

    importances: pd.Series
    """Sorted Series: index = toggle name, values = importance (0–1, sums to 1)."""
    target_col: str
    n_combos: int
    r2_score: float
    """Out-of-bag R² — how well the forest explains variance in the target."""


@dataclass
class ShapResult:
    """SHAP-based toggle impact: magnitude + direction."""

    mean_shap: pd.Series
    """Signed mean SHAP value per toggle when that toggle is enabled (conditional mean).

    Positive → enabling this toggle shifts predictions above the dataset average (good).
    Negative → enabling this toggle shifts predictions below the dataset average (bad)."""
    abs_mean_shap: pd.Series
    """Absolute mean SHAP, sorted descending — for ranking by overall impact."""
    target_col: str
    n_combos: int
    toggle_cols: list[str] = field(default_factory=list)


def _get_toggle_cols(df: pd.DataFrame) -> list[str]:
    """Return columns whose non-null values are all in {0, 1} (binary toggle columns).

    Detects toggles by value content rather than a hardcoded name exclusion list,
    so new metric columns never accidentally appear as toggles regardless of their
    names.  Internal annotation columns (names starting with ``_``) are always
    excluded even if they happen to be binary (e.g. ``_passes``).
    """
    result = []
    for col in df.columns:
        if col.startswith("_"):
            continue
        try:
            series = df[col].dropna()
            if series.empty:
                continue
            unique_vals = set(series.astype(float).unique())
            if unique_vals <= {0.0, 1.0}:
                result.append(col)
        except (ValueError, TypeError):
            continue
    return result


def _prepare_xy(
    df: pd.DataFrame,
    toggle_cols: list[str],
    target_col: str,
) -> tuple[pd.DataFrame, pd.Series] | None:
    """Return (X, y) or None if insufficient data."""
    working = df[toggle_cols + [target_col]].dropna()
    if len(working) < 20:
        _log.warning("Too few rows (%d) for analysis.", len(working))
        return None
    return working[toggle_cols].astype(float), working[target_col].astype(float)


def compute_toggle_importance(
    df: pd.DataFrame,
    cfg: RobustnessConfig,  # noqa: ARG001 — kept for API consistency
    target_col: str = "SQN",
    n_estimators: int = 200,
    random_state: int = 42,
) -> ImportanceResult | None:
    """Fit a RandomForestRegressor to predict *target_col* from toggle columns.

    Returns ``None`` if there are not enough rows or toggle columns to train.
    """
    toggle_cols = _get_toggle_cols(df)
    # Zero-variance toggles provide no signal to the RF — exclude them.
    toggle_cols = [c for c in toggle_cols if df[c].dropna().nunique() > 1]
    if not toggle_cols:
        return None
    if target_col not in df.columns:
        _log.warning("Target column '%s' not in DataFrame.", target_col)
        return None

    xy = _prepare_xy(df, toggle_cols, target_col)
    if xy is None:
        return None
    X, y = xy

    rf = RandomForestRegressor(
        n_estimators=n_estimators,
        oob_score=True,
        n_jobs=-1,
        random_state=random_state,
    )
    rf.fit(X, y)

    importances = pd.Series(rf.feature_importances_, index=toggle_cols).sort_values(ascending=False)
    return ImportanceResult(
        importances=importances,
        target_col=target_col,
        n_combos=len(X),
        r2_score=float(rf.oob_score_),
    )


def compute_shap_importance(
    df: pd.DataFrame,
    cfg: RobustnessConfig,  # noqa: ARG001
    target_col: str = "SQN",
    n_estimators: int = 200,
    random_state: int = 42,
) -> ShapResult | None:
    """Compute SHAP values using TreeExplainer on a RandomForest.

    Returns signed mean SHAP per toggle so the *direction* is visible:
    - Positive mean SHAP → enabling this toggle tends to **increase** *target_col*
    - Negative mean SHAP → enabling this toggle tends to **decrease** *target_col*

    Returns ``None`` if there are not enough rows or toggle columns.
    """
    try:
        import shap  # local import so the module loads even if shap is not installed
    except ImportError:
        _log.warning("shap not installed — skipping SHAP analysis.")
        return None

    toggle_cols = _get_toggle_cols(df)
    # Zero-variance toggles provide no signal to the RF — exclude them.
    toggle_cols = [c for c in toggle_cols if df[c].dropna().nunique() > 1]
    if not toggle_cols:
        _log.warning("No toggle columns found — skipping SHAP analysis.")
        return None
    if target_col not in df.columns:
        _log.warning("Target column '%s' not in DataFrame.", target_col)
        return None

    xy = _prepare_xy(df, toggle_cols, target_col)
    if xy is None:
        return None
    X, y = xy

    rf = RandomForestRegressor(
        n_estimators=n_estimators,
        oob_score=False,
        n_jobs=-1,
        random_state=random_state,
    )
    rf.fit(X, y)

    explainer = shap.TreeExplainer(rf)
    shap_values = explainer.shap_values(X)  # shape: (n_samples, n_toggles)

    # Conditional mean SHAP when toggle=1: shows how much *enabling* each toggle
    # shifts the prediction relative to the dataset average.
    # Unconditional mean is always ~0 for balanced binary features (it's a deviation
    # from expected value), so we use the conditional mean for direction.
    shap_array = np.array(shap_values)
    x_array    = X.values
    conditional_mean = []
    for i in range(len(toggle_cols)):
        on_mask = x_array[:, i] == 1
        conditional_mean.append(float(np.mean(shap_array[on_mask, i])) if on_mask.any() else 0.0)

    mean_shap     = pd.Series(conditional_mean, index=toggle_cols)
    abs_mean_shap = mean_shap.abs().sort_values(ascending=False)

    return ShapResult(
        mean_shap=mean_shap,
        abs_mean_shap=abs_mean_shap,
        target_col=target_col,
        n_combos=len(X),
        toggle_cols=toggle_cols,
    )
