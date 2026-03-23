#!/usr/bin/env python
"""Direct verification that trail_stop parameter affects behavior"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from UPS_py.ups_backtest import Settings, load_ohlcv_kucoin, run

# Load data
print("Loading data...")
df = load_ohlcv_kucoin(
    symbol="XBTUSDTM",
    market_type="futures",
    timeframe="1day",
    start_time="2020-03-25 00:00:00",
    end_time=None,
)

base = Settings()

print("\n" + "="*70)
print(" TEST 1: trail_stop = FALSE")
print("="*70)
bt1, result1 = run(df, settings=Settings(**{**vars(base), 'trail_stop': False}))
print(f"Return: {result1['Return [%]']:.2f}%")
print(f"Trades: {int(result1['# Trades'])}")  
print(f"Avg Trade: {result1['Avg. Trade [%]']:.4f}%")
print(f"Max Trade: {result1['Best Trade [%]']:.2f}%")
print(f"Min Trade: {result1['Worst Trade [%]']:.2f}%")

print("\n" + "="*70)
print(" TEST 2: trail_stop = TRUE")
print("="*70)
bt2, result2 = run(df, settings=Settings(**{**vars(base), 'trail_stop': True}))
print(f"Return: {result2['Return [%]']:.2f}%")
print(f"Trades: {int(result2['# Trades'])}")
print(f"Avg Trade: {result2['Avg. Trade [%]']:.4f}%")
print(f"Max Trade: {result2['Best Trade [%]']:.2f}%")
print(f"Min Trade: {result2['Worst Trade [%]']:.2f}%")

print("\n" + "="*70)
print(" VERIFICATION")
print("="*70)

return_diff = result2['Return [%]'] - result1['Return [%]']
trade_diff = int(result2['# Trades']) - int(result1['# Trades'])
avg_trade_diff = result2['Avg. Trade [%]'] - result1['Avg. Trade [%]']

print(f"Return difference: {return_diff:+.2f}% {'✓ DIFFERENT' if return_diff != 0 else '✗ SAME'}")
print(f"Trade count difference: {trade_diff:+d} {'✓ DIFFERENT' if trade_diff != 0 else '✗ SAME'}")
print(f"Avg Trade difference: {avg_trade_diff:+.4f}% {'✓ DIFFERENT' if avg_trade_diff != 0 else '✗ SAME'}")

if return_diff != 0 or trade_diff != 0:
    print("\n✓ Trail stop IS WORKING - behavior is different!")
    print("\n  This means:")
    print("  - trail_stop=False uses fixed RR targets")
    print("  - trail_stop=True activates trailing stop after target is reached")
    print("  - Results differ because winners are allowed to run longer")
else:
    print("\n✗ Trail stop NOT WORKING - behavior is identical!")
