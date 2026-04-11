"""Signal orchestrator -- computes all indicator options in one call.

This is the single entry point consumed by the backtesting runner.  All
heavy pandas/numpy work happens here (once, at init) so that next() remains
fast and side-effect-free.

Every option for every layer is computed unconditionally so raw indicators
are always available for inspection.  The boolean flags in `params` then
wire the correct series into the canonical keys the runner reads.

Entry layers (regime / setup / trigger)
----------------------------------------
All enabled flags in a layer are AND'd together.  Every active indicator
must agree before the layer fires.

Exit layer
----------
OR logic: exit when the first active stop is hit.
Implemented as: stop_series = max(active_stop_series)
When price crosses below the highest active stop, that is the first to fire.

Returned keys (canonical -- runner uses these)
----------------------------------------------
regime_filter   : 1.0 when all active regime conditions are met
setup_signal    : 1.0 when all active setup conditions are met
trigger_signal  : 1.0 when all active trigger conditions are met
stop_series     : float stop level -- max of all active exit stops (OR logic)
is_ready        : 1.0 once all active indicators have warmed up

Returned keys (raw indicators -- all computed, available for inspection)
------------------------------------------------------------------------
adx, ema_fast, ema_mid, ema_slow,
donchian_upper, donchian_lower, donchian_squeeze, vah, cmf, power_candle,
chandelier_stop, psar_stop, bb_upper

Excluded options (require external data)
-----------------------------------------
- regime "mvrv"             : MVRV Z-Score (needs Glassnode on-chain API)
- trigger "cvd"             : CVD Breakout  (needs tick-level trade data)
- setup "relative_strength" : needs a benchmark OHLCV DataFrame
"""

from __future__ import annotations

import logging

import pandas as pd

from .parameters import Parameters
from .indicators.adx import compute_adx, regime_is_trending
from .indicators.ema_ribbon import compute_ema_ribbon, regime_is_aligned
from .indicators.donchian import (
    compute_donchian_upper,
    compute_donchian_lower,
    compute_donchian_squeeze,
    setup_is_active,
)
from .indicators.volume_profile import compute_vah_series, setup_is_above_vah
from .indicators.relative_strength import setup_is_relatively_strong
from .indicators.cmf import compute_cmf, trigger_is_active
from .indicators.power_candle import trigger_is_power_candle
from .risk.stops import compute_chandelier_stop_series, compute_trailing_stop_series
from .risk.psar import compute_psar_stop_series
from .risk.bbands import compute_bbands_upper

logger = logging.getLogger(__name__)


def _and_signals(signals: list[pd.Series]) -> pd.Series:
    """AND a list of boolean Series.  All must be 1.0 for the result to be 1.0."""
    result = signals[0].copy()
    for s in signals[1:]:
        result = result & s
    return result.astype(float)


def compute_signals(
    df: pd.DataFrame,
    params: Parameters,
    benchmark_df: pd.DataFrame | None = None,
) -> dict[str, pd.Series]:
    """Compute all strategy signals from a raw OHLCV DataFrame.

    Args:
        df:           DataFrame with columns Open, High, Low, Close, Volume
                      and a DatetimeIndex.
        params:       Strategy parameters (boolean flag groups).
        benchmark_df: Optional benchmark OHLCV required when
                      use_relative_strength would be supported (future).

    Returns:
        Dict mapping signal name -> pandas Series (same index as df).

    Raises:
        ValueError: When a flag group has no active flags.
    """
    _validate_flags(params)

    high = df["High"].astype(float)
    low = df["Low"].astype(float)
    close = df["Close"].astype(float)
    volume = df["Volume"].fillna(0.0).astype(float)

    # ------------------------------------------------------------------ #
    # Regime -- compute all options
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

    if params.use_ema_ribbon:
        active_regime.append(regime_is_aligned(ema_fast, ema_mid, ema_slow))
        active_regime_ready.append(ema_slow.notna())

    regime_filter = _and_signals(active_regime)
    regime_ready = _and_signals(active_regime_ready)

    # ------------------------------------------------------------------ #
    # Setup -- compute all options
    # ------------------------------------------------------------------ #
    donchian_upper = compute_donchian_upper(high, params.donchian_lookback)
    donchian_lower = compute_donchian_lower(low, params.donchian_lookback)
    donchian_squeeze = compute_donchian_squeeze(
        high, low, params.donchian_lookback, params.squeeze_history
    )
    _width = donchian_upper - donchian_lower
    squeeze_ready = _width.rolling(params.squeeze_history).quantile(0.25).notna()

    vah = compute_vah_series(
        high, low, close, volume,
        session_bars=params.vp_session_bars,
        lookback_sessions=params.vp_lookback_sessions,
        n_bins=params.vp_n_bins,
        value_area_pct=params.vp_value_area_pct,
    )

    active_setup: list[pd.Series] = []
    active_setup_ready: list[pd.Series] = []

    if params.use_donchian:
        active_setup.append(setup_is_active(
            close, donchian_upper, donchian_squeeze, params.donchian_tolerance
        ))
        active_setup_ready.append(donchian_upper.notna() & squeeze_ready)

    if params.use_volume_profile:
        active_setup.append(setup_is_above_vah(
            close, vah, consecutive_bars=params.vp_consecutive_bars
        ))
        active_setup_ready.append(vah.notna())

    setup_signal = _and_signals(active_setup)
    setup_ready = _and_signals(active_setup_ready)

    # ------------------------------------------------------------------ #
    # Trigger -- compute all options
    # ------------------------------------------------------------------ #
    cmf = compute_cmf(high, low, close, volume, params.cmf_period)
    power_candle = trigger_is_power_candle(
        close, high, volume,
        lookback=params.power_candle_lookback,
        vol_period=params.power_candle_vol_period,
        vol_multiplier=params.power_candle_vol_mult,
    )

    active_trigger: list[pd.Series] = []
    active_trigger_ready: list[pd.Series] = []

    if params.use_cmf:
        active_trigger.append(trigger_is_active(cmf, params.cmf_threshold))
        active_trigger_ready.append(cmf.notna())

    if params.use_power_candle:
        active_trigger.append(power_candle)
        active_trigger_ready.append(
            high.rolling(params.power_candle_lookback).max().notna()
            & compute_chandelier_stop_series(
                high, low, close, params.power_candle_vol_period, 0
            ).notna()
        )

    trigger_signal = _and_signals(active_trigger)
    trigger_ready = _and_signals(active_trigger_ready)

    # ------------------------------------------------------------------ #
    # Exit -- OR logic via max-stop (first stop hit exits)
    # ------------------------------------------------------------------ #
    chandelier_stop = compute_chandelier_stop_series(
        high, low, close, params.chandelier_lookback, params.chandelier_atr_mult
    )
    psar_stop = compute_psar_stop_series(
        high, low, close,
        af_initial=params.psar_af_initial,
        af_step=params.psar_af_step,
        af_max=params.psar_af_max,
    )
    bb_upper = compute_bbands_upper(close, params.bb_period, params.bb_std)

    active_stops: list[pd.Series] = []
    active_exit_ready: list[pd.Series] = []

    if params.use_chandelier:
        active_stops.append(chandelier_stop)
        active_exit_ready.append(chandelier_stop.notna())

    if params.use_psar:
        active_stops.append(psar_stop)
        active_exit_ready.append(psar_stop.notna())

    if params.use_bbands:
        active_stops.append(bb_upper)
        active_exit_ready.append(bb_upper.notna())

    # ---- Exit D: Simple Trailing Stop ----------------------------------
    trailing_stop = compute_trailing_stop_series(
        high, low, close, params.trail_lookback, params.trail_atr_mult
    )
    if params.use_trailing_stop:
        active_stops.append(trailing_stop)
        active_exit_ready.append(trailing_stop.notna())

    # max of all active stops -> exit fires on the first (highest) stop hit
    stop_series = pd.concat(active_stops, axis=1).max(axis=1)
    exit_ready = _and_signals(active_exit_ready)

    # ------------------------------------------------------------------ #
    # is_ready: all active indicators have completed warmup
    # ------------------------------------------------------------------ #
    # _and_signals returns float; cast to bool before bitwise AND
    is_ready = (
        regime_ready.astype(bool)
        & setup_ready.astype(bool)
        & trigger_ready.astype(bool)
        & exit_ready.astype(bool)
    )

    def _f(s: pd.Series) -> pd.Series:
        return s.astype(float)

    return {
        # Canonical keys (consumed by runner)
        "regime_filter":  _f(regime_filter),
        "setup_signal":   _f(setup_signal),
        "trigger_signal": _f(trigger_signal),
        "stop_series":    stop_series,
        "is_ready":       _f(is_ready),
        # Raw indicators (available for inspection / plotting)
        "adx":               adx,
        "ema_fast":          ema_fast,
        "ema_mid":           ema_mid,
        "ema_slow":          ema_slow,
        "donchian_upper":    donchian_upper,
        "donchian_lower":    donchian_lower,
        "donchian_squeeze":  donchian_squeeze,
        "vah":               vah,
        "cmf":               cmf,
        "power_candle":      power_candle.astype(float),
        "chandelier_stop":   chandelier_stop,
        "psar_stop":         psar_stop,
        "bb_upper":          bb_upper,
        "trailing_stop":     trailing_stop,
    }


def _validate_flags(params: Parameters) -> None:
    """Raise ValueError if any active direction has an empty flag group."""
    if not params.use_long and not params.use_short:
        raise ValueError(
            "Both use_long and use_short are False. "
            "At least one direction must be enabled."
        )

    if params.use_long:
        long_groups = {
            "regime  (use_adx, use_ema_ribbon)":
                params.use_adx or params.use_ema_ribbon,
            "setup   (use_donchian, use_volume_profile)":
                params.use_donchian or params.use_volume_profile,
            "trigger (use_cmf, use_power_candle)":
                params.use_cmf or params.use_power_candle,
            "exit    (use_chandelier, use_psar, use_bbands, use_trailing_stop)":
                params.use_chandelier or params.use_psar or params.use_bbands
                or params.use_trailing_stop,
        }
        for group_name, active in long_groups.items():
            if not active:
                raise ValueError(
                    f"No flags active in the long {group_name} group. "
                    "At least one flag per group must be True."
                )

    if params.use_short:
        short_groups = {
            "short regime  (use_adx, use_ema_ribbon_short)":
                params.use_adx or params.use_ema_ribbon_short,
            "short setup   (use_donchian_short, use_volume_profile_short)":
                params.use_donchian_short or params.use_volume_profile_short,
            "short trigger (use_cmf_short, use_power_candle_short)":
                params.use_cmf_short or params.use_power_candle_short,
            "short exit    (use_chandelier_short, use_psar_short, use_bbands_short, use_trailing_stop_short)":
                params.use_chandelier_short or params.use_psar_short
                or params.use_bbands_short or params.use_trailing_stop_short,
        }
        for group_name, active in short_groups.items():
            if not active:
                raise ValueError(
                    f"No flags active in the {group_name} group. "
                    "At least one flag per group must be True."
                )
