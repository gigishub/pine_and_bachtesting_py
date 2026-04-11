"""Unit tests for indicator modules (ADX, EMA Ribbon, Donchian, Volume Profile,
Relative Strength, CMF, Power Candle, PSAR, Bollinger Bands)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from adaptive_momentum_strategy.strategy.indicators.adx import compute_adx, regime_is_trending
from adaptive_momentum_strategy.strategy.indicators.ema_ribbon import (
    compute_ema_ribbon,
    regime_is_aligned,
)
from adaptive_momentum_strategy.strategy.indicators.donchian import (
    compute_donchian_upper,
    compute_donchian_lower,
    compute_donchian_squeeze,
    setup_is_active,
)
from adaptive_momentum_strategy.strategy.indicators.volume_profile import (
    compute_vah_series,
    setup_is_above_vah,
)
from adaptive_momentum_strategy.strategy.indicators.relative_strength import (
    compute_returns,
    setup_is_relatively_strong,
)
from adaptive_momentum_strategy.strategy.indicators.cmf import compute_cmf, trigger_is_active
from adaptive_momentum_strategy.strategy.indicators.power_candle import trigger_is_power_candle
from adaptive_momentum_strategy.strategy.risk.psar import compute_psar_stop_series
from adaptive_momentum_strategy.strategy.risk.bbands import compute_bbands_upper


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_ohlcv(n: int = 300, seed: int = 42) -> pd.DataFrame:
    """Deterministic synthetic OHLCV with a slight upward trend."""
    rng = np.random.default_rng(seed)
    close = 30_000 + np.cumsum(rng.normal(10, 200, n))
    spread = np.abs(rng.normal(0, 150, n))
    high = close + spread
    low = close - spread
    open_ = close - rng.normal(0, 50, n)
    volume = np.abs(rng.normal(500, 100, n))
    idx = pd.date_range("2024-01-01", periods=n, freq="1h", tz="UTC")
    return pd.DataFrame(
        {"Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume},
        index=idx,
    )


# ---------------------------------------------------------------------------
# ADX
# ---------------------------------------------------------------------------

class TestADX:
    def test_length_matches_input(self):
        df = _make_ohlcv()
        adx = compute_adx(df["High"], df["Low"], df["Close"], period=14)
        assert len(adx) == len(df)

    def test_nan_during_warmup(self):
        df = _make_ohlcv()
        adx = compute_adx(df["High"], df["Low"], df["Close"], period=14)
        assert adx.iloc[:10].isna().any()

    def test_values_in_valid_range(self):
        df = _make_ohlcv()
        adx = compute_adx(df["High"], df["Low"], df["Close"], period=14)
        valid = adx.dropna()
        assert (valid >= 0).all() and (valid <= 100).all()

    def test_regime_filter_is_boolean_series(self):
        df = _make_ohlcv()
        adx = compute_adx(df["High"], df["Low"], df["Close"], period=14)
        regime = regime_is_trending(adx, threshold=25.0)
        assert set(regime.unique()).issubset({True, False})

    def test_no_lookahead_shift(self):
        df = _make_ohlcv()
        adx_orig = compute_adx(df["High"], df["Low"], df["Close"])
        df2 = df.copy()
        df2["Close"] = df2["Close"].shift(1)
        adx_shifted = compute_adx(df2["High"], df2["Low"], df2["Close"])
        assert not adx_orig.equals(adx_shifted)


# ---------------------------------------------------------------------------
# EMA Ribbon
# ---------------------------------------------------------------------------

class TestEMARibbon:
    def test_returns_three_series(self):
        df = _make_ohlcv()
        fast, mid, slow = compute_ema_ribbon(df["Close"])
        assert len(fast) == len(mid) == len(slow) == len(df)

    def test_aligned_on_strong_trend(self):
        """In a perfectly monotonic uptrend, ribbon should align quickly."""
        n = 300
        close = pd.Series(range(1, n + 1), dtype=float)
        fast, mid, slow = compute_ema_ribbon(close, fast=5, mid=10, slow=20)
        # After ~20 bars of warmup the ribbon should be aligned.
        aligned = regime_is_aligned(fast, mid, slow)
        assert aligned.iloc[-50:].all()

    def test_not_aligned_in_downtrend(self):
        n = 300
        close = pd.Series(list(range(n, 0, -1)), dtype=float)
        fast, mid, slow = compute_ema_ribbon(close, fast=5, mid=10, slow=20)
        aligned = regime_is_aligned(fast, mid, slow)
        assert not aligned.iloc[-50:].any()

    def test_output_is_boolean(self):
        df = _make_ohlcv()
        fast, mid, slow = compute_ema_ribbon(df["Close"])
        result = regime_is_aligned(fast, mid, slow)
        assert set(result.unique()).issubset({True, False})


# ---------------------------------------------------------------------------
# Donchian
# ---------------------------------------------------------------------------

class TestDonchian:
    def test_upper_gte_close(self):
        df = _make_ohlcv()
        upper = compute_donchian_upper(df["High"], lookback=20)
        valid = upper.dropna()
        assert (valid >= df["High"].dropna().loc[valid.index]).all()

    def test_lower_lte_close(self):
        df = _make_ohlcv()
        lower = compute_donchian_lower(df["Low"], lookback=20)
        valid = lower.dropna()
        assert (valid <= df["Low"].dropna().loc[valid.index]).all()

    def test_squeeze_produces_booleans(self):
        df = _make_ohlcv(n=500)
        squeeze = compute_donchian_squeeze(df["High"], df["Low"], lookback=20, squeeze_history=60)
        assert set(squeeze.unique()).issubset({True, False})

    def test_squeeze_fires_sometimes(self):
        df = _make_ohlcv(n=500)
        squeeze = compute_donchian_squeeze(df["High"], df["Low"], lookback=20, squeeze_history=60)
        assert squeeze.sum() > 0

    def test_setup_active_requires_both_conditions(self):
        df = _make_ohlcv(n=300)
        upper = compute_donchian_upper(df["High"], lookback=20)
        squeeze = compute_donchian_squeeze(df["High"], df["Low"], lookback=20, squeeze_history=60)
        active = setup_is_active(df["Close"], upper, squeeze)
        for idx in active[active].index:
            assert df["Close"].loc[idx] >= upper.loc[idx] * 0.99
            assert squeeze.loc[idx]


# ---------------------------------------------------------------------------
# Volume Profile VAH
# ---------------------------------------------------------------------------

class TestVolumeProfileVAH:
    def test_length_matches_input(self):
        df = _make_ohlcv(n=300)
        vah = compute_vah_series(df["High"], df["Low"], df["Close"], df["Volume"],
                                  session_bars=24, lookback_sessions=2)
        assert len(vah) == len(df)

    def test_nan_during_warmup(self):
        df = _make_ohlcv(n=200)
        vah = compute_vah_series(df["High"], df["Low"], df["Close"], df["Volume"],
                                  session_bars=24, lookback_sessions=2)
        # First 47 bars (24×2 - 1) must be NaN.
        assert vah.iloc[:47].isna().all()

    def test_vah_within_high_low_range(self):
        df = _make_ohlcv(n=200)
        vah = compute_vah_series(df["High"], df["Low"], df["Close"], df["Volume"],
                                  session_bars=24, lookback_sessions=2)
        valid = vah.dropna()
        # VAH is the upper edge of the highest value-area bin, so it must be
        # within the dataset's overall high/low range (allow tiny float tolerance).
        assert (valid >= df["Low"].min() - 1e-6).all()
        assert (valid <= df["High"].max() + 1e-6).all()

    def test_setup_above_vah_is_boolean(self):
        df = _make_ohlcv(n=300)
        vah = compute_vah_series(df["High"], df["Low"], df["Close"], df["Volume"],
                                  session_bars=24, lookback_sessions=2)
        result = setup_is_above_vah(df["Close"], vah, consecutive_bars=2)
        assert set(result.unique()).issubset({True, False})


# ---------------------------------------------------------------------------
# Relative Strength
# ---------------------------------------------------------------------------

class TestRelativeStrength:
    def test_returns_length_matches(self):
        df = _make_ohlcv(n=200)
        ret = compute_returns(df["Close"], period=24)
        assert len(ret) == len(df)

    def test_strong_outperformance_fires(self):
        """Asset with exponentially higher growth rate must fire the RS signal."""
        n = 100
        # Use exponential growth so pct_change returns differ (linear series give equal returns).
        bench = pd.Series([1.0 * 1.01**i for i in range(n)])   # +1% per bar
        token = pd.Series([1.0 * 1.04**i for i in range(n)])   # +4% per bar
        result = setup_is_relatively_strong(token, bench, period=5, multiplier=1.5,
                                             ratio_sma_period=10)
        assert result.iloc[-20:].sum() > 0

    def test_underperformance_does_not_fire(self):
        """Asset that underperforms benchmark should not fire."""
        n = 100
        bench = pd.Series([1 + i * 3 for i in range(n)], dtype=float)
        token = pd.Series(range(1, n + 1), dtype=float)
        result = setup_is_relatively_strong(token, bench, period=5, multiplier=1.5,
                                             ratio_sma_period=10)
        assert result.iloc[-20:].sum() == 0

    def test_output_is_boolean(self):
        df = _make_ohlcv(n=200)
        bench_df = _make_ohlcv(n=200, seed=99)
        result = setup_is_relatively_strong(df["Close"], bench_df["Close"])
        assert set(result.unique()).issubset({True, False})


# ---------------------------------------------------------------------------
# CMF
# ---------------------------------------------------------------------------

class TestCMF:
    def test_length_matches_input(self):
        df = _make_ohlcv()
        cmf = compute_cmf(df["High"], df["Low"], df["Close"], df["Volume"], period=20)
        assert len(cmf) == len(df)

    def test_values_roughly_in_range(self):
        df = _make_ohlcv()
        cmf = compute_cmf(df["High"], df["Low"], df["Close"], df["Volume"], period=20)
        valid = cmf.dropna()
        assert (valid >= -1.05).all() and (valid <= 1.05).all()

    def test_trigger_active_is_boolean(self):
        df = _make_ohlcv()
        cmf = compute_cmf(df["High"], df["Low"], df["Close"], df["Volume"], period=20)
        trig = trigger_is_active(cmf, threshold=0.05)
        assert set(trig.unique()).issubset({True, False})


# ---------------------------------------------------------------------------
# Power Candle
# ---------------------------------------------------------------------------

class TestPowerCandle:
    def test_length_matches_input(self):
        df = _make_ohlcv(n=200)
        result = trigger_is_power_candle(df["Close"], df["High"], df["Volume"])
        assert len(result) == len(df)

    def test_fires_on_high_volume_breakout(self):
        """A bar at a new N-bar high on very high volume must fire."""
        n = 50
        # close == high so the last bar is always at a new lookback high.
        close = pd.Series(list(range(1, n + 1)), dtype=float)
        high = close.copy()
        # Last bar has volume 10× the SMA baseline.
        volume = pd.Series([100.0] * (n - 1) + [1000.0])
        result = trigger_is_power_candle(close, high, volume, lookback=5,
                                          vol_period=10, vol_multiplier=1.5)
        assert result.iloc[-1]

    def test_does_not_fire_on_low_volume(self):
        """A breakout on average volume must NOT fire."""
        n = 50
        close = pd.Series(list(range(1, n + 1)), dtype=float)
        high = close + 0.5
        volume = pd.Series([100.0] * n)
        result = trigger_is_power_candle(close, high, volume, lookback=5,
                                          vol_period=10, vol_multiplier=1.5)
        assert not result.iloc[-1]

    def test_output_is_boolean(self):
        df = _make_ohlcv(n=200)
        result = trigger_is_power_candle(df["Close"], df["High"], df["Volume"])
        assert set(result.unique()).issubset({True, False})


# ---------------------------------------------------------------------------
# PSAR Stop
# ---------------------------------------------------------------------------

class TestPSARStop:
    def test_length_matches_input(self):
        df = _make_ohlcv(n=200)
        stop = compute_psar_stop_series(df["High"], df["Low"], df["Close"])
        assert len(stop) == len(df)

    def test_nan_during_warmup(self):
        df = _make_ohlcv(n=200)
        stop = compute_psar_stop_series(df["High"], df["Low"], df["Close"])
        # Should have some NaNs at the start.
        assert stop.isna().any()

    def test_stop_below_price_in_uptrend(self):
        """In a perfect uptrend the long SAR should be below current price."""
        n = 200
        close = pd.Series([10000.0 + i * 10 for i in range(n)])
        high = close + 50
        low = close - 50
        stop = compute_psar_stop_series(high, low, close)
        valid = stop.dropna()
        assert (valid < close.loc[valid.index]).all()


# ---------------------------------------------------------------------------
# Bollinger Band Upper
# ---------------------------------------------------------------------------

class TestBBandsUpper:
    def test_length_matches_input(self):
        df = _make_ohlcv(n=200)
        upper = compute_bbands_upper(df["Close"], period=20, std=2.0)
        assert len(upper) == len(df)

    def test_nan_during_warmup(self):
        df = _make_ohlcv(n=200)
        upper = compute_bbands_upper(df["Close"], period=20, std=2.0)
        assert upper.iloc[:19].isna().all()

    def test_upper_band_above_close_mostly(self):
        """Upper band should be above close for most bars in a random walk."""
        df = _make_ohlcv(n=200)
        upper = compute_bbands_upper(df["Close"], period=20, std=2.0)
        valid = upper.dropna()
        pct_above = (valid >= df["Close"].loc[valid.index]).mean()
        assert pct_above >= 0.85  # at least 85% of the time
