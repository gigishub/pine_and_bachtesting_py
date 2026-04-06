"""Tests for vectorbt/signals.py.

Verifies that the vectorized SL/TP computation matches the scalar
compute_long_stop / compute_short_stop helpers from the strategy layer.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from UPS_py_v2.strategy.risk.sl_tp import compute_long_stop, compute_short_stop, compute_long_target
from UPS_py_v2.strategy.strategy_parameters import StrategySettings
from UPS_py_v2.vectorbt.signals import build_vbt_arrays


def _make_ohlcv(n: int = 300, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic OHLCV data with a stable DatetimeIndex."""
    rng = np.random.default_rng(seed)
    close = np.cumprod(1 + rng.normal(0, 0.01, n)) * 30_000.0
    high = close * (1 + rng.uniform(0.001, 0.015, n))
    low = close * (1 - rng.uniform(0.001, 0.015, n))
    open_ = close * (1 + rng.normal(0, 0.005, n))
    volume = rng.uniform(1_000, 100_000, n)

    idx = pd.date_range("2023-01-01", periods=n, freq="1h")
    return pd.DataFrame(
        {"Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume},
        index=idx,
    )


class TestBuildVbtArraysShape:
    def test_returns_all_required_keys(self):
        df = _make_ohlcv()
        result = build_vbt_arrays(df)
        assert set(result.keys()) == {"entries", "short_entries", "sl_stop", "tp_stop", "size"}

    def test_all_arrays_same_length_as_input(self):
        df = _make_ohlcv()
        result = build_vbt_arrays(df)
        for key, series in result.items():
            assert len(series) == len(df), f"{key} length mismatch"

    def test_all_arrays_share_index(self):
        df = _make_ohlcv()
        result = build_vbt_arrays(df)
        for key, series in result.items():
            assert series.index.equals(df.index), f"{key} index mismatch"


class TestSlTpMatchesScalar:
    """The vectorized SL/TP should agree with the scalar helpers at entry bars."""

    def test_long_sl_matches_scalar(self):
        df = _make_ohlcv()
        s = StrategySettings(sl_reference="High/Low", stop_multiplier=1.0, atr_length=14)
        arrs = build_vbt_arrays(df, s)

        close = df["Close"].astype(float)
        low = df["Low"].astype(float)
        low_prev = low.shift(1).fillna(low)

        entry_bars = arrs["entries"][arrs["entries"]].index
        if len(entry_bars) == 0:
            pytest.skip("No long entries generated with default settings")

        # Build a rough ATR estimate to compare; use first entry bar as spot-check
        bar = entry_bars[0]
        i = df.index.get_loc(bar)
        if i < 1:
            pytest.skip("Entry on first bar, no prev bar for ATR")

        atr_approx = df["High"].rolling(14).mean().iloc[i] - df["Low"].rolling(14).mean().iloc[i]
        scalar_stop = compute_long_stop(
            sl_reference="High/Low",
            low_now=float(df["Low"].iloc[i]),
            low_prev=float(df["Low"].iloc[i - 1]),
            open_now=float(df["Open"].iloc[i]),
            close_now=float(close.iloc[i]),
            atr_now=atr_approx,
            stop_multiplier=1.0,
        )
        # sl_stop is relative fraction: (close - stop) / close
        scalar_sl_pct = (float(close.iloc[i]) - scalar_stop) / float(close.iloc[i])
        vbt_sl_pct = float(arrs["sl_stop"].iloc[i])

        # Allow for ATR computation differences (actual vs approximate)
        assert abs(vbt_sl_pct - scalar_sl_pct) < 0.05, (
            f"SL fraction mismatch at bar {bar}: vbt={vbt_sl_pct:.4f}, scalar≈{scalar_sl_pct:.4f}"
        )

    def test_sl_pct_always_positive(self):
        df = _make_ohlcv()
        arrs = build_vbt_arrays(df)
        assert (arrs["sl_stop"] > 0).all(), "sl_stop must always be > 0"

    def test_tp_pct_non_negative(self):
        df = _make_ohlcv()
        arrs = build_vbt_arrays(df)
        assert (arrs["tp_stop"] >= 0).all(), "tp_stop must be >= 0"

    def test_tp_sl_ratio_matches_rr_multiplier(self):
        """tp_pct / sl_pct should equal risk_reward_multiplier at entry bars."""
        df = _make_ohlcv()
        rr = 2.0
        s = StrategySettings(risk_reward_multiplier=rr)
        arrs = build_vbt_arrays(df, s)

        entry_bars = arrs["entries"][arrs["entries"]] | arrs["short_entries"][arrs["short_entries"]]
        entry_idx = entry_bars[entry_bars].index
        if len(entry_idx) == 0:
            pytest.skip("No entries generated")

        for bar in entry_idx[:5]:
            i = df.index.get_loc(bar)
            sl = float(arrs["sl_stop"].iloc[i])
            tp = float(arrs["tp_stop"].iloc[i])
            if sl > 0:
                ratio = tp / sl
                assert abs(ratio - rr) < 1e-6, f"RR ratio {ratio:.4f} != {rr} at bar {bar}"


class TestMinimumRrFilter:
    def test_minimum_rr_zero_unchanged(self):
        df = _make_ohlcv()
        s_no_filter = StrategySettings(minimum_rr=0.0)
        s_filter = StrategySettings(minimum_rr=0.0)
        a1 = build_vbt_arrays(df, s_no_filter)
        a2 = build_vbt_arrays(df, s_filter)
        assert a1["entries"].equals(a2["entries"])

    def test_minimum_rr_reduces_or_keeps_entries(self):
        df = _make_ohlcv()
        s_low = StrategySettings(minimum_rr=0.0)
        s_high = StrategySettings(minimum_rr=10.0)  # very strict
        a_low = build_vbt_arrays(df, s_low)
        a_high = build_vbt_arrays(df, s_high)
        assert a_high["entries"].sum() <= a_low["entries"].sum()
        assert a_high["short_entries"].sum() <= a_low["short_entries"].sum()


class TestPositionSizing:
    def test_size_within_valid_range(self):
        df = _make_ohlcv()
        arrs = build_vbt_arrays(df)
        assert (arrs["size"] >= 0).all()
        assert (arrs["size"] <= 1.0).all()

    def test_size_scales_with_risk_per_trade(self):
        df = _make_ohlcv()
        s1 = StrategySettings(risk_per_trade=1.0)
        s2 = StrategySettings(risk_per_trade=2.0)
        a1 = build_vbt_arrays(df, s1)
        a2 = build_vbt_arrays(df, s2)
        # Higher risk_per_trade should produce larger sizes (at same SL distance)
        assert a2["size"].mean() > a1["size"].mean() * 1.5
