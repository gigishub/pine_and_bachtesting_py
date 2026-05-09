"""
Unit tests for bull_strategy hypothesis_test_v2 HTF alignment engine.

Covers:
  - align_htf_series: aligned signal maps to correct LTF bar
  - shift(1) means no HTF bar is visible on its own open bar (no lookahead)
  - LookaheadError raised when future HTF data leaks into LTF signal
  - validate_no_lookahead passes for a properly shifted signal
"""

from __future__ import annotations

import pandas as pd
import pytest

from bull_strategy.hypothesis_test_v2.engine.alignment import (
    align_htf_series,
    validate_no_lookahead,
    LookaheadError,
)


def _ltf_index(n: int = 24, freq: str = "1h") -> pd.DatetimeIndex:
    return pd.date_range("2021-01-01", periods=n, freq=freq)


def _htf_index(n: int = 3, freq: str = "1D") -> pd.DatetimeIndex:
    return pd.date_range("2021-01-01", periods=n, freq=freq)


class TestAlignHTFSeries:
    def test_returns_bool_series_with_ltf_index(self) -> None:
        ltf_idx = _ltf_index(48)
        htf_idx = _htf_index(3)
        htf_signal = pd.Series([False, True, False], index=htf_idx)

        result = align_htf_series(htf_idx, htf_signal, ltf_idx)
        assert isinstance(result, pd.Series)
        assert result.index.equals(ltf_idx)
        assert result.dtype == bool

    def test_no_lookahead_htf_bar_not_visible_on_own_open(self) -> None:
        """
        HTF bar opens at 2021-01-02 00:00 (True).
        With shift(1), LTF bars on 2021-01-02 must NOT see that signal — only
        LTF bars on 2021-01-03 and later should see it.
        """
        ltf_idx = _ltf_index(72, freq="1h")       # 3 days of hourly bars
        htf_idx = _htf_index(3, freq="1D")         # 3 daily bars
        htf_signal = pd.Series([False, True, False], index=htf_idx)

        result = align_htf_series(htf_idx, htf_signal, ltf_idx)

        day1_bars = result[result.index < pd.Timestamp("2021-01-02")]
        day2_bars = result[(result.index >= pd.Timestamp("2021-01-02")) &
                           (result.index < pd.Timestamp("2021-01-03"))]
        day3_bars = result[result.index >= pd.Timestamp("2021-01-03")]

        assert not day1_bars.any(),  "Day-1 bars must not see Day-2 HTF signal"
        assert not day2_bars.any(),  "Day-2 itself must not see its own signal (shift=1)"
        assert day3_bars.any(),      "Day-3 bars should see the shifted Day-2 signal"

    def test_all_false_when_htf_all_false(self) -> None:
        ltf_idx = _ltf_index(48)
        htf_idx = _htf_index(3)
        htf_signal = pd.Series([False, False, False], index=htf_idx)
        result = align_htf_series(htf_idx, htf_signal, ltf_idx)
        assert not result.any()

    def test_no_nans_in_result(self) -> None:
        ltf_idx = _ltf_index(48)
        htf_idx = _htf_index(3)
        htf_signal = pd.Series([True, False, True], index=htf_idx)
        result = align_htf_series(htf_idx, htf_signal, ltf_idx)
        assert result.notna().all()


class TestValidateNoLookahead:
    def test_passes_for_shifted_signal(self) -> None:
        ltf_df = pd.DataFrame(
            {"close": 100.0},
            index=pd.date_range("2021-01-01", periods=48, freq="1h"),
        )
        signal = pd.Series(False, index=ltf_df.index)
        # Should not raise
        validate_no_lookahead(ltf_df, signal, context_tf="1D")

    def test_raises_for_known_future_leak(self) -> None:
        """
        A signal that fires on the exact open of a daily bar (without shift)
        should trigger LookaheadError.
        """
        ltf_df = pd.DataFrame(
            {"close": 100.0},
            index=pd.date_range("2021-01-01", periods=48, freq="1h"),
        )
        signal = pd.Series(False, index=ltf_df.index)
        # Bar 23 = 2021-01-01 23:00 — still inside Day 1's daily bar (not yet closed).
        # Firing here without shift is lookahead: the daily bar hasn't closed yet.
        signal.iloc[23] = True

        with pytest.raises(LookaheadError):
            validate_no_lookahead(ltf_df, signal, context_tf="1D")
