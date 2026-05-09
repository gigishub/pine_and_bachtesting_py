"""Tests for bull_strategy regime phase indicator modules."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from bull_strategy.hypothesis_test_v2.regime.indicators.ema_slope_up import signal as ema_slope_signal
from bull_strategy.hypothesis_test_v2.regime.indicators.close_above_ema import signal as close_above_ema_signal
from bull_strategy.hypothesis_test_v2.regime.indicators.close_above_bbands_upper import signal as bb_signal
from bull_strategy.hypothesis_test_v2.regime.indicators.close_above_sar import signal as sar_signal
from bull_strategy.hypothesis_test_v2.regime.indicators.rsi_bull_zone import signal as rsi_zone_signal
from bull_strategy.hypothesis_test_v2.regime.indicators.rsi_bull_slope_zone import signal as rsi_slope_signal
from bull_strategy.hypothesis_test_v2.regime.indicators.rsi_bull_momentum_zone import signal as rsi_momentum_signal
from bull_strategy.hypothesis_test_v2.regime.indicators.funding_rate import signal as funding_bull_signal


def test_ema_slope_up_detects_rising_ema() -> None:
    """EMA slope should be positive (True) on a steadily rising price series."""
    idx = pd.date_range("2021-01-01", periods=60, freq="D")
    closes = pd.Series(range(60), index=idx, dtype=float)
    df = pd.DataFrame({"close": closes})

    result = ema_slope_signal(df, {"period": 20})

    assert result.dtype == bool
    # Later bars (after warm-up) should be True — EMA is rising
    assert result.iloc[-10:].all(), "Rising price should yield upward EMA slope"


def test_ema_slope_up_false_on_falling_price() -> None:
    """Falling prices → negative EMA slope → all False."""
    idx = pd.date_range("2021-01-01", periods=60, freq="D")
    closes = pd.Series(range(60, 0, -1), index=idx, dtype=float)
    df = pd.DataFrame({"close": closes})

    result = ema_slope_signal(df, {"period": 20})

    assert result.dtype == bool
    assert not result.iloc[-10:].any(), "Falling price should yield downward EMA slope"


def test_close_above_ema_fires_when_price_above() -> None:
    """close > EMA should be True after a sharp price spike above the EMA."""
    idx = pd.date_range("2021-01-01", periods=50, freq="D")
    # Flat at 100 then jump to 200 on the last bar
    closes = pd.Series([100.0] * 49 + [200.0], index=idx)
    df = pd.DataFrame({"close": closes})

    result = close_above_ema_signal(df, {"period": 20})

    assert result.dtype == bool
    assert result.iloc[-1], "Price far above EMA should return True on last bar"


def test_close_above_ema_false_when_price_below() -> None:
    """close < EMA → close_above_ema should return False."""
    idx = pd.date_range("2021-01-01", periods=50, freq="D")
    # Flat at 100 then drop to 50 on the last bar
    closes = pd.Series([100.0] * 49 + [50.0], index=idx)
    df = pd.DataFrame({"close": closes})

    result = close_above_ema_signal(df, {"period": 20})

    assert result.dtype == bool
    assert not result.iloc[-1], "Price far below EMA should return False on last bar"


def test_close_above_bbands_upper_detects_price_above_upper_band() -> None:
    """A sharp spike upward should push price above the upper Bollinger Band."""
    idx = pd.date_range("2021-01-01", periods=10, freq="D")
    close = pd.Series([100, 99, 101, 100, 98, 99, 100, 101, 99, 120], index=idx)
    df = pd.DataFrame({"close": close})

    result = bb_signal(df, {"period": 5, "std_dev": 1.5})

    assert result.dtype == bool
    assert result.iloc[-1], "Price spike should be above upper Bollinger Band"


def test_close_above_sar_reports_uptrend_for_rising_price() -> None:
    """Steadily rising prices should produce a SAR bullish regime (close > SAR)."""
    idx = pd.date_range("2021-01-01", periods=10, freq="D")
    df = pd.DataFrame(
        {
            "high":  [101, 103, 105, 106, 108, 109, 111, 112, 114, 115],
            "low":   [ 99, 101, 103, 104, 106, 107, 109, 110, 112, 113],
            "close": [100, 102, 104, 105, 107, 108, 110, 111, 113, 114],
        },
        index=idx,
    )

    result = sar_signal(df, {"af_initial": 0.02, "af_step": 0.02, "af_max": 0.20})

    assert result.dtype == bool
    assert result.iloc[-1], "Persistent uptrend should be detected as SAR bullish regime"


# ── Helper: build a price series that keeps RSI in the bull zone (50–70) ─────

def _bull_zone_close(n: int = 100) -> pd.Series:
    """Alternating +0.9 / -0.5 pattern keeps RSI in ~52–65 range."""
    rng = np.array([0.9, -0.5] * (n // 2 + 1))[:n]
    prices = 100.0 + np.cumsum(rng)
    idx = pd.date_range("2021-01-01", periods=n, freq="h")
    return pd.Series(prices, index=idx)


def _oversold_close(n: int = 100) -> pd.Series:
    """Steady downtrend pushes RSI well below 50."""
    idx = pd.date_range("2021-01-01", periods=n, freq="h")
    return pd.Series(range(200, 200 - n, -1), index=idx, dtype=float)


def test_rsi_bull_zone_fires_in_bull_zone() -> None:
    """RSI and RSI_MA both in (50, 70) — signal should be True on later bars."""
    df = pd.DataFrame({"close": _bull_zone_close(100)})
    result = rsi_zone_signal(df, {"rsi_period": 14, "ma_period": 9, "lower": 50, "upper": 70})
    assert result.dtype == bool
    assert result.iloc[30:].any(), "RSI bull zone should fire during bull-zone price pattern"


def test_rsi_bull_zone_no_fire_oversold() -> None:
    """Steady downtrend → RSI far below 50 → should not fire."""
    df = pd.DataFrame({"close": _oversold_close(100)})
    result = rsi_zone_signal(df, {"rsi_period": 14, "ma_period": 9, "lower": 50, "upper": 70})
    assert result.dtype == bool
    assert not result.iloc[30:].any(), "Oversold RSI should not fire rsi_bull_zone"


def test_rsi_bull_slope_zone_fires_with_rising_rsi_ma() -> None:
    """With zone price, add a rising stretch so RSI_MA slope goes positive.

    Phase 1 (+0.5/-0.4, 80 bars): RSI ~55 — warms up in zone.
    Phase 2 (+0.8/-0.5, 80 bars): RSI ~62 — RSI_MA drifts higher → slope > 0.
    """
    rng: list[float] = [0.5, -0.4] * 40 + [0.8, -0.5] * 40
    prices = 100.0 + np.cumsum(rng)
    n = len(prices)
    idx = pd.date_range("2021-01-01", periods=n, freq="h")
    df = pd.DataFrame({"close": pd.Series(prices, index=idx)})

    result = rsi_slope_signal(df, {"rsi_period": 14, "ma_period": 9, "lower": 50, "upper": 70})
    assert result.dtype == bool
    # After phase-2 starts (bar 90+) RSI_MA should be rising inside zone
    assert result.iloc[90:130].any(), "Rising RSI_MA in zone should fire rsi_bull_slope_zone"


def test_rsi_bull_slope_zone_no_fire_oversold() -> None:
    """Oversold: neither zone nor slope criteria met."""
    df = pd.DataFrame({"close": _oversold_close(100)})
    result = rsi_slope_signal(df, {"rsi_period": 14, "ma_period": 9, "lower": 50, "upper": 70})
    assert not result.iloc[30:].any(), "Oversold RSI should not fire rsi_bull_slope_zone"


def test_rsi_bull_momentum_zone_fires_when_rsi_rising_in_zone() -> None:
    """During the bull-zone pattern RSI rises on 'up' bars — momentum fires."""
    df = pd.DataFrame({"close": _bull_zone_close(100)})
    result = rsi_momentum_signal(df, {"rsi_period": 14, "lower": 50, "upper": 70})
    assert result.dtype == bool
    assert result.iloc[20:].any(), "Rising RSI in zone should fire rsi_bull_momentum_zone"


def test_rsi_bull_momentum_zone_no_fire_oversold() -> None:
    """Oversold: RSI below 50, momentum indicator should not fire."""
    df = pd.DataFrame({"close": _oversold_close(100)})
    result = rsi_momentum_signal(df, {"rsi_period": 14, "lower": 50, "upper": 70})
    assert not result.iloc[30:].any(), "Oversold RSI should not fire rsi_bull_momentum_zone"


# ── Helper: build a synthetic funding rate DataFrame ─────────────────────────

def _funding_df(rates: list[float], start: str = "2021-01-01 00:00") -> pd.DataFrame:
    """Build a fake 8h funding parquet-like DataFrame."""
    idx = pd.date_range(start, periods=len(rates), freq="8h")
    return pd.DataFrame({"fundingrate": rates}, index=idx)


def _price_df(n: int = 50) -> pd.DataFrame:
    """Hourly OHLCV stub — only 'close' needed by funding indicator."""
    idx = pd.date_range("2021-01-01", periods=n, freq="h")
    return pd.DataFrame({"close": 100.0}, index=idx)


def test_funding_bull_fires_when_rate_positive() -> None:
    """Positive funding → signal should be True (bullish regime confirmed)."""
    rates = [0.0005] * 20
    df  = _price_df(60)
    params = {"threshold": 0.0, "ma_period": 1, "_funding_df": _funding_df(rates)}
    result = funding_bull_signal(df, params)
    assert result.dtype == bool
    assert result.iloc[10:].any(), "Positive funding should fire bull funding signal"


def test_funding_bull_no_fire_when_rate_negative() -> None:
    """All negative funding → threshold=0 → signal should be False."""
    rates = [-0.0005] * 20
    df  = _price_df(60)
    params = {"threshold": 0.0, "ma_period": 1, "_funding_df": _funding_df(rates)}
    result = funding_bull_signal(df, params)
    assert result.dtype == bool
    assert not result.any(), "Negative funding should not fire bull funding signal (threshold=0)"


def test_funding_bull_ma_smoothing_reduces_noise() -> None:
    """One spike into negative should not break an otherwise-positive MA signal."""
    rates = [0.0005] * 18 + [-0.01] + [0.0005]
    df  = _price_df(80)
    params = {"threshold": 0.0, "ma_period": 3, "_funding_df": _funding_df(rates)}
    result = funding_bull_signal(df, params)
    assert result.iloc[5:18].all(), "MA should smooth over a single negative spike"
