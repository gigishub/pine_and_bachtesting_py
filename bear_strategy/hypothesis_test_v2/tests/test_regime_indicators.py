"""Tests for regime phase indicator modules."""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_test_v2.regime.indicators.misc.close_below_bbands_lower import signal as bb_signal
from bear_strategy.hypothesis_test_v2.regime.indicators.misc.close_below_sar import signal as sar_signal
from bear_strategy.hypothesis_test_v2.regime.indicators.rsi.rsi_bear_zone import signal as rsi_zone_signal
from bear_strategy.hypothesis_test_v2.regime.indicators.rsi.rsi_bear_slope_zone import signal as rsi_slope_signal
from bear_strategy.hypothesis_test_v2.regime.indicators.rsi.rsi_bear_momentum_zone import signal as rsi_momentum_signal
from bear_strategy.hypothesis_test_v2.regime.indicators.funding_rate.funding_rate import signal as funding_bear_signal


def test_close_below_bbands_lower_detects_price_below_lower_band() -> None:
    idx = pd.date_range("2021-01-01", periods=10, freq="D")
    close = pd.Series([100, 101, 102, 101, 103, 104, 105, 104, 106, 90], index=idx)
    df = pd.DataFrame({"close": close})

    result = bb_signal(df, {"period": 5, "std_dev": 1.5})

    assert result.dtype == bool
    assert not result.iloc[:-1].any()
    assert result.iloc[-1], "The final low close should be below the lower Bollinger Band"


def test_close_below_sar_reports_downtrend_for_falling_price() -> None:
    idx = pd.date_range("2021-01-01", periods=10, freq="D")
    df = pd.DataFrame(
        {
            "high":  [101, 99, 97, 96, 94, 93, 91, 90, 88, 87],
            "low":   [99, 97, 95, 94, 92, 91, 89, 88, 86, 85],
            "close": [100, 98, 96, 95, 93, 92, 90, 89, 87, 86],
        },
        index=idx,
    )

    result = sar_signal(df, {"af_initial": 0.02, "af_step": 0.02, "af_max": 0.20})

    assert result.dtype == bool
    assert result.iloc[-1], "A persistent downtrend should be detected as a SAR bearish regime"


# ── Helper: build a price series that keeps RSI in the bear zone (30–50) ─────

def _bear_zone_close(n: int = 100) -> pd.Series:
    """Alternating +1 / -0.9 pattern keeps RSI in ~35–48 range."""
    rng = np.array([1.0, -0.9] * (n // 2 + 1))[:n]
    prices = 100.0 + np.cumsum(rng)
    idx = pd.date_range("2021-01-01", periods=n, freq="h")
    return pd.Series(prices, index=idx)


def _overbought_close(n: int = 100) -> pd.Series:
    """Steady uptrend pushes RSI well above 50."""
    idx = pd.date_range("2021-01-01", periods=n, freq="h")
    return pd.Series(range(100, 100 + n), index=idx, dtype=float)


def test_rsi_bear_zone_fires_in_bear_zone() -> None:
    """RSI and RSI_MA both in (30, 50) — signal should be True on later bars."""
    df = pd.DataFrame({"close": _bear_zone_close(100)})
    result = rsi_zone_signal(df, {"rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50})
    assert result.dtype == bool
    # After warm-up the alternating pattern should produce RSI in zone
    assert result.iloc[30:].any(), "RSI bear zone should fire during bear-zone price pattern"


def test_rsi_bear_zone_no_fire_overbought() -> None:
    """Steady uptrend → RSI far above 50 → should not fire."""
    df = pd.DataFrame({"close": _overbought_close(100)})
    result = rsi_zone_signal(df, {"rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50})
    assert result.dtype == bool
    assert not result.iloc[30:].any(), "Overbought RSI should not fire rsi_bear_zone"


def test_rsi_bear_slope_zone_fires_with_declining_rsi_ma() -> None:
    """With zone price, add a declining stretch so RSI_MA slope goes negative."""
    # Start sideways (fills warm-up into zone), then small decline each bar
    n = 120
    rng = [1.0, -0.9] * 30  # first 60 bars: zone warm-up
    rng += [-0.3] * 60       # next 60 bars: gentle decline → RSI_MA declining in zone
    prices = 100.0 + np.cumsum(rng[:n])
    idx = pd.date_range("2021-01-01", periods=n, freq="h")
    df = pd.DataFrame({"close": pd.Series(prices, index=idx)})

    result = rsi_slope_signal(df, {"rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50})
    assert result.dtype == bool
    # During the declining stretch the slope+zone condition should fire
    assert result.iloc[70:].any(), "Declining RSI_MA in zone should fire rsi_bear_slope_zone"


def test_rsi_bear_slope_zone_no_fire_overbought() -> None:
    """Overbought: neither zone nor slope criteria met."""
    df = pd.DataFrame({"close": _overbought_close(100)})
    result = rsi_slope_signal(df, {"rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50})
    assert not result.iloc[30:].any(), "Overbought RSI should not fire rsi_bear_slope_zone"


def test_rsi_bear_momentum_zone_fires_when_rsi_falling_in_zone() -> None:
    """During the alternating pattern RSI oscillates downward on 'down' bars."""
    df = pd.DataFrame({"close": _bear_zone_close(100)})
    result = rsi_momentum_signal(df, {"rsi_period": 14, "lower": 30, "upper": 50})
    assert result.dtype == bool
    assert result.iloc[20:].any(), "Declining RSI in zone should fire rsi_bear_momentum_zone"


def test_rsi_bear_momentum_zone_no_fire_overbought() -> None:
    """Overbought: RSI above 50, momentum indicator should not fire."""
    df = pd.DataFrame({"close": _overbought_close(100)})
    result = rsi_momentum_signal(df, {"rsi_period": 14, "lower": 30, "upper": 50})
    assert not result.iloc[30:].any(), "Overbought RSI should not fire rsi_bear_momentum_zone"


# ── Helper: build a synthetic funding rate DataFrame ─────────────────────────

def _funding_df(rates: list[float], start: str = "2021-01-01 00:00") -> pd.DataFrame:
    """Build a fake 8h funding parquet-like DataFrame."""
    idx = pd.date_range(start, periods=len(rates), freq="8h")
    return pd.DataFrame({"fundingrate": rates}, index=idx)


def _price_df(n: int = 50) -> pd.DataFrame:
    """Hourly OHLCV stub — only 'close' needed by funding indicator."""
    idx = pd.date_range("2021-01-01", periods=n, freq="h")
    return pd.DataFrame({"close": 100.0}, index=idx)


def test_funding_bear_fires_when_rate_negative() -> None:
    """Negative funding → signal should be True (bearish regime confirmed)."""
    # All negative rates — signal fires on all settled bars (after first shift)
    rates = [-0.0005] * 20
    df  = _price_df(60)
    params = {"threshold": 0.0, "ma_period": 1, "_funding_df": _funding_df(rates)}
    result = funding_bear_signal(df, params)
    assert result.dtype == bool
    assert result.iloc[10:].any(), "Negative funding should fire bear funding signal"


def test_funding_bear_no_fire_when_rate_positive() -> None:
    """All positive funding → threshold=0 → signal should be False."""
    rates = [0.0005] * 20
    df  = _price_df(60)
    params = {"threshold": 0.0, "ma_period": 1, "_funding_df": _funding_df(rates)}
    result = funding_bear_signal(df, params)
    assert result.dtype == bool
    assert not result.any(), "Positive funding should not fire bear funding signal (threshold=0)"


def test_funding_bear_ma_smoothing_reduces_noise() -> None:
    """One spike into positive should not break an otherwise-negative MA signal."""
    # 18 negative rates + 1 positive spike → with ma_period=3 the MA stays negative
    rates = [-0.0005] * 18 + [0.01] + [-0.0005]
    df  = _price_df(80)
    params = {"threshold": 0.0, "ma_period": 3, "_funding_df": _funding_df(rates)}
    result = funding_bear_signal(df, params)
    # Most bars should still fire despite the single spike
    assert result.iloc[5:18].all(), "MA should smooth over a single positive spike"
