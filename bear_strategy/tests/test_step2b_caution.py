"""Tests for Step 2b — Caution Exclusion Filter.

Four test classes:
    TestCautionNoLookahead    — signals use only past/current bar data
    TestPopulationMasks       — mask structure, subsets, and column guards
    TestVerdictThresholdMath  — WR lift and PF diff formulas
    TestOutcomeEngine         — deterministic stop/target forward-scan cases
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest

from bear_strategy.hypothesis_tests.caution_exclusion_check.config import TestConfig
from bear_strategy.hypothesis_tests.caution_exclusion_check.entries import (
    build_population_masks,
)
from bear_strategy.hypothesis_tests.caution_exclusion_check.run import (
    _min_pf_diff,
    _min_wr_lift,
)
from bear_strategy.hypothesis_tests.caution_exclusion_check.runner import (
    _compute_outcomes,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_df(
    n: int = 30,
    freq: str = "1h",
    regime_on: bool = True,
    close_val: float = 80.0,   # below ema20=100 → no EMA caution
    high_val: float | None = None,
    low_val: float | None = None,
    atr_val: float = 2.0,
) -> pd.DataFrame:
    """Build a minimal DataFrame where no caution flags fire by default.

    With close=80, ema20 converges to 80 over time → above_ema20 is False.
    High=81, Low=79 → range7 ≈ 2 ≤ 2 × 1.5 = 3 → wide_range is False.
    """
    if high_val is None:
        high_val = close_val + 1.0
    if low_val is None:
        low_val = close_val - 1.0
    idx = pd.date_range("2023-01-01", periods=n, freq=freq)
    return pd.DataFrame(
        {
            "Open": np.full(n, close_val),
            "High": np.full(n, high_val),
            "Low": np.full(n, low_val),
            "Close": np.full(n, close_val),
            "Volume": np.ones(n) * 1000.0,
            "ema_below_50_regime": np.ones(n, dtype=bool) if regime_on else np.zeros(n, dtype=bool),
            "atr": np.full(n, atr_val),
        },
        index=idx,
    )


def _make_config(**kwargs) -> TestConfig:
    return TestConfig(**kwargs)


# ---------------------------------------------------------------------------
# 1. No-lookahead tests
# ---------------------------------------------------------------------------


class TestCautionNoLookahead:
    def test_future_close_does_not_affect_past_ema20_signal(self) -> None:
        """Changing a future close must not affect ema20_filter at past bars."""
        config = _make_config(ema20_period=5, range_period=5)
        df = _make_df(n=30)

        masks_before = build_population_masks(df.copy(), config)
        df_modified = df.copy()
        # Push last bar's close far above ema20 to change the flag
        df_modified.loc[df_modified.index[-1], "Close"] = 9999.0
        masks_after = build_population_masks(df_modified, config)

        # All bars except the last should be unchanged
        pd.testing.assert_series_equal(
            masks_before["ema20_filter"].iloc[:-1],
            masks_after["ema20_filter"].iloc[:-1],
        )

    def test_future_low_does_not_affect_past_range7(self) -> None:
        """Changing a future Low must not affect range7 at prior bars."""
        config = _make_config(range_period=5)
        df = _make_df(n=30)

        masks_before = build_population_masks(df.copy(), config)
        df_modified = df.copy()
        df_modified.loc[df_modified.index[-1], "Low"] = -9999.0
        masks_after = build_population_masks(df_modified, config)

        # range7 uses rolling min — only current bar's mask should differ
        pd.testing.assert_series_equal(
            masks_before["range_filter"].iloc[:-1],
            masks_after["range_filter"].iloc[:-1],
        )

    def test_warmup_bars_excluded_from_all_populations(self) -> None:
        """First range_period-1 bars must be absent from all populations."""
        config = _make_config(range_period=7)
        df = _make_df(n=30)
        masks = build_population_masks(df, config)

        for name, mask in masks.items():
            warmup = mask.iloc[: config.range_period - 1]
            assert not warmup.any(), (
                f"Population '{name}' has True in warmup period (first {config.range_period - 1} bars)."
            )

    def test_atr_first_bar_excluded(self) -> None:
        """First bar has NaN ATR (no prev_close) → must be absent from all populations.

        In this test df already has atr pre-computed as a constant; but the
        runner computes it from OHLCV.  We simulate by setting atr=NaN at bar 0.
        """
        config = _make_config(range_period=3)
        df = _make_df(n=20)
        # Manually NaN the first ATR row to simulate runner's first-bar ATR
        df.loc[df.index[0], "atr"] = float("nan")
        masks = build_population_masks(df, config)
        for name, mask in masks.items():
            assert not mask.iloc[0], f"Population '{name}' has True at bar 0 (NaN ATR)."

    def test_range7_uses_rolling_not_single_bar(self) -> None:
        """range7 should reflect the 7-bar window — a single low outlier in window."""
        config = _make_config(range_period=7, range_atr_mult=1.5)
        n = 20
        idx = pd.date_range("2023-01-01", periods=n, freq="1h")
        closes = np.full(n, 100.0)
        highs = np.full(n, 101.0)
        lows = np.full(n, 99.0)
        # Plant a very low low 3 bars before the last bar — should widen range7
        lows[n - 4] = 50.0
        df = pd.DataFrame(
            {
                "Open": closes,
                "High": highs,
                "Low": lows,
                "Close": closes,
                "Volume": np.ones(n),
                "ema_below_50_regime": np.ones(n, dtype=bool),
                "atr": np.full(n, 2.0),  # range7 = 101-50=51 >> 2*1.5=3 → caution
            },
            index=idx,
        )
        masks = build_population_masks(df, config)
        # At the last bar, the low outlier at n-4 is still in the rolling window
        assert not masks["range_filter"].iloc[-1], (
            "Low outlier within the range_period window should trigger wide_range caution."
        )
        # Once outside the window the outlier no longer affects range7 — not testable
        # with only 20 bars, but the assertion above confirms rolling is used.


# ---------------------------------------------------------------------------
# 2. Population mask tests
# ---------------------------------------------------------------------------


class TestPopulationMasks:
    def test_no_caution_subset_of_ema20_filter(self) -> None:
        config = _make_config(range_period=5)
        df = _make_df(n=30)
        masks = build_population_masks(df, config)
        bad = masks["no_caution"] & ~masks["ema20_filter"]
        assert not bad.any(), "no_caution has bars outside ema20_filter"

    def test_no_caution_subset_of_range_filter(self) -> None:
        config = _make_config(range_period=5)
        df = _make_df(n=30)
        masks = build_population_masks(df, config)
        bad = masks["no_caution"] & ~masks["range_filter"]
        assert not bad.any(), "no_caution has bars outside range_filter"

    def test_all_subsets_of_regime_only(self) -> None:
        config = _make_config(range_period=5)
        df = _make_df(n=30)
        masks = build_population_masks(df, config)
        for name in ["ema20_filter", "range_filter", "no_caution"]:
            bad = masks[name] & ~masks["regime_only"]
            assert not bad.any(), f"'{name}' has bars outside regime_only"

    def test_non_regime_excluded_from_all(self) -> None:
        config = _make_config(range_period=5)
        df = _make_df(n=30, regime_on=False)
        masks = build_population_masks(df, config)
        for name, mask in masks.items():
            assert not mask.any(), f"Population '{name}' has True values with regime off"

    def test_missing_regime_column_raises(self) -> None:
        config = _make_config()
        df = _make_df(n=20).drop(columns=["ema_below_50_regime"])
        with pytest.raises(ValueError, match="missing required columns"):
            build_population_masks(df, config)

    def test_missing_atr_column_raises(self) -> None:
        config = _make_config()
        df = _make_df(n=20).drop(columns=["atr"])
        with pytest.raises(ValueError, match="missing required columns"):
            build_population_masks(df, config)

    def test_missing_high_column_raises(self) -> None:
        config = _make_config()
        df = _make_df(n=20).drop(columns=["High"])
        with pytest.raises(ValueError, match="missing required columns"):
            build_population_masks(df, config)

    def test_close_above_ema20_empties_ema20_filter(self) -> None:
        """When all closes are above a rising EMA, ema20_filter must be empty."""
        config = _make_config(ema20_period=5, range_period=5, range_atr_mult=1000.0)
        n = 30
        idx = pd.date_range("2023-01-01", periods=n, freq="1h")
        # Strongly rising closes → close always above EMA(5)
        closes = np.linspace(50.0, 200.0, n)
        df = pd.DataFrame(
            {
                "Open": closes,
                "High": closes + 1,
                "Low": closes - 1,
                "Close": closes,
                "Volume": np.ones(n),
                "ema_below_50_regime": np.ones(n, dtype=bool),
                "atr": np.full(n, 1.0),
            },
            index=idx,
        )
        masks = build_population_masks(df, config)
        # After warmup, all bars have close > ema20 → ema20_filter must be empty
        assert not masks["ema20_filter"].any(), (
            "ema20_filter should be empty when close always exceeds EMA20"
        )

    def test_always_wide_range_empties_range_filter(self) -> None:
        """When range7 always exceeds 1.5× ATR, range_filter must be empty."""
        config = _make_config(range_period=5, range_atr_mult=1.5)
        n = 30
        idx = pd.date_range("2023-01-01", periods=n, freq="1h")
        closes = np.full(n, 100.0)
        df = pd.DataFrame(
            {
                "Open": closes,
                "High": np.full(n, 200.0),   # huge High → range7 is enormous
                "Low": np.full(n, 50.0),
                "Close": closes,
                "Volume": np.ones(n),
                "ema_below_50_regime": np.ones(n, dtype=bool),
                "atr": np.full(n, 1.0),      # range7 >> 1.5 × 1.0 = 1.5
            },
            index=idx,
        )
        masks = build_population_masks(df, config)
        assert not masks["range_filter"].any(), (
            "range_filter should be empty when range7 always exceeds threshold"
        )

    def test_no_caution_equals_intersection_of_components(self) -> None:
        """no_caution must equal ema20_filter AND range_filter (by definition)."""
        config = _make_config(range_period=5)
        df = _make_df(n=30)
        masks = build_population_masks(df, config)
        expected = masks["ema20_filter"] & masks["range_filter"]
        pd.testing.assert_series_equal(masks["no_caution"], expected)


# ---------------------------------------------------------------------------
# 3. Verdict threshold math
# ---------------------------------------------------------------------------


class TestVerdictThresholdMathStep2b:
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
        assert _min_pf_diff(config, 50_001) == 0.02  # strictly > 50k
        assert _min_pf_diff(config, 50_000) == 0.05  # exactly 50k → mid tier
        assert _min_pf_diff(config, 49_999) == 0.05
        assert _min_pf_diff(config, 10_000) == 0.05  # boundary: ≥ 10k
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
        """OHLCV DataFrame where Close=100, ATR=2 — no caution, no movement."""
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

    def test_target_hit_gives_win(self) -> None:
        """Low drops below target → win at duration 1."""
        config = _make_config(stop_atr_mult=2.0, target_atr_mult=3.0)
        df = self._make_outcome_df(10)
        # entry=100, stop=104, target=94
        df.loc[df.index[1], "Low"] = 90.0  # ≤ 94 → win
        mask = pd.Series([True] + [False] * 9, index=df.index)
        result = _compute_outcomes(df, mask, config)
        assert result["win_rate"] == 1.0
        assert result["n_trades"] == 1
        assert result["avg_duration"] == 1.0

    def test_stop_hit_gives_loss(self) -> None:
        config = _make_config(stop_atr_mult=2.0, target_atr_mult=3.0)
        df = self._make_outcome_df(10)
        df.loc[df.index[1], "High"] = 105.0  # ≥ 104 → loss
        mask = pd.Series([True] + [False] * 9, index=df.index)
        result = _compute_outcomes(df, mask, config)
        assert result["win_rate"] == 0.0
        assert result["n_trades"] == 1

    def test_same_bar_stop_and_target_is_loss(self) -> None:
        """When stop and target both trigger on the same bar, stop wins (conservative)."""
        config = _make_config(stop_atr_mult=2.0, target_atr_mult=3.0)
        df = self._make_outcome_df(10)
        df.loc[df.index[1], "High"] = 105.0  # ≥ 104 stop
        df.loc[df.index[1], "Low"] = 90.0    # ≤ 94 target — stop checked first
        mask = pd.Series([True] + [False] * 9, index=df.index)
        result = _compute_outcomes(df, mask, config)
        assert result["win_rate"] == 0.0, "Stop should take priority on same bar"

    def test_unresolved_at_end_excluded(self) -> None:
        """Entry at the last bar cannot resolve — must be excluded from n_trades."""
        config = _make_config(stop_atr_mult=2.0, target_atr_mult=3.0)
        df = self._make_outcome_df(3)
        mask = pd.Series([False, False, True], index=df.index)
        result = _compute_outcomes(df, mask, config)
        assert result["n_trades"] == 0

    def test_empty_mask_returns_nan_stats(self) -> None:
        config = _make_config()
        df = self._make_outcome_df(10)
        mask = pd.Series([False] * 10, index=df.index)
        result = _compute_outcomes(df, mask, config)
        assert result["n_trades"] == 0
        assert math.isnan(result["win_rate"])
        assert math.isnan(result["profit_factor"])

    def test_profit_factor_two_wins_one_loss(self) -> None:
        """Two wins (3 R each) and one loss (2 R): PF = 6/2 = 3.0."""
        config = _make_config(stop_atr_mult=2.0, target_atr_mult=3.0)
        n = 15
        df = self._make_outcome_df(n)
        df.loc[df.index[1], "Low"] = 90.0   # win from bar 0
        df.loc[df.index[5], "Low"] = 90.0   # win from bar 4
        df.loc[df.index[10], "High"] = 105.0  # loss from bar 9
        entries = [0, 4, 9]
        mask = pd.Series(
            [i in entries for i in range(n)],
            index=df.index,
        )
        result = _compute_outcomes(df, mask, config)
        assert result["n_trades"] == 3
        assert math.isclose(result["profit_factor"], 3.0, rel_tol=1e-9)

    def test_duration_is_bars_until_resolution(self) -> None:
        """Duration counts bars from entry bar (exclusive) to resolution bar (inclusive)."""
        config = _make_config(stop_atr_mult=2.0, target_atr_mult=3.0)
        df = self._make_outcome_df(10)
        # Bar 0: entry. Bar 3: target hit → duration = 3.
        df.loc[df.index[3], "Low"] = 90.0
        mask = pd.Series([True] + [False] * 9, index=df.index)
        result = _compute_outcomes(df, mask, config)
        assert result["avg_duration"] == 3.0
