"""Translate PineScript 'Bitcoin Momentum Strategy' to backtesting.py.

Usage:
  source .venv/bin/activate && python bitcoin_momentum_backtest.py
  source .venv/bin/activate && python bitcoin_momentum_backtest.py --csv btc_1d.csv

CSV requirements:
  - Datetime index column or a column named: Date / Datetime / Timestamp / Time
  - Columns: Open, High, Low, Close, Volume
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from backtesting import Strategy
from backtesting.lib import FractionalBacktest
from entry_exit.entry_rules import should_open_long
from entry_exit.exit_rules import should_close_long
from fetch_data.fetch_kucoin_candles import load_ohlcv_kucoin
from strategy_logic import build_strategy_series
from SL_TP.trail_rules import compute_long_trail_candidate, update_long_trail_stop




@dataclass
class Settings:
    long_trades: bool = True
    higher_timeframe: str = "W"
    ema_length: int = 20
    atr_length: int = 5
    trail_stop_source: str = "Low"  # Pine default: low
    trail_stop_lookback: int = 7
    trail_stop_multi: float = 0.2
    bb_length: int = 20
    bb_mult: float = 2.0


class BitcoinMomentumStrategy(Strategy):
    # Strategy entry settings
    long_trades = True
    higher_timeframe = "W"
    ema_length = 20
    atr_length = 5

    # Exit settings
    trail_stop_source = "Low"
    trail_stop_lookback = 7
    trail_stop_multi = 0.2

    bb_length = 20
    bb_mult = 2.0

    def init(self) -> None:
        # Run all indicator logic once up-front on the full DataFrame.
        # backtesting.py calls init() before the bar loop starts, so this is
        # the right place for any computation that doesn't depend on bar index.
        df = self.data.df.copy()
        signals = build_strategy_series(
            df=df,
            higher_timeframe=self.higher_timeframe,
            ema_length=self.ema_length,
            atr_length=self.atr_length,
            bb_length=self.bb_length,
            bb_mult=self.bb_mult,
            trail_stop_source=self.trail_stop_source,
            trail_stop_lookback=self.trail_stop_lookback,
        )

        # Register each signal with self.I() so backtesting.py tracks it as an
        # indicator series — this makes it sliceable with [-1], [-2] in next().
        def _reg(key: str):
            return self.I(lambda: signals[key].values.copy())

        self.atr_value         = _reg("atr_value")          # ATR(atr_length) in USD
        self.htf_ema_value     = _reg("htf_ema_value")      # Weekly EMA — trend filter
        self.is_bullish        = _reg("is_bullish")          # True when price > HTF EMA
        self.is_caution        = _reg("is_caution")          # True when BB squeeze / caution zone
        self.highest_trail_src = _reg("highest_trail_src")  # Rolling highest low for trail anchor
        self.is_ready          = _reg("is_ready")            # False until all indicators have enough bars

        # trail_stop is stateful: updated bar-by-bar in next(), not precomputed.
        self.trail_stop = None

    def _open_position_if_needed(self, bullish: bool, caution: bool) -> None:
        if should_open_long(self.long_trades, bullish, caution, self.position.size):
            self.buy(size=0.99)  # ~100% of equity (Pine: percent_of_equity=100)
            self.trail_stop = None

    def _update_trailing_stop(self, atr_now: float, prev_caution: bool, highest_trail_src_now: float) -> None:
        candidate = compute_long_trail_candidate(
            highest_trail_src_now=highest_trail_src_now,
            atr_now=atr_now,
            trail_stop_multi=self.trail_stop_multi,
            prev_caution=prev_caution,
        )
        self.trail_stop = update_long_trail_stop(
            position_size=self.position.size,
            current_trail_stop=self.trail_stop,
            candidate_trail_stop=candidate,
        )

    def _close_position_if_needed(self, close_now: float, htf_ema_now: float) -> None:
        if should_close_long(
            position_size=self.position.size,
            close_now=close_now,
            trail_stop=self.trail_stop,
            htf_ema_now=htf_ema_now,
        ):
            self.position.close()
            self.trail_stop = None

    def next(self) -> None:
        # Skip bars where indicators haven't warmed up yet (e.g. first ~20 bars).
        if not bool(self.is_ready[-1]):
            return

        # --- Snapshot current-bar values ---
        # Reading [-1] gives the value at the current (most recent visible) bar.
        close_now = self.data.Close[-1]

        bullish = bool(self.is_bullish[-1])   # is the HTF trend up?
        caution = bool(self.is_caution[-1])   # are we in a caution/squeeze zone?

        atr_now               = self.atr_value[-1]
        htf_ema_now           = self.htf_ema_value[-1]
        highest_trail_src_now = self.highest_trail_src[-1]

        # prev_caution: needed by the trail logic to detect caution-zone *exit*
        # (the moment caution flips False is when the trail resets its anchor).
        prev_caution = bool(self.is_caution[-2] if len(self.is_caution) > 1 else False)

        # --- Bar logic: always entry first, then trail update, then exit ---
        # Order matters: entering before updating the stop ensures the stop is
        # set on the same bar as the entry, not one bar late.
        self._open_position_if_needed(bullish, caution)
        self._update_trailing_stop(atr_now, prev_caution, highest_trail_src_now)
        self._close_position_if_needed(close_now, htf_ema_now)


def run_backtest(df: pd.DataFrame) -> tuple[pd.Series, FractionalBacktest]:
    bt = FractionalBacktest(
        df,
        BitcoinMomentumStrategy,
        cash=10_000,        # Pine: initial_capital=10000
        commission=0.001,  # Pine: 0.1%
        trade_on_close=True,
        hedging=False,
        exclusive_orders=True,
        finalize_trades=True,
    )
    stats = bt.run()
    print(stats)
    return stats, bt


def main() -> None:
    # No CLI args mode: fixed KuCoin futures symbol/timeframe range.
    df = load_ohlcv_kucoin(
        symbol="XBTUSDTM",
        market_type="futures",
        timeframe="1day",
        start_time="2020-03-25 00:00:00",
        end_time=None,
    )

    stats, bt = run_backtest(df)
    print("\nTop trades:")
    print(stats["_trades"].head(10).to_string(index=False))
    bt.plot()  # visual check

if __name__ == "__main__":
    main()
