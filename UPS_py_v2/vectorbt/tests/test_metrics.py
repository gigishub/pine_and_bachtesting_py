"""Tests for vectorbt/metrics.py.

Verifies that extract_stats() returns a pd.Series with the correct keys
and sensible numeric values.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest

from UPS_py_v2.strategy.strategy_parameters import StrategySettings
from UPS_py_v2.vectorbt.metrics import extract_stats
from UPS_py_v2.vectorbt.runner import run


def _make_ohlcv(n: int = 400, seed: int = 99) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    close = np.cumprod(1 + rng.normal(0, 0.01, n)) * 30_000.0
    high = close * (1 + rng.uniform(0.001, 0.015, n))
    low = close * (1 - rng.uniform(0.001, 0.015, n))
    open_ = close * (1 + rng.normal(0, 0.005, n))
    volume = rng.uniform(1_000, 100_000, n)
    idx = pd.date_range("2023-01-01", periods=n, freq="1h")
    return pd.DataFrame(
        {"Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume},
        index=idx,
    )


REQUIRED_KEYS = [
    "Return [%]",
    "Expectancy [%]",
    "Profit Factor",
    "Win Rate [%]",
    "Max. Drawdown [%]",
    "# Trades",
    "SQN",
    "Avg. Trade [%]",
    "Best Trade [%]",
    "Worst Trade [%]",
    "Avg. Win Trade [%]",
    "Avg. Loss Trade [%]",
    "Max. Drawdown Duration",
    "Sharpe Ratio",
    "Calmar Ratio",
]


class TestExtractStatsKeys:
    def test_has_all_required_keys(self):
        df = _make_ohlcv()
        pf = run(df)
        stats = extract_stats(pf)
        for key in REQUIRED_KEYS:
            assert key in stats.index, f"Missing key: {key}"

    def test_returns_pandas_series(self):
        df = _make_ohlcv()
        pf = run(df)
        stats = extract_stats(pf)
        assert isinstance(stats, pd.Series)


class TestExtractStatsValues:
    def test_n_trades_is_non_negative_int(self):
        df = _make_ohlcv()
        pf = run(df)
        stats = extract_stats(pf)
        n = stats.get("# Trades")
        assert isinstance(n, int)
        assert n >= 0

    def test_win_rate_in_valid_range(self):
        df = _make_ohlcv()
        pf = run(df)
        stats = extract_stats(pf)
        wr = float(stats.get("Win Rate [%]"))
        if not math.isnan(wr):
            assert 0.0 <= wr <= 100.0

    def test_max_drawdown_non_negative(self):
        df = _make_ohlcv()
        pf = run(df)
        stats = extract_stats(pf)
        dd = float(stats.get("Max. Drawdown [%]"))
        if not math.isnan(dd):
            assert dd >= 0.0

    def test_expectancy_matches_formula(self):
        """Expectancy [%] = wr * avg_win + (1 - wr) * avg_loss."""
        df = _make_ohlcv()
        pf = run(df)
        stats = extract_stats(pf)

        wr = float(stats.get("Win Rate [%]"))
        avg_win = float(stats.get("Avg. Win Trade [%]"))
        avg_loss = float(stats.get("Avg. Loss Trade [%]"))
        exp = float(stats.get("Expectancy [%]"))

        if any(math.isnan(v) for v in (wr, avg_win, avg_loss, exp)):
            pytest.skip("Not enough data for expectancy check")

        expected = (wr / 100.0) * avg_win + (1.0 - wr / 100.0) * avg_loss
        assert abs(exp - expected) < 1e-9

    def test_no_trades_gives_zero_count(self):
        """When no entries fire, trade count should be 0."""
        df = _make_ohlcv(n=50)  # too short for signals to warm up
        s = StrategySettings(ma_length=200)  # MA won't compute on short data
        pf = run(df, s)
        stats = extract_stats(pf)
        assert stats.get("# Trades") == 0
