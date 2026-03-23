#!/usr/bin/env python
"""Quick test to compare trail_stop=True vs False"""

from UPS_py.ups_backtest import Settings, run, load_ohlcv_kucoin

# Load data once
print("Loading data...")
df = load_ohlcv_kucoin(
    symbol="XBTUSDTM",
    market_type="futures",
    timeframe="1day",
    start_time="2020-03-25 00:00:00",
    end_time=None,
)

# Create base settings
base_settings = Settings(
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
    trail_stop_size=1.0,
    trail_source="High/Low",
    lookback=5,
    atr_length=14,
    point_allowance=0,
    risk_per_trade=1.0,
)

# Test with trail_stop=False
print("\n" + "="*60)
print("Testing with trail_stop=FALSE")
print("="*60)
settings_no_trail = Settings(**{**vars(base_settings), 'trail_stop': False})
bt_no_trail, stats_no_trail = run(df, settings=settings_no_trail)
print(f"Trades: {stats_no_trail['# Trades']}")
print(f"Return: {stats_no_trail['Return [%]']:.2f}%")
print(f"Win Rate: {stats_no_trail['Win Rate [%]']:.2f}%")
print(f"Avg Trade: {stats_no_trail['Avg. Trade [%]']:.4f}%")

# Test with trail_stop=True
print("\n" + "="*60)
print("Testing with trail_stop=TRUE")
print("="*60)
settings_with_trail = Settings(**{**vars(base_settings), 'trail_stop': True})
bt_with_trail, stats_with_trail = run(df, settings=settings_with_trail)
print(f"Trades: {stats_with_trail['# Trades']}")
print(f"Return: {stats_with_trail['Return [%]']:.2f}%")
print(f"Win Rate: {stats_with_trail['Win Rate [%]']:.2f}%")
print(f"Avg Trade: {stats_with_trail['Avg. Trade [%]']:.4f}%")

# Compare
print("\n" + "="*60)
print("DIFFERENCE")
print("="*60)
print(f"Return difference: {stats_with_trail['Return [%]'] - stats_no_trail['Return [%]']:.2f}%")
print(f"Trades difference: {int(stats_with_trail['# Trades']) - int(stats_no_trail['# Trades'])}")
print(f"Win Rate difference: {stats_with_trail['Win Rate [%]'] - stats_no_trail['Win Rate [%]']:.2f}%")
