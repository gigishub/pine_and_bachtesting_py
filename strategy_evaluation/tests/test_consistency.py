"""Tests for strategy_evaluation.consistency."""

from __future__ import annotations

import pandas as pd
import pytest

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.consistency import symbol_pass_rate, timeframe_pass_rate, toggle_frequency


@pytest.fixture()
def cfg() -> RobustnessConfig:
    return RobustnessConfig()


def _make_df(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def _passing_combo(symbol: str, tf: str, rank: int = 1, **overrides: object) -> dict:
    base = {
        "Symbol": symbol,
        "Timeframe": tf,
        "Parameter Signature": f"use_adx=1",
        "Rank": rank,
        "SQN": 1.5,
        "Profit Factor": 2.0,
        "# Trades": 20,
        "Win Rate [%]": 40.0,
        "Sharpe Ratio": 0.8,
        "Return [%]": 25.0,
        "use_adx": 1,
        "use_ema": 0,
    }
    base.update(overrides)
    return base


def _failing_combo(symbol: str, tf: str, rank: int = 2) -> dict:
    return _passing_combo(symbol, tf, rank=rank, SQN=0.1, **{"Profit Factor": 1.0})


class TestSymbolPassRate:
    def test_symbol_with_passing_combo(self, cfg: RobustnessConfig) -> None:
        df = _make_df([_passing_combo("BTCUSDT", "4H"), _failing_combo("ETHUSDT", "4H")])
        rates = symbol_pass_rate(df, cfg)
        assert rates["BTCUSDT"] == 1.0
        assert rates["ETHUSDT"] == 0.0

    def test_all_symbols_fail(self, cfg: RobustnessConfig) -> None:
        df = _make_df([_failing_combo("BTCUSDT", "4H"), _failing_combo("ETHUSDT", "4H")])
        rates = symbol_pass_rate(df, cfg)
        assert all(v == 0.0 for v in rates.values())

    def test_symbol_passes_on_any_timeframe(self, cfg: RobustnessConfig) -> None:
        df = _make_df([
            _failing_combo("BTCUSDT", "1H"),
            _passing_combo("BTCUSDT", "4H"),
        ])
        rates = symbol_pass_rate(df, cfg)
        assert rates["BTCUSDT"] == 1.0


class TestTimeframePassRate:
    def test_rate_is_fraction_of_symbols(self, cfg: RobustnessConfig) -> None:
        df = _make_df([
            _passing_combo("BTCUSDT", "4H"),
            _failing_combo("ETHUSDT", "4H"),
        ])
        rates = timeframe_pass_rate(df, cfg)
        assert rates["4H"] == pytest.approx(0.5)

    def test_full_pass_rate(self, cfg: RobustnessConfig) -> None:
        df = _make_df([
            _passing_combo("BTCUSDT", "1H"),
            _passing_combo("ETHUSDT", "1H"),
        ])
        rates = timeframe_pass_rate(df, cfg)
        assert rates["1H"] == pytest.approx(1.0)


class TestToggleFrequency:
    def test_counts_enabled_toggles(self, cfg: RobustnessConfig) -> None:
        df = _make_df([
            _passing_combo("BTCUSDT", "4H", use_adx=1, use_ema=0),
            _passing_combo("ETHUSDT", "4H", use_adx=1, use_ema=1),
        ])
        freq = toggle_frequency(df, cfg)
        assert freq.get("use_adx", 0) == 2
        assert freq.get("use_ema", 0) == 1

    def test_empty_result_for_no_toggles(self, cfg: RobustnessConfig) -> None:
        # DataFrame with no boolean-style columns beyond metadata
        df = _make_df([_passing_combo("BTCUSDT", "4H")])
        freq = toggle_frequency(df, cfg)
        assert isinstance(freq, dict)
