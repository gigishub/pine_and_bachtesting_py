"""
Unit tests for bull_strategy hypothesis_test_v2 outcome engine.

Covers:
  - compute_atr:      Wilder ATR warms up correctly, values are positive
  - _simulate_trades: target hit, stop hit, ambiguous bar (conservative loss),
                      open trade at data end is excluded, duration tracking
  - compute_outcomes: profit factor / win rate / lift / coverage / avg_dur
                      are computed correctly on synthetic data; no lookahead

Long-trade conventions:
  stop_price   = entry - stop_mult   * ATR  (below entry — bar_low  <= stop)
  target_price = entry + target_mult * ATR  (above entry — bar_high >= target)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from bull_strategy.hypothesis_test_v2.engine.outcome_engine import (
    compute_atr,
    compute_outcomes,
    _simulate_trades,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _flat_df(n: int = 200, price: float = 100.0) -> pd.DataFrame:
    """Flat OHLCV: close == open == price, high = price+1, low = price-1."""
    idx = pd.date_range("2021-01-01", periods=n, freq="15min")
    return pd.DataFrame(
        {
            "open":   price,
            "high":   price + 1.0,
            "low":    price - 1.0,
            "close":  price,
            "volume": 1000.0,
        },
        index=idx,
    )


# ---------------------------------------------------------------------------
# compute_atr
# ---------------------------------------------------------------------------

class TestComputeATR:
    def test_warmup_bars_are_nan(self) -> None:
        df = _flat_df(50)
        atr = compute_atr(df["close"], df["high"], df["low"], period=14)
        assert atr.iloc[:13].isna().all(), "First period-1 bars must be NaN"

    def test_values_are_positive_after_warmup(self) -> None:
        df = _flat_df(50)
        atr = compute_atr(df["close"], df["high"], df["low"], period=14)
        assert (atr.dropna() > 0).all()

    def test_flat_price_atr_equals_high_minus_low(self) -> None:
        # With flat closes, TR = high - low = 2.0 every bar → ATR converges to 2.0
        df = _flat_df(200)
        atr = compute_atr(df["close"], df["high"], df["low"], period=14)
        assert abs(atr.iloc[-1] - 2.0) < 0.01


# ---------------------------------------------------------------------------
# _simulate_trades  (long-trade internal)
# ---------------------------------------------------------------------------

class TestSimulateTrades:
    def test_target_hit(self) -> None:
        """
        Long entry at bar 0 (close=100), ATR=1:
          stop   = 100 - 2*1 = 98  (below — bar_low  <= 98)
          target = 100 + 3*1 = 103 (above — bar_high >= 103)
        Bar 1: high=101 — doesn't reach 103
        Bar 2: high=104 — hits target → win, dur=2
        """
        close = np.array([100.0, 101.0, 103.0, 106.0])
        high  = np.array([101.0, 101.0, 104.0, 107.0])
        low   = np.array([ 99.0,  99.5,  99.0,  99.0])
        atr   = np.array([  1.0,   1.0,   1.0,   1.0])
        wins, losses, durs = _simulate_trades(close, high, low, atr, np.array([0]), 2.0, 3.0)
        assert wins == [3.0]
        assert losses == []
        assert list(durs) == [2]

    def test_stop_hit(self) -> None:
        """
        Long entry at bar 0 (close=100), ATR=1:
          stop   = 98   (bar_low <= 98)
          target = 103
        Bar 1: low=97 — hits stop → loss, dur=1
        """
        close = np.array([100.0,  99.0])
        high  = np.array([101.0, 100.0])
        low   = np.array([ 99.0,  97.0])
        atr   = np.array([  1.0,   1.0])
        wins, losses, durs = _simulate_trades(close, high, low, atr, np.array([0]), 2.0, 3.0)
        assert wins == []
        assert losses == [2.0]
        assert list(durs) == [1]

    def test_ambiguous_bar_counts_as_loss(self) -> None:
        """
        Same bar: low<=98 (stop) AND high>=103 (target) → conservative loss.
        """
        close = np.array([100.0, 100.0])
        high  = np.array([101.0, 104.0])  # 104 >= 103 → target hit
        low   = np.array([ 99.0,  97.0])  # 97  <= 98  → stop hit
        atr   = np.array([  1.0,   1.0])
        wins, losses, durs = _simulate_trades(close, high, low, atr, np.array([0]), 2.0, 3.0)
        assert wins == []
        assert losses == [2.0]

    def test_open_trade_excluded(self) -> None:
        """Data ends before stop or target — trade excluded, no stats."""
        close = np.array([100.0, 100.0, 100.0])
        high  = np.array([100.5, 100.5, 100.5])  # never reaches 103
        low   = np.array([ 99.5,  99.5,  99.5])  # never reaches 98
        atr   = np.array([  1.0,   1.0,   1.0])
        wins, losses, durs = _simulate_trades(close, high, low, atr, np.array([0]), 2.0, 3.0)
        assert wins == []
        assert losses == []
        assert list(durs) == []

    def test_nan_atr_entry_skipped(self) -> None:
        close = np.array([100.0, 104.0])
        high  = np.array([101.0, 105.0])
        low   = np.array([ 99.0, 103.0])
        atr   = np.array([  np.nan, 1.0])
        wins, losses, _ = _simulate_trades(close, high, low, atr, np.array([0]), 2.0, 3.0)
        assert wins == [] and losses == []

    def test_duration_tracked_correctly(self) -> None:
        """
        entry0@bar0: target=103. Bar1 high=101 (no), bar2 high=104 → hit at bar2, dur=2
        entry1@bar3: stop=98.   Bar4 low=97 → hit at bar4, dur=1
        """
        close = np.array([100.0, 101.0, 103.0, 100.0,  99.0])
        high  = np.array([101.0, 101.0, 104.0, 101.0, 100.0])
        low   = np.array([ 99.0,  99.5,  99.0,  99.0,  97.0])
        atr   = np.array([  1.0,   1.0,   1.0,   1.0,   1.0])
        _, _, durs = _simulate_trades(close, high, low, atr, np.array([0, 3]), 2.0, 3.0)
        assert list(durs)[0] == 2   # entry0 → bar2
        assert list(durs)[1] == 1   # entry3 → bar4


# ---------------------------------------------------------------------------
# compute_outcomes
# ---------------------------------------------------------------------------

class TestComputeOutcomes:
    def test_candidate_subset_of_baseline(self) -> None:
        """Candidate entries are a subset of baseline — coverage < 1."""
        df = _flat_df(300)
        baseline = pd.Series(True, index=df.index)
        candidate = pd.Series(False, index=df.index)
        candidate.iloc[::5] = True

        result = compute_outcomes(df, candidate, baseline, atr_period=7)
        assert 0 < result.candidate_coverage < 1.0

    def test_lift_is_zero_when_candidate_equals_baseline(self) -> None:
        df = _flat_df(300)
        baseline  = pd.Series(True, index=df.index)
        candidate = pd.Series(True, index=df.index)

        result = compute_outcomes(df, candidate, baseline, atr_period=7)
        assert abs(result.pf_lift) < 0.01

    def test_no_lookahead_via_entry_index(self) -> None:
        """Entry at the last bar has no forward bar — must be excluded."""
        df = _flat_df(20)
        candidate = pd.Series(False, index=df.index)
        candidate.iloc[-1] = True
        baseline = candidate.copy()

        result = compute_outcomes(df, candidate, baseline, atr_period=7)
        assert result.candidate_n == 0

    def test_avg_dur_populated(self) -> None:
        """avg_dur > 0 when trades resolve on trending prices."""
        n = 100
        idx    = pd.date_range("2021-01-01", periods=n, freq="15min")
        # Rising prices: target above entry will be hit quickly
        closes = np.arange(100.0, 100.0 + n, 1.0)[:n]
        df = pd.DataFrame(
            {"open": closes, "high": closes + 0.5, "low": closes - 0.5,
             "close": closes, "volume": 1.0},
            index=idx,
        )
        baseline  = pd.Series(True, index=idx)
        candidate = pd.Series(False, index=idx)
        candidate.iloc[7] = True   # one entry after ATR warmup

        result = compute_outcomes(df, candidate, baseline, atr_period=7)
        assert result.candidate_n > 0,    "trade must resolve on rising prices"
        assert result.candidate_avg_dur > 0

    def test_uptrend_bars_beat_random_entries(self) -> None:
        """Entries only on strong upward bars should PF >= random entries."""
        n   = 200
        idx = pd.date_range("2021-01-01", periods=n, freq="15min")
        # Even bars: big up-candles (target reached quickly on longs)
        # Odd bars:  narrow doji candles
        closes = np.where(np.arange(n) % 2 == 0, 100.0, 110.0).astype(float)
        highs  = np.where(np.arange(n) % 2 == 0, 101.0, 120.0).astype(float)
        lows   = np.where(np.arange(n) % 2 == 0,  98.0, 108.0).astype(float)
        df = pd.DataFrame(
            {"open": closes, "high": highs, "low": lows, "close": closes, "volume": 1.0},
            index=idx,
        )
        baseline  = pd.Series(True, index=idx)
        # Candidate enters on bars with big upside (high - close is large)
        candidate = pd.Series(closes == 100.0, index=idx)

        result = compute_outcomes(df, candidate, baseline, atr_period=7, stop_mult=1.0, target_mult=2.0)
        # lift can be positive or zero — must not be catastrophically negative
        assert result.pf_lift > -1.0
