"""Unit tests for compute_signals, boolean flag selection, and risk helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from adaptive_momentum_strategy.strategy.parameters import Parameters
from adaptive_momentum_strategy.strategy.signals import compute_signals
from adaptive_momentum_strategy.strategy.risk.stops import ratchet_stop
from adaptive_momentum_strategy.strategy.risk.sizing import compute_position_size


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_ohlcv(n: int = 500, seed: int = 7) -> pd.DataFrame:
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
# compute_signals — default golden path (use_adx + use_donchian + use_cmf + use_chandelier)
# ---------------------------------------------------------------------------

class TestComputeSignalsDefault:
    def test_returns_all_canonical_keys(self):
        df = _make_ohlcv()
        params = Parameters(squeeze_history=60)
        out = compute_signals(df, params)
        canonical = {"regime_filter", "setup_signal", "trigger_signal", "stop_series", "is_ready"}
        assert canonical.issubset(out.keys())

    def test_returns_all_raw_indicator_keys(self):
        df = _make_ohlcv()
        params = Parameters(squeeze_history=60)
        out = compute_signals(df, params)
        raw = {"adx", "ema_fast", "ema_mid", "ema_slow",
               "donchian_upper", "donchian_lower", "donchian_squeeze",
               "vah", "cmf", "power_candle",
               "chandelier_stop", "psar_stop", "bb_upper"}
        assert raw.issubset(out.keys())

    def test_all_series_same_length_as_input(self):
        df = _make_ohlcv()
        params = Parameters(squeeze_history=60)
        out = compute_signals(df, params)
        for key, series in out.items():
            assert len(series) == len(df), f"{key} length mismatch"

    def test_is_ready_false_early_then_true(self):
        df = _make_ohlcv()
        params = Parameters(squeeze_history=60)
        out = compute_signals(df, params)
        is_ready = out["is_ready"]
        assert is_ready.iloc[:30].sum() == 0
        assert is_ready.iloc[-50:].sum() > 0

    def test_canonical_signals_are_binary(self):
        df = _make_ohlcv()
        params = Parameters(squeeze_history=60)
        out = compute_signals(df, params)
        for key in ("regime_filter", "setup_signal", "trigger_signal", "is_ready"):
            vals = set(out[key].dropna().unique())
            assert vals.issubset({0.0, 1.0}), f"{key} not binary"

    def test_chandelier_only_stop_series_equals_chandelier_stop(self):
        """With only chandelier enabled, stop_series == chandelier_stop."""
        df = _make_ohlcv()
        params = Parameters(
            squeeze_history=60,
            use_chandelier=True,
            use_psar=False,
            use_bbands=False,
        )
        out = compute_signals(df, params)
        pd.testing.assert_series_equal(out["stop_series"], out["chandelier_stop"])


# ---------------------------------------------------------------------------
# Boolean flag selection — regime layer
# ---------------------------------------------------------------------------

class TestRegimeFlags:
    def test_adx_only_regime_filter(self):
        """use_adx=True, use_ema_ribbon=False → regime_filter tracks ADX threshold."""
        df = _make_ohlcv()
        params = Parameters(squeeze_history=60, use_adx=True, use_ema_ribbon=False)
        out = compute_signals(df, params)
        adx_regime = (out["adx"] > params.adx_threshold).fillna(False)
        pd.testing.assert_series_equal(
            out["regime_filter"].astype(bool),
            adx_regime,
            check_names=False,
        )

    def test_ema_ribbon_only_regime_filter(self):
        """use_adx=False, use_ema_ribbon=True → regime_filter tracks EMA alignment."""
        df = _make_ohlcv()
        params = Parameters(squeeze_history=60, use_adx=False, use_ema_ribbon=True)
        out = compute_signals(df, params)
        expected = (
            (out["ema_fast"] > out["ema_mid"]) & (out["ema_mid"] > out["ema_slow"])
        ).fillna(False)
        pd.testing.assert_series_equal(
            out["regime_filter"].astype(bool),
            expected,
            check_names=False,
        )

    def test_both_regime_flags_and_together(self):
        """use_adx=True, use_ema_ribbon=True → regime_filter = ADX AND EMA alignment."""
        df = _make_ohlcv()
        params = Parameters(squeeze_history=60, use_adx=True, use_ema_ribbon=True)
        out = compute_signals(df, params)
        adx_part = (out["adx"] > params.adx_threshold).fillna(False)
        ema_part = (
            (out["ema_fast"] > out["ema_mid"]) & (out["ema_mid"] > out["ema_slow"])
        ).fillna(False)
        expected = adx_part & ema_part
        pd.testing.assert_series_equal(
            out["regime_filter"].astype(bool),
            expected,
            check_names=False,
        )

    def test_all_regime_flags_false_raises(self):
        """No active regime flags → ValueError."""
        df = _make_ohlcv()
        params = Parameters(use_adx=False, use_ema_ribbon=False)
        with pytest.raises(ValueError, match="regime"):
            compute_signals(df, params)


# ---------------------------------------------------------------------------
# Boolean flag selection — setup layer
# ---------------------------------------------------------------------------

class TestSetupFlags:
    def test_volume_profile_only_setup(self):
        df = _make_ohlcv()
        params = Parameters(
            squeeze_history=60,
            use_donchian=False,
            use_volume_profile=True,
            vp_session_bars=24,
            vp_lookback_sessions=2,
        )
        out = compute_signals(df, params)
        assert out["setup_signal"].dtype == float
        assert set(out["setup_signal"].dropna().unique()).issubset({0.0, 1.0})

    def test_all_setup_flags_false_raises(self):
        df = _make_ohlcv()
        params = Parameters(use_donchian=False, use_volume_profile=False)
        with pytest.raises(ValueError, match="setup"):
            compute_signals(df, params)


# ---------------------------------------------------------------------------
# Boolean flag selection — trigger layer
# ---------------------------------------------------------------------------

class TestTriggerFlags:
    def test_power_candle_only_trigger(self):
        df = _make_ohlcv()
        params = Parameters(squeeze_history=60, use_cmf=False, use_power_candle=True)
        out = compute_signals(df, params)
        assert set(out["trigger_signal"].dropna().unique()).issubset({0.0, 1.0})

    def test_all_trigger_flags_false_raises(self):
        df = _make_ohlcv()
        params = Parameters(use_cmf=False, use_power_candle=False)
        with pytest.raises(ValueError, match="trigger"):
            compute_signals(df, params)


# ---------------------------------------------------------------------------
# Boolean flag selection — exit layer (OR logic)
# ---------------------------------------------------------------------------

class TestExitFlags:
    def test_psar_only_stop_series_equals_psar_stop(self):
        df = _make_ohlcv()
        params = Parameters(
            squeeze_history=60,
            use_chandelier=False,
            use_psar=True,
            use_bbands=False,
        )
        out = compute_signals(df, params)
        pd.testing.assert_series_equal(out["stop_series"], out["psar_stop"], check_names=False)

    def test_bbands_only_stop_series_equals_bb_upper(self):
        df = _make_ohlcv()
        params = Parameters(
            squeeze_history=60,
            use_chandelier=False,
            use_psar=False,
            use_bbands=True,
        )
        out = compute_signals(df, params)
        pd.testing.assert_series_equal(out["stop_series"], out["bb_upper"], check_names=False)

    def test_or_logic_stop_series_is_max_of_active_stops(self):
        """With two stops enabled, stop_series = max(chandelier_stop, psar_stop)."""
        df = _make_ohlcv()
        params = Parameters(
            squeeze_history=60,
            use_chandelier=True,
            use_psar=True,
            use_bbands=False,
        )
        out = compute_signals(df, params)
        expected = pd.concat(
            [out["chandelier_stop"], out["psar_stop"]], axis=1
        ).max(axis=1)
        pd.testing.assert_series_equal(out["stop_series"], expected)

    def test_all_exit_flags_false_raises(self):
        df = _make_ohlcv()
        params = Parameters(use_chandelier=False, use_psar=False, use_bbands=False)
        with pytest.raises(ValueError, match="exit"):
            compute_signals(df, params)


# ---------------------------------------------------------------------------
# ratchet_stop
# ---------------------------------------------------------------------------

class TestRatchetStop:
    def test_initialises_on_first_call(self):
        assert ratchet_stop(None, 45_000.0, 1.0) == 45_000.0

    def test_ratchets_upward(self):
        stop = ratchet_stop(45_000.0, 47_000.0, 1.0)
        assert stop == 47_000.0

    def test_never_loosens(self):
        stop = ratchet_stop(47_000.0, 44_000.0, 1.0)
        assert stop == 47_000.0

    def test_returns_none_when_no_position(self):
        assert ratchet_stop(47_000.0, 50_000.0, 0.0) is None


# ---------------------------------------------------------------------------
# compute_position_size
# ---------------------------------------------------------------------------

class TestPositionSize:
    def test_basic_sizing(self):
        size = compute_position_size(50_000, 49_000, 10_000, risk_pct=1.0)
        assert abs(size - 0.5) < 1e-6

    def test_zero_when_stop_above_entry(self):
        assert compute_position_size(50_000, 51_000, 10_000) == 0.0

    def test_capped_at_9999(self):
        size = compute_position_size(50_000, 49_999, 10_000, risk_pct=1.0)
        assert size <= 0.9999

    def test_zero_when_equity_zero(self):
        assert compute_position_size(50_000, 49_000, 0) == 0.0
