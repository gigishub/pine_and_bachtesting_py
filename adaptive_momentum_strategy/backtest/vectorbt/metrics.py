"""Metric extraction for vbt Portfolio objects.

WHY THIS FILE EXISTS
--------------------
vbt.Portfolio.stats() uses different key names than backtesting.py.
This module bridges the gap so both engines produce pd.Series with identical
keys, letting the pipeline code process results from either engine unchanged.

KEY DIFFERENCES
---------------
| backtesting.py key        | vbt key                  | Notes                    |
|---------------------------|--------------------------|--------------------------|
| Return [%]                | Total Return [%]         | renamed                  |
| Expectancy [%]            | (not in vbt)             | computed from wr/avg     |
| Max. Drawdown [%]         | Max Drawdown [%]         | dot removed in vbt       |
| # Trades                  | Total Closed Trades      | renamed                  |
| SQN                       | (not in vbt)             | computed from trades     |
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd


def extract_stats(pf) -> pd.Series:
    """Extract standardised metrics from a vbt.Portfolio.

    Returns pd.Series with same keys as backtesting.py's Backtest.run() output.
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

    # E = wr * avg_win + (1 - wr) * avg_loss  (avg_loss is negative)
    if not any(math.isnan(v) for v in (win_rate, avg_win, avg_loss)):
        wr = win_rate / 100.0
        expectancy_pct = wr * avg_win + (1.0 - wr) * avg_loss
    else:
        expectancy_pct = math.nan

    return pd.Series({
        "Return [%]":             _f("Total Return [%]"),
        "Expectancy [%]":         expectancy_pct,
        "Profit Factor":          _f("Profit Factor"),
        "Win Rate [%]":           win_rate,
        "Max. Drawdown [%]":      _f("Max Drawdown [%]"),
        "# Trades":               _i("Total Closed Trades"),
        "SQN":                    _compute_sqn(pf),
        "Avg. Trade [%]":         expectancy_pct,
        "Best Trade [%]":         _f("Best Trade [%]"),
        "Worst Trade [%]":        _f("Worst Trade [%]"),
        "Avg. Win Trade [%]":     avg_win,
        "Avg. Loss Trade [%]":    avg_loss,
        "Max. Drawdown Duration": str(raw.get("Max Drawdown Duration", "")),
        "Exposure Time [%]":      math.nan,
        "Sharpe Ratio":           _f("Sharpe Ratio"),
        "Calmar Ratio":           _f("Calmar Ratio"),
    })


def _compute_sqn(pf) -> float:
    """SQN = sqrt(n) * mean(R) / std(R) where R is per-trade return in %."""
    try:
        rets = pf.trades.returns.values * 100.0
        n = len(rets)
        if n < 2:
            return math.nan
        mean_r = float(np.mean(rets))
        std_r  = float(np.std(rets, ddof=1))
        if std_r == 0.0:
            return math.nan
        return float(math.sqrt(n) * mean_r / std_r)
    except Exception:
        return math.nan
