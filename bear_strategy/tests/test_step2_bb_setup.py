"""Tests for revised Step 2 — Bollinger Band Setup Edge Check.

Four test classes:
    TestBBNoLookahead      — BB computation uses only past/current bar data
    TestPopulationMasks    — mask structure, subsets, and column guards
    TestVerdictThresholdMath — WR lift and PF diff formulas
    TestOutcomeEngine      — deterministic stop/target forward-scan cases
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest

from bear_strategy.hypothesis_tests.setup_bb_edge_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_bb_edge_check.entries import (
    build_population_masks,
)
from bear_strategy.hypothesis_tests.setup_bb_edge_check.run import (
    _min_pf_diff,
    _min_wr_lift,
)
from bear_strategy.hypothesis_tests.setup_bb_edge_check.runner import (
    _compute_outcomes,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_df(
    n: int = 60,
    freq: str = "1h",
    regime_on: bool = True,
    close_val: float = 100.0,
) -> pd.DataFrame:
    """Build a minimal OHLCV + regime + atr DataFrame."""
    idx = pd.date_range("2023-01-01", periods=n, freq=freq)
    closes = np.full(n, close_val)
    df = pd.DataFrame(
        {
            "Open": closes,
            "High": closes + 1.0,
            "Low": closes - 1.0,
            "Close": closes,
            "Volume": np.ones(n) * 1000.0,
            "ema_below_50_regime": np.ones(n, dtype=bool) if regime_on else np.zeros(n, dtype=bool),
            "atr": np.full(n, 2.0),
        },
        index=idx,
    )
    return df


def _make_config(**kwargs) -> TestConfig:
    return TestConfig(**kwargs)


# ---------------------------------------------------------------------------
# 1. No-lookahead tests
# ---------------------------------------------------------------------------


class TestBBNoLookahead:
    def test_bb_does_not_use_future_close(self) -> None:
        """Changing a future close should not affect BB values at past bars."""
        config = _make_config()
        df = _make_df(n=60)

        # Baseline BB masks
        masks_before = build_population_masks(df.copy(), config)
        base_bb_count = masks_before["bb_downtrend"].sum()

        # Alter a future bar only
        df_modified = df.copy()
        df_modified.loc[df_modified.index[-1], "Close"] = 9999.0
        masks_after = build_population_masks(df_modified, config)

        # The last bar's change should NOT affect all earlier bars
        assert (
            masks_before["bb_downtrend"].iloc[:-1].equals(
                masks_after["bb_downtrend"].iloc[:-1]
            )
        ), "Changing the last bar's close modified earlier bb_downtrend values — lookahead detected."

    def test_warmup_bars_excluded_from_all_populations(self) -> None:
        """First bb_period-1 bars must be NaN in BB and absent from all populations."""
        config = _make_config(bb_period=20)
        df = _make_df(n=50)
        masks = build_population_masks(df, config)

        # All populations (including regime_only via bb_ready gate) must have
        # False in the first bb_period - 1 bars
        for name, mask in masks.items():
            warmup_set = mask.iloc[: config.bb_period - 1]
            assert not warmup_set.any(), (
                f"Population '{name}' has True values in warmup period."
            )

    def test_declining_basis_uses_only_previous_bar(self) -> None:
        """bb_declining is True only when BB_basis[t] < BB_basis[t-1]."""
        config = _make_config(bb_period=5)
        n = 30
        idx = pd.date_range("2023-01-01", periods=n, freq="1h")
        # Decreasing closes → basis should be declining at most bars
        closes = np.linspace(110.0, 80.0, n)
        df = pd.DataFrame(
            {
                "Open": closes,
                "High": closes + 1,
                "Low": closes - 1,
                "Close": closes,
                "Volume": np.ones(n),
                "ema_below_50_regime": np.ones(n, dtype=bool),
                "atr": np.full(n, 2.0),
            },
            index=idx,
        )
        masks = build_population_masks(df, config)
        basis = pd.Series(closes, index=idx).rolling(5).mean()
        expected_declining = (basis < basis.shift(1)) & basis.notna()

        # bb_basis_only requires below_basis AND bb_declining — spot-check declining portion
        basis_valid = basis.notna()
        below_basis = pd.Series(closes, index=idx) < basis
        expected_basis_only = (
            pd.Series(np.ones(n, dtype=bool), index=idx)  # regime always on
            & basis_valid
            & below_basis
            & expected_declining
        )
        pd.testing.assert_series_equal(
            masks["bb_basis_only"].rename(None),
            expected_basis_only.rename(None),
            check_names=False,
        )

    def test_atr_ready_excludes_first_bar(self) -> None:
        """First bar has no prev_close so True ATR → regime_only must be False there."""
        config = _make_config(bb_period=5)
        df = _make_df(n=30)
        masks = build_population_masks(df, config)
        # First bar cannot be in any population due to ATR warmup + BB warmup
        assert not masks["regime_only"].iloc[0]


# ---------------------------------------------------------------------------
# 2. Population mask tests
# ---------------------------------------------------------------------------


class TestPopulationMasks:
    def test_bb_downtrend_subset_of_regime_only(self) -> None:
        config = _make_config(bb_period=5)
        df = _make_df(n=40, close_val=90.0)
        masks = build_population_masks(df, config)
        bad = masks["bb_downtrend"] & ~masks["regime_only"]
        assert not bad.any(), "bb_downtrend has bars outside regime_only"

    def test_bb_basis_only_subset_of_regime_only(self) -> None:
        config = _make_config(bb_period=5)
        df = _make_df(n=40, close_val=90.0)
        masks = build_population_masks(df, config)
        bad = masks["bb_basis_only"] & ~masks["regime_only"]
        assert not bad.any(), "bb_basis_only has bars outside regime_only"

    def test_bb_lower_only_subset_of_regime_only(self) -> None:
        config = _make_config(bb_period=5)
        df = _make_df(n=40, close_val=90.0)
        masks = build_population_masks(df, config)
        bad = masks["bb_lower_only"] & ~masks["regime_only"]
        assert not bad.any(), "bb_lower_only has bars outside regime_only"

    def test_bb_downtrend_subset_of_bb_basis_only(self) -> None:
        """bb_downtrend ⊆ bb_basis_only because downtrend requires declining basis + below basis."""
        config = _make_config(bb_period=5)
        n = 60
        idx = pd.date_range("2023-01-01", periods=n, freq="1h")
        closes = np.linspace(110.0, 70.0, n)  # strongly declining to trigger conditions
        df = pd.DataFrame(
            {
                "Open": closes,
                "High": closes + 0.5,
                "Low": closes - 3.0,  # low enough to break lower band
                "Close": closes,
                "Volume": np.ones(n),
                "ema_below_50_regime": np.ones(n, dtype=bool),
                "atr": np.full(n, 1.0),
            },
            index=idx,
        )
        masks = build_population_masks(df, config)
        bad = masks["bb_downtrend"] & ~masks["bb_basis_only"]
        assert not bad.any(), "bb_downtrend is not a subset of bb_basis_only"

    def test_bb_downtrend_subset_of_bb_lower_only(self) -> None:
        """bb_downtrend ⊆ bb_lower_only because downtrend requires close < lower."""
        config = _make_config(bb_period=5)
        n = 60
        idx = pd.date_range("2023-01-01", periods=n, freq="1h")
        closes = np.linspace(110.0, 70.0, n)
        df = pd.DataFrame(
            {
                "Open": closes,
                "High": closes + 0.5,
                "Low": closes - 3.0,
                "Close": closes,
                "Volume": np.ones(n),
                "ema_below_50_regime": np.ones(n, dtype=bool),
                "atr": np.full(n, 1.0),
            },
            index=idx,
        )
        masks = build_population_masks(df, config)
        bad = masks["bb_downtrend"] & ~masks["bb_lower_only"]
        assert not bad.any(), "bb_downtrend is not a subset of bb_lower_only"

    def test_non_regime_excluded_from_all(self) -> None:
        config = _make_config(bb_period=5)
        df = _make_df(n=40, regime_on=False)
        masks = build_population_masks(df, config)
        for name, mask in masks.items():
            assert not mask.any(), f"Population '{name}' has True values with regime off"

    def test_missing_regime_column_raises(self) -> None:
        config = _make_config()
        df = _make_df(n=30).drop(columns=["ema_below_50_regime"])
        with pytest.raises(ValueError, match="missing required columns"):
            build_population_masks(df, config)

    def test_missing_atr_column_raises(self) -> None:
        config = _make_config()
        df = _make_df(n=30).drop(columns=["atr"])
        with pytest.raises(ValueError, match="missing required columns"):
            build_population_masks(df, config)

    def test_constant_close_has_zero_std_no_lower_band_triggers(self) -> None:
        """With constant close, std=0 → lower band = basis = close → no close < lower."""
        config = _make_config(bb_period=5)
        df = _make_df(n=40, close_val=100.0)  # constant close
        masks = build_population_masks(df, config)
        assert not masks["bb_lower_only"].any(), "Constant close should never trigger bb_lower_only"
        assert not masks["bb_downtrend"].any(), "Constant close should never trigger bb_downtrend"


# ---------------------------------------------------------------------------
# 3. Verdict threshold math
# ---------------------------------------------------------------------------


class TestVerdictThresholdMathStep2BB:
    def test_min_wr_lift_formula(self) -> None:
        config = _make_config()
        p, n = 0.47, 20_000
        expected = 2.5 * math.sqrt(p * (1 - p) / n)
        assert math.isclose(_min_wr_lift(config, p, n), expected, rel_tol=1e-9)

    def test_min_wr_lift_zero_n(self) -> None:
        config = _make_config()
        assert _min_wr_lift(config, 0.5, 0) == float("inf")

    def test_min_pf_diff_tiers(self) -> None:
        config = _make_config()
        assert _min_pf_diff(config, 60_000) == 0.02
        assert _min_pf_diff(config, 50_001) == 0.02  # boundary: strictly > 50k
        assert _min_pf_diff(config, 50_000) == 0.05  # boundary: 50k is in mid tier
        assert _min_pf_diff(config, 49_999) == 0.05
        assert _min_pf_diff(config, 10_000) == 0.05  # boundary: >= 10k
        assert _min_pf_diff(config, 9_999) == 0.10

    def test_larger_n_gives_smaller_wr_threshold(self) -> None:
        config = _make_config()
        small = _min_wr_lift(config, 0.47, 1_000)
        large = _min_wr_lift(config, 0.47, 50_000)
        assert small > large


# ---------------------------------------------------------------------------
# 4. Outcome engine — deterministic cases
# ---------------------------------------------------------------------------


class TestOutcomeEngine:
    def _make_outcome_df(self, n: int = 20) -> pd.DataFrame:
        """OHLCV DataFrame where Close=100, ATR=2."""
        idx = pd.date_range("2023-01-01", periods=n, freq="1h")
        return pd.DataFrame(
            {
                "Open": np.full(n, 100.0),
                "High": np.full(n, 101.0),
                "Low": np.full(n, 99.0),
                "Close": np.full(n, 100.0),
                "Volume": np.ones(n),
                "atr": np.full(n, 2.0),
            },
            index=idx,
        )

    def test_target_hit_when_low_drops_far(self) -> None:
        """If the next bar's low goes well below target, trade is a win."""
        config = _make_config(stop_atr_mult=2.0, target_atr_mult=3.0)
        df = self._make_outcome_df(10)
        # Entry at bar 0: entry=100, stop=104, target=94
        # Bar 1: high=101 (< 104), low=90 (≤ 94) → win
        df.loc[df.index[1], "Low"] = 90.0
        mask = pd.Series([True] + [False] * 9, index=df.index)
        result = _compute_outcomes(df, mask, config)
        assert result["win_rate"] == 1.0
        assert result["n_trades"] == 1
        assert result["avg_duration"] == 1.0

    def test_stop_hit_when_high_exceeds_stop(self) -> None:
        config = _make_config(stop_atr_mult=2.0, target_atr_mult=3.0)
        df = self._make_outcome_df(10)
        # Entry at bar 0: entry=100, stop=104, target=94
        # Bar 1: high=105 (≥ 104) → loss
        df.loc[df.index[1], "High"] = 105.0
        mask = pd.Series([True] + [False] * 9, index=df.index)
        result = _compute_outcomes(df, mask, config)
        assert result["win_rate"] == 0.0
        assert result["n_trades"] == 1

    def test_stop_priority_over_target_same_bar(self) -> None:
        """When stop and target both hit on the same bar, stop wins (conservative)."""
        config = _make_config(stop_atr_mult=2.0, target_atr_mult=3.0)
        df = self._make_outcome_df(10)
        df.loc[df.index[1], "High"] = 105.0  # ≥ stop 104
        df.loc[df.index[1], "Low"] = 90.0    # ≤ target 94
        mask = pd.Series([True] + [False] * 9, index=df.index)
        result = _compute_outcomes(df, mask, config)
        assert result["win_rate"] == 0.0, "Stop should take priority on same bar"

    def test_unresolved_trade_excluded(self) -> None:
        """Trade at the last entry bar cannot resolve — should be excluded."""
        config = _make_config(stop_atr_mult=2.0, target_atr_mult=3.0)
        df = self._make_outcome_df(3)
        # Only entry at final bar — no bars to scan forward
        mask = pd.Series([False, False, True], index=df.index)
        result = _compute_outcomes(df, mask, config)
        assert result["n_trades"] == 0

    def test_empty_mask_returns_nan(self) -> None:
        config = _make_config()
        df = self._make_outcome_df(10)
        mask = pd.Series([False] * 10, index=df.index)
        result = _compute_outcomes(df, mask, config)
        assert result["n_trades"] == 0
        assert math.isnan(result["win_rate"])

    def test_profit_factor_correct(self) -> None:
        """Two wins (3×ATR each) and one loss (2×ATR): PF = 6/2 = 3.0."""
        config = _make_config(stop_atr_mult=2.0, target_atr_mult=3.0)
        n = 15
        df = self._make_outcome_df(n)
        # Win at bar 1
        df.loc[df.index[1], "Low"] = 90.0
        # Win at bar 5
        df.loc[df.index[5], "Low"] = 90.0
        # Loss at bar 10 (stop)
        df.loc[df.index[10], "High"] = 105.0
        entries = [0, 4, 9]
        mask = pd.Series(
            [i in entries for i in range(n)],
            index=df.index,
        )
        result = _compute_outcomes(df, mask, config)
        assert result["n_trades"] == 3
        assert math.isclose(result["profit_factor"], 3.0, rel_tol=1e-9)
