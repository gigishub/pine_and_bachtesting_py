"""Metric extraction for vbt Portfolio objects.

WHY THIS FILE EXISTS
--------------------
vbt.Portfolio.stats() uses different key names than backtesting.py's Backtest.run()
output.  This module bridges the gap so both engines produce pd.Series objects with
identical keys, allowing the same robustness pipeline code to process results from
either engine without modification.

KEY DIFFERENCES FROM backtesting.py stats
------------------------------------------
| backtesting.py key        | vbt key                  | Notes                      |
|---------------------------|--------------------------|----------------------------|
| Return [%]                | Total Return [%]         | renamed                    |
| Expectancy [%]            | (not in vbt)             | computed here from wr/avg  |
| Max. Drawdown [%]         | Max Drawdown [%]         | dot removed in vbt         |
| # Trades                  | Total Closed Trades      | renamed                    |
| SQN                       | (not in vbt)             | computed here from trades  |
| Avg. Trade [%]            | (not in vbt)             | same formula as Expectancy |
| Avg. Win Trade [%]        | Avg Winning Trade [%]    | renamed                    |
| Avg. Loss Trade [%]       | Avg Losing Trade [%]     | renamed                    |
| Exposure Time [%]         | (not directly exposed)   | returned as NaN            |
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd


def extract_stats(pf) -> pd.Series:
    """Extract standardised metrics from a vbt.Portfolio.

    Maps vbt stat keys to the same column names produced by backtesting.py's
    Backtest.run(), so both engines feed into the same robustness pipeline
    without any changes to pipeline.py or reporter.py.

    Returns a pd.Series — behaves like a dict for .get() calls in _build_row().
    """
    raw = pf.stats()

    def _f(key: str) -> float:
        """Read a float from the vbt stats Series; return NaN if missing or non-numeric."""
        try:
            return float(raw.get(key, math.nan))
        except (TypeError, ValueError):
            return math.nan

    def _i(key: str) -> int:
        """Read an int from the vbt stats Series; return 0 if missing (0 trades is valid)."""
        v = _f(key)
        return 0 if math.isnan(v) else int(v)

    win_rate = _f("Win Rate [%]")
    avg_win = _f("Avg Winning Trade [%]")    # vbt name differs from backtesting.py
    avg_loss = _f("Avg Losing Trade [%]")    # vbt name differs from backtesting.py

    # vbt does not expose Expectancy [%] directly, so we compute it from the
    # component parts using the same formula backtesting.py uses:
    #   E = win_rate * avg_win_pct + (1 - win_rate) * avg_loss_pct
    # avg_loss is negative, so profitable strategies have E > 0.
    if not any(math.isnan(v) for v in (win_rate, avg_win, avg_loss)):
        wr = win_rate / 100.0
        expectancy_pct = wr * avg_win + (1.0 - wr) * avg_loss
    else:
        expectancy_pct = math.nan

    # backtesting.py reports Avg. Trade [%] which is mathematically identical to Expectancy
    avg_trade_pct = expectancy_pct

    return pd.Series({
        # --- Core metrics (drive ranking in pipeline._rank_results()) ---
        "Return [%]":         _f("Total Return [%]"),   # vbt: "Total Return [%]"
        "Expectancy [%]":     expectancy_pct,            # computed — not in vbt
        "Profit Factor":      _f("Profit Factor"),
        "Win Rate [%]":       win_rate,
        # backtesting.py uses "Max. Drawdown [%]" with a dot; we replicate that key
        # so pipeline._build_row() picks it up with stats.get("Max. Drawdown [%]")
        "Max. Drawdown [%]":  _f("Max Drawdown [%]"),   # vbt: "Max Drawdown [%]" (no dot)
        "# Trades":           _i("Total Closed Trades"), # vbt: "Total Closed Trades"
        "SQN":                _compute_sqn(pf),          # computed — not in vbt
        # --- Extended stats (saved to CSV for manual inspection) ---
        "Avg. Trade [%]":         avg_trade_pct,
        "Best Trade [%]":         _f("Best Trade [%]"),
        "Worst Trade [%]":        _f("Worst Trade [%]"),
        "Avg. Win Trade [%]":     avg_win,
        "Avg. Loss Trade [%]":    avg_loss,
        "Max. Drawdown Duration": str(raw.get("Max Drawdown Duration", "")),
        "Exposure Time [%]":      math.nan,  # not directly exposed by vbt.stats()
        "Sharpe Ratio":           _f("Sharpe Ratio"),
        "Calmar Ratio":           _f("Calmar Ratio"),
    })


def _compute_sqn(pf) -> float:
    """Compute System Quality Number from individual trade returns.

    SQN = sqrt(n_trades) * mean(R) / std(R)
    where R = per-trade return as a percentage.
    """
    try:
        rets = pf.trades.returns.values * 100.0  # fractional → [%]
        n = len(rets)
        if n < 2:
            return math.nan
        mean_r = float(np.mean(rets))
        std_r = float(np.std(rets, ddof=1))
        if std_r == 0.0:
            return math.nan
        return float(math.sqrt(n) * mean_r / std_r)
    except Exception:
        return math.nan
