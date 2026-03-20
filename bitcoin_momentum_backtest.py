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
from typing import Optional

import pandas as pd
from backtesting import Backtest, Strategy
from btc_momentum.fetch_kucoin_candles import get_kucoin_candles_df
from indicators import ind_ema, ind_atr, ind_bbands, non_repainting_htf_ema


def load_ohlcv_kucoin(
    symbol: str = "XBTUSDTM",
    market_type: str = "futures",
    timeframe: str = "1day",
    start_time: str = "2026-02-01 00:00:00",
    end_time: Optional[str] = None,
) -> pd.DataFrame:
    df = get_kucoin_candles_df(
        symbol=symbol,
        market_type=market_type,
        timeframe=timeframe,
        start_time=start_time,
        end_time=end_time,
    )
    return df[["Open", "High", "Low", "Close", "Volume"]]


@dataclass
class Settings:
    long_trades: bool = True
    short_trades: bool = True
    higher_timeframe: str = "W"
    ema_length: int = 20
    atr_length: int = 5
    trail_stop_source: str = "Low"  # Pine default: low
    trail_stop_lookback: int = 7
    trail_stop_multi: float = 0.2
    use_bb_short_filter: bool = True
    bb_length: int = 20
    bb_mult: float = 2.0
    start_time: str = "2000-01-01 13:30:00+00:00"
    end_time: str = "2099-01-01 19:30:00+00:00"


class BitcoinMomentumStrategy(Strategy):
    # Strategy entry settings
    long_trades = True
    short_trades = True
    higher_timeframe = "W"
    ema_length = 20
    atr_length = 5

    # Exit settings
    trail_stop_source = "Low"
    trail_stop_lookback = 7
    trail_stop_multi = 0.2

    # Filters
    use_bb_short_filter = True
    bb_length = 20
    bb_mult = 2.0
    start_time = "2000-01-01 13:30:00+00:00"
    end_time = "2099-01-01 19:30:00+00:00"

    def init(self) -> None:
        df = self.data.df.copy()
        close = df["Close"]
        high = df["High"]
        low = df["Low"]

        atr_value = ind_atr(high, low, close, self.atr_length)
        ema_value = ind_ema(close, self.ema_length)
        htf_ema_value = non_repainting_htf_ema(close, self.higher_timeframe, self.ema_length)

        bb_basis, bb_lower = ind_bbands(close, self.bb_length, self.bb_mult)

        is_bullish = close > htf_ema_value
        is_bearish = close < htf_ema_value
        bb_downtrend = (close < bb_basis) & (bb_basis < bb_basis.shift(1)) & (close < bb_lower)
        if self.use_bb_short_filter:
            short_trend_confirmed = bb_downtrend
        else:
            short_trend_confirmed = pd.Series(True, index=df.index)

        highest_price_7 = high.rolling(7).max()
        lowest_low_7 = low.rolling(7).min()
        is_caution = is_bullish & (((highest_price_7 - low) > (atr_value * 1.5)) | (close < ema_value))
        is_caution_short = is_bearish & (((high - lowest_low_7) > (atr_value * 1.5)) | (close > ema_value))

        trail_src = low if self.trail_stop_source.lower() == "low" else df[self.trail_stop_source]
        highest_trail_src = trail_src.rolling(self.trail_stop_lookback).max()
        highest_high_lb = high.rolling(self.trail_stop_lookback).max()

        date_index = pd.to_datetime(df.index, utc=True)
        start_ts = pd.Timestamp(self.start_time)
        end_ts = pd.Timestamp(self.end_time)
        date_ok = (date_index >= start_ts) & (date_index <= end_ts)

        self.atr_value = self.I(lambda: atr_value.values)
        self.htf_ema_value = self.I(lambda: htf_ema_value.values)
        self.is_bullish = self.I(lambda: is_bullish.fillna(False).values)
        self.is_bearish = self.I(lambda: is_bearish.fillna(False).values)
        self.short_trend_confirmed = self.I(lambda: short_trend_confirmed.fillna(False).values)
        self.is_caution = self.I(lambda: is_caution.fillna(False).values)
        self.is_caution_short = self.I(lambda: is_caution_short.fillna(False).values)
        self.highest_trail_src = self.I(lambda: highest_trail_src.values)
        self.highest_high_lb = self.I(lambda: highest_high_lb.values)
        self.date_ok = self.I(lambda: date_ok)

        self.trail_stop = None
        self.short_trail_stop = None

    def next(self) -> None:
        close = self.data.Close[-1]
        high = self.data.High[-1]

        bullish = bool(self.is_bullish[-1])
        bearish = bool(self.is_bearish[-1])
        caution = bool(self.is_caution[-1])
        caution_short = bool(self.is_caution_short[-1])
        short_ok = bool(self.short_trend_confirmed[-1])
        date_ok = bool(self.date_ok[-1])

        atr_now = self.atr_value[-1]
        htf_ema_now = self.htf_ema_value[-1]
        highest_trail_src_now = self.highest_trail_src[-1]
        highest_high_lb_now = self.highest_high_lb[-1]

        prev_caution = bool(self.is_caution[-2]) if len(self.is_caution) > 1 else False
        prev_caution_short = bool(self.is_caution_short[-2]) if len(self.is_caution_short) > 1 else False

        # Long entry
        if (
            self.long_trades
            and bullish
            and self.position.size == 0
            and date_ok
            and not caution
        ):
            self.buy(size=0.9999)
            self.trail_stop = None

        # Long trailing stop update
        long_atr_dist = atr_now * (self.trail_stop_multi if prev_caution else 1.0)
        temp_trail_stop = highest_trail_src_now - long_atr_dist
        if self.position.size > 0:
            if self.trail_stop is None or temp_trail_stop > self.trail_stop:
                self.trail_stop = temp_trail_stop

        # Long exit
        if self.position.size > 0 and self.trail_stop is not None:
            if (close < self.trail_stop) or (close < htf_ema_now):
                self.position.close()
                self.trail_stop = None

        # Short entry
        if (
            self.short_trades
            and bearish
            and short_ok
            and self.position.size == 0
            and date_ok
            and not caution_short
        ):
            self.sell(size=0.9999)
            self.short_trail_stop = None

        # Short trailing stop update
        short_atr_dist = atr_now * (self.trail_stop_multi if prev_caution_short else 1.0)
        temp_short_trail_stop = highest_high_lb_now + short_atr_dist
        if self.position.size < 0:
            if self.short_trail_stop is None or temp_short_trail_stop < self.short_trail_stop:
                self.short_trail_stop = temp_short_trail_stop

        # Short exit
        if self.position.size < 0 and self.short_trail_stop is not None:
            if (high > self.short_trail_stop) or (close > htf_ema_now):
                self.position.close()
                self.short_trail_stop = None


def run_backtest(df: pd.DataFrame) -> pd.Series:
    bt = Backtest(
        df,
        BitcoinMomentumStrategy,
        cash=1_000_000,
        commission=0.001,  # Pine: 0.1%
        trade_on_close=False,
        hedging=False,
        exclusive_orders=True,
        finalize_trades=True,
    )
    stats = bt.run()
    print(stats)
    return stats


def main() -> None:
    # No CLI args mode: fixed KuCoin futures symbol/timeframe range.
    df = load_ohlcv_kucoin(
        symbol="XBTUSDTM",
        market_type="futures",
        timeframe="1day",
        start_time="2026-01-01 00:00:00",
        end_time=None,
    )

    stats = run_backtest(df)
    print("\nTop trades:")
    print(stats["_trades"].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
