"""Shared scoring utilities for Phase 1 and Phase 2 dashboards.

Single source of truth for the weighted robustness score formula:
    Final Score = avg_score × (coins_passing / N) × 1.5^(n_TFs − 1)
"""

from __future__ import annotations

import pandas as pd

from strategy_evaluation.config import RobustnessConfig


def compute_combo_weighted_scores(df: pd.DataFrame, cfg: RobustnessConfig) -> pd.DataFrame:
    """Compute weighted robustness scores per parameter signature.

    Expects *df* to already have ``_passes`` and ``_score`` columns (added by
    ``annotate_dataframe``).

    Parameters
    ----------
    df:
        Annotated result DataFrame (must contain ``_passes`` and ``_score``).
    cfg:
        Config providing column-name constants.

    Returns
    -------
    pd.DataFrame
        One row per signature with columns:
        Parameter Signature, avg_score, coins_passing, n_TFs,
        breadth, tf_multiplier, final_score.
        Sorted descending by ``final_score``.  Empty if no combos pass.
    """
    col_sig = cfg.col_param_sig
    col_sym = cfg.col_symbol
    col_tf  = cfg.col_timeframe

    if "_passes" not in df.columns or col_sig not in df.columns:
        return pd.DataFrame()

    n_coins    = df[col_sym].nunique()
    passing_df = df[df["_passes"]]

    if passing_df.empty or n_coins == 0:
        return pd.DataFrame()

    records = []
    for sig, grp in passing_df.groupby(col_sig):
        avg_score     = float(grp["_score"].mean()) if "_score" in grp.columns else 0.0
        coins_passing = int(grp[col_sym].nunique())
        n_tfs         = int(grp[col_tf].nunique())
        breadth       = coins_passing / n_coins
        tf_multiplier = 1.5 ** (n_tfs - 1)
        final_score   = avg_score * breadth * tf_multiplier
        records.append({
            "Parameter Signature": sig,
            "avg_score":           round(avg_score, 4),
            "coins_passing":       coins_passing,
            "n_TFs":               n_tfs,
            "breadth":             round(breadth, 4),
            "tf_multiplier":       round(tf_multiplier, 4),
            "final_score":         round(final_score, 4),
        })

    return (
        pd.DataFrame(records)
        .sort_values("final_score", ascending=False)
        .reset_index(drop=True)
    )
