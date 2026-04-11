"""Short signal orchestrator — parallel to signals.py but for short entries.

Mirrors the long-side architecture with direction-appropriate logic:
- Regime: bearish EMA ribbon (fast < mid < slow) and/or ADX (non-directional)
- Setup:  Donchian lower-band breakdown and/or VAL rejection
- Trigger: CMF < -threshold and/or bearish power candle
- Exit:   Chandelier short (lowest_low + ATR*mult), PSAR short, BB lower band

Returned canonical keys
-----------------------
short_regime_filter   : 1.0 when bearish regime conditions are met
short_setup_signal    : 1.0 when short setup conditions are met
short_trigger_signal  : 1.0 when short trigger conditions are met
short_stop_series     : float stop level — min of active short stops (OR logic for covers)
short_is_ready        : 1.0 once all active short indicators have warmed up

Returned raw indicators (all computed unconditionally)
------------------------------------------------------
adx, ema_fast, ema_mid, ema_slow,
donchian_lower_short, donchian_squeeze_short, val,
cmf, bearish_power_candle,
chandelier_short_stop, psar_short_stop, bb_lower
"""

from __future__ import annotations

import logging

import pandas as pd

from .parameters import Parameters
from .indicators.adx import compute_adx, regime_is_trending
from .indicators.ema_ribbon import compute_ema_ribbon, regime_is_bearish
from .indicators.donchian import (
    compute_donchian_lower,
    compute_donchian_squeeze,
    setup_short_is_active,
)
from .indicators.volume_profile import compute_val_series, setup_is_below_val
from .indicators.cmf import compute_cmf, trigger_short_is_active
from .indicators.power_candle import trigger_is_bearish_power_candle
from .risk.stops import compute_chandelier_short_stop_series, compute_trailing_stop_short_series
from .risk.psar import compute_psar_stop_series
from .risk.bbands import compute_bbands_lower

logger = logging.getLogger(__name__)


def _and_signals(signals: list[pd.Series]) -> pd.Series:
    """AND a list of boolean Series. All must be 1.0 for the result to be 1.0."""
    result = signals[0].copy()
    for s in signals[1:]:
        result = result & s
    return result.astype(float)


def compute_short_signals(
    df: pd.DataFrame,
    params: Parameters,
) -> dict[str, pd.Series]:
    """Compute all short strategy signals from a raw OHLCV DataFrame.

    Args:
        df:     DataFrame with columns Open, High, Low, Close, Volume
                and a DatetimeIndex.
        params: Strategy parameters (use_short must be True).

    Returns:
        Dict mapping signal name -> pandas Series (same index as df).
    """
    high   = df["High"].astype(float)
    low    = df["Low"].astype(float)
    close  = df["Close"].astype(float)
    volume = df["Volume"].fillna(0.0).astype(float)

    # ------------------------------------------------------------------ #
    # Regime — bearish conditions
    # ADX is non-directional; EMA ribbon is flipped for shorts.
    # ------------------------------------------------------------------ #
    adx = compute_adx(high, low, close, params.adx_period)
    ema_fast, ema_mid, ema_slow = compute_ema_ribbon(
        close, params.ema_fast, params.ema_mid, params.ema_slow
    )

    active_regime: list[pd.Series] = []
    active_regime_ready: list[pd.Series] = []

    if params.use_adx:
        active_regime.append(regime_is_trending(adx, params.adx_threshold))
        active_regime_ready.append(adx.notna())

    if params.use_ema_ribbon_short:
        active_regime.append(regime_is_bearish(ema_fast, ema_mid, ema_slow))
        active_regime_ready.append(ema_slow.notna())

    if not active_regime:
        # Fallback: always True (caller should have validated flags first)
        active_regime = [pd.Series(True, index=close.index)]
        active_regime_ready = [pd.Series(True, index=close.index)]

    short_regime_filter = _and_signals(active_regime)
    regime_ready        = _and_signals(active_regime_ready)

    # ------------------------------------------------------------------ #
    # Setup — structural breakdown
    # ------------------------------------------------------------------ #
    donchian_lower_short = compute_donchian_lower(low, params.short_donchian_lookback)
    donchian_squeeze_short = compute_donchian_squeeze(
        high, low, params.short_donchian_lookback, params.squeeze_history
    )
    _width_short = (
        high.rolling(params.short_donchian_lookback).max() - donchian_lower_short
    )
    squeeze_ready_short = (
        _width_short.rolling(params.squeeze_history).quantile(0.25).notna()
    )

    val = compute_val_series(
        high, low, close, volume,
        session_bars=params.vp_session_bars,
        lookback_sessions=params.vp_lookback_sessions,
        n_bins=params.vp_n_bins,
        value_area_pct=params.vp_value_area_pct,
    )

    active_setup: list[pd.Series] = []
    active_setup_ready: list[pd.Series] = []

    if params.use_donchian_short:
        active_setup.append(setup_short_is_active(
            close, donchian_lower_short, donchian_squeeze_short,
            params.short_donchian_tolerance,
        ))
        active_setup_ready.append(donchian_lower_short.notna() & squeeze_ready_short)

    if params.use_volume_profile_short:
        active_setup.append(setup_is_below_val(
            close, val, consecutive_bars=params.vp_consecutive_bars
        ))
        active_setup_ready.append(val.notna())

    if not active_setup:
        active_setup = [pd.Series(True, index=close.index)]
        active_setup_ready = [pd.Series(True, index=close.index)]

    short_setup_signal = _and_signals(active_setup)
    setup_ready        = _and_signals(active_setup_ready)

    # ------------------------------------------------------------------ #
    # Trigger — distribution confirmation
    # ------------------------------------------------------------------ #
    cmf = compute_cmf(high, low, close, volume, params.cmf_period)
    bearish_power_candle = trigger_is_bearish_power_candle(
        close, low, volume,
        lookback=params.power_candle_lookback,
        vol_period=params.power_candle_vol_period,
        vol_multiplier=params.power_candle_vol_mult,
    )

    active_trigger: list[pd.Series] = []
    active_trigger_ready: list[pd.Series] = []

    if params.use_cmf_short:
        active_trigger.append(trigger_short_is_active(cmf, params.short_cmf_threshold))
        active_trigger_ready.append(cmf.notna())

    if params.use_power_candle_short:
        active_trigger.append(bearish_power_candle)
        active_trigger_ready.append(
            low.rolling(params.power_candle_lookback).min().notna()
        )

    if not active_trigger:
        active_trigger = [pd.Series(True, index=close.index)]
        active_trigger_ready = [pd.Series(True, index=close.index)]

    short_trigger_signal = _and_signals(active_trigger)
    trigger_ready        = _and_signals(active_trigger_ready)

    # ------------------------------------------------------------------ #
    # Exit — OR logic via min-stop (first cover hit exits)
    # For shorts: price must rise ABOVE the stop → we take the minimum active
    # stop (the lowest cover level) as the most restrictive.
    # ------------------------------------------------------------------ #
    chandelier_short_stop = compute_chandelier_short_stop_series(
        high, low, close,
        params.short_chandelier_lookback,
        params.short_chandelier_atr_mult,
    )
    trailing_stop_short = compute_trailing_stop_short_series(
        high, low, close,
        params.trail_lookback,
        params.trail_atr_mult,
    )
    # PSAR: use the short-side column (PSARs) — shares long-side AF params
    psar_result = _compute_psar_short(high, low, close, params)
    bb_lower = compute_bbands_lower(close, params.bb_period, params.bb_std)

    active_short_stops: list[pd.Series] = []
    active_exit_ready:  list[pd.Series] = []

    if params.use_chandelier_short:
        active_short_stops.append(chandelier_short_stop)
        active_exit_ready.append(chandelier_short_stop.notna())

    if params.use_trailing_stop_short:
        active_short_stops.append(trailing_stop_short)
        active_exit_ready.append(trailing_stop_short.notna())

    if params.use_psar_short:
        active_short_stops.append(psar_result)
        active_exit_ready.append(psar_result.notna())

    if params.use_bbands_short:
        active_short_stops.append(bb_lower)
        active_exit_ready.append(bb_lower.notna())

    if not active_short_stops:
        # Fallback: never triggers
        active_short_stops = [pd.Series(float("nan"), index=close.index, dtype=float)]
        active_exit_ready  = [pd.Series(False, index=close.index)]

    # min of active short stops: a rising price only needs to exceed the
    # *lowest* (most aggressive) stop to exit — first cover hit exits.
    short_stop_series = pd.concat(active_short_stops, axis=1).min(axis=1)
    exit_ready        = _and_signals([s.notna() for s in active_short_stops])

    # ------------------------------------------------------------------ #
    # short_is_ready
    # ------------------------------------------------------------------ #
    short_is_ready = (
        regime_ready.astype(bool)
        & setup_ready.astype(bool)
        & trigger_ready.astype(bool)
        & exit_ready.astype(bool)
    )

    def _f(s: pd.Series) -> pd.Series:
        return s.astype(float)

    return {
        "short_regime_filter":   _f(short_regime_filter),
        "short_setup_signal":    _f(short_setup_signal),
        "short_trigger_signal":  _f(short_trigger_signal),
        "short_stop_series":     short_stop_series,
        "short_is_ready":        _f(short_is_ready),
        # Raw indicators
        "adx":                   adx,
        "ema_fast":              ema_fast,
        "ema_mid":               ema_mid,
        "ema_slow":              ema_slow,
        "donchian_lower_short":  donchian_lower_short,
        "donchian_squeeze_short": donchian_squeeze_short,
        "val":                   val,
        "cmf":                   cmf,
        "bearish_power_candle":  _f(bearish_power_candle),
        "chandelier_short_stop":  chandelier_short_stop,
        "trailing_stop_short":    trailing_stop_short,
        "psar_short_stop":        psar_result,
        "bb_lower":               bb_lower,
    }


def _compute_psar_short(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    params: Parameters,
) -> pd.Series:
    """Extract the short-side PSAR column (PSARs_* — the stop for short trades)."""
    import pandas_ta as pta
    result = pta.psar(
        high, low, close,
        af0=params.psar_af_initial,
        af=params.psar_af_step,
        max_af=params.psar_af_max,
    )
    if result is None or result.empty:
        return pd.Series(float("nan"), index=close.index, dtype=float)
    # pandas_ta names the short SAR column PSARs_<af>_<max_af>
    short_col = [c for c in result.columns if c.startswith("PSARs")]
    if not short_col:
        return pd.Series(float("nan"), index=close.index, dtype=float)
    return result[short_col[0]].astype(float)
