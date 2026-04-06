"""UPSStrategy — backtesting.py Strategy class.

Isolated from the runner so the class can be imported independently
(e.g. for optimisation or notebook use).
"""

from __future__ import annotations

from backtesting import Strategy

from ..strategy.signals import build_strategy_series
from ..strategy.decision.entry import should_open_long, should_open_short
from ..strategy.decision.exit import should_close_long, should_close_short
from ..strategy.risk.sl_tp import (
    compute_long_stop, compute_short_stop,
    compute_long_target, compute_short_target,
)
from ..strategy.risk.trailing import (
    compute_long_trail_candidate, compute_short_trail_candidate,
    update_long_trail_stop, update_short_trail_stop,
    active_long_stop, active_short_stop,
)
from ..strategy.risk.sizing import compute_long_size_fraction, compute_short_size_fraction


class UPSStrategy(Strategy):
    # --- class-level params (overridable via Backtest(..., param=val)) ---
    # MA
    ma_length = 50
    max_candles_beyond_ma = 1
    ma_consolidation_lookback = 10
    ma_consolidation_count = 4
    ma_breach_lookback = 5
    # IQ filter
    use_iq_filter = True
    iq_lookback = 20
    iq_min_score = 0.55
    iq_slope_atr_scale = 1.5
    iq_er_weight = 0.5
    iq_slope_weight = 0.3
    iq_bias_weight = 0.2
    use_sq_boost = True
    sq_boost_weight = 0.3
    sq_vol_lookback = 20
    # RSI filter
    use_rsi_filter = False
    rsi_period = 14
    rsi_overbought = 70.0
    # ADX filter
    use_adx_filter = False
    adx_period = 14
    adx_min_strength = 20.0
    # Volume filter
    use_volume_filter = False
    volume_filter_lookback = 20
    volume_filter_multiplier = 1.0
    # Trade direction
    long_trades = True
    short_trades = True
    # Patterns
    enable_ec = True
    enable_bullish_engulfing = True
    enable_shooting_star = True
    ec_wick = False
    enable_hammer = True
    atr_max_size = 2.5
    rejection_wick_max_size = 0.0
    hammer_fib = 0.3
    hammer_size = 0.1
    # Stops & targets
    stop_multiplier = 1.0
    risk_reward_multiplier = 1.0
    minimum_rr = 0.0
    pb_reference = "Close"
    sl_reference = "High/Low"
    # Trailing
    trail_stop = False
    trail_stop_size = 1.0
    trail_source = "High/Low"
    # Lookback / misc
    lookback = 5
    atr_length = 14
    point_allowance = 0
    # Backtester sizing
    risk_per_trade = 1.0

    def init(self) -> None:
        df = self.data.df.copy()
        signals = build_strategy_series(
            df=df,
            ma_length=self.ma_length,
            max_candles_beyond_ma=self.max_candles_beyond_ma,
            ma_consolidation_lookback=self.ma_consolidation_lookback,
            ma_consolidation_count=self.ma_consolidation_count,
            ma_breach_lookback=self.ma_breach_lookback,
            use_iq_filter=self.use_iq_filter,
            iq_lookback=self.iq_lookback,
            iq_min_score=self.iq_min_score,
            iq_slope_atr_scale=self.iq_slope_atr_scale,
            iq_er_weight=self.iq_er_weight,
            iq_slope_weight=self.iq_slope_weight,
            iq_bias_weight=self.iq_bias_weight,
            use_sq_boost=self.use_sq_boost,
            sq_boost_weight=self.sq_boost_weight,
            sq_vol_lookback=self.sq_vol_lookback,
            use_rsi_filter=self.use_rsi_filter,
            rsi_period=self.rsi_period,
            rsi_overbought=self.rsi_overbought,
            use_adx_filter=self.use_adx_filter,
            adx_period=self.adx_period,
            adx_min_strength=self.adx_min_strength,
            use_volume_filter=self.use_volume_filter,
            volume_filter_lookback=self.volume_filter_lookback,
            volume_filter_multiplier=self.volume_filter_multiplier,
            long_trades=self.long_trades,
            short_trades=self.short_trades,
            enable_ec=self.enable_ec,
            enable_bullish_engulfing=self.enable_bullish_engulfing,
            enable_shooting_star=self.enable_shooting_star,
            ec_wick=self.ec_wick,
            enable_hammer=self.enable_hammer,
            atr_max_size=self.atr_max_size,
            rejection_wick_max_size=self.rejection_wick_max_size,
            hammer_fib=self.hammer_fib,
            hammer_size=self.hammer_size,
            stop_multiplier=self.stop_multiplier,
            risk_reward_multiplier=self.risk_reward_multiplier,
            minimum_rr=self.minimum_rr,
            pb_reference=self.pb_reference,
            sl_reference=self.sl_reference,
            trail_stop=self.trail_stop,
            trail_stop_size=self.trail_stop_size,
            trail_source=self.trail_source,
            lookback=self.lookback,
            atr_length=self.atr_length,
            point_allowance=self.point_allowance,
        )

        def _reg(key: str):
            return self.I(lambda s=signals[key]: s.values.copy(), name=key)

        self.atr_value           = _reg("atr_value")
        self.ma1                 = _reg("ma1")
        self.price_above_ma      = _reg("price_above_ma")
        self.candles_below_ma    = _reg("candles_below_ma")
        self.candles_above_ma    = _reg("candles_above_ma")
        self.ma_cross_filter     = _reg("ma_cross_filter")
        self.iq_long_filter      = _reg("iq_long_filter")
        self.iq_short_filter     = _reg("iq_short_filter")
        self.long_conditions_met  = _reg("long_conditions_met")
        self.short_conditions_met = _reg("short_conditions_met")
        self.bearish_pb           = _reg("bearish_pb")
        self.bullish_pb           = _reg("bullish_pb")
        self.long_entry_pattern   = _reg("long_entry_pattern")
        self.short_entry_pattern  = _reg("short_entry_pattern")
        self.long_stop_price      = _reg("long_stop_price")
        self.long_target_price    = _reg("long_target_price")
        self.short_stop_price     = _reg("short_stop_price")
        self.short_target_price   = _reg("short_target_price")
        self.valid_long_entry     = _reg("valid_long_entry")
        self.valid_short_entry    = _reg("valid_short_entry")
        self.is_ready             = _reg("is_ready")

        self._trade_stop_price: float | None = None
        self._trade_target_price: float | None = None
        self._trail_stop_price: float | None = None
        self._active_stop_price: float | None = None
        self._look_for_exit: bool = False

    def next(self) -> None:
        if not bool(self.is_ready[-1]):
            return

        if should_open_long(
            position_size=float(self.position.size),
            is_flat=bool(self.position.size == 0),
            price_above_ma=bool(self.price_above_ma[-1]),
            long_conditions_met=bool(self.long_conditions_met[-1]),
            bearish_pb=bool(self.bearish_pb[-1]),
            long_entry_pattern=bool(self.long_entry_pattern[-1]),
        ):
            low_now = float(self.data.Low[-1])
            low_prev = float(self.data.Low[-2]) if len(self.data.Low) >= 2 else low_now
            open_now = float(self.data.Open[-1])
            close_now = float(self.data.Close[-1])
            atr_now = float(self.atr_value[-1])

            trade_stop_price = compute_long_stop(
                sl_reference=self.sl_reference, low_now=low_now, low_prev=low_prev,
                open_now=open_now, close_now=close_now, atr_now=atr_now,
                stop_multiplier=self.stop_multiplier,
            )
            trade_target_price = compute_long_target(
                entry_price=close_now, stop_price=trade_stop_price,
                risk_reward_multiplier=self.risk_reward_multiplier,
            )
            size_fraction = compute_long_size_fraction(
                entry_price=close_now, stop_price=trade_stop_price,
                equity=float(self.equity), risk_per_trade=float(self.risk_per_trade),
            )
            if size_fraction <= 0:
                return
            self.buy(size=size_fraction)
            self._trade_stop_price = trade_stop_price
            self._trade_target_price = trade_target_price
            self._trail_stop_price = None
            self._active_stop_price = self._trade_stop_price
            self._look_for_exit = False

        elif should_open_short(
            position_size=float(self.position.size),
            is_flat=bool(self.position.size == 0),
            price_above_ma=bool(self.price_above_ma[-1]),
            short_conditions_met=bool(self.short_conditions_met[-1]),
            bullish_pb=bool(self.bullish_pb[-1]),
            short_entry_pattern=bool(self.short_entry_pattern[-1]),
        ):
            high_now = float(self.data.High[-1])
            high_prev = float(self.data.High[-2]) if len(self.data.High) >= 2 else high_now
            open_now = float(self.data.Open[-1])
            close_now = float(self.data.Close[-1])
            atr_now = float(self.atr_value[-1])

            trade_stop_price = compute_short_stop(
                sl_reference=self.sl_reference, high_now=high_now, high_prev=high_prev,
                open_now=open_now, close_now=close_now, atr_now=atr_now,
                stop_multiplier=self.stop_multiplier,
            )
            trade_target_price = compute_short_target(
                entry_price=close_now, stop_price=trade_stop_price,
                risk_reward_multiplier=self.risk_reward_multiplier,
            )
            size_fraction = compute_short_size_fraction(
                entry_price=close_now, stop_price=trade_stop_price,
                equity=float(self.equity), risk_per_trade=float(self.risk_per_trade),
            )
            if size_fraction <= 0:
                return
            self.sell(size=size_fraction)
            self._trade_stop_price = trade_stop_price
            self._trade_target_price = trade_target_price
            self._trail_stop_price = None
            self._active_stop_price = self._trade_stop_price
            self._look_for_exit = False

        # --- Stop / target / trailing management ---
        if self.position.size > 0 and self._trade_stop_price is not None:
            if (
                self.trail_stop and not self._look_for_exit
                and self._trade_target_price is not None
                and float(self.data.High[-1]) >= self._trade_target_price
            ):
                self._look_for_exit = True

            if self.trail_stop and self._look_for_exit:
                close_prev = float(self.data.Close[-2]) if len(self.data.Close) >= 2 else float(self.data.Close[-1])
                open_prev = float(self.data.Open[-2]) if len(self.data.Open) >= 2 else float(self.data.Open[-1])
                lookback_low = float(min(self.data.Low[-self.lookback:])) if self.lookback > 0 else float(self.data.Low[-1])
                candidate = compute_long_trail_candidate(
                    trail_source=self.trail_source, close_prev=close_prev, open_prev=open_prev,
                    lookback_low=lookback_low, atr_now=float(self.atr_value[-1]),
                    trail_stop_size=self.trail_stop_size,
                )
                self._trail_stop_price = update_long_trail_stop(
                    position_size=float(self.position.size), look_for_exit=self._look_for_exit,
                    current_trail_stop=self._trail_stop_price, candidate_trail_stop=candidate,
                )

            self._active_stop_price = active_long_stop(
                trade_stop_price=self._trade_stop_price, trail_stop_price=self._trail_stop_price,
            )
            if self.trades:
                trade = self.trades[-1]
                trade.sl = self._active_stop_price
                if (not self.trail_stop) and (self._trade_target_price is not None):
                    trade.tp = self._trade_target_price

            if should_close_long(position_size=float(self.position.size)):
                self.position.close()

        elif self.position.size < 0 and self._trade_stop_price is not None:
            if (
                self.trail_stop and not self._look_for_exit
                and self._trade_target_price is not None
                and float(self.data.Low[-1]) <= self._trade_target_price
            ):
                self._look_for_exit = True

            if self.trail_stop and self._look_for_exit:
                close_prev = float(self.data.Close[-2]) if len(self.data.Close) >= 2 else float(self.data.Close[-1])
                open_prev = float(self.data.Open[-2]) if len(self.data.Open) >= 2 else float(self.data.Open[-1])
                lookback_high = float(max(self.data.High[-self.lookback:])) if self.lookback > 0 else float(self.data.High[-1])
                candidate = compute_short_trail_candidate(
                    trail_source=self.trail_source, close_prev=close_prev, open_prev=open_prev,
                    lookback_high=lookback_high, atr_now=float(self.atr_value[-1]),
                    trail_stop_size=self.trail_stop_size,
                )
                self._trail_stop_price = update_short_trail_stop(
                    position_size=float(self.position.size), look_for_exit=self._look_for_exit,
                    current_trail_stop=self._trail_stop_price, candidate_trail_stop=candidate,
                )

            self._active_stop_price = active_short_stop(
                trade_stop_price=self._trade_stop_price, trail_stop_price=self._trail_stop_price,
            )
            if self.trades:
                trade = self.trades[-1]
                trade.sl = self._active_stop_price
                if (not self.trail_stop) and (self._trade_target_price is not None):
                    trade.tp = self._trade_target_price

            if should_close_short(position_size=float(self.position.size)):
                self.position.close()

        if (not self.position.size) and (not self.orders):
            self._trade_stop_price = None
            self._trade_target_price = None
            self._trail_stop_price = None
            self._active_stop_price = None
            self._look_for_exit = False
