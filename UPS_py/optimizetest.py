"""Simple optimization example for the UPS strategy.

Usage:
  source .venv/bin/activate && python UPS_py/optimizetest.py
"""

from ups_backtest import Settings, UPSStrategy, load_ohlcv_kucoin, run
from backtesting.lib import FractionalBacktest


# 1) Load data once
df = load_ohlcv_kucoin(
    symbol="XBTUSDTM",
    market_type="futures",
    timeframe="1day",
    start_time="2020-03-25 00:00:00",
    end_time=None,
)


# 2) Baseline run (single config)
baseline = Settings(
    ma_length=50,
    stop_multiplier=1.0,
    risk_reward_multiplier=1.0,
    trail_stop=True,
    trail_stop_size=1.0,
)

_, baseline_stats = run(df, settings=baseline)

print("=== Baseline ===")
print(baseline_stats[["Return [%]", "# Trades", "Win Rate [%]", "SQN"]])


# 3) Simple optimize example
# For optimize(), you only need to pass params you want to search.
# Everything else uses UPSStrategy class defaults.
bt = FractionalBacktest(
    df,
    UPSStrategy,
    cash=10_000,
    commission=0.001,
    exclusive_orders=True,
    finalize_trades=True,
)

opt = bt.optimize(
    ma_length=[20, 30, 40, 50],
    stop_multiplier=[0.8, 1.0, 1.2],
    risk_reward_multiplier=[1.0, 1.5, 2.0],
    trail_stop=[False, True],
    maximize="SQN",  # try also: "Return [%]"
    method="grid",
)

print("\n=== Best From Optimize ===")
print(opt[["Return [%]", "# Trades", "Win Rate [%]", "SQN"]])
print("Best params:", opt["_strategy"])






