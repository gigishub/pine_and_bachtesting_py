"""Per-combo quality scoring against configurable thresholds."""

from __future__ import annotations

import math

import pandas as pd

from strategy_evaluation.config import RobustnessConfig


def passes_thresholds(row: pd.Series, cfg: RobustnessConfig) -> bool:
    """Return True if a single combo row meets all minimum thresholds.

    NaN values in any *required* metric cause the row to fail so that
    combos with no trades (all-NaN metrics) are excluded automatically.
    Max drawdown is enforced only when the value is present (not NaN) so
    that older CSVs without that column are not silently rejected.
    """
    def _val(col: str) -> float:
        v = row.get(col, float("nan"))
        return float("nan") if pd.isna(v) else float(v)

    sqn      = _val(cfg.col_sqn)
    pf       = _val(cfg.col_pf)
    trades   = _val(cfg.col_trades)
    win_rate = _val(cfg.col_win_rate)
    sharpe   = _val(cfg.col_sharpe)
    max_dd   = _val(cfg.col_max_drawdown)

    # Required metrics — any NaN → fail
    if any(math.isnan(x) for x in [sqn, pf, trades, win_rate, sharpe]):
        return False

    passes = (
        sqn    >= cfg.min_sqn
        and pf >= cfg.min_profit_factor
        and trades >= cfg.min_trades
        and win_rate >= cfg.min_win_rate
        and sharpe >= cfg.min_sharpe
    )

    # Max drawdown gate is optional: only enforced when column is present
    if passes and not math.isnan(max_dd):
        passes = max_dd <= cfg.max_max_drawdown

    return passes


def score_combo(row: pd.Series, cfg: RobustnessConfig) -> float:
    """Return a composite 0–1 score for a single combo row.

    Components: SQN, Profit Factor, Expectancy, Sharpe, Max Drawdown
    (inverted), Calmar Ratio.  Win rate and trade count are pass/fail
    gates only and do not contribute to the score.

    Each metric is normalised to [0, 1] before weighting.  Values above
    the ceiling clip to 1.0; values below the floor clip to 0.0.  The
    drawdown component is inverted so a lower drawdown scores higher.
    Missing metrics (NaN) contribute 0 for that component.
    """
    def _norm(value: float, minimum: float, ceiling: float) -> float:
        if math.isnan(value):
            return 0.0
        return max(0.0, min(1.0, (value - minimum) / (ceiling - minimum)))

    def _get(col: str) -> float:
        v = row.get(col, float("nan"))
        return float("nan") if pd.isna(v) else float(v)

    sqn        = _get(cfg.col_sqn)
    pf         = _get(cfg.col_pf)
    expectancy = _get(cfg.col_expectancy)
    sharpe     = _get(cfg.col_sharpe)
    max_dd     = _get(cfg.col_max_drawdown)
    calmar     = _get(cfg.col_calmar)

    components = {
        "sqn":           _norm(sqn,        0.0, 3.0),
        "profit_factor": _norm(pf,         1.0, 4.0),
        "expectancy":    _norm(expectancy, 0.0, 5.0),
        "sharpe":        _norm(sharpe,     0.0, 2.0),
        # Inverted: lower drawdown → higher score; clipped by _norm already
        "max_drawdown":  1.0 - _norm(max_dd, 0.0, 60.0),
        "calmar":        _norm(calmar,     0.0, 5.0),
    }

    return sum(cfg.weights[k] * v for k, v in components.items())


def annotate_dataframe(df: pd.DataFrame, cfg: RobustnessConfig) -> pd.DataFrame:
    """Add `_passes` and `_score` columns to *df* in-place and return it."""
    df = df.copy()
    df["_passes"] = df.apply(passes_thresholds, axis=1, cfg=cfg)
    df["_score"]  = df.apply(score_combo,       axis=1, cfg=cfg)
    return df
