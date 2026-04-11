"""backtesting.py Strategy class for the Adaptive Momentum Strategy."""

from __future__ import annotations

import logging
import math

from backtesting import Strategy

from adaptive_momentum_strategy.strategy.parameters import Parameters
from adaptive_momentum_strategy.strategy.signals import compute_signals
from adaptive_momentum_strategy.strategy.short_signals import compute_short_signals
from adaptive_momentum_strategy.strategy.decision.entry import should_buy
from adaptive_momentum_strategy.strategy.decision.exit import should_sell
from adaptive_momentum_strategy.strategy.decision.short_entry import should_short
from adaptive_momentum_strategy.strategy.decision.short_exit import should_cover
from adaptive_momentum_strategy.strategy.risk.stops import (
    ratchet_stop,
    ratchet_short_stop,
)
from adaptive_momentum_strategy.strategy.risk.sizing import compute_position_size

logger = logging.getLogger(__name__)


class AdaptiveMomentumStrategy(Strategy):
    """backtesting.py Strategy wrapper for the Adaptive Momentum Strategy.

    Each class attribute is exposed as an optimisable parameter.
    Boolean flags control which indicators are active; multiple flags in a
    layer are AND'd for entry conditions.  Exit uses OR (first stop hit).
    """

    # --- Boolean flag groups ---
    # Regime: all enabled flags must agree (AND)
    use_adx: bool = True
    use_ema_ribbon: bool = False

    # Setup: all enabled flags must agree (AND)
    use_donchian: bool = True
    use_volume_profile: bool = False

    # Trigger: all enabled flags must agree (AND)
    use_cmf: bool = True
    use_power_candle: bool = False

    # Exit: first stop hit exits (OR via max-stop logic)
    use_chandelier: bool = True
    use_psar: bool = False
    use_bbands: bool = False
    use_trailing_stop: bool = False  # btc_momentum-style: rolling_max(low,N)-ATR*mult

    # --- Regime A: ADX ---
    adx_period: int = 14
    adx_threshold: float = 25.0

    # --- Regime C: EMA Ribbon ---
    ema_fast: int = 20
    ema_mid: int = 50
    ema_slow: int = 200

    # --- Setup A: Donchian ---
    donchian_lookback: int = 20
    donchian_tolerance: float = 0.01
    squeeze_history: int = 240

    # --- Setup B: Volume Profile ---
    vp_session_bars: int = 24
    vp_lookback_sessions: int = 3
    vp_n_bins: int = 20
    vp_value_area_pct: float = 0.70
    vp_consecutive_bars: int = 2

    # --- Setup C: Relative Strength (excluded from grid, kept for API completeness) ---
    rs_period: int = 24
    rs_multiplier: float = 1.5
    rs_ratio_sma_period: int = 20

    # --- Trigger A: CMF ---
    cmf_period: int = 20
    cmf_threshold: float = 0.05

    # --- Trigger C: Power Candle ---
    power_candle_lookback: int = 15
    power_candle_vol_period: int = 20
    power_candle_vol_mult: float = 1.5

    # --- Exit A: Chandelier ---
    chandelier_lookback: int = 22
    chandelier_atr_mult: float = 3.0

    # --- Exit B: PSAR ---
    psar_af_initial: float = 0.02
    psar_af_step: float = 0.02
    psar_af_max: float = 0.20

    # --- Exit C: Bollinger Bands ---
    bb_period: int = 20
    bb_std: float = 2.0

    # --- Exit D: Simple Trailing Stop ---
    trail_lookback: int = 22
    trail_atr_mult: float = 2.0

    # --- Direction ---
    use_long:  bool = True
    use_short: bool = False

    # --- Short Regime ---
    use_ema_ribbon_short: bool = False

    # --- Short Setup ---
    use_donchian_short:       bool = False
    use_volume_profile_short: bool = False

    # --- Short Trigger ---
    use_cmf_short:          bool = False
    use_power_candle_short: bool = False

    # --- Short Exit ---
    use_chandelier_short:    bool = False
    use_psar_short:          bool = False
    use_bbands_short:        bool = False
    use_trailing_stop_short: bool = False

    # --- Short Params ---
    short_donchian_lookback:   int   = 15
    short_donchian_tolerance:  float = 0.01
    short_cmf_threshold:       float = 0.05
    short_chandelier_lookback: int   = 22
    short_chandelier_atr_mult: float = 2.5

    # --- Sizing ---
    risk_pct: float = 1.0

    # ------------------------------------------------------------------ #

    def init(self) -> None:
        params = Parameters(
            use_adx=self.use_adx,
            use_ema_ribbon=self.use_ema_ribbon,
            use_donchian=self.use_donchian,
            use_volume_profile=self.use_volume_profile,
            use_cmf=self.use_cmf,
            use_power_candle=self.use_power_candle,
            use_chandelier=self.use_chandelier,
            use_psar=self.use_psar,
            use_bbands=self.use_bbands,
            use_trailing_stop=self.use_trailing_stop,
            adx_period=self.adx_period,
            adx_threshold=self.adx_threshold,
            ema_fast=self.ema_fast,
            ema_mid=self.ema_mid,
            ema_slow=self.ema_slow,
            donchian_lookback=self.donchian_lookback,
            donchian_tolerance=self.donchian_tolerance,
            squeeze_history=self.squeeze_history,
            vp_session_bars=self.vp_session_bars,
            vp_lookback_sessions=self.vp_lookback_sessions,
            vp_n_bins=self.vp_n_bins,
            vp_value_area_pct=self.vp_value_area_pct,
            vp_consecutive_bars=self.vp_consecutive_bars,
            rs_period=self.rs_period,
            rs_multiplier=self.rs_multiplier,
            rs_ratio_sma_period=self.rs_ratio_sma_period,
            cmf_period=self.cmf_period,
            cmf_threshold=self.cmf_threshold,
            power_candle_lookback=self.power_candle_lookback,
            power_candle_vol_period=self.power_candle_vol_period,
            power_candle_vol_mult=self.power_candle_vol_mult,
            chandelier_lookback=self.chandelier_lookback,
            chandelier_atr_mult=self.chandelier_atr_mult,
            psar_af_initial=self.psar_af_initial,
            psar_af_step=self.psar_af_step,
            psar_af_max=self.psar_af_max,
            bb_period=self.bb_period,
            bb_std=self.bb_std,
            trail_lookback=self.trail_lookback,
            trail_atr_mult=self.trail_atr_mult,
            use_long=self.use_long,
            use_short=self.use_short,
            use_ema_ribbon_short=self.use_ema_ribbon_short,
            use_donchian_short=self.use_donchian_short,
            use_volume_profile_short=self.use_volume_profile_short,
            use_cmf_short=self.use_cmf_short,
            use_power_candle_short=self.use_power_candle_short,
            use_chandelier_short=self.use_chandelier_short,
            use_psar_short=self.use_psar_short,
            use_bbands_short=self.use_bbands_short,
            use_trailing_stop_short=self.use_trailing_stop_short,
            short_donchian_lookback=self.short_donchian_lookback,
            short_donchian_tolerance=self.short_donchian_tolerance,
            short_cmf_threshold=self.short_cmf_threshold,
            short_chandelier_lookback=self.short_chandelier_lookback,
            short_chandelier_atr_mult=self.short_chandelier_atr_mult,
            risk_pct=self.risk_pct,
        )

        df = self.data.df.copy()

        def _reg(key: str, signals: dict):
            return self.I(lambda s=signals[key]: s.values.copy(), name=key)

        # Long signals
        if params.use_long:
            sig = compute_signals(df, params)
            self._regime_filter  = _reg("regime_filter",  sig)
            self._setup_signal   = _reg("setup_signal",   sig)
            self._trigger_signal = _reg("trigger_signal", sig)
            self._stop_raw       = _reg("stop_series",    sig)
            self._is_ready       = _reg("is_ready",       sig)
        else:
            # Placeholders — never used, but init() must define them
            _zero = self.I(lambda: df["Close"].values * 0, name="long_disabled")
            self._regime_filter = self._setup_signal = self._trigger_signal = _zero
            self._stop_raw = _zero
            self._is_ready = _zero

        # Short signals
        if params.use_short:
            short_sig = compute_short_signals(df, params)
            self._short_regime_filter  = _reg("short_regime_filter",  short_sig)
            self._short_setup_signal   = _reg("short_setup_signal",   short_sig)
            self._short_trigger_signal = _reg("short_trigger_signal", short_sig)
            self._short_stop_raw       = _reg("short_stop_series",    short_sig)
            self._short_is_ready       = _reg("short_is_ready",       short_sig)
        else:
            _zero2 = self.I(lambda: df["Close"].values * 0, name="short_disabled")
            self._short_regime_filter = self._short_setup_signal = _zero2
            self._short_trigger_signal = self._short_stop_raw = _zero2
            self._short_is_ready = _zero2

        # Stateful trailing stops
        self._trail_stop: float | None = None        # long stop
        self._short_trail_stop: float | None = None  # short stop

        # Chandelier and trailing_stop are ratcheted; PSAR/BBands update directly.
        self._ratchet_stop: bool = params.use_chandelier or params.use_trailing_stop

    def next(self) -> None:
        close = self.data.Close[-1]
        in_long  = self.position.size > 0
        in_short = self.position.size < 0

        # ---------------------------------------------------------------- #
        # Long trade management
        # ---------------------------------------------------------------- #
        if self._is_ready[-1] and self.use_long:
            stop_candidate = float(self._stop_raw[-1])

            if in_long and not math.isnan(stop_candidate):
                if self._ratchet_stop:
                    self._trail_stop = ratchet_stop(
                        self._trail_stop, stop_candidate, self.position.size
                    )
                else:
                    self._trail_stop = stop_candidate

                if self._trail_stop is not None:
                    for trade in self.trades:
                        if trade.size > 0:
                            trade.sl = self._trail_stop

            if should_sell(close, self._trail_stop, in_long):
                self.position.close()
                self._trail_stop = None
                return

            if should_buy(
                bool(self._regime_filter[-1]),
                bool(self._setup_signal[-1]),
                bool(self._trigger_signal[-1]),
                in_long or in_short,  # no new long while short is open
            ):
                initial_stop = stop_candidate
                if math.isnan(initial_stop) or initial_stop <= 0:
                    return
                size = compute_position_size(
                    entry_price=close,
                    stop_price=initial_stop,
                    equity=self.equity,
                    risk_pct=self.risk_pct,
                )
                if size <= 0:
                    return
                self.buy(size=size, sl=initial_stop)
                self._trail_stop = initial_stop

        # ---------------------------------------------------------------- #
        # Short trade management
        # ---------------------------------------------------------------- #
        if self._short_is_ready[-1] and self.use_short:
            short_stop_candidate = float(self._short_stop_raw[-1])

            if in_short and not math.isnan(short_stop_candidate):
                # Short chandelier is always ratcheted downward
                self._short_trail_stop = ratchet_short_stop(
                    self._short_trail_stop, short_stop_candidate, self.position.size
                )
                if self._short_trail_stop is not None:
                    for trade in self.trades:
                        if trade.size < 0:
                            trade.sl = self._short_trail_stop

            if should_cover(close, self._short_trail_stop, in_short):
                self.position.close()
                self._short_trail_stop = None
                return

            if should_short(
                bool(self._short_regime_filter[-1]),
                bool(self._short_setup_signal[-1]),
                bool(self._short_trigger_signal[-1]),
                in_short or in_long,  # no new short while long is open
            ):
                initial_short_stop = short_stop_candidate
                if math.isnan(initial_short_stop) or initial_short_stop <= 0:
                    return
                size = compute_position_size(
                    entry_price=close,
                    stop_price=initial_short_stop,
                    equity=self.equity,
                    risk_pct=self.risk_pct,
                )
                if size <= 0:
                    return
                self.sell(size=size, sl=initial_short_stop)
                self._short_trail_stop = initial_short_stop
