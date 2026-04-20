"""Cross-symbol and cross-timeframe consistency analysis."""

from __future__ import annotations

import dataclasses
from collections import Counter
from typing import Literal

import numpy as np
import pandas as pd

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.importance import _get_toggle_cols
from strategy_evaluation.metrics import annotate_dataframe

# Maps the VBT metric column name to the RobustnessConfig field that gates it.
_METRIC_TO_CFG_FIELD: dict[str, str] = {
    "SQN":               "min_sqn",
    "Profit Factor":     "min_profit_factor",
    "# Trades":          "min_trades",
    "Max Drawdown [%]":  "max_max_drawdown",
}


def symbol_pass_rate(df: pd.DataFrame, cfg: RobustnessConfig) -> dict[str, float]:
    """Return fraction of symbols where ≥ cfg.min_combo_pass_rate of combos pass.

    Returns
    -------
    dict mapping symbol name → 1.0 if the combo pass fraction meets the
    configured minimum, else 0.0.
    """
    annotated = annotate_dataframe(df, cfg)
    result: dict[str, float] = {}
    for symbol, group in annotated.groupby(cfg.col_symbol):
        passes = bool(group["_passes"].mean() >= cfg.min_combo_pass_rate)
        result[str(symbol)] = 1.0 if passes else 0.0
    return result


def timeframe_pass_rate(df: pd.DataFrame, cfg: RobustnessConfig) -> dict[str, float]:
    """Return fraction of (symbol, timeframe) pairs per timeframe that pass.

    A symbol/TF pair passes when ≥ cfg.min_combo_pass_rate of its combos pass.
    Returns a normalised 0–1 rate per timeframe.
    """
    annotated = annotate_dataframe(df, cfg)
    tf_symbol_pass: dict[str, set[str]] = {}
    tf_symbol_total: dict[str, set[str]] = {}

    for (symbol, tf), group in annotated.groupby([cfg.col_symbol, cfg.col_timeframe]):
        tf_str = str(tf)
        tf_symbol_total.setdefault(tf_str, set()).add(str(symbol))
        if group["_passes"].mean() >= cfg.min_combo_pass_rate:
            tf_symbol_pass.setdefault(tf_str, set()).add(str(symbol))

    return {
        tf: len(tf_symbol_pass.get(tf, set())) / len(total)
        for tf, total in tf_symbol_total.items()
    }


def sweep_threshold(
    df: pd.DataFrame,
    metric_col: str,
    sweep_values: list[float],
    cfg: RobustnessConfig,
    comparison: Literal[">=", "<="] = ">=",
) -> pd.DataFrame:
    """Compute symbol and TF pass rates across a range of threshold values.

    For each value in *sweep_values* a local copy of *cfg* is created with
    the relevant threshold field updated — the original *cfg* is never mutated.

    Parameters
    ----------
    df:
        Raw (unannotated) backtest DataFrame.
    metric_col:
        VBT column name to sweep (e.g. ``"SQN"``, ``"Profit Factor"``).
    sweep_values:
        Ordered sequence of threshold values to evaluate.
    cfg:
        Base config.  A ``dataclasses.replace`` copy is made per step.
    comparison:
        ``">="`` for metrics where higher is better (SQN, PF, Trades).
        ``"<="`` for metrics where lower is better (Max Drawdown).

    Returns
    -------
    pd.DataFrame with columns:
      - ``threshold``
      - ``symbol_pass_rate``   : fraction of symbols where ≥ min_combo_pass_rate of combos pass
      - ``symbol_any_pass_rate``: fraction of symbols with at least 1 passing combo
      - ``tf_pass_rate``       : fraction of timeframes meeting the pass-rate criterion
    """
    if metric_col not in _METRIC_TO_CFG_FIELD:
        raise ValueError(
            f"metric_col {metric_col!r} not supported. "
            f"Choose from: {list(_METRIC_TO_CFG_FIELD)}"
        )

    cfg_field = _METRIC_TO_CFG_FIELD[metric_col]
    rows: list[dict] = []

    for threshold in sweep_values:
        step_cfg = dataclasses.replace(cfg, **{cfg_field: threshold})
        ann = annotate_dataframe(df, step_cfg)

        # Compute all three metrics in one groupby pass to avoid re-annotating.
        sym_grouped = ann.groupby(cfg.col_symbol)["_passes"]
        n_syms = sym_grouped.ngroups
        n_pct_pass = sum(
            1 for _, g in sym_grouped if g.mean() >= step_cfg.min_combo_pass_rate
        )
        n_any_pass = sum(1 for _, g in sym_grouped if g.any())
        sym_rate = n_pct_pass / n_syms if n_syms else 0.0
        any_rate = n_any_pass / n_syms if n_syms else 0.0

        tf_pass: dict[str, set] = {}
        tf_total: dict[str, set] = {}
        for (sym, tf), g in ann.groupby([cfg.col_symbol, cfg.col_timeframe])["_passes"]:
            k = str(tf)
            tf_total.setdefault(k, set()).add(str(sym))
            if g.mean() >= step_cfg.min_combo_pass_rate:
                tf_pass.setdefault(k, set()).add(str(sym))
        tf_rate = (
            float(np.mean([
                len(tf_pass.get(tf, set())) / len(tot)
                for tf, tot in tf_total.items()
            ]))
            if tf_total else 0.0
        )

        rows.append({
            "threshold":             threshold,
            "symbol_pass_rate":      sym_rate,
            "symbol_any_pass_rate":  any_rate,
            "tf_pass_rate":          tf_rate,
        })

    return pd.DataFrame(rows)


def toggle_frequency(df: pd.DataFrame, cfg: RobustnessConfig, top_n: int = 5) -> dict[str, int]:
    """Count how often each boolean toggle appears enabled in top-N combos.

    Useful for identifying which indicator filters consistently appear in the
    best-performing combos — high frequency = likely important signal.
    Zero-frequency toggles may be noise.

    Only qualifying combos (``_passes=True``) are considered so that low-trade
    outliers with inflated Expectancy do not skew toggle importance.
    """
    source = df[df["_passes"]].copy() if "_passes" in df.columns else df.copy()
    top_rows = (
        source.sort_values(cfg.col_rank)
        .groupby([cfg.col_symbol, cfg.col_timeframe])
        .head(top_n)
    )
    # Binary-detection: only columns whose values are all 0/1 are toggles.
    toggle_cols = _get_toggle_cols(top_rows)

    counts: dict[str, int] = {}
    for col in toggle_cols:
        enabled = top_rows[col]
        # Support both bool and 0/1 int columns
        try:
            enabled = enabled.astype(float).fillna(0)
            counts[col] = int((enabled == 1).sum())
        except (ValueError, TypeError):
            pass

    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def compute_toggle_consensus(
    df: pd.DataFrame,
    cfg: RobustnessConfig,
    ols: "OLSResult | None",
    shap: "ShapResult | None",
    top_n: int = 5,
    shap_noise_floor: float = 0.02,
) -> pd.DataFrame:
    """Cross-check toggle signals: frequency in passing combos, OLS coefficient, SHAP direction.

    Combines three complementary signals into a single per-toggle verdict:

    - **Toggle Frequency** (threshold-sensitive): how often the toggle appears in top-N passing
      combos. High frequency means it's consistently present in winning configurations *at the
      current thresholds*.
    - **OLS coefficient** (landscape): average change in SQN when the toggle is ON across *all*
      combos. Positive + significant = reliably helpful.
    - **SHAP mean** (landscape): signed mean SHAP when toggle is ON. Positive = raises predicted
      SQN above baseline. Negative = lowers it.

    Verdict rules:

    - ``✅ Keep ON`` — freq ≥ 60% AND OLS significant positive AND SHAP positive (any magnitude)
    - ``❌ Remove`` — freq ≤ 20% AND OLS significant negative AND SHAP < −noise_floor
    - ``⚠️ Conflict`` — freq ≥ 40% (borderline or high) AND (OLS hurts OR SHAP hurts)
    - ``⚠️ Absent but helpful`` — freq ≤ 20% AND (OLS helps OR SHAP positive)
    - ``— Neutral`` — signals are mixed or too weak to act on

    Parameters
    ----------
    df:
        Annotated backtest DataFrame (must have ``_passes`` column from ``annotate_dataframe``).
    cfg:
        Active ``RobustnessConfig`` — used for column names and to select passing combos.
    ols:
        OLS result from ``compute_ols_significance``, or ``None`` if unavailable.
    shap:
        SHAP result from ``compute_shap_importance``, or ``None`` if unavailable.
    top_n:
        Number of top-ranked combos per (symbol, timeframe) pair to include in frequency count.
    shap_noise_floor:
        Minimum |mean_shap| to treat as a *negative* directional signal. Only applied for
        ``❌ Remove`` and conflict checks — positive SHAP is accepted at any magnitude.

    Returns
    -------
    pd.DataFrame with columns:
        ``toggle``, ``freq_pct``, ``ols_coeff``, ``ols_p``, ``ols_sig``, ``shap_mean``,
        ``consensus`` — sorted by ``freq_pct`` descending.
        Returns an empty DataFrame (same columns) when there are no passing combos.
    """
    # Deferred imports to avoid circular dependency at module load time.
    from strategy_evaluation.significance import OLSResult  # noqa: F401
    from strategy_evaluation.importance import ShapResult  # noqa: F401

    _EMPTY_COLS = ["toggle", "freq_pct", "ols_coeff", "ols_p", "ols_sig", "shap_mean", "consensus"]

    source = df[df["_passes"]].copy() if "_passes" in df.columns else df.copy()
    top_rows = (
        source.sort_values(cfg.col_rank)
        .groupby([cfg.col_symbol, cfg.col_timeframe])
        .head(top_n)
    )
    n_top_rows = len(top_rows)
    if n_top_rows == 0:
        return pd.DataFrame(columns=_EMPTY_COLS)

    # Binary-detection: only columns whose values are all 0/1 are toggles.
    toggle_cols = _get_toggle_cols(top_rows)

    # Build OLS lookup: toggle → (coeff, p_value, significant)
    ols_lookup: dict[str, tuple[float, float, bool]] = {}
    if ols is not None:
        for _, row in ols.table.iterrows():
            ols_lookup[str(row["toggle"])] = (
                float(row["coefficient"]),
                float(row["p_value"]),
                bool(row["significant"]),
            )

    # Build SHAP lookup: toggle → mean_shap
    shap_lookup: dict[str, float] = {}
    if shap is not None:
        for toggle_name, val in shap.mean_shap.items():
            shap_lookup[str(toggle_name)] = float(val)

    rows: list[dict] = []
    for col in toggle_cols:
        try:
            enabled = top_rows[col].astype(float).fillna(0)
        except (ValueError, TypeError):
            continue

        freq_pct = float((enabled == 1).sum()) / n_top_rows

        ols_coeff, ols_p, ols_sig = ols_lookup.get(col, (float("nan"), float("nan"), False))
        shap_mean = shap_lookup.get(col, float("nan"))

        freq_high = freq_pct >= 0.60
        freq_mid  = freq_pct >= 0.40   # wider band for conflict detection
        freq_low = freq_pct <= 0.20
        # NaN comparisons always return False — safe for missing OLS/SHAP
        ols_helps = (not np.isnan(ols_coeff)) and ols_coeff > 0 and ols_sig
        ols_hurts = (not np.isnan(ols_coeff)) and ols_coeff < 0 and ols_sig
        # For "Keep ON" use direction only (any positive SHAP); for hurts keep noise floor
        shap_helps = (not np.isnan(shap_mean)) and shap_mean > 0
        shap_hurts = (not np.isnan(shap_mean)) and shap_mean < -shap_noise_floor

        if freq_high and ols_helps and shap_helps:
            consensus = "✅ Keep ON"
        elif freq_low and ols_hurts and shap_hurts:
            consensus = "❌ Remove"
        elif freq_mid and (ols_hurts or shap_hurts):
            consensus = "⚠️ Present in top combos but signals say it hurts"
        elif freq_low and (ols_helps or shap_helps):
            consensus = "⚠️ Signals say helpful but absent from top combos"
        else:
            consensus = "— Neutral"

        rows.append({
            "toggle": col,
            "freq_pct": freq_pct,
            "ols_coeff": ols_coeff,
            "ols_p": ols_p,
            "ols_sig": ols_sig,
            "shap_mean": shap_mean,
            "consensus": consensus,
        })

    return pd.DataFrame(rows, columns=_EMPTY_COLS).sort_values("freq_pct", ascending=False).reset_index(drop=True)
