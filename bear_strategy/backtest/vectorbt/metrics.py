"""Metric extraction for Bear Strategy vbt Portfolio objects.

Bridges vbt.Portfolio.stats() key names to the standardised set used by
backtesting.py so both engines produce comparable pd.Series outputs.

| backtesting.py key        | vbt key                  | Notes                    |
|---------------------------|--------------------------|--------------------------|
| Return [%]                | Total Return [%]         | renamed                  |
| Expectancy [%]            | (not in vbt)             | computed: wr×avg_win + (1-wr)×avg_loss |
| Max. Drawdown [%]         | Max Drawdown [%]         | dot removed in vbt       |
| # Trades                  | Total Closed Trades      | renamed                  |
| SQN                       | (not in vbt)             | computed from per-trade R |
| R:R Ratio                 | (not in vbt)             | avg_win / |avg_loss|      |
| Recovery Factor           | (not in vbt)             | Return / Max Drawdown     |
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd


def extract_stats(pf) -> pd.Series:
    """Extract standardised metrics from a vbt.Portfolio.

    Returns pd.Series with the same keys as backtesting.py's Backtest.run() output,
    plus additional metrics useful for edge analysis.
    """
    raw = pf.stats()

    def _f(key: str) -> float:
        try:
            return float(raw.get(key, math.nan))
        except (TypeError, ValueError):
            return math.nan

    def _i(key: str) -> int:
        v = _f(key)
        return 0 if math.isnan(v) else int(v)

    win_rate = _f("Win Rate [%]")
    avg_win  = _f("Avg Winning Trade [%]")
    avg_loss = _f("Avg Losing Trade [%]")
    ret      = _f("Total Return [%]")
    max_dd   = _f("Max Drawdown [%]")

    # Expectancy: E = wr × avg_win + (1 − wr) × avg_loss  (avg_loss typically negative)
    if not any(math.isnan(v) for v in (win_rate, avg_win, avg_loss)):
        wr = win_rate / 100.0
        expectancy_pct = wr * avg_win + (1.0 - wr) * avg_loss
    else:
        expectancy_pct = math.nan

    # R:R Ratio: average win / |average loss|  (> 1 means winners larger than losers)
    if not math.isnan(avg_win) and not math.isnan(avg_loss) and avg_loss != 0:
        rr_ratio = avg_win / abs(avg_loss)
    else:
        rr_ratio = math.nan

    # Recovery Factor: total return / max drawdown  (how much gain per unit of max pain)
    if not math.isnan(ret) and not math.isnan(max_dd) and max_dd != 0:
        recovery_factor = ret / max_dd
    else:
        recovery_factor = math.nan

    return pd.Series({
        # ── Core performance ────────────────────────────────────────────────
        "Return [%]":             ret,
        "Expectancy [%]":         expectancy_pct,
        "Profit Factor":          _f("Profit Factor"),
        "Win Rate [%]":           win_rate,
        "# Trades":               _i("Total Closed Trades"),
        # ── Risk / drawdown ─────────────────────────────────────────────────
        "Max. Drawdown [%]":      max_dd,
        "Recovery Factor":        recovery_factor,
        # ── Risk-adjusted returns ────────────────────────────────────────────
        "SQN":                    _compute_sqn(pf),
        "Sharpe Ratio":           _f("Sharpe Ratio"),
        "Sortino Ratio":          _f("Sortino Ratio"),
        "Calmar Ratio":           _f("Calmar Ratio"),
        "Omega Ratio":            _f("Omega Ratio"),
        # ── Trade quality ────────────────────────────────────────────────────
        "R:R Ratio":              rr_ratio,
        "Avg. Win Trade [%]":     avg_win,
        "Avg. Loss Trade [%]":    avg_loss,
        "Best Trade [%]":         _f("Best Trade [%]"),
        "Worst Trade [%]":        _f("Worst Trade [%]"),
        # ── Misc ─────────────────────────────────────────────────────────────
        "Exposure Time [%]":      math.nan,   # not meaningful for short-only crypto
        "Max. Drawdown Duration": str(raw.get("Max Drawdown Duration", "")),
    })


def _compute_sqn(pf) -> float:
    """SQN = sqrt(n) × mean(R) / std(R)  where R is per-trade return in %."""
    try:
        rets = pf.trades.returns.values * 100.0
        n    = len(rets)
        if n < 2:
            return math.nan
        mean_r = float(np.mean(rets))
        std_r  = float(np.std(rets, ddof=1))
        if std_r == 0.0:
            return math.nan
        return float(math.sqrt(n) * mean_r / std_r)
    except Exception:
        return math.nan
