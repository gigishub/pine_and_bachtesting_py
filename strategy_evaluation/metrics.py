"""Per-combo quality scoring against configurable thresholds."""

from __future__ import annotations

import math

import pandas as pd

from strategy_evaluation.config import RobustnessConfig


def passes_thresholds(row: pd.Series, cfg: RobustnessConfig) -> bool:
    """Return True if a single combo row meets all minimum thresholds.

    NaN values in any required metric cause the row to fail so that
    combos with no trades (all-NaN metrics) are excluded automatically.
    """
    def _val(col: str) -> float:
        v = row.get(col, float("nan"))
        return float("nan") if pd.isna(v) else float(v)

    sqn = _val(cfg.col_sqn)
    pf = _val(cfg.col_pf)
    trades = _val(cfg.col_trades)
    win_rate = _val(cfg.col_win_rate)
    sharpe = _val(cfg.col_sharpe)

    # Any required metric being NaN → fail
    if any(math.isnan(x) for x in [sqn, pf, trades, win_rate, sharpe]):
        return False

    return (
        sqn >= cfg.min_sqn
        and pf >= cfg.min_profit_factor
        and trades >= cfg.min_trades
        and win_rate >= cfg.min_win_rate
        and sharpe >= cfg.min_sharpe
    )


def score_combo(row: pd.Series, cfg: RobustnessConfig) -> float:
    """Return a composite 0–1 score for a single combo row.

    Each metric is clamped to a reasonable ceiling before normalisation so
    outlier combos (e.g. 1 trade with 500 % return) don't dominate.
    Missing metrics score 0 for that component.
    """
    def _norm(value: float, minimum: float, ceiling: float) -> float:
        if math.isnan(value):
            return 0.0
        return max(0.0, min(1.0, (value - minimum) / (ceiling - minimum)))

    sqn = float("nan") if pd.isna(row.get(cfg.col_sqn)) else float(row[cfg.col_sqn])
    pf = float("nan") if pd.isna(row.get(cfg.col_pf)) else float(row[cfg.col_pf])
    trades = float("nan") if pd.isna(row.get(cfg.col_trades)) else float(row[cfg.col_trades])
    win_rate = float("nan") if pd.isna(row.get(cfg.col_win_rate)) else float(row[cfg.col_win_rate])
    sharpe = float("nan") if pd.isna(row.get(cfg.col_sharpe)) else float(row[cfg.col_sharpe])

    components = {
        "sqn": _norm(sqn, 0.0, 3.0),
        "profit_factor": _norm(pf, 1.0, 4.0),
        "sharpe": _norm(sharpe, 0.0, 2.0),
        "win_rate": _norm(win_rate, 0.0, 70.0),
        "trades": _norm(trades, 0.0, 100.0),
    }

    return sum(cfg.weights[k] * v for k, v in components.items())


def annotate_dataframe(df: pd.DataFrame, cfg: RobustnessConfig) -> pd.DataFrame:
    """Add `_passes` and `_score` columns to *df* in-place and return it."""
    df = df.copy()
    df["_passes"] = df.apply(passes_thresholds, axis=1, cfg=cfg)
    df["_score"] = df.apply(score_combo, axis=1, cfg=cfg)
    return df
