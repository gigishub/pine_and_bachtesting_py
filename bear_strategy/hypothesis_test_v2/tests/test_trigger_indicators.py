"""Tests for newly added trigger indicator modules."""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.trigger.indicators.adx_di_minus_cross import signal as adx_signal
from bear_strategy.hypothesis_test_v2.trigger.indicators.bb_percent_b_below import signal as bb_signal
from bear_strategy.hypothesis_test_v2.trigger.indicators.close_below_prior_low import signal as inside_bar_signal
from bear_strategy.hypothesis_test_v2.trigger.indicators.stoch_cross_below import signal as stoch_signal
from bear_strategy.hypothesis_test_v2.trigger.indicators.vwap_close_below import signal as vwap_signal


def test_close_below_prior_low_detects_price_action() -> None:
    idx = pd.date_range("2021-01-01", periods=3, freq="h")
    df = pd.DataFrame(
        {
            "high": [100, 101, 99],
            "low": [98, 99, 92],
            "close": [99, 100, 91],
            "volume": [1000, 1100, 1200],
        },
        index=idx,
    )

    result = inside_bar_signal(df, {})
    assert result.dtype == bool
    assert result.iloc[-1], "Close below prior low should fire on the final bar"


def test_bb_percent_b_drops_below_half() -> None:
    idx = pd.date_range("2021-01-01", periods=30, freq="h")
    close = pd.Series([100.0] * 10 + [110.0] * 10 + [105.0] * 10, index=idx)
    df = pd.DataFrame({"close": close})

    result = bb_signal(df, {"length": 10, "std": 2.0, "threshold": 0.5})
    assert result.dtype == bool
    assert result.iloc[-1], "BB %B should be below 0.5 after price drops back toward the middle band"


def test_vwap_close_below_fires_when_price_drops_below_daily_vwap() -> None:
    idx = pd.date_range("2021-01-01", periods=5, freq="h")
    df = pd.DataFrame(
        {
            "high": [100, 102, 104, 103, 99],
            "low": [98, 100, 101, 100, 94],
            "close": [99, 101, 103, 102, 95],
            "volume": [100, 120, 110, 100, 130],
        },
        index=idx,
    )

    result = vwap_signal(df, {})
    assert result.dtype == bool
    assert result.iloc[-1], "Close below daily VWAP should fire on a genuine VWAP breakout lower"


def test_stoch_cross_below_threshold_detects_failed_rally() -> None:
    idx = pd.date_range("2021-01-01", periods=30, freq="h")
    high = pd.Series([100, 101, 102, 103, 104, 103, 102, 101, 100, 99] + [99] * 20, index=idx)
    low = pd.Series([98, 99, 100, 101, 102, 101, 100, 99, 98, 97] + [97] * 20, index=idx)
    close = pd.Series([99, 100, 101, 102, 103, 102, 101, 100, 99, 98] + [98] * 20, index=idx)
    df = pd.DataFrame({"high": high, "low": low, "close": close})

    result = stoch_signal(df, {"k_period": 5, "d_period": 3, "smooth_k": 3, "threshold": 50.0})
    assert result.dtype == bool
    assert result.iloc[-1], "Stochastic cross below 50 should fire after an early rally fails"


def test_adx_di_minus_cross_detects_bearish_trend_strength() -> None:
    idx = pd.date_range("2021-01-01", periods=40, freq="h")
    high = pd.Series(list(range(100, 120)), index=idx)
    low = pd.Series(list(range(98, 118)), index=idx)
    close = pd.Series(list(range(99, 119)), index=idx)
    close.iloc[30:] = close.iloc[30:] - 5
    df = pd.DataFrame({"high": high, "low": low, "close": close})

    result = adx_signal(df, {"length": 14, "adx_threshold": 20.0})
    assert result.dtype == bool
    assert result.iloc[-1] or result.iloc[-2], "ADX bearish DI- cross should fire on the late downtrend"
