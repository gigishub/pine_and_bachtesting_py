"""Tests for strategy_evaluation.importance (RF + SHAP)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.importance import (
    ImportanceResult,
    ShapResult,
    compute_shap_importance,
    compute_toggle_importance,
)


def _make_df(n: int = 200, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    toggle_a = rng.integers(0, 2, n).astype(float)
    toggle_b = rng.integers(0, 2, n).astype(float)
    toggle_c = rng.integers(0, 2, n).astype(float)
    # SQN is mostly driven by toggle_a; toggle_b has a clear negative effect
    sqn = 0.8 * toggle_a - 0.6 * toggle_b + 0.05 * toggle_c + rng.normal(0, 0.2, n)
    return pd.DataFrame(
        {
            "Symbol": rng.choice(["BTC", "ETH"], n),
            "Timeframe": rng.choice(["1H", "4H"], n),
            "toggle_a": toggle_a,
            "toggle_b": toggle_b,
            "toggle_c": toggle_c,
            "SQN": sqn,
            "Return [%]": sqn * 5,
            "# Trades": rng.integers(10, 100, n),
        }
    )


@pytest.fixture()
def cfg() -> RobustnessConfig:
    return RobustnessConfig()


@pytest.fixture()
def sample_df() -> pd.DataFrame:
    return _make_df()


class TestComputeToggleImportance:
    def test_returns_importance_result(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_toggle_importance(sample_df, cfg)
        assert isinstance(result, ImportanceResult)

    def test_importances_sum_to_one(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_toggle_importance(sample_df, cfg)
        assert result is not None
        assert abs(result.importances.sum() - 1.0) < 1e-6

    def test_toggle_a_most_important(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        """toggle_a has the highest coefficient → should rank first."""
        result = compute_toggle_importance(sample_df, cfg)
        assert result is not None
        assert result.importances.index[0] == "toggle_a"

    def test_all_toggle_columns_present(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_toggle_importance(sample_df, cfg)
        assert result is not None
        assert set(result.importances.index) == {"toggle_a", "toggle_b", "toggle_c"}

    def test_r2_is_float_in_range(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_toggle_importance(sample_df, cfg)
        assert result is not None
        assert isinstance(result.r2_score, float)
        # OOB R² can be negative for very small datasets; just check it's a number
        assert not np.isnan(result.r2_score)

    def test_n_combos_matches_rows(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_toggle_importance(sample_df, cfg)
        assert result is not None
        assert result.n_combos == len(sample_df)

    def test_custom_target_col(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_toggle_importance(sample_df, cfg, target_col="Return [%]")
        assert result is not None
        assert result.target_col == "Return [%]"

    def test_returns_none_on_missing_target(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_toggle_importance(sample_df, cfg, target_col="NonExistent")
        assert result is None

    def test_returns_none_when_no_toggle_cols(self, cfg: RobustnessConfig) -> None:
        df = pd.DataFrame({"Symbol": ["BTC"] * 50, "SQN": [1.0] * 50})
        result = compute_toggle_importance(df, cfg)
        assert result is None

    def test_returns_none_when_too_few_rows(self, cfg: RobustnessConfig) -> None:
        df = _make_df(n=10)
        result = compute_toggle_importance(df, cfg)
        assert result is None

    def test_importances_sorted_descending(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_toggle_importance(sample_df, cfg)
        assert result is not None
        vals = result.importances.values
        assert all(vals[i] >= vals[i + 1] for i in range(len(vals) - 1))


class TestComputeShapImportance:
    def test_returns_shap_result(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_shap_importance(sample_df, cfg)
        assert isinstance(result, ShapResult)

    def test_mean_shap_index_matches_toggles(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_shap_importance(sample_df, cfg)
        assert result is not None
        assert set(result.mean_shap.index) == {"toggle_a", "toggle_b", "toggle_c"}

    def test_toggle_a_positive_shap(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        """toggle_a has a positive SQN coefficient → mean SHAP should be positive."""
        result = compute_shap_importance(sample_df, cfg)
        assert result is not None
        assert result.mean_shap["toggle_a"] > 0

    def test_toggle_b_negative_shap(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        """toggle_b has a negative SQN coefficient → mean SHAP should be negative."""
        result = compute_shap_importance(sample_df, cfg)
        assert result is not None
        assert result.mean_shap["toggle_b"] < 0

    def test_abs_mean_shap_sorted_descending(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_shap_importance(sample_df, cfg)
        assert result is not None
        vals = result.abs_mean_shap.values
        assert all(vals[i] >= vals[i + 1] for i in range(len(vals) - 1))

    def test_toggle_a_highest_abs_shap(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_shap_importance(sample_df, cfg)
        assert result is not None
        assert result.abs_mean_shap.index[0] == "toggle_a"

    def test_n_combos_matches_rows(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_shap_importance(sample_df, cfg)
        assert result is not None
        assert result.n_combos == len(sample_df)

    def test_returns_none_when_too_few_rows(self, cfg: RobustnessConfig) -> None:
        df = _make_df(n=10)
        result = compute_shap_importance(df, cfg)
        assert result is None

    def test_returns_none_when_no_toggle_cols(self, cfg: RobustnessConfig) -> None:
        df = pd.DataFrame({"Symbol": ["BTC"] * 50, "SQN": [1.0] * 50})
        result = compute_shap_importance(df, cfg)
        assert result is None

    def test_toggle_cols_attribute(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_shap_importance(sample_df, cfg)
        assert result is not None
        assert set(result.toggle_cols) == {"toggle_a", "toggle_b", "toggle_c"}

    def test_mean_and_abs_shap_consistent(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_shap_importance(sample_df, cfg)
        assert result is not None
        for col in result.mean_shap.index:
            assert abs(result.mean_shap[col]) == pytest.approx(
                result.abs_mean_shap.get(col, float("nan")), rel=1e-6
            )
