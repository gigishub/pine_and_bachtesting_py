#!/usr/bin/env python
"""Debug script to trace trailing stop activation"""

from UPS_py.ups_backtest import Settings, load_ohlcv_kucoin
from UPS_py.ups_backtest import UPSStrategy
from backtesting.lib import FractionalBacktest

# Load data
print("Loading data...")
df = load_ohlcv_kucoin(
    symbol="XBTUSDTM",
    market_type="futures",
    timeframe="1day",
    start_time="2020-03-25 00:00:00",
    end_time="2020-06-30 00:00:00",  # Short period for debugging
)

settings = Settings(
    ma_length=50,
    max_candles_beyond_ma=1,
    ma_consolidation_lookback=10,
    ma_consolidation_count=4,
    ma_breach_lookback=5,
    use_iq_filter=True,
    iq_lookback=20,
    iq_min_score=0.55,
    iq_slope_atr_scale=1.5,
    iq_er_weight=0.5,
    iq_slope_weight=0.3,
    iq_bias_weight=0.2,
    use_sq_boost=True,
    sq_boost_weight=0.3,
    sq_vol_lookback=20,
    enable_ec=True,
    enable_bullish_engulfing=True,
    enable_shooting_star=True,
    enable_hammer=True,
    ec_wick=False,
    atr_max_size=2.5,
    rejection_wick_max_size=0.0,
    hammer_fib=0.3,
    hammer_size=0.1,
    stop_multiplier=1.0,
    risk_reward_multiplier=1.0,
    minimum_rr=0.0,
    pb_reference="Close",
    sl_reference="High/Low",
    trail_stop=True,  # Enable trail stop
    trail_stop_size=1.0,
    trail_source="High/Low",
    lookback=5,
    atr_length=14,
    point_allowance=0,
    risk_per_trade=1.0,
)

bt = FractionalBacktest(
    df,
    UPSStrategy,
    cash=10_000,
    commission=0.001,
    exclusive_orders=True,
    finalize_trades=True,
    trade_on_close=False,
)

result = bt.run(
    ma_length=settings.ma_length,
    max_candles_beyond_ma=settings.max_candles_beyond_ma,
    ma_consolidation_lookback=settings.ma_consolidation_lookback,
    ma_consolidation_count=settings.ma_consolidation_count,
    ma_breach_lookback=settings.ma_breach_lookback,
    use_iq_filter=settings.use_iq_filter,
    iq_lookback=settings.iq_lookback,
    iq_min_score=settings.iq_min_score,
    iq_slope_atr_scale=settings.iq_slope_atr_scale,
    iq_er_weight=settings.iq_er_weight,
    iq_slope_weight=settings.iq_slope_weight,
    iq_bias_weight=settings.iq_bias_weight,
    use_sq_boost=settings.use_sq_boost,
    sq_boost_weight=settings.sq_boost_weight,
    sq_vol_lookback=settings.sq_vol_lookback,
    long_trades=settings.long_trades,
    short_trades=settings.short_trades,
    enable_ec=settings.enable_ec,
    enable_bullish_engulfing=settings.enable_bullish_engulfing,
    enable_shooting_star=settings.enable_shooting_star,
    ec_wick=settings.ec_wick,
    enable_hammer=settings.enable_hammer,
    atr_max_size=settings.atr_max_size,
    rejection_wick_max_size=settings.rejection_wick_max_size,
    hammer_fib=settings.hammer_fib,
    hammer_size=settings.hammer_size,
    stop_multiplier=settings.stop_multiplier,
    risk_reward_multiplier=settings.risk_reward_multiplier,
    minimum_rr=settings.minimum_rr,
    pb_reference=settings.pb_reference,
    sl_reference=settings.sl_reference,
    trail_stop=settings.trail_stop,
    trail_stop_size=settings.trail_stop_size,
    trail_source=settings.trail_source,
    lookback=settings.lookback,
    atr_length=settings.atr_length,
    point_allowance=settings.point_allowance,
    risk_per_trade=settings.risk_per_trade,
)

print("\n" + "="*60)
print("TRADES WITH TRAIL_STOP=TRUE:")
print("="*60)
print(f"Total Trades: {result['# Trades']}")
print(f"Return: {result['Return [%]']:.2f}%")
print(f"Win Rate: {result['Win Rate [%]']:.2f}%")
print(f"Avg Trade: {result['Avg. Trade [%]']:.4f}%")

trades_df = result._trades

print("\nTrade Analysis:")
for idx, row in trades_df.iterrows():
    entry_price = row['EntryPrice']
    exit_price = row['ExitPrice']
    entry_target = row['Entry_long_target_price']
    entry_stop = row['Entry_long_stop_price']
    exit_stop = row['Exit_long_stop_price']
    
    target_reached = exit_price >= entry_target if entry_target > 0 else False
    
    print(f"\nTrade {idx+1}:")
    print(f"  Entry:        {entry_price:.2f}")
    print(f"  Exit:         {exit_price:.2f}")
    print(f"  Base Stop:    {entry_stop:.2f}")
    print(f"  Target:       {entry_target:.2f}")
    print(f"  Target Reached: {target_reached}")
    print(f"  Exit Stop:    {exit_stop:.2f}")
    print(f"  SL on Close:  {row['SL']:.2f}")
    print(f"  TP on Close:  {row['TP']}")
    print(f"  Return:       {row['ReturnPct']:.4f}%")
