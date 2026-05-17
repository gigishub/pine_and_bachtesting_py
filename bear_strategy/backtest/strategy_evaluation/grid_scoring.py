"""Scoring and pass/fail gates for run_grid results (flag-driven bear strategy format).

Column names match the new pipeline._build_row output:
  - "Max Drawdown [%]"  (no dot — distinct from the old sweep format's "Max. Drawdown [%]")
  - "Expectancy [%]", "Sharpe Ratio", "Calmar Ratio"

Scoring formula (0–1 composite, weights sum to 1.0)
----------------------------------------------------
  SQN           30 %  — captures both edge size and trade count
  Profit Factor 25 %  — gross edge in dollar terms
  Expectancy %  25 %  — average per-trade outcome
  Sharpe Ratio  10 %  — consistency of returns
  Max Drawdown  10 %  — survivability (inverted: lower DD scores higher)

Robustness score (cross-symbol, single-TF)
------------------------------------------
  final_score = avg_score × (symbols_passing / N_total)

No timeframe multiplier — the bear strategy runs on a single 1H timeframe.
"""

from __future__ import annotations

import math

import pandas as pd

# ── Gate defaults ──────────────────────────────────────────────────────────────
DEFAULT_MIN_SQN:    float = 0.0
DEFAULT_MIN_PF:     float = 1.0
DEFAULT_MIN_TRADES: int   = 10
DEFAULT_MIN_WR:     float = 0.0
DEFAULT_MAX_DD:     float = 60.0

# ── Score weights ──────────────────────────────────────────────────────────────
_W = {"sqn": 0.30, "pf": 0.25, "exp": 0.25, "sharpe": 0.10, "dd": 0.10}


def _norm(v: float, lo: float, hi: float) -> float:
    if math.isnan(v):
        return 0.0
    return max(0.0, min(1.0, (v - lo) / (hi - lo)))


def _g(row: pd.Series, col: str) -> float:
    v = row.get(col, float("nan"))
    return float("nan") if pd.isna(v) else float(v)


def score_row(row: pd.Series) -> float:
    """0–1 composite edge score for one combo/symbol row."""
    return (
        _W["sqn"]    * _norm(_g(row, "SQN"),              0.0, 3.0)
        + _W["pf"]   * _norm(_g(row, "Profit Factor"),    1.0, 4.0)
        + _W["exp"]  * _norm(_g(row, "Expectancy [%]"),   0.0, 5.0)
        + _W["sharpe"] * _norm(_g(row, "Sharpe Ratio"),   0.0, 2.0)
        + _W["dd"]   * (1.0 - _norm(_g(row, "Max Drawdown [%]"), 0.0, 60.0))
    )


def passes_gates(
    row: pd.Series,
    min_sqn:    float = DEFAULT_MIN_SQN,
    min_pf:     float = DEFAULT_MIN_PF,
    min_trades: int   = DEFAULT_MIN_TRADES,
    min_wr:     float = DEFAULT_MIN_WR,
    max_dd:     float = DEFAULT_MAX_DD,
) -> bool:
    """Return True when all hard pass/fail gates are met."""
    sqn    = _g(row, "SQN")
    pf     = _g(row, "Profit Factor")
    trades = _g(row, "# Trades")
    wr     = _g(row, "Win Rate [%]")
    dd     = _g(row, "Max Drawdown [%]")

    if any(math.isnan(x) for x in [sqn, pf, trades, wr]):
        return False

    ok = (
        sqn    >= min_sqn
        and pf >= min_pf
        and int(trades) >= min_trades
        and wr >= min_wr
    )
    if ok and not math.isnan(dd):
        ok = dd <= max_dd
    return ok


def annotate(
    df: pd.DataFrame,
    min_sqn:    float = DEFAULT_MIN_SQN,
    min_pf:     float = DEFAULT_MIN_PF,
    min_trades: int   = DEFAULT_MIN_TRADES,
    min_wr:     float = DEFAULT_MIN_WR,
    max_dd:     float = DEFAULT_MAX_DD,
) -> pd.DataFrame:
    """Add _passes (bool) and _score (float) columns. Returns a copy."""
    df = df.copy()
    df["_passes"] = df.apply(
        passes_gates, axis=1,
        min_sqn=min_sqn, min_pf=min_pf, min_trades=min_trades,
        min_wr=min_wr, max_dd=max_dd,
    )
    df["_score"] = df.apply(score_row, axis=1)
    return df


def compute_weighted_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Robustness score per signature across symbols (no TF multiplier).

    Formula: final_score = avg_score × (symbols_passing / N_total_symbols)

    Parameters
    ----------
    df : annotated DataFrame (must have _passes and _score columns).

    Returns
    -------
    DataFrame sorted by final_score descending.  Empty if nothing passes.
    """
    if "_passes" not in df.columns or "Parameter Signature" not in df.columns:
        return pd.DataFrame()

    n_total = df["Symbol"].nunique()
    passing = df[df["_passes"]]
    if passing.empty or n_total == 0:
        return pd.DataFrame()

    records: list[dict] = []
    for sig, grp in passing.groupby("Parameter Signature"):
        avg_score = float(grp["_score"].mean())
        n_pass    = int(grp["Symbol"].nunique())
        breadth   = n_pass / n_total
        records.append({
            "Parameter Signature": sig,
            "avg_score":       round(avg_score, 4),
            "symbols_passing": n_pass,
            "N_total":         n_total,
            "breadth":         round(breadth, 4),
            "final_score":     round(avg_score * breadth, 4),
        })

    return (
        pd.DataFrame(records)
        .sort_values("final_score", ascending=False)
        .reset_index(drop=True)
    )
