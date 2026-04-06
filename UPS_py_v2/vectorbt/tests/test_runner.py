"""Tests for vectorbt/runner.py.

Smoke tests that the runner returns a vbt.Portfolio with expected properties.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
import vectorbt as vbt

from UPS_py_v2.strategy.strategy_parameters import StrategySettings
from UPS_py_v2.vectorbt.runner import run


def _make_ohlcv(n: int = 400, seed: int = 7) -> pd.DataFrame:
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


class TestRunnerReturnsPortfolio:
    def test_returns_vbt_portfolio(self):
        df = _make_ohlcv()
        pf = run(df)
        assert isinstance(pf, vbt.Portfolio)

    def test_stats_has_required_keys(self):
        df = _make_ohlcv()
        pf = run(df)
        stats = pf.stats()
        required = {"Total Return [%]", "Win Rate [%]", "Profit Factor", "Max Drawdown [%]"}
        for key in required:
            assert key in stats.index, f"Missing stat key: {key}"

    def test_runs_with_custom_settings(self):
        df = _make_ohlcv()
        s = StrategySettings(
            ma_length=20,
            use_iq_filter=False,
            risk_reward_multiplier=2.0,
            stop_multiplier=1.5,
        )
        pf = run(df, s)
        assert isinstance(pf, vbt.Portfolio)

    def test_runs_with_short_trades_only(self):
        df = _make_ohlcv()
        s = StrategySettings(long_trades=False, short_trades=True)
        pf = run(df, s)
        assert isinstance(pf, vbt.Portfolio)

    def test_runs_with_long_trades_only(self):
        df = _make_ohlcv()
        s = StrategySettings(long_trades=True, short_trades=False)
        pf = run(df, s)
        assert isinstance(pf, vbt.Portfolio)


class TestRunnerFinancials:
    def test_start_value_matches_init_cash(self):
        df = _make_ohlcv()
        pf = run(df, init_cash=10_000.0)
        assert float(pf.stats().get("Start Value")) == pytest.approx(10_000.0)

    def test_end_value_is_positive(self):
        df = _make_ohlcv()
        pf = run(df)
        assert float(pf.stats().get("End Value")) > 0

    def test_custom_fees(self):
        df = _make_ohlcv()
        pf_cheap = run(df, fees=0.0)
        pf_expensive = run(df, fees=0.01)
        # Higher fees → lower or equal end value
        ev_cheap = float(pf_cheap.stats().get("End Value"))
        ev_expensive = float(pf_expensive.stats().get("End Value"))
        assert ev_cheap >= ev_expensive
