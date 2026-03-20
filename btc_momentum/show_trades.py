"""Compare Python backtest trades vs TradingView screenshot (Jan-May 2021)."""
from backtesting.lib import FractionalBacktest
from bitcoin_momentum_backtest import BitcoinMomentumStrategy
from fetch_kucoin_candles import load_ohlcv_kucoin

# Same params as Pine: KuCoin BTC perpetual, 1D, from same start date
df = load_ohlcv_kucoin(
    symbol="XBTUSDTM",
    market_type="futures",
    timeframe="1day",
    start_time="2020-03-25 00:00:00",
    end_time=None,
)

bt = FractionalBacktest(
    df,
    BitcoinMomentumStrategy,
    cash=10_000,          # match Pine: initial_capital=10000
    commission=0.001,     # match Pine commission 0.1%
    trade_on_close=False, # Pine fills on next bar open (default); True = current close
    hedging=False,
    exclusive_orders=True,
    finalize_trades=True,
)
stats = bt.run()
trades = stats["_trades"]

print("Total Python trades:", len(trades))
print()
print("All trades:")
print(
    trades[["EntryTime", "ExitTime", "EntryPrice", "ExitPrice", "ReturnPct"]]
    .to_string()
)
