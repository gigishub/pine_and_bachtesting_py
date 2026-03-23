#!/usr/bin/env python
"""Add logging to strategy next() method to debug trail stop"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from UPS_py.ups_backtest import Settings, load_ohlcv_kucoin, UPSStrategy
from backtesting.lib import FractionalBacktest

# Instrument the strategy
original_next = UPSStrategy.next

def logged_next(self):
    """Wrapped next() with logging"""
    if not bool(self.is_ready[-1]):
        return
    
    # Log entries
    if self.position.size == 0:
        if bool(self.valid_long_entry[-1]):
            entry_price = float(self.data.Close[-1])
            target = self._trade_target_price
            print(f"[BAR {len(self.data)}] ENTRY at {entry_price:.2f}, Target={target if target else 'N/A'}")
    
    # Log trail stop state
    if self.position.size > 0:
        print(f"[BAR {len(self.data)}] POS OPEN: High={float(self.data.High[-1]):.2f}, "
              f"Target={self._trade_target_price:.2f}, "
              f"LookForExit={self._look_for_exit}, "
              f"TrailStop={self._trail_stop_price}")
    
    # Call original
    original_next(self)

UPSStrategy.next = logged_next

# Load minimal data
df = load_ohlcv_kucoin(
    symbol="XBTUSDTM",
    market_type="futures",
    timeframe="1day",
    start_time="2020-03-25 00:00:00",
    end_time="2020-05-31 00:00:00",
)

settings = Settings(
    trail_stop=True,
    risk_reward_multiplier=1.0,
)

bt = FractionalBacktest(df, UPSStrategy, cash=10_000, commission=0.001)
result = bt.run(
    trail_stop=True,
    risk_reward_multiplier=1.0,
    # ... other params from settings
)

print(f"\nTotal trades: {result['# Trades']}")
