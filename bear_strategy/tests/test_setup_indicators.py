"""Unit tests for Step 2 — Setup Level Edge Check.

Tests:
  1. TestAtr4hNoLookahead      — shift(1)+merge_asof only exposes t-1 data at t
  2. TestSetupMaskClassification — near/away/vpvr/vwap mask logic
  3. TestVerdictThresholdMath   — _min_wr_lift and _min_pf_diff formulas
  4. TestOutcomeEngineDeterminism — stop/target forward-scan
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest

from bear_strategy.hypothesis_tests.setup_level_edge_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_level_edge_check.entries import (
    build_population_masks,
)
from bear_strategy.hypothesis_tests.setup_level_edge_check.run import (
    _min_pf_diff,
    _min_wr_lift,
)
from bear_strategy.hypothesis_tests.setup_level_edge_check.runner import (
    _align_4h_to_1h,
    _compute_outcomes,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_1h_index(n: int, start: str = "2023-01-01") -> pd.DatetimeIndex:
    return pd.date_range(start, periods=n, freq="1h")


def _make_4h_index(n: int, start: str = "2023-01-01") -> pd.DatetimeIndex:
    return pd.date_range(start, periods=n, freq="4h")


# ---------------------------------------------------------------------------
# 1. No-lookahead: shift(1) + merge_asof
# ---------------------------------------------------------------------------


class TestAtr4hNoLookahead:
    """Verify that _align_4h_to_1h never exposes 4H bar T on a 1h bar
    that falls *within* 4H bar T (i.e., before T+1)."""

    def test_within_4h_bar_sees_previous_value(self) -> None:
        """A 1h bar at 01:00 sits inside the 4H bar that opened at 00:00.
        After shift(1), that 1h bar must see the value from 4H bar t-1,
        not the value computed at 4H bar t=00:00."""
        idx_4h = _make_4h_index(5)
        df_4h_signals = pd.DataFrame(
            {
                "atr_4h": [10.0, 20.0, 30.0, 40.0, 50.0],
                "vpvr_hvn": [100.0, 200.0, 300.0, 400.0, 500.0],
                "anchored_vwap": [90.0, 190.0, 290.0, 390.0, 490.0],
            },
            index=idx_4h,
        )

        # 1h bars: three inside each 4H bar (01:00, 02:00, 03:00 all within 4H bar at 00:00)
        idx_1h = pd.date_range("2023-01-01 01:00", periods=6, freq="1h")
        df_1h = pd.DataFrame(index=idx_1h)

        aligned = _align_4h_to_1h(df_1h, df_4h_signals)

        # 01:00 and 02:00 fall inside 4H bar t=0 (opened 00:00).
        # shift(1) means the merged value at those bars is the value of t=-1 → NaN.
        assert pd.isna(aligned.loc[pd.Timestamp("2023-01-01 01:00"), "atr_4h"])
        assert pd.isna(aligned.loc[pd.Timestamp("2023-01-01 02:00"), "atr_4h"])

    def test_after_4h_close_sees_completed_bar(self) -> None:
        """After the first 4H bar T+1 opens, bars inside it should see
        T's value (shifted from T+1 to T via shift(1))."""
        idx_4h = _make_4h_index(5)
        df_4h_signals = pd.DataFrame(
            {
                "atr_4h": [10.0, 20.0, 30.0, 40.0, 50.0],
                "vpvr_hvn": [100.0, 200.0, 300.0, 400.0, 500.0],
                "anchored_vwap": [90.0, 190.0, 290.0, 390.0, 490.0],
            },
            index=idx_4h,
        )

        # First 1h bar of the second 4H period (05:00 falls inside 4H bar t=1 at 04:00)
        idx_1h = pd.date_range("2023-01-01 05:00", periods=1, freq="1h")
        df_1h = pd.DataFrame(index=idx_1h)

        aligned = _align_4h_to_1h(df_1h, df_4h_signals)

        # After shift: the 4H bar at 04:00 carries the value that was at t=0 (10.0)
        assert aligned.loc[pd.Timestamp("2023-01-01 05:00"), "atr_4h"] == pytest.approx(10.0)


# ---------------------------------------------------------------------------
# 2. Setup mask classification
# ---------------------------------------------------------------------------


class TestSetupMaskClassification:
    """Verify that near_vpvr, near_vwap, near_setup, away_from_setup,
    vpvr_only, and vwap_only are classified correctly for a synthetic df."""

    def _make_df(self) -> tuple[pd.DataFrame, TestConfig]:
        config = TestConfig()
        # distance threshold = 0.5 × atr_4h = 0.5 × 200 = 100

        #          close   atr_4h  vpvr_hvn  avwap   regime
        data = {
            # near_vpvr: vpvr - close = 50 ≤ 100, avwap below → vpvr_only
            "close":        [1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0],
            "atr_4h":       [ 200.0,  200.0,  200.0,  200.0,  200.0,  200.0],
            # vpvr 50 above close → near_vpvr ✓  (delta = 50 ≤ 100)
            # vpvr 150 above close → far         (delta = 150 > 100)
            # vpvr NaN → not valid
            "vpvr_hvn":     [1050.0, 1150.0,    np.nan, 1050.0, 1150.0, np.nan],
            # avwap 60 above close → near_vwap ✓ (delta = 60 ≤ 100)
            # avwap below close → avwap > close is False
            "anchored_vwap":[  np.nan, np.nan, 1060.0, 1060.0, 1060.0, np.nan],
            "regime":       [True, True, True, True, True, True],
        }

        n = len(data["close"])
        idx = _make_1h_index(n)
        df = pd.DataFrame(data, index=idx)
        df["Close"] = df["close"]
        df["ema_below_50_regime"] = df["regime"]
        return df, config

    def test_vpvr_only_near(self) -> None:
        df, config = self._make_df()
        masks = build_population_masks(df, config)
        # Row 0: vpvr near (50 ≤ 100), avwap NaN → vpvr_only
        assert masks["vpvr_only"].iloc[0] is True or masks["vpvr_only"].iloc[0]
        assert not masks["vwap_only"].iloc[0]
        assert masks["near_setup"].iloc[0]

    def test_vpvr_far_excluded(self) -> None:
        df, config = self._make_df()
        masks = build_population_masks(df, config)
        # Row 1: vpvr far (150 > 100), avwap NaN → away
        assert not masks["near_setup"].iloc[1]
        assert masks["away_from_setup"].iloc[1]

    def test_vwap_only_near(self) -> None:
        df, config = self._make_df()
        masks = build_population_masks(df, config)
        # Row 2: vpvr NaN, avwap near (60 ≤ 100) → vwap_only
        assert masks["vwap_only"].iloc[2]
        assert not masks["vpvr_only"].iloc[2]
        assert masks["near_setup"].iloc[2]

    def test_both_near(self) -> None:
        df, config = self._make_df()
        masks = build_population_masks(df, config)
        # Row 3: vpvr near (50) AND avwap near (60) → near_setup, vpvr_only, vwap_only all True
        assert masks["near_setup"].iloc[3]
        assert masks["vpvr_only"].iloc[3]
        assert masks["vwap_only"].iloc[3]
        assert not masks["away_from_setup"].iloc[3]

    def test_away_when_both_far(self) -> None:
        df, config = self._make_df()
        masks = build_population_masks(df, config)
        # Row 4: vpvr far (150), avwap near (60) → vwap_only near, NOT away
        assert masks["vwap_only"].iloc[4]
        assert masks["near_setup"].iloc[4]
        assert not masks["away_from_setup"].iloc[4]

    def test_both_nan_excluded(self) -> None:
        df, config = self._make_df()
        masks = build_population_masks(df, config)
        # Row 5: both NaN → not eligible → not in near, not in away
        assert not masks["near_setup"].iloc[5]
        assert not masks["away_from_setup"].iloc[5]

    def test_non_regime_excluded(self) -> None:
        df, config = self._make_df()
        df.loc[df.index[0], "ema_below_50_regime"] = False
        masks = build_population_masks(df, config)
        # Row 0 now off-regime → not near_setup
        assert not masks["near_setup"].iloc[0]
        assert not masks["all_regime"].iloc[0]


# ---------------------------------------------------------------------------
# 3. Verdict threshold math
# ---------------------------------------------------------------------------


class TestVerdictThresholdMath:
    def test_min_wr_lift_formula(self) -> None:
        config = TestConfig()
        p = 0.4
        n = 1000
        expected = config.significance_zscore * math.sqrt(p * (1 - p) / n)
        result = _min_wr_lift(config, baseline_wr=p, smaller_n=n)
        assert result == pytest.approx(expected, rel=1e-6)

    def test_min_wr_lift_zero_n(self) -> None:
        config = TestConfig()
        assert _min_wr_lift(config, baseline_wr=0.4, smaller_n=0) == float("inf")

    def test_min_pf_diff_high_n(self) -> None:
        config = TestConfig()
        assert _min_pf_diff(config, 51_000) == pytest.approx(config.min_pf_diff_high_n)

    def test_min_pf_diff_mid_n(self) -> None:
        config = TestConfig()
        assert _min_pf_diff(config, 10_000) == pytest.approx(config.min_pf_diff_mid_n)
        assert _min_pf_diff(config, 30_000) == pytest.approx(config.min_pf_diff_mid_n)
        assert _min_pf_diff(config, 50_000) == pytest.approx(config.min_pf_diff_mid_n)

    def test_min_pf_diff_low_n(self) -> None:
        config = TestConfig()
        assert _min_pf_diff(config, 9_999) == pytest.approx(config.min_pf_diff_low_n)
        assert _min_pf_diff(config, 500) == pytest.approx(config.min_pf_diff_low_n)

    def test_wr_lift_larger_n_smaller_threshold(self) -> None:
        config = TestConfig()
        threshold_small = _min_wr_lift(config, 0.4, 1_000)
        threshold_large = _min_wr_lift(config, 0.4, 100_000)
        assert threshold_large < threshold_small


# ---------------------------------------------------------------------------
# 4. Outcome engine determinism
# ---------------------------------------------------------------------------


class TestOutcomeEngineDeterminism:
    """Verify the forward-scan stop/target engine with a controlled
    synthetic price sequence."""

    def _make_df_outcome(self) -> tuple[pd.DataFrame, pd.Series]:
        """Two trades: first hits stop, second hits target.

        Layout (15 bars total):
          bar 0  entry (close=100, atr=10)
                 stop  = 100 + 2.0×10 = 120
                 target= 100 - 3.0×10 =  70
          bar 1  high=125 → stop hit → loss of 2×ATR = 20

          bar 5  entry (close=200, atr=10)
                 stop  = 200 + 2.0×10 = 220
                 target= 200 - 3.0×10 = 170
          bar 6  low=165 → target hit → win of 3×ATR = 30
        """
        n = 15
        closes = [100.0] + [100.0] * 4 + [200.0] + [200.0] * 9
        highs =  [101.0,   125.0] + [101.0] * 3 + [201.0] + [201.0] * 9
        lows =   [ 99.0,    99.0] + [ 99.0] * 3 + [199.0,   165.0] + [199.0] * 8
        atrs =   [10.0] * n

        idx = _make_1h_index(n)
        df = pd.DataFrame(
            {"Close": closes, "High": highs, "Low": lows, "atr": atrs},
            index=idx,
        )
        entry_mask = pd.Series([True, False, False, False, False, True] + [False] * 9, index=idx)
        return df, entry_mask

    def test_n_trades(self) -> None:
        df, mask = self._make_df_outcome()
        config = TestConfig()
        result = _compute_outcomes(df, mask, config)
        assert result["n_trades"] == 2

    def test_win_rate(self) -> None:
        df, mask = self._make_df_outcome()
        config = TestConfig()
        result = _compute_outcomes(df, mask, config)
        # 1 win, 1 loss
        assert result["win_rate"] == pytest.approx(0.5)

    def test_profit_factor(self) -> None:
        """PF = sum_wins / sum_losses = 3.0 / 2.0 = 1.5."""
        df, mask = self._make_df_outcome()
        config = TestConfig()
        result = _compute_outcomes(df, mask, config)
        assert result["profit_factor"] == pytest.approx(1.5)

    def test_avg_duration(self) -> None:
        """Both trades resolve in 1 forward bar → avg_duration = 1.0."""
        df, mask = self._make_df_outcome()
        config = TestConfig()
        result = _compute_outcomes(df, mask, config)
        assert result["avg_duration"] == pytest.approx(1.0)

    def test_empty_mask_returns_nan(self) -> None:
        n = 10
        idx = _make_1h_index(n)
        df = pd.DataFrame(
            {
                "Close": np.ones(n) * 100,
                "High": np.ones(n) * 102,
                "Low": np.ones(n) * 98,
                "atr": np.ones(n) * 10,
            },
            index=idx,
        )
        mask = pd.Series([False] * n, index=idx)
        config = TestConfig()
        result = _compute_outcomes(df, mask, config)
        assert result["n_trades"] == 0
        assert math.isnan(result["win_rate"])
        assert math.isnan(result["profit_factor"])

    def test_unresolved_trades_excluded(self) -> None:
        """If price never hits stop or target, trade is excluded (not counted)."""
        n = 5
        idx = _make_1h_index(n)
        closes = [100.0] * n
        df = pd.DataFrame(
            {
                "Close": closes,
                "High": [101.0] * n,  # never reaches stop (120)
                "Low": [99.0] * n,    # never reaches target (70)
                "atr": [10.0] * n,
            },
            index=idx,
        )
        # Only one entry at bar 0; stop=120, target=70 — never hit in 4 remaining bars
        mask = pd.Series([True, False, False, False, False], index=idx)
        config = TestConfig()
        result = _compute_outcomes(df, mask, config)
        assert result["n_trades"] == 0
