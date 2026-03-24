"""UPS strategy — backtesting.py runner.

Usage:
  source .venv/bin/activate && python UPS_py/ups_backtest.py
  source .venv/bin/activate && python UPS_py/ups_backtest.py --csv path/to/data.csv

CSV requirements:
  - Datetime index or a column named: Date / Datetime / Timestamp / Time
  - Columns: Open, High, Low, Close, Volume
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
from backtesting import Strategy
from backtesting.lib import FractionalBacktest

# Add UPS_py to path so relative imports work when run directly.
sys.path.insert(0, str(Path(__file__).parent))

from strategy_logic import build_strategy_series
from entry_exit.entry_rules import should_open_long, should_open_short
from entry_exit.exit_rules import should_close_long, should_close_short
from fetch_data.fetch_kucoin_candles import load_ohlcv_kucoin
from SL_TP.sl import compute_long_stop, compute_short_stop
from SL_TP.tp import compute_long_target, compute_short_target
from SL_TP.trail_rules import (
    compute_long_trail_candidate,
    compute_short_trail_candidate,
    update_long_trail_stop,
    update_short_trail_stop,
    active_long_stop,
    active_short_stop,
)
from position_sizing import compute_long_size_fraction, compute_short_size_fraction


# ---------------------------------------------------------------------------
# Settings dataclass — mirrors Pine inputs (long-only first pass).
# ---------------------------------------------------------------------------

@dataclass
class Settings:
    # MA
    ma_length: int = 50
    max_candles_beyond_ma: int = 1
    ma_consolidation_lookback: int = 10
    ma_consolidation_count: int = 4
    ma_breach_lookback: int = 5

    # IQ filter
    use_iq_filter: bool = True  # Set True to enable IQ filter, False to disable
    iq_lookback: int = 20
    iq_min_score: float = 0.55
    iq_slope_atr_scale: float = 1.5
    iq_er_weight: float = 0.5
    iq_slope_weight: float = 0.3
    iq_bias_weight: float = 0.2

    use_sq_boost: bool = True
    sq_boost_weight: float = 0.3
    sq_vol_lookback: int = 20

    # Trade direction
    long_trades: bool = True
    short_trades: bool = True

    # Entry Patterns
    # Engulfing pattern controls
    enable_ec: bool = True  # Legacy engulfing candle feature
    enable_bullish_engulfing: bool = True  # Use bullish engulfing in long-entry filter

    # Reversal pattern controls
    enable_shooting_star: bool = True  # Use shooting star as exit/block signal

    # Hammer pattern controls
    enable_hammer: bool = True  # Use hammer as long-entry filter

    # Wick/size filters used by pattern logic
    ec_wick: bool = False
    atr_max_size: float = 2.5
    rejection_wick_max_size: float = 0.0
    hammer_fib: float = 0.3
    hammer_size: float = 0.1

    # Stops & targets
    stop_multiplier: float = 1.0
    risk_reward_multiplier: float = 1.0
    minimum_rr: float = 0.0
    pb_reference: str = "Close"    # "Close" | "Wick"
    sl_reference: str = "High/Low" # "High/Low" | "Open" | "Close"
    # Trailing
    trail_stop: bool = True     # Set True to enable trailing stop, False to disable
    trail_stop_size: float = 1.0
    trail_source: str = "High/Low" # "High/Low" | "Close" | "Open"
    # Lookback / misc
    lookback: int = 5
    atr_length: int = 14
    point_allowance: int = 0
    # Backtester
    risk_per_trade: float = 1.0    # % of equity risked per trade


# ---------------------------------------------------------------------------
# Strategy class
# ---------------------------------------------------------------------------

class UPSStrategy(Strategy):
    # --- class-level params (overridable via Backtest(..., param=val)) ---
    # MA
    ma_length = 50
    max_candles_beyond_ma = 1
    ma_consolidation_lookback = 10
    ma_consolidation_count = 4
    ma_breach_lookback = 5
    # IQ filter
    use_iq_filter = True  # Toggle IQ filter logic
    iq_lookback = 20
    iq_min_score = 0.55
    iq_slope_atr_scale = 1.5
    iq_er_weight = 0.5
    iq_slope_weight = 0.3
    iq_bias_weight = 0.2
    use_sq_boost = True
    sq_boost_weight = 0.3
    sq_vol_lookback = 20
    # Trade direction
    long_trades = True
    short_trades = True
    # Patterns
    enable_ec = True
    enable_bullish_engulfing = True  # Toggle bullish engulfing pattern rule
    enable_shooting_star = True      # Toggle shooting star pattern rule
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
    trail_stop = False     # Toggle trailing stop logic
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
            use_iq_filter=self.use_iq_filter,  # IQ filter toggle
            iq_lookback=self.iq_lookback,
            iq_min_score=self.iq_min_score,
            iq_slope_atr_scale=self.iq_slope_atr_scale,
            iq_er_weight=self.iq_er_weight,
            iq_slope_weight=self.iq_slope_weight,
            iq_bias_weight=self.iq_bias_weight,
            use_sq_boost=self.use_sq_boost,
            sq_boost_weight=self.sq_boost_weight,
            sq_vol_lookback=self.sq_vol_lookback,
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
            trail_stop=self.trail_stop,  # Trailing stop toggle
            trail_stop_size=self.trail_stop_size,
            trail_source=self.trail_source,
            lookback=self.lookback,
            atr_length=self.atr_length,
            point_allowance=self.point_allowance,
        )

        def _reg(key: str):
            return self.I(lambda s=signals[key]: s.values.copy(), name=key)

        # Step 3 will populate build_strategy_series and these will be real.
        # Keys listed here must match what strategy_logic.py returns.
        self.atr_value          = _reg("atr_value")         # ATR(atr_length)
        self.ma1                = _reg("ma1")                # EMA(ma_length)
        self.price_above_ma     = _reg("price_above_ma")    # close > ma1
        self.candles_below_ma   = _reg("candles_below_ma")  # barsBelowMA
        self.candles_above_ma   = _reg("candles_above_ma")  # barsAboveMA
        self.ma_cross_filter    = _reg("ma_cross_filter")   # maCrossCount < maConsolidationCount
        self.iq_long_filter     = _reg("iq_long_filter")    # IQ filter pass for longs
        self.iq_short_filter    = _reg("iq_short_filter")   # IQ filter pass for shorts
        self.long_conditions_met = _reg("long_conditions_met")
        self.short_conditions_met = _reg("short_conditions_met")
        self.bearish_pb         = _reg("bearish_pb")        # pullback bar count >= 2 for long setups
        self.bullish_pb         = _reg("bullish_pb")        # pullback bar count >= 2 for short setups
        self.long_entry_pattern = _reg("long_entry_pattern")
        self.short_entry_pattern = _reg("short_entry_pattern")
        self.long_stop_price    = _reg("long_stop_price")   # ATR stop below entry
        self.long_target_price  = _reg("long_target_price") # RR target above entry
        self.short_stop_price   = _reg("short_stop_price")  # ATR stop above entry
        self.short_target_price = _reg("short_target_price") # RR target below entry
        self.valid_long_entry   = _reg("valid_long_entry")  # all long conditions combined
        self.valid_short_entry  = _reg("valid_short_entry") # all short conditions combined
        self.is_ready           = _reg("is_ready")          # warmup guard

        # Stateful: trail stop managed bar-by-bar in next(), not precomputed.
        self._trade_stop_price: float | None = None
        self._trade_target_price: float | None = None
        self._trail_stop_price: float | None = None
        self._active_stop_price: float | None = None
        self._look_for_exit: bool = False

    def next(self) -> None:
        # Skip warmup bars.
        if not bool(self.is_ready[-1]):
            return

        # --- Step 4: entry only ---
        # Entry logic: IQ filter and trailing stop are controlled by their respective toggles
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
                sl_reference=self.sl_reference,
                low_now=low_now,
                low_prev=low_prev,
                open_now=open_now,
                close_now=close_now,
                atr_now=atr_now,
                stop_multiplier=self.stop_multiplier,
            )
            trade_target_price = compute_long_target(
                entry_price=close_now,
                stop_price=trade_stop_price,
                risk_reward_multiplier=self.risk_reward_multiplier,
            )

            size_fraction = compute_long_size_fraction(
                entry_price=close_now,
                stop_price=trade_stop_price,
                equity=float(self.equity),
                risk_per_trade=float(self.risk_per_trade),
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
                sl_reference=self.sl_reference,
                high_now=high_now,
                high_prev=high_prev,
                open_now=open_now,
                close_now=close_now,
                atr_now=atr_now,
                stop_multiplier=self.stop_multiplier,
            )
            trade_target_price = compute_short_target(
                entry_price=close_now,
                stop_price=trade_stop_price,
                risk_reward_multiplier=self.risk_reward_multiplier,
            )

            size_fraction = compute_short_size_fraction(
                entry_price=close_now,
                stop_price=trade_stop_price,
                equity=float(self.equity),
                risk_per_trade=float(self.risk_per_trade),
            )
            if size_fraction <= 0:
                return

            self.sell(size=size_fraction)
            self._trade_stop_price = trade_stop_price
            self._trade_target_price = trade_target_price
            self._trail_stop_price = None
            self._active_stop_price = self._trade_stop_price
            self._look_for_exit = False

        # --- Step 5: stop/target/trailing state management ---
        if self.position.size > 0 and self._trade_stop_price is not None:
            # Trailing stop logic is only active if trail_stop is enabled
            if (
                self.trail_stop
                and not self._look_for_exit
                and self._trade_target_price is not None
                and float(self.data.High[-1]) >= self._trade_target_price
            ):
                self._look_for_exit = True

            if self.trail_stop and self._look_for_exit:
                close_prev = float(self.data.Close[-2]) if len(self.data.Close) >= 2 else float(self.data.Close[-1])
                open_prev = float(self.data.Open[-2]) if len(self.data.Open) >= 2 else float(self.data.Open[-1])

                if self.lookback > 0:
                    lookback_low = float(min(self.data.Low[-self.lookback:]))
                else:
                    lookback_low = float(self.data.Low[-1])

                candidate = compute_long_trail_candidate(
                    trail_source=self.trail_source,
                    close_prev=close_prev,
                    open_prev=open_prev,
                    lookback_low=lookback_low,
                    atr_now=float(self.atr_value[-1]),
                    trail_stop_size=self.trail_stop_size,
                )
                self._trail_stop_price = update_long_trail_stop(
                    position_size=float(self.position.size),
                    look_for_exit=self._look_for_exit,
                    current_trail_stop=self._trail_stop_price,
                    candidate_trail_stop=candidate,
                )

            self._active_stop_price = active_long_stop(
                trade_stop_price=self._trade_stop_price,
                trail_stop_price=self._trail_stop_price,
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
                self.trail_stop
                and not self._look_for_exit
                and self._trade_target_price is not None
                and float(self.data.Low[-1]) <= self._trade_target_price
            ):
                self._look_for_exit = True

            if self.trail_stop and self._look_for_exit:
                close_prev = float(self.data.Close[-2]) if len(self.data.Close) >= 2 else float(self.data.Close[-1])
                open_prev = float(self.data.Open[-2]) if len(self.data.Open) >= 2 else float(self.data.Open[-1])

                if self.lookback > 0:
                    lookback_high = float(max(self.data.High[-self.lookback:]))
                else:
                    lookback_high = float(self.data.High[-1])

                candidate = compute_short_trail_candidate(
                    trail_source=self.trail_source,
                    close_prev=close_prev,
                    open_prev=open_prev,
                    lookback_high=lookback_high,
                    atr_now=float(self.atr_value[-1]),
                    trail_stop_size=self.trail_stop_size,
                )
                self._trail_stop_price = update_short_trail_stop(
                    position_size=float(self.position.size),
                    look_for_exit=self._look_for_exit,
                    current_trail_stop=self._trail_stop_price,
                    candidate_trail_stop=candidate,
                )

            self._active_stop_price = active_short_stop(
                trade_stop_price=self._trade_stop_price,
                trail_stop_price=self._trail_stop_price,
            )

            if self.trades:
                trade = self.trades[-1]
                trade.sl = self._active_stop_price
                if (not self.trail_stop) and (self._trade_target_price is not None):
                    trade.tp = self._trade_target_price

            if should_close_short(position_size=float(self.position.size)):
                self.position.close()

        if (not self.position.size) and (not self.orders):
            # Reset state only when truly flat and no pending orders.
            # This preserves stop/target state between signal bar and next-bar fill.
            self._trade_stop_price = None
            self._trade_target_price = None
            self._trail_stop_price = None
            self._active_stop_price = None
            self._look_for_exit = False


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def _load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    df.index.name = "Date"
    return df


def run(
    df: pd.DataFrame,
    settings: Settings | None = None,
    *,
    finalize_trades: bool = True,
    trade_on_close: bool = False,
    **strategy_kwargs,
):
    """Run the backtest and return the result object."""
    s = settings or Settings()
    bt = FractionalBacktest(
        df,
        UPSStrategy,
        cash=10_000,
        commission=0.001,   # 0.1% per side — adjust to your exchange
        exclusive_orders=True,
        finalize_trades=finalize_trades,
        trade_on_close=trade_on_close,
    )
    result = bt.run(
        ma_length=s.ma_length,
        max_candles_beyond_ma=s.max_candles_beyond_ma,
        ma_consolidation_lookback=s.ma_consolidation_lookback,
        ma_consolidation_count=s.ma_consolidation_count,
        ma_breach_lookback=s.ma_breach_lookback,
        use_iq_filter=s.use_iq_filter,
        iq_lookback=s.iq_lookback,
        iq_min_score=s.iq_min_score,
        iq_slope_atr_scale=s.iq_slope_atr_scale,
        iq_er_weight=s.iq_er_weight,
        iq_slope_weight=s.iq_slope_weight,
        iq_bias_weight=s.iq_bias_weight,
        use_sq_boost=s.use_sq_boost,
        sq_boost_weight=s.sq_boost_weight,
        sq_vol_lookback=s.sq_vol_lookback,
        long_trades=s.long_trades,
        short_trades=s.short_trades,
        enable_ec=s.enable_ec,
        enable_bullish_engulfing=s.enable_bullish_engulfing,
        enable_shooting_star=s.enable_shooting_star,
        ec_wick=s.ec_wick,
        enable_hammer=s.enable_hammer,
        atr_max_size=s.atr_max_size,
        rejection_wick_max_size=s.rejection_wick_max_size,
        hammer_fib=s.hammer_fib,
        hammer_size=s.hammer_size,
        stop_multiplier=s.stop_multiplier,
        risk_reward_multiplier=s.risk_reward_multiplier,
        minimum_rr=s.minimum_rr,
        pb_reference=s.pb_reference,
        sl_reference=s.sl_reference,
        trail_stop=s.trail_stop,
        trail_stop_size=s.trail_stop_size,
        trail_source=s.trail_source,
        lookback=s.lookback,
        atr_length=s.atr_length,
        point_allowance=s.point_allowance,
        risk_per_trade=s.risk_per_trade,
        **strategy_kwargs,
    )
    return bt, result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run UPS backtest")
    parser.add_argument("--csv", default=None, help="Path to OHLCV CSV file")
    parser.add_argument("--symbol", default="XBTUSDTM", help="KuCoin symbol, e.g. XBTUSDTM or BTC-USDT")
    parser.add_argument("--market-type", default="futures", choices=["futures", "spot"], help="KuCoin market type")
    parser.add_argument("--timeframe", default="1day", help="KuCoin interval, e.g. 1hour, 4hour, 1day")
    parser.add_argument("--start-time", default="2020-03-25 00:00:00", help="UTC start time 'YYYY-MM-DD HH:MM:SS'")
    parser.add_argument("--end-time", default=None, help="UTC end time 'YYYY-MM-DD HH:MM:SS' (default: now UTC)")
    parser.add_argument("--no-plot", action="store_true", help="Run backtest without generating HTML plot")
    parser.add_argument("--plot-filename", default="ups_backtest_plot.html", help="Output HTML filename for bt.plot()")
    args = parser.parse_args()

    if args.csv:
        data = _load_csv(args.csv)
    else:
        data = load_ohlcv_kucoin(
            symbol=args.symbol,
            market_type=args.market_type,
            timeframe=args.timeframe,
            start_time=args.start_time,
            end_time=args.end_time,
        )

    bt, result = run(data)
    print(result)
    if not args.no_plot:
        bt.plot(filename=args.plot_filename)
