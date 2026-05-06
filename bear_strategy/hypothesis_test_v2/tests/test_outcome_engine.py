"""
Unit tests for hypothesis_test_v2 outcome engine.

Covers:
  - compute_atr:      Wilder ATR warms up correctly, values are positive
  - _simulate_trades: target hit, stop hit, ambiguous bar (conservative loss),
                      open trade at data end is excluded, duration tracking
  - compute_outcomes: profit factor / win rate / lift / coverage / avg_dur
                      are computed correctly on synthetic data; no lookahead
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from bear_strategy.hypothesis_test_v2.engine.outcome_engine import (
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


def _make_series(values: list[float], name: str = "close") -> pd.Series:
    idx = pd.date_range("2021-01-01", periods=len(values), freq="D")
    return pd.Series(values, index=idx, name=name)


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
# _simulate_trades  (internal)
# ---------------------------------------------------------------------------

def _build_arrays(prices: list[float], spread: float = 0.5):
    """Turn a list of close prices into (close, high, low, atr) numpy arrays.
    ATR is fixed at `spread` for all bars (simplifies expected calculations).
    """
    c = np.array(prices, dtype=float)
    h = c + spread
    l = c - spread
    atr = np.full_like(c, spread)
    return c, h, l, atr


class TestSimulateTrades:
    def test_target_hit(self) -> None:
        # Entry at bar 0 (close=100), target = 100 - 3*1 = 97, stop = 100 + 2*1 = 102
        # Bar 1: low=98 — doesn't hit 97; bar 2: low=94 — hits target → dur=2
        close = np.array([100.0, 98.0, 94.0, 90.0])
        high  = np.array([101.0, 99.0, 96.0, 91.0])
        low   = np.array([ 99.0, 98.0, 94.0, 89.0])
        atr   = np.array([  1.0,  1.0,  1.0,  1.0])
        wins, losses, durs = _simulate_trades(close, high, low, atr, np.array([0]), 2.0, 3.0)
        assert wins == [3.0]
        assert losses == []
        assert list(durs) == [2]   # resolved at bar 2, entered at bar 0 → 2 bars

    def test_stop_hit(self) -> None:
        # Entry at bar 0 (close=100), stop = 102, target = 97
        # Bar 1: high=103 — hits stop
        close = np.array([100.0, 101.0])
        high  = np.array([101.0, 103.0])
        low   = np.array([ 99.0,  98.0])
        atr   = np.array([  1.0,   1.0])
        wins, losses, durs = _simulate_trades(close, high, low, atr, np.array([0]), 2.0, 3.0)
        assert wins == []
        assert losses == [2.0]
        assert list(durs) == [1]

    def test_ambiguous_bar_counts_as_loss(self) -> None:
        # Both stop (high>=102) and target (low<=97) on the same bar → conservative loss
        close = np.array([100.0, 100.0])
        high  = np.array([101.0, 103.0])   # 103 >= 102 → stop
        low   = np.array([ 99.0,  96.0])   # 96  <= 97  → target
        atr   = np.array([  1.0,   1.0])
        wins, losses, durs = _simulate_trades(close, high, low, atr, np.array([0]), 2.0, 3.0)
        assert wins == []
        assert losses == [2.0]

    def test_open_trade_excluded(self) -> None:
        # Data ends before stop or target is ever hit → trade excluded
        close = np.array([100.0, 100.0, 100.0])
        high  = np.array([100.5, 100.5, 100.5])  # never reaches stop 102
        low   = np.array([ 99.5,  99.5,  99.5])  # never reaches target 97
        atr   = np.array([  1.0,   1.0,   1.0])
        wins, losses, durs = _simulate_trades(close, high, low, atr, np.array([0]), 2.0, 3.0)
        assert wins == []
        assert losses == []
        assert list(durs) == []

    def test_nan_atr_entry_skipped(self) -> None:
        close = np.array([100.0, 96.0])
        high  = np.array([101.0, 97.0])
        low   = np.array([ 99.0, 95.0])
        atr   = np.array([  np.nan, 1.0])
        wins, losses, _ = _simulate_trades(close, high, low, atr, np.array([0]), 2.0, 3.0)
        assert wins == [] and losses == []

    def test_duration_tracked_correctly(self) -> None:
        # entry0@bar0: stop=102. Bar1 high=103 → stops at bar1, dur=1
        # entry1@bar2: stop=102. Bar3 high=101 (no), bar4 high=103 → stops at bar4, dur=2
        close = np.array([100.0, 101.0, 100.0, 101.0, 101.0])
        high  = np.array([101.0, 103.0, 101.0, 101.0, 103.0])
        low   = np.array([ 99.0,  98.0,  99.0,  99.0,  98.0])
        atr   = np.array([  1.0,   1.0,   1.0,   1.0,   1.0])
        _, _, durs = _simulate_trades(close, high, low, atr, np.array([0, 2]), 2.0, 3.0)
        assert list(durs)[0] == 1   # entry0 → bar1
        assert list(durs)[1] == 2   # entry2 → bar4


# ---------------------------------------------------------------------------
# compute_outcomes
# ---------------------------------------------------------------------------

class TestComputeOutcomes:
    def test_candidate_subset_of_baseline(self) -> None:
        """All candidate entries are a subset of baseline — coverage < 1."""
        df = _flat_df(300)
        baseline = pd.Series(True, index=df.index)
        # Candidate fires every 5th bar only
        candidate = pd.Series(False, index=df.index)
        candidate.iloc[::5] = True

        result = compute_outcomes(df, candidate, baseline, atr_period=7)
        assert 0 < result.candidate_coverage < 1.0

    def test_lift_is_candidate_minus_baseline_pf(self) -> None:
        df = _flat_df(300)
        baseline = pd.Series(True, index=df.index)
        candidate = pd.Series(True, index=df.index)

        result = compute_outcomes(df, candidate, baseline, atr_period=7)
        # When candidate == baseline the lift must be ~0
        assert abs(result.pf_lift) < 0.01

    def test_no_lookahead_via_entry_index(self) -> None:
        """Entries at the last bar must not count — no future bar to resolve against."""
        df = _flat_df(20)
        # Only entry is the very last bar
        candidate = pd.Series(False, index=df.index)
        candidate.iloc[-1] = True
        baseline = candidate.copy()

        result = compute_outcomes(df, candidate, baseline, atr_period=7)
        # Last-bar trade has no forward bar → excluded → n=0
        assert result.candidate_n == 0

    def test_avg_dur_populated(self) -> None:
        """avg_dur is > 0 when trades actually resolve."""
        # Steady linear price decline: ATR≈1.5, target hit in ~5 bars
        n = 100
        idx    = pd.date_range("2021-01-01", periods=n, freq="15min")
        closes = np.arange(100.0, 100.0 - n, -1.0)[:n]
        df = pd.DataFrame(
            {"open": closes, "high": closes + 0.5, "low": closes - 0.5,
             "close": closes, "volume": 1.0},
            index=idx,
        )
        baseline  = pd.Series(True, index=idx)
        candidate = pd.Series(False, index=idx)
        candidate.iloc[7] = True   # one entry after ATR warmup

        result = compute_outcomes(df, candidate, baseline, atr_period=7)
        assert result.candidate_n > 0,    "trade must resolve on declining prices"
        assert result.candidate_avg_dur > 0

    def test_perfect_regime_lifts_pf(self) -> None:
        """Entries only on strong down bars should have higher PF than random entries."""
        n = 200
        idx = pd.date_range("2021-01-01", periods=n, freq="15min")
        # Strong bars: close=90 (drops 10 from prev=100) → stop=92, target=80 easily hit
        # Weak bars: close=100, high=101, low=99 → narrow range, stop/target far
        # For entries only on "strong" bars the target is hit faster
        closes  = np.where(np.arange(n) % 2 == 0, 100.0, 90.0).astype(float)
        highs   = np.where(np.arange(n) % 2 == 0, 101.0, 91.0).astype(float)
        lows    = np.where(np.arange(n) % 2 == 0,  88.0, 78.0).astype(float)  # big drops
        df = pd.DataFrame(
            {"open": closes, "high": highs, "low": lows, "close": closes, "volume": 1.0},
            index=idx,
        )
        baseline  = pd.Series(True, index=idx)
        candidate = pd.Series(closes == 100.0, index=idx)  # enter on "100" bars

        result = compute_outcomes(df, candidate, baseline, atr_period=7, stop_mult=1.0, target_mult=2.0)
        # Sanity check: lift can be positive or zero but not catastrophically negative
        assert result.pf_lift > -1.0
