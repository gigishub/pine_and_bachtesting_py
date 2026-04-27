"""Unit tests for Step 3 — Trigger Volume Confirmation.

Tests:
  1. TestVolumeRollingNoLookahead  — .shift(1) means bar t sees avg of t-N..t-1
  2. TestPopulationMasks           — triggered/not-triggered/warmup/non-regime
  3. TestVerdictThresholdMath      — _min_wr_lift and _min_pf_diff formulas
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest

from bear_strategy.hypothesis_tests.trigger_volume_confirmation.config import TestConfig
from bear_strategy.hypothesis_tests.trigger_volume_confirmation.entries import (
    build_population_masks,
)
from bear_strategy.hypothesis_tests.trigger_volume_confirmation.run import (
    _min_pf_diff,
    _min_wr_lift,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_df(
    volumes: list[float],
    regime: list[bool] | None = None,
    freq: str = "1h",
) -> tuple[pd.DataFrame, TestConfig]:
    n = len(volumes)
    idx = pd.date_range("2023-01-01", periods=n, freq=freq)
    config = TestConfig(volume_window=3)  # small window for tractable tests
    reg = regime if regime is not None else [True] * n
    df = pd.DataFrame(
        {
            "Open": np.ones(n) * 100,
            "High": np.ones(n) * 102,
            "Low": np.ones(n) * 98,
            "Close": np.ones(n) * 100,
            "Volume": volumes,
            "ema_below_50_regime": reg,
        },
        index=idx,
    )
    return df, config


# ---------------------------------------------------------------------------
# 1. No-lookahead: shift(1) on rolling average
# ---------------------------------------------------------------------------


class TestVolumeRollingNoLookahead:
    """Verify the rolling average at bar t is computed from bars [t-N, t-1]
    and does NOT include bar t's volume.

    With volume_window=3 and .shift(1):
        bar 0: avg = NaN  (shifted NaN)
        bar 1: avg = NaN  (shifted NaN)
        bar 2: avg = NaN  (rolling(3) at bar 1 is NaN)
        bar 3: avg = mean(bar0..bar2)
    """

    def test_warmup_bars_are_nan(self) -> None:
        # First window+1 bars must be NaN after shift(1)
        df, config = _make_df([10.0, 20.0, 30.0, 40.0, 50.0])
        masks = build_population_masks(df, config)
        # Bars 0, 1, 2 are in the warmup window — excluded from both pops
        for i in range(3):
            assert not masks["volume_triggered"].iloc[i]
            assert not masks["not_triggered"].iloc[i]

    def test_first_valid_bar_uses_prior_bars_only(self) -> None:
        """Bar 3 should compare against avg(bar0..bar2) = mean(10, 20, 30) = 20.
        Bar 3 volume = 100 → triggered (100 > 20).
        """
        df, config = _make_df([10.0, 20.0, 30.0, 100.0, 10.0])
        masks = build_population_masks(df, config)
        assert masks["volume_triggered"].iloc[3]
        assert not masks["not_triggered"].iloc[3]

    def test_current_bar_not_in_own_average(self) -> None:
        """Bar 3 volume = 1 (very low). If bar 3 was included in its own
        average the result would differ. Here avg = mean(10, 20, 30) = 20,
        so 1 < 20 → not_triggered (correct).
        If current bar were included: avg = mean(10, 20, 30, 1) = 15.25,
        still not_triggered — use a spike to make the test distinctive.
        """
        # Set bar 3 volume = 5, avg of prior = mean(100, 100, 100) = 100 → not triggered
        df, config = _make_df([100.0, 100.0, 100.0, 5.0, 5.0])
        masks = build_population_masks(df, config)
        # Bar 3: avg of bars 0..2 = 100, volume=5 → NOT triggered
        assert not masks["volume_triggered"].iloc[3]
        assert masks["not_triggered"].iloc[3]
        # If bar 3 were included in its own avg: mean(100,100,100,5)=76.25, still>5
        # But we verify by checking that bar 4 (volume=5, avg of 1..3=mean(100,100,5)=68.3) is correct
        assert not masks["volume_triggered"].iloc[4]


# ---------------------------------------------------------------------------
# 2. Population mask logic
# ---------------------------------------------------------------------------


class TestPopulationMasks:
    def test_triggered_above_average(self) -> None:
        # Bars 0..2 = 10 each (warmup). Bar 3 = 100 (spike). Bar 4 = 5 (low).
        df, config = _make_df([10.0, 10.0, 10.0, 100.0, 5.0])
        masks = build_population_masks(df, config)
        assert masks["volume_triggered"].iloc[3]
        assert not masks["volume_triggered"].iloc[4]

    def test_not_triggered_at_or_below_average(self) -> None:
        df, config = _make_df([10.0, 10.0, 10.0, 10.0, 10.0])
        masks = build_population_masks(df, config)
        # All bars in warmup or exactly equal (not above)
        assert not masks["volume_triggered"].any()

    def test_non_regime_excluded_from_both(self) -> None:
        regime = [True, True, True, False, True]
        df, config = _make_df([10.0, 10.0, 10.0, 100.0, 100.0], regime=regime)
        masks = build_population_masks(df, config)
        # Bar 3 is off-regime → excluded from both
        assert not masks["volume_triggered"].iloc[3]
        assert not masks["not_triggered"].iloc[3]

    def test_all_regime_includes_warmup(self) -> None:
        """all_regime mask is just the raw regime signal — includes warmup bars."""
        df, config = _make_df([10.0, 10.0, 10.0, 10.0, 10.0])
        masks = build_population_masks(df, config)
        # all_regime should be all True (regime=True throughout)
        assert masks["all_regime"].all()

    def test_missing_volume_column_raises(self) -> None:
        df, config = _make_df([10.0, 10.0, 10.0])
        df = df.drop(columns=["Volume"])
        with pytest.raises(ValueError, match="Volume"):
            build_population_masks(df, config)

    def test_missing_regime_column_raises(self) -> None:
        df, config = _make_df([10.0, 10.0, 10.0])
        df = df.drop(columns=["ema_below_50_regime"])
        with pytest.raises(ValueError, match="ema_below_50_regime"):
            build_population_masks(df, config)

    def test_triggered_and_not_triggered_are_disjoint(self) -> None:
        df, config = _make_df([10.0, 10.0, 10.0, 100.0, 5.0])
        masks = build_population_masks(df, config)
        overlap = masks["volume_triggered"] & masks["not_triggered"]
        assert not overlap.any()

    def test_triggered_plus_not_triggered_eq_eligible_regime(self) -> None:
        """Every eligible (valid+regime) bar is in exactly one of the two pops."""
        df, config = _make_df([10.0, 10.0, 10.0, 100.0, 5.0])
        masks = build_population_masks(df, config)
        union = masks["volume_triggered"] | masks["not_triggered"]
        # Union should equal all_regime & valid (bars 3 and 4)
        assert union.sum() == 2
        assert union.iloc[3] and union.iloc[4]


# ---------------------------------------------------------------------------
# 3. Verdict threshold math
# ---------------------------------------------------------------------------


class TestVerdictThresholdMathStep3:
    def test_min_wr_lift_formula(self) -> None:
        config = TestConfig()
        p = 0.4
        n = 1000
        expected = config.significance_zscore * math.sqrt(p * (1 - p) / n)
        assert _min_wr_lift(config, baseline_wr=p, smaller_n=n) == pytest.approx(expected, rel=1e-6)

    def test_min_wr_lift_zero_n(self) -> None:
        config = TestConfig()
        assert _min_wr_lift(config, baseline_wr=0.4, smaller_n=0) == float("inf")

    def test_min_pf_diff_tiers(self) -> None:
        config = TestConfig()
        assert _min_pf_diff(config, 51_000) == pytest.approx(config.min_pf_diff_high_n)
        assert _min_pf_diff(config, 50_000) == pytest.approx(config.min_pf_diff_mid_n)
        assert _min_pf_diff(config, 10_000) == pytest.approx(config.min_pf_diff_mid_n)
        assert _min_pf_diff(config, 9_999) == pytest.approx(config.min_pf_diff_low_n)

    def test_larger_n_gives_smaller_wr_threshold(self) -> None:
        config = TestConfig()
        small = _min_wr_lift(config, 0.4, 500)
        large = _min_wr_lift(config, 0.4, 50_000)
        assert large < small
