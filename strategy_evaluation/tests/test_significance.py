"""Tests for strategy_evaluation.significance (OLS regression)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.significance import OLSResult, compute_ols_significance


def _make_df(n: int = 200, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    toggle_a = rng.integers(0, 2, n).astype(float)
    toggle_b = rng.integers(0, 2, n).astype(float)
    toggle_c = rng.integers(0, 2, n).astype(float)
    # toggle_a strongly positive, toggle_b mildly negative, toggle_c pure noise
    sqn = 1.2 * toggle_a - 0.5 * toggle_b + 0.05 * toggle_c + rng.normal(0, 0.2, n)
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


class TestComputeOLSSignificance:
    def test_returns_ols_result(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_ols_significance(sample_df, cfg)
        assert isinstance(result, OLSResult)

    def test_table_has_required_columns(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_ols_significance(sample_df, cfg)
        assert result is not None
        expected = {"toggle", "coefficient", "std_err", "t_stat", "p_value", "significant"}
        assert expected.issubset(set(result.table.columns))

    def test_all_toggles_in_table(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_ols_significance(sample_df, cfg)
        assert result is not None
        assert set(result.table["toggle"]) == {"toggle_a", "toggle_b", "toggle_c"}

    def test_p_values_in_0_1(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_ols_significance(sample_df, cfg)
        assert result is not None
        assert (result.table["p_value"] >= 0).all()
        assert (result.table["p_value"] <= 1).all()

    def test_significant_column_is_bool(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_ols_significance(sample_df, cfg)
        assert result is not None
        assert result.table["significant"].dtype == bool

    def test_toggle_a_significant_positive(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        """toggle_a has a large positive coefficient → should be significant and positive."""
        result = compute_ols_significance(sample_df, cfg)
        assert result is not None
        row = result.table[result.table["toggle"] == "toggle_a"].iloc[0]
        assert row["coefficient"] > 0
        assert row["significant"] is True or row["p_value"] < 0.05

    def test_toggle_b_significant_negative(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        """toggle_b has a negative coefficient → should be negative."""
        result = compute_ols_significance(sample_df, cfg)
        assert result is not None
        row = result.table[result.table["toggle"] == "toggle_b"].iloc[0]
        assert row["coefficient"] < 0

    def test_r_squared_in_range(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_ols_significance(sample_df, cfg)
        assert result is not None
        assert 0.0 <= result.r_squared <= 1.0

    def test_n_combos_matches_rows(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_ols_significance(sample_df, cfg)
        assert result is not None
        assert result.n_combos == len(sample_df)

    def test_returns_none_when_too_few_rows(self, cfg: RobustnessConfig) -> None:
        df = _make_df(n=10)
        result = compute_ols_significance(df, cfg)
        assert result is None

    def test_returns_none_when_no_toggle_cols(self, cfg: RobustnessConfig) -> None:
        df = pd.DataFrame({"Symbol": ["BTC"] * 50, "SQN": [1.0] * 50})
        result = compute_ols_significance(df, cfg)
        assert result is None

    def test_returns_none_on_missing_target(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_ols_significance(sample_df, cfg, target_col="NonExistent")
        assert result is None

    def test_table_sorted_by_p_value(self, sample_df: pd.DataFrame, cfg: RobustnessConfig) -> None:
        result = compute_ols_significance(sample_df, cfg)
        assert result is not None
        p_vals = result.table["p_value"].values
        assert all(p_vals[i] <= p_vals[i + 1] for i in range(len(p_vals) - 1))
