"""Scoring and pass/fail logic for bear strategy sweep results.

Only metrics that directly indicate whether the strategy has an edge are used.
Decorative ratios (R:R, Omega) are excluded.

Scoring formula (0–1 composite, weights sum to 1.0)
----------------------------------------------------
  SQN           30 %   captures both edge size and trade count
  Profit Factor 25 %   gross edge — wins vs losses in $ terms
  Expectancy %  25 %   per-trade average outcome
  Sharpe Ratio  10 %   consistency of returns over time
  Max Drawdown  10 %   practical survivability (inverted)

A row "passes" when ALL four hard gates are met:
  SQN ≥ min_sqn, PF ≥ min_pf, trades ≥ min_trades, WR ≥ min_wr
"""

from __future__ import annotations

import math

import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# Default gate thresholds (overridable at call sites)
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_MIN_SQN:    float = 0.0
DEFAULT_MIN_PF:     float = 1.0
DEFAULT_MIN_TRADES: int   = 10
DEFAULT_MIN_WR:     float = 0.0

# Normalisation ceilings — values above are capped at 1.0
_SQN_CEIL = 3.0
_PF_CEIL  = 4.0
_EXP_CEIL = 5.0   # Expectancy %
_SH_CEIL  = 2.0   # Sharpe Ratio
_DD_CEIL  = 60.0  # Max Drawdown % (inverted)

# Scoring weights
_W_SQN = 0.30
_W_PF  = 0.25
_W_EXP = 0.25
_W_SH  = 0.10
_W_DD  = 0.10


# ─────────────────────────────────────────────────────────────────────────────
# Public helpers
# ─────────────────────────────────────────────────────────────────────────────

def score_row(row: pd.Series) -> float:
    """Return a 0–1 composite edge score for a single pair/combo row."""
    def _g(col: str) -> float:
        v = row.get(col, float("nan"))
        return float("nan") if pd.isna(v) else float(v)

    sqn = _g("SQN")
    pf  = _g("Profit Factor")
    exp = _g("Expectancy [%]")
    sh  = _g("Sharpe Ratio")
    dd  = _g("Max. Drawdown [%]")

    return (
        _W_SQN * _norm(sqn,  0.0, _SQN_CEIL)
        + _W_PF  * _norm(pf,  1.0, _PF_CEIL)
        + _W_EXP * _norm(exp, 0.0, _EXP_CEIL)
        + _W_SH  * _norm(sh,  0.0, _SH_CEIL)
        + _W_DD  * (1.0 - _norm(dd, 0.0, _DD_CEIL))
    )


def passes_gates(
    row: pd.Series,
    min_sqn:    float = DEFAULT_MIN_SQN,
    min_pf:     float = DEFAULT_MIN_PF,
    min_trades: int   = DEFAULT_MIN_TRADES,
    min_wr:     float = DEFAULT_MIN_WR,
) -> bool:
    """Return True when the row clears ALL hard pass/fail gates."""
    def _g(col: str) -> float:
        v = row.get(col, float("nan"))
        return float("nan") if pd.isna(v) else float(v)

    sqn    = _g("SQN")
    pf     = _g("Profit Factor")
    trades = _g("# Trades")
    wr     = _g("Win Rate [%]")

    if any(math.isnan(x) for x in [sqn, pf, trades, wr]):
        return False
    return (
        sqn    >= min_sqn
        and pf >= min_pf
        and trades >= min_trades
        and wr >= min_wr
    )


def combo_label(
    sl: float,
    tp: float,
    exit_mode: str = "fixed_tp",
    exit_rsi_level:     float | None = None,
    rsi_oversold_level: float | None = None,
    exit_ema_period:    int   | None = None,
) -> str:
    """Short human-readable label for a sweep combo."""
    label = f"SL={sl:.1f}× TP={tp:.1f}×"
    if exit_mode == "fixed_tp":
        return label

    _MODE_SHORT = {
        "fixed_tp_or_rsi_cross_up": "tp+rsi↑",
        "rsi_cross_up":             "rsi↑",
        "macd_hist_cross_zero":     "macd_hist",
        "rsi_oversold":             "rsi_os",
        "ema_reclaim":              "ema_rec",
        "funding_regime_shift":     "fund_flip",
    }
    suffix = _MODE_SHORT.get(exit_mode, exit_mode)
    label += f" | {suffix}"

    if exit_rsi_level is not None:
        label += f"@{exit_rsi_level:.0f}"
    elif rsi_oversold_level is not None:
        label += f"@{rsi_oversold_level:.0f}"
    elif exit_ema_period is not None:
        label += f"({exit_ema_period})"

    return label


# ─────────────────────────────────────────────────────────────────────────────
# Internal helper
# ─────────────────────────────────────────────────────────────────────────────

def _norm(v: float, lo: float, hi: float) -> float:
    if math.isnan(v):
        return 0.0
    return max(0.0, min(1.0, (v - lo) / (hi - lo)))
