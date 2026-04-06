"""Backtest runner for the UPS strategy.

Usage:
  source .venv/bin/activate && python -m UPS_py_v2.backtest.runner
  source .venv/bin/activate && python -m UPS_py_v2.backtest.runner --csv path/to/data.csv

CSV requirements:
  - Datetime index or a column named: Date / Datetime / Timestamp / Time
  - Columns: Open, High, Low, Close, Volume
"""

from __future__ import annotations

import argparse

import pandas as pd
from backtesting.lib import FractionalBacktest

from .strategy import UPSStrategy
from ...strategy.strategy_parameters import StrategySettings


def _load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    df.index.name = "Date"
    return df


def run(
    df: pd.DataFrame,
    settings: StrategySettings | None = None,
    *,
    finalize_trades: bool = True,
    trade_on_close: bool = False,
    **strategy_kwargs,
):
    """Run the backtest and return (bt, result)."""
    s = settings or StrategySettings()
    bt = FractionalBacktest(
        df,
        UPSStrategy,
        cash=10_000,
        commission=0.001,
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
    parser = argparse.ArgumentParser(description="Run UPS backtest (refactored)")
    parser.add_argument("--csv", default=None, help="Path to OHLCV CSV file")
    parser.add_argument("--source", default="bybit", choices=["bybit", "kucoin"])
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--market-type", default="futures", choices=["futures", "spot"])
    parser.add_argument("--timeframe", default="1h")
    parser.add_argument("--start-time", default="2025-03-25 00:00:00")
    parser.add_argument("--end-time", default=None)
    parser.add_argument("--no-plot", action="store_true")
    parser.add_argument("--plot-filename", default="ups_backtest_plot.html")
    args = parser.parse_args()

    if args.csv:
        data = _load_csv(args.csv)
    else:
        # Lazy import so the runner can still be imported without exchange deps
        from ..data.fetch import load_ohlcv
        data = load_ohlcv(
            source=args.source,
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
