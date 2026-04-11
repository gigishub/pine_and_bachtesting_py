"""Tests for strategy_evaluation.metrics."""

from __future__ import annotations

import math

import pandas as pd
import pytest

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.metrics import annotate_dataframe, passes_thresholds, score_combo


@pytest.fixture()
def cfg() -> RobustnessConfig:
    return RobustnessConfig()


def _row(**kwargs: object) -> pd.Series:
    defaults = {
        "SQN": 1.5,
        "Profit Factor": 2.0,
        "# Trades": 20,
        "Win Rate [%]": 40.0,
        "Sharpe Ratio": 0.8,
        "Return [%]": 25.0,
    }
    defaults.update(kwargs)
    return pd.Series(defaults)


class TestPassesThresholds:
    def test_passing_row(self, cfg: RobustnessConfig) -> None:
        assert passes_thresholds(_row(), cfg) is True

    def test_fails_on_low_sqn(self, cfg: RobustnessConfig) -> None:
        assert passes_thresholds(_row(SQN=0.5), cfg) is False

    def test_fails_on_low_profit_factor(self, cfg: RobustnessConfig) -> None:
        assert passes_thresholds(_row(**{"Profit Factor": 1.0}), cfg) is False

    def test_fails_on_too_few_trades(self, cfg: RobustnessConfig) -> None:
        assert passes_thresholds(_row(**{"# Trades": 5}), cfg) is False

    def test_fails_on_nan_sqn(self, cfg: RobustnessConfig) -> None:
        assert passes_thresholds(_row(SQN=float("nan")), cfg) is False

    def test_fails_on_zero_trades(self, cfg: RobustnessConfig) -> None:
        assert passes_thresholds(_row(**{"# Trades": 0}), cfg) is False


class TestScoreCombo:
    def test_score_range(self, cfg: RobustnessConfig) -> None:
        score = score_combo(_row(), cfg)
        assert 0.0 <= score <= 1.0

    def test_better_row_scores_higher(self, cfg: RobustnessConfig) -> None:
        good = score_combo(_row(SQN=2.5, **{"Profit Factor": 3.5, "Sharpe Ratio": 1.5}), cfg)
        bad = score_combo(_row(SQN=0.2, **{"Profit Factor": 1.1, "Sharpe Ratio": 0.1}), cfg)
        assert good > bad

    def test_nan_scores_zero_for_component(self, cfg: RobustnessConfig) -> None:
        score = score_combo(_row(SQN=float("nan")), cfg)
        assert not math.isnan(score)
        assert score < score_combo(_row(), cfg)


class TestAnnotateDataframe:
    def test_adds_passes_and_score_columns(self, cfg: RobustnessConfig) -> None:
        df = pd.DataFrame([_row().to_dict(), _row(SQN=0.1).to_dict()])
        result = annotate_dataframe(df, cfg)
        assert "_passes" in result.columns
        assert "_score" in result.columns

    def test_passes_column_correct(self, cfg: RobustnessConfig) -> None:
        df = pd.DataFrame([_row().to_dict(), _row(SQN=0.1).to_dict()])
        result = annotate_dataframe(df, cfg)
        assert result["_passes"].tolist() == [True, False]
