"""Unit tests for the bull_strategy setup indicators."""

from __future__ import annotations

import pandas as pd
import pytest

from bull_strategy.hypothesis_test_v2.setup.indicators.kde_lower import signal as kde_lower_signal
from bull_strategy.hypothesis_test_v2.setup.indicators.rsi_range import signal as rsi_range_signal


# ---------------------------------------------------------------------------
# kde_lower
# ---------------------------------------------------------------------------

def test_kde_lower_fires_when_price_near_lower_peak() -> None:
    """The first N bars below the lower KDE peak should be True (max_bars limit)."""
    idx = pd.date_range("2021-01-01", periods=26, freq="D")
    closes = pd.Series(
        # 20 bars oscillating around 100 then 6 bars near the lower KDE peak (~90)
        [100.0, 101.0, 99.0, 102.0, 98.0, 103.0, 97.0, 104.0, 96.0, 105.0,
         100.0, 101.0, 99.0, 102.0, 98.0, 103.0, 97.0, 104.0, 96.0, 105.0,
         90.0, 90.0, 90.0, 90.0, 90.0, 90.0],
        index=idx,
    )
    df = pd.DataFrame({"close": closes})

    result = kde_lower_signal(df, {"bandwidth": 0.15, "lookback_bars": 20, "max_bars": 5})

    assert result.dtype == bool
    assert result.iloc[:20].sum() == 0,       "Warm-up bars must not fire"
    assert result.iloc[20:25].all(),           "First 5 near-lower-peak bars should be True"
    assert not result.iloc[25],               "Sixth consecutive bar exceeds max_bars → False"


def test_kde_lower_false_when_price_at_high() -> None:
    """Price at the upper extreme of the KDE distribution should NOT fire."""
    idx = pd.date_range("2021-01-01", periods=26, freq="D")
    closes = pd.Series(
        [100.0, 101.0, 99.0, 102.0, 98.0, 103.0, 97.0, 104.0, 96.0, 105.0,
         100.0, 101.0, 99.0, 102.0, 98.0, 103.0, 97.0, 104.0, 96.0, 105.0,
         # Price spikes HIGH — far from the lower KDE peak
         115.0, 116.0, 117.0, 118.0, 119.0, 120.0],
        index=idx,
    )
    df = pd.DataFrame({"close": closes})

    result = kde_lower_signal(df, {"bandwidth": 0.15, "lookback_bars": 20, "max_bars": 5})

    assert result.dtype == bool
    assert not result.iloc[20:].any(), "High prices should not fire lower KDE signal"


# ---------------------------------------------------------------------------
# rsi_range  (35–60 for longs: not oversold, not overbought)
# ---------------------------------------------------------------------------

def test_rsi_range_fires_in_valid_range() -> None:
    """RSI between 35 and 60 should yield True for an alternating up/down series."""
    idx = pd.date_range("2021-01-01", periods=50, freq="D")
    # Alternating +1/-0.8 keeps RSI ≈ 52 (well within [35, 60])
    diffs  = [1.0, -0.8] * 25
    closes = pd.Series(100 + pd.Series(diffs).cumsum().values, index=idx)
    df = pd.DataFrame({"close": closes})

    result = rsi_range_signal(df, {"period": 14, "low": 35, "high": 60})

    assert result.dtype == bool
    assert result.any(), "Alternating up/down series should have RSI in [35, 60]"


def test_rsi_range_false_when_overbought() -> None:
    """An extreme parabolic rally drives RSI above 60 → should be False."""
    idx = pd.date_range("2021-01-01", periods=30, freq="D")
    # Aggressive upward movement: +5 every bar → RSI will be very high
    closes = pd.Series(range(100, 250, 5), index=idx, dtype=float)
    df = pd.DataFrame({"close": closes})

    result = rsi_range_signal(df, {"period": 14, "low": 35, "high": 60})

    assert result.dtype == bool
    # After warmup the RSI of a strong rally should exceed 60 → False
    assert not result.iloc[-5:].any(), "Strong rally should push RSI above 60 → False"


def test_rsi_range_false_when_oversold() -> None:
    """A sharp crash pushes RSI below 35 → should be False."""
    idx = pd.date_range("2021-01-01", periods=30, freq="D")
    # Heavy decline: -5 every bar → RSI will be very low
    closes = pd.Series(range(250, 100, -5), index=idx, dtype=float)
    df = pd.DataFrame({"close": closes})

    result = rsi_range_signal(df, {"period": 14, "low": 35, "high": 60})

    assert result.dtype == bool
    # After warm-up the RSI of a strong decline should be below 35 → False
    assert not result.iloc[-5:].any(), "Strong decline should push RSI below 35 → False"
