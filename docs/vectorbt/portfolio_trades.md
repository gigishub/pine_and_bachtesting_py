# trades - VectorBT

> **Source:** https://vectorbt.dev/api/portfolio/trades/

---

[ ](https://vectorbt.dev/ "VectorBT") VectorBT 

[ vectorbt  ](https://github.com/polakowo/vectorbt "Go to repository")

  * [ Getting started  ](https://vectorbt.dev/)

Getting started 
    * [ Features  ](https://vectorbt.dev/getting-started/features/)
    * [ Installation  ](https://vectorbt.dev/getting-started/installation/)
    * [ Usage  ](https://vectorbt.dev/getting-started/usage/)
    * [ Resources  ](https://vectorbt.dev/getting-started/resources/)
    * [ Contributing  ](https://vectorbt.dev/getting-started/contributing/)
  * [ API  ](https://vectorbt.dev/api/)

API 
    * [ _settings  ](https://vectorbt.dev/api/_settings/)
    * [ base  ](https://vectorbt.dev/api/base/)

base 
      * [ accessors  ](https://vectorbt.dev/api/base/accessors/)
      * [ array_wrapper  ](https://vectorbt.dev/api/base/array_wrapper/)
      * [ column_grouper  ](https://vectorbt.dev/api/base/column_grouper/)
      * [ combine_fns  ](https://vectorbt.dev/api/base/combine_fns/)
      * [ index_fns  ](https://vectorbt.dev/api/base/index_fns/)
      * [ indexing  ](https://vectorbt.dev/api/base/indexing/)
      * [ reshape_fns  ](https://vectorbt.dev/api/base/reshape_fns/)
    * [ data  ](https://vectorbt.dev/api/data/)

data 
      * [ base  ](https://vectorbt.dev/api/data/base/)
      * [ custom  ](https://vectorbt.dev/api/data/custom/)
      * [ updater  ](https://vectorbt.dev/api/data/updater/)
    * [ generic  ](https://vectorbt.dev/api/generic/)

generic 
      * [ accessors  ](https://vectorbt.dev/api/generic/accessors/)
      * [ decorators  ](https://vectorbt.dev/api/generic/decorators/)
      * [ drawdowns  ](https://vectorbt.dev/api/generic/drawdowns/)
      * [ enums  ](https://vectorbt.dev/api/generic/enums/)
      * [ nb  ](https://vectorbt.dev/api/generic/nb/)
      * [ plots_builder  ](https://vectorbt.dev/api/generic/plots_builder/)
      * [ plotting  ](https://vectorbt.dev/api/generic/plotting/)
      * [ ranges  ](https://vectorbt.dev/api/generic/ranges/)
      * [ splitters  ](https://vectorbt.dev/api/generic/splitters/)
      * [ stats_builder  ](https://vectorbt.dev/api/generic/stats_builder/)
    * [ indicators  ](https://vectorbt.dev/api/indicators/)

indicators 
      * [ basic  ](https://vectorbt.dev/api/indicators/basic/)
      * [ configs  ](https://vectorbt.dev/api/indicators/configs/)
      * [ factory  ](https://vectorbt.dev/api/indicators/factory/)
      * [ nb  ](https://vectorbt.dev/api/indicators/nb/)
    * [ labels  ](https://vectorbt.dev/api/labels/)

labels 
      * [ enums  ](https://vectorbt.dev/api/labels/enums/)
      * [ generators  ](https://vectorbt.dev/api/labels/generators/)
      * [ nb  ](https://vectorbt.dev/api/labels/nb/)
    * [ messaging  ](https://vectorbt.dev/api/messaging/)

messaging 
      * [ telegram  ](https://vectorbt.dev/api/messaging/telegram/)
    * [ ohlcv_accessors  ](https://vectorbt.dev/api/ohlcv_accessors/)
    * [ portfolio  ](https://vectorbt.dev/api/portfolio/)

portfolio 
      * [ base  ](https://vectorbt.dev/api/portfolio/base/)
      * [ decorators  ](https://vectorbt.dev/api/portfolio/decorators/)
      * [ enums  ](https://vectorbt.dev/api/portfolio/enums/)
      * [ logs  ](https://vectorbt.dev/api/portfolio/logs/)
      * [ nb  ](https://vectorbt.dev/api/portfolio/nb/)
      * [ orders  ](https://vectorbt.dev/api/portfolio/orders/)
      * trades  [ trades  ](https://vectorbt.dev/api/portfolio/trades/) Table of contents 
        * Trade types 
          * Entry trades 
          * Exit trades 
          * Positions 
        * Example 
        * Stats 
        * Plots 
        * entry_trades_field_config 
        * exit_trades_field_config 
        * positions_field_config 
        * trades_attach_field_config 
        * trades_field_config 
        * EntryTrades() 
          * from_orders() 
        * ExitTrades() 
          * from_orders() 
        * Positions() 
          * from_trades() 
        * Trades() 
          * close 
          * direction 
          * entry_fees 
          * entry_idx 
          * entry_price 
          * exit_fees 
          * exit_idx 
          * exit_price 
          * expectancy() 
          * field_config 
          * indexing_func() 
          * long 
          * losing 
          * losing_streak 
          * metrics 
          * parent_id 
          * plot() 
          * plot_pnl() 
          * plots_defaults 
          * pnl 
          * profit_factor() 
          * returns 
          * short 
          * size 
          * sqn() 
          * stats_defaults 
          * subplots 
          * win_rate() 
          * winning 
          * winning_streak 
    * [ px_accessors  ](https://vectorbt.dev/api/px_accessors/)
    * [ records  ](https://vectorbt.dev/api/records/)

records 
      * [ base  ](https://vectorbt.dev/api/records/base/)
      * [ col_mapper  ](https://vectorbt.dev/api/records/col_mapper/)
      * [ decorators  ](https://vectorbt.dev/api/records/decorators/)
      * [ mapped_array  ](https://vectorbt.dev/api/records/mapped_array/)
      * [ nb  ](https://vectorbt.dev/api/records/nb/)
    * [ returns  ](https://vectorbt.dev/api/returns/)

returns 
      * [ accessors  ](https://vectorbt.dev/api/returns/accessors/)
      * [ metrics  ](https://vectorbt.dev/api/returns/metrics/)
      * [ nb  ](https://vectorbt.dev/api/returns/nb/)
      * [ qs_adapter  ](https://vectorbt.dev/api/returns/qs_adapter/)
    * [ root_accessors  ](https://vectorbt.dev/api/root_accessors/)
    * [ signals  ](https://vectorbt.dev/api/signals/)

signals 
      * [ accessors  ](https://vectorbt.dev/api/signals/accessors/)
      * [ enums  ](https://vectorbt.dev/api/signals/enums/)
      * [ factory  ](https://vectorbt.dev/api/signals/factory/)
      * [ generators  ](https://vectorbt.dev/api/signals/generators/)
      * [ nb  ](https://vectorbt.dev/api/signals/nb/)
    * [ utils  ](https://vectorbt.dev/api/utils/)

utils 
      * [ array_  ](https://vectorbt.dev/api/utils/array_/)
      * [ attr_  ](https://vectorbt.dev/api/utils/attr_/)
      * [ checks  ](https://vectorbt.dev/api/utils/checks/)
      * [ colors  ](https://vectorbt.dev/api/utils/colors/)
      * [ config  ](https://vectorbt.dev/api/utils/config/)
      * [ datetime_  ](https://vectorbt.dev/api/utils/datetime_/)
      * [ decorators  ](https://vectorbt.dev/api/utils/decorators/)
      * [ docs  ](https://vectorbt.dev/api/utils/docs/)
      * [ enum_  ](https://vectorbt.dev/api/utils/enum_/)
      * [ figure  ](https://vectorbt.dev/api/utils/figure/)
      * [ image_  ](https://vectorbt.dev/api/utils/image_/)
      * [ mapping  ](https://vectorbt.dev/api/utils/mapping/)
      * [ math_  ](https://vectorbt.dev/api/utils/math_/)
      * [ module_  ](https://vectorbt.dev/api/utils/module_/)
      * [ params  ](https://vectorbt.dev/api/utils/params/)
      * [ random_  ](https://vectorbt.dev/api/utils/random_/)
      * [ requests_  ](https://vectorbt.dev/api/utils/requests_/)
      * [ schedule_  ](https://vectorbt.dev/api/utils/schedule_/)
      * [ tags  ](https://vectorbt.dev/api/utils/tags/)
      * [ template  ](https://vectorbt.dev/api/utils/template/)
  * [ Terms  ](https://vectorbt.dev/terms/)

Terms 
    * [ License  ](https://vectorbt.dev/terms/license/)



Table of contents 

  * Trade types 
    * Entry trades 
    * Exit trades 
    * Positions 
  * Example 
  * Stats 
  * Plots 
  * entry_trades_field_config 
  * exit_trades_field_config 
  * positions_field_config 
  * trades_attach_field_config 
  * trades_field_config 
  * EntryTrades() 
    * from_orders() 
  * ExitTrades() 
    * from_orders() 
  * Positions() 
    * from_trades() 
  * Trades() 
    * close 
    * direction 
    * entry_fees 
    * entry_idx 
    * entry_price 
    * exit_fees 
    * exit_idx 
    * exit_price 
    * expectancy() 
    * field_config 
    * indexing_func() 
    * long 
    * losing 
    * losing_streak 
    * metrics 
    * parent_id 
    * plot() 
    * plot_pnl() 
    * plots_defaults 
    * pnl 
    * profit_factor() 
    * returns 
    * short 
    * size 
    * sqn() 
    * stats_defaults 
    * subplots 
    * win_rate() 
    * winning 
    * winning_streak 



# trades module[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py "Jump to source")¶

Base class for working with trade records.

Trade records capture information on trades.

In vectorbt, a trade is a sequence of orders that starts with an opening order and optionally ends with a closing order. Every pair of opposite orders can be represented by a trade. Each trade has a PnL info attached to quickly assess its performance. An interesting effect of this representation is the ability to aggregate trades: if two or more trades are happening one after another in time, they can be aggregated into a bigger trade. This way, for example, single-order trades can be aggregated into positions; but also multiple positions can be aggregated into a single blob that reflects the performance of the entire symbol.

Warning

All classes return both closed AND open trades/positions, which may skew your performance results. To only consider closed trades/positions, you should explicitly query the `closed` attribute.

## Trade types¶

There are three main types of trades.

### Entry trades¶

An entry trade is created from each order that opens or adds to a position.

For example, if we have a single large buy order and 100 smaller sell orders, we will see a single trade with the entry information copied from the buy order and the exit information being a size-weighted average over the exit information of all sell orders. On the other hand, if we have 100 smaller buy orders and a single sell order, we will see 100 trades, each with the entry information copied from the buy order and the exit information being a size-based fraction of the exit information of the sell order.

Use [EntryTrades.from_orders()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.EntryTrades.from_orders "vectorbt.portfolio.trades.EntryTrades.from_orders") to build entry trades from orders. Also available as [Portfolio.entry_trades](https://vectorbt.dev/api/portfolio/base/#vectorbt.portfolio.base.Portfolio.entry_trades "vectorbt.portfolio.base.Portfolio.entry_trades").

### Exit trades¶

An exit trade is created from each order that closes or removes from a position.

Use [ExitTrades.from_orders()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.ExitTrades.from_orders "vectorbt.portfolio.trades.ExitTrades.from_orders") to build exit trades from orders. Also available as [Portfolio.exit_trades](https://vectorbt.dev/api/portfolio/base/#vectorbt.portfolio.base.Portfolio.exit_trades "vectorbt.portfolio.base.Portfolio.exit_trades").

### Positions¶

A position is created from a sequence of entry or exit trades.

Use [Positions.from_trades()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Positions.from_trades "vectorbt.portfolio.trades.Positions.from_trades") to build positions from entry or exit trades. Also available as [Portfolio.positions](https://vectorbt.dev/api/portfolio/base/#vectorbt.portfolio.base.Portfolio.positions "vectorbt.portfolio.base.Portfolio.positions").

## Example¶

  * Increasing position:


    
    
    >>> import pandas as pd
    >>> import numpy as np
    >>> from datetime import datetime, timedelta
    >>> import vectorbt as vbt
    
    >>> # Entry trades
    >>> pf_kwargs = dict(
    ...     close=pd.Series([1., 2., 3., 4., 5.]),
    ...     size=pd.Series([1., 1., 1., 1., -4.]),
    ...     fixed_fees=1.
    ... )
    >>> entry_trades = vbt.Portfolio.from_orders(**pf_kwargs).entry_trades
    >>> entry_trades.records_readable
       Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \
    0         0       0   1.0                0              1.0         1.0
    1         1       0   1.0                1              2.0         1.0
    2         2       0   1.0                2              3.0         1.0
    3         3       0   1.0                3              4.0         1.0
    
       Exit Timestamp  Avg Exit Price  Exit Fees   PnL  Return Direction  Status  \
    0               4             5.0       0.25  2.75  2.7500      Long  Closed
    1               4             5.0       0.25  1.75  0.8750      Long  Closed
    2               4             5.0       0.25  0.75  0.2500      Long  Closed
    3               4             5.0       0.25 -0.25 -0.0625      Long  Closed
    
       Parent Id
    0          0
    1          0
    2          0
    3          0
    
    >>> # Exit trades
    >>> exit_trades = vbt.Portfolio.from_orders(**pf_kwargs).exit_trades
    >>> exit_trades.records_readable
       Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \
    0         0       0   4.0                0              2.5         4.0
    
       Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction  Status  \
    0               4             5.0        1.0  5.0     0.5      Long  Closed
    
       Parent Id
    0          0
    
    >>> # Positions
    >>> positions = vbt.Portfolio.from_orders(**pf_kwargs).positions
    >>> positions.records_readable
       Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \
    0         0       0   4.0                0              2.5         4.0
    
       Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction  Status  \
    0               4             5.0        1.0  5.0     0.5      Long  Closed
    
       Parent Id
    0          0
    
    >>> entry_trades.pnl.sum() == exit_trades.pnl.sum() == positions.pnl.sum()
    True
    

  * Decreasing position:


    
    
    >>> # Entry trades
    >>> pf_kwargs = dict(
    ...     close=pd.Series([1., 2., 3., 4., 5.]),
    ...     size=pd.Series([4., -1., -1., -1., -1.]),
    ...     fixed_fees=1.
    ... )
    >>> entry_trades = vbt.Portfolio.from_orders(**pf_kwargs).entry_trades
    >>> entry_trades.records_readable
       Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \
    0         0       0   4.0                0              1.0         1.0
    
       Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction  Status  \
    0               4             3.5        4.0  5.0    1.25      Long  Closed
    
       Parent Id
    0          0
    
    >>> # Exit trades
    >>> exit_trades = vbt.Portfolio.from_orders(**pf_kwargs).exit_trades
    >>> exit_trades.records_readable
       Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \
    0         0       0   1.0                0              1.0        0.25
    1         1       0   1.0                0              1.0        0.25
    2         2       0   1.0                0              1.0        0.25
    3         3       0   1.0                0              1.0        0.25
    
       Exit Timestamp  Avg Exit Price  Exit Fees   PnL  Return Direction  Status  \
    0               1             2.0        1.0 -0.25   -0.25      Long  Closed
    1               2             3.0        1.0  0.75    0.75      Long  Closed
    2               3             4.0        1.0  1.75    1.75      Long  Closed
    3               4             5.0        1.0  2.75    2.75      Long  Closed
    
       Parent Id
    0          0
    1          0
    2          0
    3          0
    
    >>> # Positions
    >>> positions = vbt.Portfolio.from_orders(**pf_kwargs).positions
    >>> positions.records_readable
       Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \
    0         0       0   4.0                0              1.0         1.0
    
       Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction  Status  \
    0               4             3.5        4.0  5.0    1.25      Long  Closed
    
       Parent Id
    0          0
    
    >>> entry_trades.pnl.sum() == exit_trades.pnl.sum() == positions.pnl.sum()
    True
    

  * Multiple reversing positions:


    
    
    >>> # Entry trades
    >>> pf_kwargs = dict(
    ...     close=pd.Series([1., 2., 3., 4., 5.]),
    ...     size=pd.Series([1., -2., 2., -2., 1.]),
    ...     fixed_fees=1.
    ... )
    >>> entry_trades = vbt.Portfolio.from_orders(**pf_kwargs).entry_trades
    >>> entry_trades.records_readable
       Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \
    0         0       0   1.0                0              1.0         1.0
    1         1       0   1.0                1              2.0         0.5
    2         2       0   1.0                2              3.0         0.5
    3         3       0   1.0                3              4.0         0.5
    
       Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction  Status  \
    0               1             2.0        0.5 -0.5  -0.500      Long  Closed
    1               2             3.0        0.5 -2.0  -1.000     Short  Closed
    2               3             4.0        0.5  0.0   0.000      Long  Closed
    3               4             5.0        1.0 -2.5  -0.625     Short  Closed
    
       Parent Id
    0          0
    1          1
    2          2
    3          3
    
    >>> # Exit trades
    >>> exit_trades = vbt.Portfolio.from_orders(**pf_kwargs).exit_trades
    >>> exit_trades.records_readable
       Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \
    0         0       0   1.0                0              1.0         1.0
    1         1       0   1.0                1              2.0         0.5
    2         2       0   1.0                2              3.0         0.5
    3         3       0   1.0                3              4.0         0.5
    
       Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction  Status  \
    0               1             2.0        0.5 -0.5  -0.500      Long  Closed
    1               2             3.0        0.5 -2.0  -1.000     Short  Closed
    2               3             4.0        0.5  0.0   0.000      Long  Closed
    3               4             5.0        1.0 -2.5  -0.625     Short  Closed
    
       Parent Id
    0          0
    1          1
    2          2
    3          3
    
    >>> # Positions
    >>> positions = vbt.Portfolio.from_orders(**pf_kwargs).positions
    >>> positions.records_readable
       Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \
    0         0       0   1.0                0              1.0         1.0
    1         1       0   1.0                1              2.0         0.5
    2         2       0   1.0                2              3.0         0.5
    3         3       0   1.0                3              4.0         0.5
    
       Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction  Status  \
    0               1             2.0        0.5 -0.5  -0.500      Long  Closed
    1               2             3.0        0.5 -2.0  -1.000     Short  Closed
    2               3             4.0        0.5  0.0   0.000      Long  Closed
    3               4             5.0        1.0 -2.5  -0.625     Short  Closed
    
       Parent Id
    0          0
    1          1
    2          2
    3          3
    
    >>> entry_trades.pnl.sum() == exit_trades.pnl.sum() == positions.pnl.sum()
    True
    

  * Open position:


    
    
    >>> # Entry trades
    >>> pf_kwargs = dict(
    ...     close=pd.Series([1., 2., 3., 4., 5.]),
    ...     size=pd.Series([1., 0., 0., 0., 0.]),
    ...     fixed_fees=1.
    ... )
    >>> entry_trades = vbt.Portfolio.from_orders(**pf_kwargs).entry_trades
    >>> entry_trades.records_readable
       Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \
    0         0       0   1.0                0              1.0         1.0
    
       Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction Status  \
    0               4             5.0        0.0  3.0     3.0      Long   Open
    
       Parent Id
    0          0
    
    >>> # Exit trades
    >>> exit_trades = vbt.Portfolio.from_orders(**pf_kwargs).exit_trades
    >>> exit_trades.records_readable
       Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \
    0         0       0   1.0                0              1.0         1.0
    
       Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction Status  \
    0               4             5.0        0.0  3.0     3.0      Long   Open
    
       Parent Id
    0          0
    
    >>> # Positions
    >>> positions = vbt.Portfolio.from_orders(**pf_kwargs).positions
    >>> positions.records_readable
       Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \
    0         0       0   1.0                0              1.0         1.0
    
       Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction Status  \
    0               4             5.0        0.0  3.0     3.0      Long   Open
    
       Parent Id
    0          0
    
    >>> entry_trades.pnl.sum() == exit_trades.pnl.sum() == positions.pnl.sum()
    True
    

Get trade count, trade PnL, and winning trade PnL:
    
    
    >>> price = pd.Series([1., 2., 3., 4., 3., 2., 1.])
    >>> size = pd.Series([1., -0.5, -0.5, 2., -0.5, -0.5, -0.5])
    >>> trades = vbt.Portfolio.from_orders(price, size).trades
    
    >>> trades.count()
    6
    
    >>> trades.pnl.sum()
    -3.0
    
    >>> trades.winning.count()
    2
    
    >>> trades.winning.pnl.sum()
    1.5
    

Get count and PnL of trades with duration of more than 2 days:
    
    
    >>> mask = (trades.records['exit_idx'] - trades.records['entry_idx']) > 2
    >>> trades_filtered = trades.apply_mask(mask)
    >>> trades_filtered.count()
    2
    
    >>> trades_filtered.pnl.sum()
    -3.0
    

## Stats¶

Hint

See [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.generic.stats_builder.StatsBuilderMixin.stats") and [Trades.metrics](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.metrics "vectorbt.portfolio.trades.Trades.metrics").
    
    
    >>> np.random.seed(42)
    >>> price = pd.DataFrame({
    ...     'a': np.random.uniform(1, 2, size=100),
    ...     'b': np.random.uniform(1, 2, size=100)
    ... }, index=[datetime(2020, 1, 1) + timedelta(days=i) for i in range(100)])
    >>> size = pd.DataFrame({
    ...     'a': np.random.uniform(-1, 1, size=100),
    ...     'b': np.random.uniform(-1, 1, size=100),
    ... }, index=[datetime(2020, 1, 1) + timedelta(days=i) for i in range(100)])
    >>> pf = vbt.Portfolio.from_orders(price, size, fees=0.01, freq='d')
    
    >>> pf.trades['a'].stats()
    Start                                2020-01-01 00:00:00
    End                                  2020-04-09 00:00:00
    Period                                 100 days 00:00:00
    First Trade Start                    2020-01-01 00:00:00
    Last Trade End                       2020-04-09 00:00:00
    Coverage                               100 days 00:00:00
    Overlap Coverage                        97 days 00:00:00
    Total Records                                         48
    Total Long Trades                                     22
    Total Short Trades                                    26
    Total Closed Trades                                   47
    Total Open Trades                                      1
    Open Trade PnL                                 -1.290981
    Win Rate [%]                                    51.06383
    Max Win Streak                                         3
    Max Loss Streak                                        3
    Best Trade [%]                                 43.326077
    Worst Trade [%]                               -59.478304
    Avg Winning Trade [%]                          21.418522
    Avg Losing Trade [%]                          -18.856792
    Avg Winning Trade Duration              22 days 22:00:00
    Avg Losing Trade Duration     29 days 01:02:36.521739130
    Profit Factor                                   0.976634
    Expectancy                                     -0.001569
    SQN                                            -0.064929
    Name: a, dtype: object
    

Positions share almost identical metrics with trades:
    
    
    >>> pf.positions['a'].stats()
    Start                            2020-01-01 00:00:00
    End                              2020-04-09 00:00:00
    Period                             100 days 00:00:00
    Coverage [%]                                   100.0
    First Position Start             2020-01-01 00:00:00
    Last Position End                2020-04-09 00:00:00
    Total Records                                      3
    Total Long Positions                               2
    Total Short Positions                              1
    Total Closed Positions                             2
    Total Open Positions                               1
    Open Position PnL                          -0.929746
    Win Rate [%]                                    50.0
    Max Win Streak                                     1
    Max Loss Streak                                    1
    Best Position [%]                          39.498421
    Worst Position [%]                          -3.32533
    Avg Winning Position [%]                   39.498421
    Avg Losing Position [%]                     -3.32533
    Avg Winning Position Duration        1 days 00:00:00
    Avg Losing Position Duration        47 days 00:00:00
    Profit Factor                               0.261748
    Expectancy                                 -0.217492
    SQN                                        -0.585103
    Name: a, dtype: object
    

To also include open trades/positions when calculating metrics such as win rate, pass `incl_open=True`:
    
    
    >>> pf.trades['a'].stats(settings=dict(incl_open=True))
    Start                         2020-01-01 00:00:00
    End                           2020-04-09 00:00:00
    Period                          100 days 00:00:00
    First Trade Start             2020-01-01 00:00:00
    Last Trade End                2020-04-09 00:00:00
    Coverage                        100 days 00:00:00
    Overlap Coverage                 97 days 00:00:00
    Total Records                                  48
    Total Long Trades                              22
    Total Short Trades                             26
    Total Closed Trades                            47
    Total Open Trades                               1
    Open Trade PnL                          -1.290981
    Win Rate [%]                             51.06383
    Max Win Streak                                  3
    Max Loss Streak                                 3
    Best Trade [%]                          43.326077
    Worst Trade [%]                        -59.478304
    Avg Winning Trade [%]                   21.418522
    Avg Losing Trade [%]                   -19.117677
    Avg Winning Trade Duration       22 days 22:00:00
    Avg Losing Trade Duration        30 days 00:00:00
    Profit Factor                            0.693135
    Expectancy                              -0.028432
    SQN                                     -0.794284
    Name: a, dtype: object
    

[StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.portfolio.trades.Trades.stats") also supports (re-)grouping:
    
    
    >>> pf.trades.stats(group_by=True)
    Start                                2020-01-01 00:00:00
    End                                  2020-04-09 00:00:00
    Period                                 100 days 00:00:00
    First Trade Start                    2020-01-01 00:00:00
    Last Trade End                       2020-04-09 00:00:00
    Coverage                               100 days 00:00:00
    Overlap Coverage                       100 days 00:00:00
    Total Records                                        104
    Total Long Trades                                     32
    Total Short Trades                                    72
    Total Closed Trades                                  102
    Total Open Trades                                      2
    Open Trade PnL                                 -1.790938
    Win Rate [%]                                   46.078431
    Max Win Streak                                         5
    Max Loss Streak                                        5
    Best Trade [%]                                 43.326077
    Worst Trade [%]                               -87.793448
    Avg Winning Trade [%]                          19.023926
    Avg Losing Trade [%]                          -20.605892
    Avg Winning Trade Duration    24 days 08:40:51.063829787
    Avg Losing Trade Duration     25 days 11:20:43.636363636
    Profit Factor                                   0.909581
    Expectancy                                     -0.006035
    SQN                                            -0.365593
    Name: group, dtype: object
    

## Plots¶

Hint

See [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.generic.plots_builder.PlotsBuilderMixin.plots") and [Trades.subplots](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.subplots "vectorbt.portfolio.trades.Trades.subplots").

[Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades "vectorbt.portfolio.trades.Trades") class has two subplots based on [Trades.plot()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.plot "vectorbt.portfolio.trades.Trades.plot") and [Trades.plot_pnl()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.plot_pnl "vectorbt.portfolio.trades.Trades.plot_pnl"):
    
    
    >>> pf.trades['a'].plots(settings=dict(plot_zones=False)).show_svg()
    

* * *

## entry_trades_field_config Config[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py "Jump to source")¶

Field config for [EntryTrades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.EntryTrades "vectorbt.portfolio.trades.EntryTrades").
    
    
    Config({
        "settings": {
            "id": {
                "title": "Entry Trade Id"
            },
            "idx": {
                "name": "entry_idx"
            }
        }
    })
    

* * *

## exit_trades_field_config Config[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py "Jump to source")¶

Field config for [ExitTrades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.ExitTrades "vectorbt.portfolio.trades.ExitTrades").
    
    
    Config({
        "settings": {
            "id": {
                "title": "Exit Trade Id"
            }
        }
    })
    

* * *

## positions_field_config Config[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py "Jump to source")¶

Field config for [Positions](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Positions "vectorbt.portfolio.trades.Positions").
    
    
    Config({
        "settings": {
            "id": {
                "title": "Position Id"
            },
            "parent_id": {
                "title": "Parent Id",
                "ignore": true
            }
        }
    })
    

* * *

## trades_attach_field_config Config[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py "Jump to source")¶

Config of fields to be attached to [Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades "vectorbt.portfolio.trades.Trades").
    
    
    Config({
        "return": {
            "attach": "returns"
        },
        "direction": {
            "attach_filters": true
        },
        "status": {
            "attach_filters": true,
            "on_conflict": "ignore"
        }
    })
    

* * *

## trades_field_config Config[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py "Jump to source")¶

Field config for [Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades "vectorbt.portfolio.trades.Trades").
    
    
    Config({
        "dtype": {
            "id": "int64",
            "col": "int64",
            "size": "float64",
            "entry_idx": "int64",
            "entry_price": "float64",
            "entry_fees": "float64",
            "exit_idx": "int64",
            "exit_price": "float64",
            "exit_fees": "float64",
            "pnl": "float64",
            "return": "float64",
            "direction": "int64",
            "status": "int64",
            "parent_id": "int64"
        },
        "settings": {
            "id": {
                "title": "Trade Id"
            },
            "idx": {
                "name": "exit_idx"
            },
            "start_idx": {
                "name": "entry_idx"
            },
            "end_idx": {
                "name": "exit_idx"
            },
            "size": {
                "title": "Size"
            },
            "entry_idx": {
                "title": "Entry Timestamp",
                "mapping": "index"
            },
            "entry_price": {
                "title": "Avg Entry Price"
            },
            "entry_fees": {
                "title": "Entry Fees"
            },
            "exit_idx": {
                "title": "Exit Timestamp",
                "mapping": "index"
            },
            "exit_price": {
                "title": "Avg Exit Price"
            },
            "exit_fees": {
                "title": "Exit Fees"
            },
            "pnl": {
                "title": "PnL"
            },
            "return": {
                "title": "Return"
            },
            "direction": {
                "title": "Direction",
                "mapping": {
                    "Long": 0,
                    "Short": 1
                }
            },
            "status": {
                "title": "Status",
                "mapping": {
                    "Open": 0,
                    "Closed": 1
                }
            },
            "parent_id": {
                "title": "Position Id"
            }
        }
    })
    

* * *

## EntryTrades class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L1487-L1505 "Jump to source")¶
    
    
    EntryTrades(
        wrapper,
        records_arr,
        close,
        **kwargs
    )
    

Extends [Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades "vectorbt.portfolio.trades.Trades") for working with entry trade records.

**Superclasses**

  * [AttrResolver](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver "vectorbt.utils.attr_.AttrResolver")
  * [Configured](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured "vectorbt.utils.config.Configured")
  * [Documented](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented "vectorbt.utils.docs.Documented")
  * [IndexingBase](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.IndexingBase "vectorbt.base.indexing.IndexingBase")
  * [PandasIndexer](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer "vectorbt.base.indexing.PandasIndexer")
  * [Pickleable](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable "vectorbt.utils.config.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin "vectorbt.generic.plots_builder.PlotsBuilderMixin")
  * [Ranges](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges "vectorbt.generic.ranges.Ranges")
  * [Records](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records "vectorbt.records.base.Records")
  * [RecordsWithFields](https://vectorbt.dev/api/records/base/#vectorbt.records.base.RecordsWithFields "vectorbt.records.base.RecordsWithFields")
  * [StatsBuilderMixin](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin "vectorbt.generic.stats_builder.StatsBuilderMixin")
  * [Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades "vectorbt.portfolio.trades.Trades")
  * [Wrapping](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping "vectorbt.base.array_wrapper.Wrapping")



**Inherited members**

  * [AttrResolver.deep_getattr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.deep_getattr "vectorbt.portfolio.trades.Trades.deep_getattr")
  * [AttrResolver.post_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.post_resolve_attr "vectorbt.portfolio.trades.Trades.post_resolve_attr")
  * [AttrResolver.pre_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.pre_resolve_attr "vectorbt.portfolio.trades.Trades.pre_resolve_attr")
  * [AttrResolver.resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.resolve_attr "vectorbt.portfolio.trades.Trades.resolve_attr")
  * [Configured.copy()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.copy "vectorbt.portfolio.trades.Trades.copy")
  * [Configured.dumps()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.dumps "vectorbt.portfolio.trades.Trades.dumps")
  * [Configured.loads()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.loads "vectorbt.portfolio.trades.Trades.loads")
  * [Configured.to_doc()](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented.to_doc "vectorbt.portfolio.trades.Trades.to_doc")
  * [Configured.update_config()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.update_config "vectorbt.portfolio.trades.Trades.update_config")
  * [PandasIndexer.xs()](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.xs "vectorbt.portfolio.trades.Trades.xs")
  * [Pickleable.load()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.load "vectorbt.portfolio.trades.Trades.load")
  * [Pickleable.save()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.save "vectorbt.portfolio.trades.Trades.save")
  * [PlotsBuilderMixin.build_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbt.portfolio.trades.Trades.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbt.portfolio.trades.Trades.override_subplots_doc")
  * [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.portfolio.trades.Trades.plots")
  * [Ranges.avg_duration()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.avg_duration "vectorbt.portfolio.trades.Trades.avg_duration")
  * [Ranges.coverage()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.coverage "vectorbt.portfolio.trades.Trades.coverage")
  * [Ranges.max_duration()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.max_duration "vectorbt.portfolio.trades.Trades.max_duration")
  * [Ranges.to_mask()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.to_mask "vectorbt.portfolio.trades.Trades.to_mask")
  * [Records.apply()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.apply "vectorbt.portfolio.trades.Trades.apply")
  * [Records.apply_mask()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.apply_mask "vectorbt.portfolio.trades.Trades.apply_mask")
  * [Records.build_field_config_doc()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.build_field_config_doc "vectorbt.portfolio.trades.Trades.build_field_config_doc")
  * [Records.count()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.count "vectorbt.portfolio.trades.Trades.count")
  * [Records.get_apply_mapping_arr()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_apply_mapping_arr "vectorbt.portfolio.trades.Trades.get_apply_mapping_arr")
  * [Records.get_by_col_idxs()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_by_col_idxs "vectorbt.portfolio.trades.Trades.get_by_col_idxs")
  * [Records.get_field_arr()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_arr "vectorbt.portfolio.trades.Trades.get_field_arr")
  * [Records.get_field_mapping()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_mapping "vectorbt.portfolio.trades.Trades.get_field_mapping")
  * [Records.get_field_name()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_name "vectorbt.portfolio.trades.Trades.get_field_name")
  * [Records.get_field_setting()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_setting "vectorbt.portfolio.trades.Trades.get_field_setting")
  * [Records.get_field_title()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_title "vectorbt.portfolio.trades.Trades.get_field_title")
  * [Records.get_map_field()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_map_field "vectorbt.portfolio.trades.Trades.get_map_field")
  * [Records.get_map_field_to_index()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_map_field_to_index "vectorbt.portfolio.trades.Trades.get_map_field_to_index")
  * [Records.indexing_func_meta()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.indexing_func_meta "vectorbt.portfolio.trades.Trades.indexing_func_meta")
  * [Records.is_sorted()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.is_sorted "vectorbt.portfolio.trades.Trades.is_sorted")
  * [Records.map()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map "vectorbt.portfolio.trades.Trades.map")
  * [Records.map_array()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map_array "vectorbt.portfolio.trades.Trades.map_array")
  * [Records.map_field()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map_field "vectorbt.portfolio.trades.Trades.map_field")
  * [Records.override_field_config_doc()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.override_field_config_doc "vectorbt.portfolio.trades.Trades.override_field_config_doc")
  * [Records.replace()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.replace "vectorbt.portfolio.trades.Trades.replace")
  * [Records.sort()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.sort "vectorbt.portfolio.trades.Trades.sort")
  * [RecordsWithFields.field_config](https://vectorbt.dev/api/records/base/#vectorbt.records.base.RecordsWithFields.field_config "vectorbt.records.base.RecordsWithFields.field_config")
  * [StatsBuilderMixin.build_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbt.portfolio.trades.Trades.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbt.portfolio.trades.Trades.override_metrics_doc")
  * [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.portfolio.trades.Trades.stats")
  * [Trades.close](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.close "vectorbt.portfolio.trades.Trades.close")
  * [Trades.closed](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.closed "vectorbt.portfolio.trades.Trades.closed")
  * [Trades.col](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.col "vectorbt.portfolio.trades.Trades.col")
  * [Trades.col_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.col_arr "vectorbt.portfolio.trades.Trades.col_arr")
  * [Trades.col_mapper](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.col_mapper "vectorbt.portfolio.trades.Trades.col_mapper")
  * [Trades.config](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.config "vectorbt.portfolio.trades.Trades.config")
  * [Trades.direction](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.direction "vectorbt.portfolio.trades.Trades.direction")
  * [Trades.duration](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.duration "vectorbt.portfolio.trades.Trades.duration")
  * [Trades.end_idx](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.end_idx "vectorbt.portfolio.trades.Trades.end_idx")
  * [Trades.entry_fees](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.entry_fees "vectorbt.portfolio.trades.Trades.entry_fees")
  * [Trades.entry_idx](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.entry_idx "vectorbt.portfolio.trades.Trades.entry_idx")
  * [Trades.entry_price](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.entry_price "vectorbt.portfolio.trades.Trades.entry_price")
  * [Trades.exit_fees](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.exit_fees "vectorbt.portfolio.trades.Trades.exit_fees")
  * [Trades.exit_idx](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.exit_idx "vectorbt.portfolio.trades.Trades.exit_idx")
  * [Trades.exit_price](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.exit_price "vectorbt.portfolio.trades.Trades.exit_price")
  * [Trades.expectancy()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.expectancy "vectorbt.portfolio.trades.Trades.expectancy")
  * [Trades.from_ts()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.from_ts "vectorbt.portfolio.trades.Trades.from_ts")
  * [Trades.id](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.id "vectorbt.portfolio.trades.Trades.id")
  * [Trades.id_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.id_arr "vectorbt.portfolio.trades.Trades.id_arr")
  * [Trades.idx_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.idx_arr "vectorbt.portfolio.trades.Trades.idx_arr")
  * [Trades.iloc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.iloc "vectorbt.portfolio.trades.Trades.iloc")
  * [Trades.indexing_func()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.indexing_func "vectorbt.portfolio.trades.Trades.indexing_func")
  * [Trades.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.indexing_kwargs "vectorbt.portfolio.trades.Trades.indexing_kwargs")
  * [Trades.loc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.loc "vectorbt.portfolio.trades.Trades.loc")
  * [Trades.long](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.long "vectorbt.portfolio.trades.Trades.long")
  * [Trades.losing](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.losing "vectorbt.portfolio.trades.Trades.losing")
  * [Trades.losing_streak](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.losing_streak "vectorbt.portfolio.trades.Trades.losing_streak")
  * [Trades.open](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.open "vectorbt.portfolio.trades.Trades.open")
  * [Trades.parent_id](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.parent_id "vectorbt.portfolio.trades.Trades.parent_id")
  * [Trades.plot()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.plot "vectorbt.portfolio.trades.Trades.plot")
  * [Trades.plot_pnl()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.plot_pnl "vectorbt.portfolio.trades.Trades.plot_pnl")
  * [Trades.plots_defaults](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.plots_defaults "vectorbt.portfolio.trades.Trades.plots_defaults")
  * [Trades.pnl](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.pnl "vectorbt.portfolio.trades.Trades.pnl")
  * [Trades.profit_factor()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.profit_factor "vectorbt.portfolio.trades.Trades.profit_factor")
  * [Trades.records](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records "vectorbt.portfolio.trades.Trades.records")
  * [Trades.records_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records_arr "vectorbt.portfolio.trades.Trades.records_arr")
  * [Trades.records_readable](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records_readable "vectorbt.portfolio.trades.Trades.records_readable")
  * [Trades.returns](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.returns "vectorbt.portfolio.trades.Trades.returns")
  * [Trades.self_aliases](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.self_aliases "vectorbt.portfolio.trades.Trades.self_aliases")
  * [Trades.short](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.short "vectorbt.portfolio.trades.Trades.short")
  * [Trades.size](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.size "vectorbt.portfolio.trades.Trades.size")
  * [Trades.sqn()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.sqn "vectorbt.portfolio.trades.Trades.sqn")
  * [Trades.start_idx](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.start_idx "vectorbt.portfolio.trades.Trades.start_idx")
  * [Trades.stats_defaults](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.stats_defaults "vectorbt.portfolio.trades.Trades.stats_defaults")
  * [Trades.status](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.status "vectorbt.portfolio.trades.Trades.status")
  * [Trades.ts](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.ts "vectorbt.portfolio.trades.Trades.ts")
  * [Trades.values](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.values "vectorbt.portfolio.trades.Trades.values")
  * [Trades.win_rate()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.win_rate "vectorbt.portfolio.trades.Trades.win_rate")
  * [Trades.winning](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.winning "vectorbt.portfolio.trades.Trades.winning")
  * [Trades.winning_streak](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.winning_streak "vectorbt.portfolio.trades.Trades.winning_streak")
  * [Trades.wrapper](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.wrapper "vectorbt.portfolio.trades.Trades.wrapper")
  * [Trades.writeable_attrs](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.writeable_attrs "vectorbt.portfolio.trades.Trades.writeable_attrs")
  * [Wrapping.regroup()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.regroup "vectorbt.portfolio.trades.Trades.regroup")
  * [Wrapping.resolve_self()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.resolve_self "vectorbt.portfolio.trades.Trades.resolve_self")
  * [Wrapping.select_one()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one "vectorbt.portfolio.trades.Trades.select_one")
  * [Wrapping.select_one_from_obj()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one_from_obj "vectorbt.portfolio.trades.Trades.select_one_from_obj")



* * *

### from_orders class method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L1491-L1505 "Jump to source")¶
    
    
    EntryTrades.from_orders(
        orders,
        close=None,
        attach_close=True,
        **kwargs
    )
    

Build [EntryTrades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.EntryTrades "vectorbt.portfolio.trades.EntryTrades") from [Orders](https://vectorbt.dev/api/portfolio/orders/#vectorbt.portfolio.orders.Orders "vectorbt.portfolio.orders.Orders").

* * *

## ExitTrades class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L1533-L1551 "Jump to source")¶
    
    
    ExitTrades(
        wrapper,
        records_arr,
        close,
        **kwargs
    )
    

Extends [Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades "vectorbt.portfolio.trades.Trades") for working with exit trade records.

**Superclasses**

  * [AttrResolver](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver "vectorbt.utils.attr_.AttrResolver")
  * [Configured](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured "vectorbt.utils.config.Configured")
  * [Documented](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented "vectorbt.utils.docs.Documented")
  * [IndexingBase](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.IndexingBase "vectorbt.base.indexing.IndexingBase")
  * [PandasIndexer](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer "vectorbt.base.indexing.PandasIndexer")
  * [Pickleable](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable "vectorbt.utils.config.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin "vectorbt.generic.plots_builder.PlotsBuilderMixin")
  * [Ranges](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges "vectorbt.generic.ranges.Ranges")
  * [Records](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records "vectorbt.records.base.Records")
  * [RecordsWithFields](https://vectorbt.dev/api/records/base/#vectorbt.records.base.RecordsWithFields "vectorbt.records.base.RecordsWithFields")
  * [StatsBuilderMixin](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin "vectorbt.generic.stats_builder.StatsBuilderMixin")
  * [Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades "vectorbt.portfolio.trades.Trades")
  * [Wrapping](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping "vectorbt.base.array_wrapper.Wrapping")



**Inherited members**

  * [AttrResolver.deep_getattr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.deep_getattr "vectorbt.portfolio.trades.Trades.deep_getattr")
  * [AttrResolver.post_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.post_resolve_attr "vectorbt.portfolio.trades.Trades.post_resolve_attr")
  * [AttrResolver.pre_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.pre_resolve_attr "vectorbt.portfolio.trades.Trades.pre_resolve_attr")
  * [AttrResolver.resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.resolve_attr "vectorbt.portfolio.trades.Trades.resolve_attr")
  * [Configured.copy()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.copy "vectorbt.portfolio.trades.Trades.copy")
  * [Configured.dumps()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.dumps "vectorbt.portfolio.trades.Trades.dumps")
  * [Configured.loads()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.loads "vectorbt.portfolio.trades.Trades.loads")
  * [Configured.to_doc()](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented.to_doc "vectorbt.portfolio.trades.Trades.to_doc")
  * [Configured.update_config()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.update_config "vectorbt.portfolio.trades.Trades.update_config")
  * [PandasIndexer.xs()](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.xs "vectorbt.portfolio.trades.Trades.xs")
  * [Pickleable.load()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.load "vectorbt.portfolio.trades.Trades.load")
  * [Pickleable.save()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.save "vectorbt.portfolio.trades.Trades.save")
  * [PlotsBuilderMixin.build_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbt.portfolio.trades.Trades.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbt.portfolio.trades.Trades.override_subplots_doc")
  * [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.portfolio.trades.Trades.plots")
  * [Ranges.avg_duration()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.avg_duration "vectorbt.portfolio.trades.Trades.avg_duration")
  * [Ranges.coverage()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.coverage "vectorbt.portfolio.trades.Trades.coverage")
  * [Ranges.max_duration()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.max_duration "vectorbt.portfolio.trades.Trades.max_duration")
  * [Ranges.to_mask()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.to_mask "vectorbt.portfolio.trades.Trades.to_mask")
  * [Records.apply()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.apply "vectorbt.portfolio.trades.Trades.apply")
  * [Records.apply_mask()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.apply_mask "vectorbt.portfolio.trades.Trades.apply_mask")
  * [Records.build_field_config_doc()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.build_field_config_doc "vectorbt.portfolio.trades.Trades.build_field_config_doc")
  * [Records.count()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.count "vectorbt.portfolio.trades.Trades.count")
  * [Records.get_apply_mapping_arr()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_apply_mapping_arr "vectorbt.portfolio.trades.Trades.get_apply_mapping_arr")
  * [Records.get_by_col_idxs()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_by_col_idxs "vectorbt.portfolio.trades.Trades.get_by_col_idxs")
  * [Records.get_field_arr()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_arr "vectorbt.portfolio.trades.Trades.get_field_arr")
  * [Records.get_field_mapping()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_mapping "vectorbt.portfolio.trades.Trades.get_field_mapping")
  * [Records.get_field_name()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_name "vectorbt.portfolio.trades.Trades.get_field_name")
  * [Records.get_field_setting()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_setting "vectorbt.portfolio.trades.Trades.get_field_setting")
  * [Records.get_field_title()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_title "vectorbt.portfolio.trades.Trades.get_field_title")
  * [Records.get_map_field()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_map_field "vectorbt.portfolio.trades.Trades.get_map_field")
  * [Records.get_map_field_to_index()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_map_field_to_index "vectorbt.portfolio.trades.Trades.get_map_field_to_index")
  * [Records.indexing_func_meta()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.indexing_func_meta "vectorbt.portfolio.trades.Trades.indexing_func_meta")
  * [Records.is_sorted()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.is_sorted "vectorbt.portfolio.trades.Trades.is_sorted")
  * [Records.map()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map "vectorbt.portfolio.trades.Trades.map")
  * [Records.map_array()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map_array "vectorbt.portfolio.trades.Trades.map_array")
  * [Records.map_field()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map_field "vectorbt.portfolio.trades.Trades.map_field")
  * [Records.override_field_config_doc()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.override_field_config_doc "vectorbt.portfolio.trades.Trades.override_field_config_doc")
  * [Records.replace()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.replace "vectorbt.portfolio.trades.Trades.replace")
  * [Records.sort()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.sort "vectorbt.portfolio.trades.Trades.sort")
  * [RecordsWithFields.field_config](https://vectorbt.dev/api/records/base/#vectorbt.records.base.RecordsWithFields.field_config "vectorbt.records.base.RecordsWithFields.field_config")
  * [StatsBuilderMixin.build_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbt.portfolio.trades.Trades.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbt.portfolio.trades.Trades.override_metrics_doc")
  * [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.portfolio.trades.Trades.stats")
  * [Trades.close](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.close "vectorbt.portfolio.trades.Trades.close")
  * [Trades.closed](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.closed "vectorbt.portfolio.trades.Trades.closed")
  * [Trades.col](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.col "vectorbt.portfolio.trades.Trades.col")
  * [Trades.col_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.col_arr "vectorbt.portfolio.trades.Trades.col_arr")
  * [Trades.col_mapper](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.col_mapper "vectorbt.portfolio.trades.Trades.col_mapper")
  * [Trades.config](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.config "vectorbt.portfolio.trades.Trades.config")
  * [Trades.direction](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.direction "vectorbt.portfolio.trades.Trades.direction")
  * [Trades.duration](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.duration "vectorbt.portfolio.trades.Trades.duration")
  * [Trades.end_idx](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.end_idx "vectorbt.portfolio.trades.Trades.end_idx")
  * [Trades.entry_fees](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.entry_fees "vectorbt.portfolio.trades.Trades.entry_fees")
  * [Trades.entry_idx](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.entry_idx "vectorbt.portfolio.trades.Trades.entry_idx")
  * [Trades.entry_price](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.entry_price "vectorbt.portfolio.trades.Trades.entry_price")
  * [Trades.exit_fees](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.exit_fees "vectorbt.portfolio.trades.Trades.exit_fees")
  * [Trades.exit_idx](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.exit_idx "vectorbt.portfolio.trades.Trades.exit_idx")
  * [Trades.exit_price](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.exit_price "vectorbt.portfolio.trades.Trades.exit_price")
  * [Trades.expectancy()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.expectancy "vectorbt.portfolio.trades.Trades.expectancy")
  * [Trades.from_ts()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.from_ts "vectorbt.portfolio.trades.Trades.from_ts")
  * [Trades.id](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.id "vectorbt.portfolio.trades.Trades.id")
  * [Trades.id_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.id_arr "vectorbt.portfolio.trades.Trades.id_arr")
  * [Trades.idx_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.idx_arr "vectorbt.portfolio.trades.Trades.idx_arr")
  * [Trades.iloc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.iloc "vectorbt.portfolio.trades.Trades.iloc")
  * [Trades.indexing_func()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.indexing_func "vectorbt.portfolio.trades.Trades.indexing_func")
  * [Trades.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.indexing_kwargs "vectorbt.portfolio.trades.Trades.indexing_kwargs")
  * [Trades.loc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.loc "vectorbt.portfolio.trades.Trades.loc")
  * [Trades.long](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.long "vectorbt.portfolio.trades.Trades.long")
  * [Trades.losing](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.losing "vectorbt.portfolio.trades.Trades.losing")
  * [Trades.losing_streak](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.losing_streak "vectorbt.portfolio.trades.Trades.losing_streak")
  * [Trades.open](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.open "vectorbt.portfolio.trades.Trades.open")
  * [Trades.parent_id](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.parent_id "vectorbt.portfolio.trades.Trades.parent_id")
  * [Trades.plot()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.plot "vectorbt.portfolio.trades.Trades.plot")
  * [Trades.plot_pnl()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.plot_pnl "vectorbt.portfolio.trades.Trades.plot_pnl")
  * [Trades.plots_defaults](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.plots_defaults "vectorbt.portfolio.trades.Trades.plots_defaults")
  * [Trades.pnl](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.pnl "vectorbt.portfolio.trades.Trades.pnl")
  * [Trades.profit_factor()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.profit_factor "vectorbt.portfolio.trades.Trades.profit_factor")
  * [Trades.records](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records "vectorbt.portfolio.trades.Trades.records")
  * [Trades.records_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records_arr "vectorbt.portfolio.trades.Trades.records_arr")
  * [Trades.records_readable](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records_readable "vectorbt.portfolio.trades.Trades.records_readable")
  * [Trades.returns](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.returns "vectorbt.portfolio.trades.Trades.returns")
  * [Trades.self_aliases](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.self_aliases "vectorbt.portfolio.trades.Trades.self_aliases")
  * [Trades.short](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.short "vectorbt.portfolio.trades.Trades.short")
  * [Trades.size](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.size "vectorbt.portfolio.trades.Trades.size")
  * [Trades.sqn()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.sqn "vectorbt.portfolio.trades.Trades.sqn")
  * [Trades.start_idx](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.start_idx "vectorbt.portfolio.trades.Trades.start_idx")
  * [Trades.stats_defaults](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.stats_defaults "vectorbt.portfolio.trades.Trades.stats_defaults")
  * [Trades.status](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.status "vectorbt.portfolio.trades.Trades.status")
  * [Trades.ts](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.ts "vectorbt.portfolio.trades.Trades.ts")
  * [Trades.values](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.values "vectorbt.portfolio.trades.Trades.values")
  * [Trades.win_rate()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.win_rate "vectorbt.portfolio.trades.Trades.win_rate")
  * [Trades.winning](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.winning "vectorbt.portfolio.trades.Trades.winning")
  * [Trades.winning_streak](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.winning_streak "vectorbt.portfolio.trades.Trades.winning_streak")
  * [Trades.wrapper](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.wrapper "vectorbt.portfolio.trades.Trades.wrapper")
  * [Trades.writeable_attrs](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.writeable_attrs "vectorbt.portfolio.trades.Trades.writeable_attrs")
  * [Wrapping.regroup()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.regroup "vectorbt.portfolio.trades.Trades.regroup")
  * [Wrapping.resolve_self()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.resolve_self "vectorbt.portfolio.trades.Trades.resolve_self")
  * [Wrapping.select_one()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one "vectorbt.portfolio.trades.Trades.select_one")
  * [Wrapping.select_one_from_obj()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one_from_obj "vectorbt.portfolio.trades.Trades.select_one_from_obj")



* * *

### from_orders class method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L1537-L1551 "Jump to source")¶
    
    
    ExitTrades.from_orders(
        orders,
        close=None,
        attach_close=True,
        **kwargs
    )
    

Build [ExitTrades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.ExitTrades "vectorbt.portfolio.trades.ExitTrades") from [Orders](https://vectorbt.dev/api/portfolio/orders/#vectorbt.portfolio.orders.Orders "vectorbt.portfolio.orders.Orders").

* * *

## Positions class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L1583-L1601 "Jump to source")¶
    
    
    Positions(
        wrapper,
        records_arr,
        close,
        **kwargs
    )
    

Extends [Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades "vectorbt.portfolio.trades.Trades") for working with position records.

**Superclasses**

  * [AttrResolver](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver "vectorbt.utils.attr_.AttrResolver")
  * [Configured](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured "vectorbt.utils.config.Configured")
  * [Documented](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented "vectorbt.utils.docs.Documented")
  * [IndexingBase](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.IndexingBase "vectorbt.base.indexing.IndexingBase")
  * [PandasIndexer](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer "vectorbt.base.indexing.PandasIndexer")
  * [Pickleable](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable "vectorbt.utils.config.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin "vectorbt.generic.plots_builder.PlotsBuilderMixin")
  * [Ranges](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges "vectorbt.generic.ranges.Ranges")
  * [Records](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records "vectorbt.records.base.Records")
  * [RecordsWithFields](https://vectorbt.dev/api/records/base/#vectorbt.records.base.RecordsWithFields "vectorbt.records.base.RecordsWithFields")
  * [StatsBuilderMixin](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin "vectorbt.generic.stats_builder.StatsBuilderMixin")
  * [Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades "vectorbt.portfolio.trades.Trades")
  * [Wrapping](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping "vectorbt.base.array_wrapper.Wrapping")



**Inherited members**

  * [AttrResolver.deep_getattr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.deep_getattr "vectorbt.portfolio.trades.Trades.deep_getattr")
  * [AttrResolver.post_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.post_resolve_attr "vectorbt.portfolio.trades.Trades.post_resolve_attr")
  * [AttrResolver.pre_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.pre_resolve_attr "vectorbt.portfolio.trades.Trades.pre_resolve_attr")
  * [AttrResolver.resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.resolve_attr "vectorbt.portfolio.trades.Trades.resolve_attr")
  * [Configured.copy()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.copy "vectorbt.portfolio.trades.Trades.copy")
  * [Configured.dumps()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.dumps "vectorbt.portfolio.trades.Trades.dumps")
  * [Configured.loads()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.loads "vectorbt.portfolio.trades.Trades.loads")
  * [Configured.to_doc()](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented.to_doc "vectorbt.portfolio.trades.Trades.to_doc")
  * [Configured.update_config()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.update_config "vectorbt.portfolio.trades.Trades.update_config")
  * [PandasIndexer.xs()](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.xs "vectorbt.portfolio.trades.Trades.xs")
  * [Pickleable.load()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.load "vectorbt.portfolio.trades.Trades.load")
  * [Pickleable.save()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.save "vectorbt.portfolio.trades.Trades.save")
  * [PlotsBuilderMixin.build_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbt.portfolio.trades.Trades.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbt.portfolio.trades.Trades.override_subplots_doc")
  * [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.portfolio.trades.Trades.plots")
  * [Ranges.avg_duration()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.avg_duration "vectorbt.portfolio.trades.Trades.avg_duration")
  * [Ranges.coverage()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.coverage "vectorbt.portfolio.trades.Trades.coverage")
  * [Ranges.max_duration()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.max_duration "vectorbt.portfolio.trades.Trades.max_duration")
  * [Ranges.to_mask()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.to_mask "vectorbt.portfolio.trades.Trades.to_mask")
  * [Records.apply()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.apply "vectorbt.portfolio.trades.Trades.apply")
  * [Records.apply_mask()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.apply_mask "vectorbt.portfolio.trades.Trades.apply_mask")
  * [Records.build_field_config_doc()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.build_field_config_doc "vectorbt.portfolio.trades.Trades.build_field_config_doc")
  * [Records.count()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.count "vectorbt.portfolio.trades.Trades.count")
  * [Records.get_apply_mapping_arr()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_apply_mapping_arr "vectorbt.portfolio.trades.Trades.get_apply_mapping_arr")
  * [Records.get_by_col_idxs()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_by_col_idxs "vectorbt.portfolio.trades.Trades.get_by_col_idxs")
  * [Records.get_field_arr()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_arr "vectorbt.portfolio.trades.Trades.get_field_arr")
  * [Records.get_field_mapping()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_mapping "vectorbt.portfolio.trades.Trades.get_field_mapping")
  * [Records.get_field_name()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_name "vectorbt.portfolio.trades.Trades.get_field_name")
  * [Records.get_field_setting()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_setting "vectorbt.portfolio.trades.Trades.get_field_setting")
  * [Records.get_field_title()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_title "vectorbt.portfolio.trades.Trades.get_field_title")
  * [Records.get_map_field()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_map_field "vectorbt.portfolio.trades.Trades.get_map_field")
  * [Records.get_map_field_to_index()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_map_field_to_index "vectorbt.portfolio.trades.Trades.get_map_field_to_index")
  * [Records.indexing_func_meta()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.indexing_func_meta "vectorbt.portfolio.trades.Trades.indexing_func_meta")
  * [Records.is_sorted()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.is_sorted "vectorbt.portfolio.trades.Trades.is_sorted")
  * [Records.map()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map "vectorbt.portfolio.trades.Trades.map")
  * [Records.map_array()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map_array "vectorbt.portfolio.trades.Trades.map_array")
  * [Records.map_field()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map_field "vectorbt.portfolio.trades.Trades.map_field")
  * [Records.override_field_config_doc()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.override_field_config_doc "vectorbt.portfolio.trades.Trades.override_field_config_doc")
  * [Records.replace()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.replace "vectorbt.portfolio.trades.Trades.replace")
  * [Records.sort()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.sort "vectorbt.portfolio.trades.Trades.sort")
  * [RecordsWithFields.field_config](https://vectorbt.dev/api/records/base/#vectorbt.records.base.RecordsWithFields.field_config "vectorbt.records.base.RecordsWithFields.field_config")
  * [StatsBuilderMixin.build_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbt.portfolio.trades.Trades.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbt.portfolio.trades.Trades.override_metrics_doc")
  * [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.portfolio.trades.Trades.stats")
  * [Trades.close](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.close "vectorbt.portfolio.trades.Trades.close")
  * [Trades.closed](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.closed "vectorbt.portfolio.trades.Trades.closed")
  * [Trades.col](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.col "vectorbt.portfolio.trades.Trades.col")
  * [Trades.col_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.col_arr "vectorbt.portfolio.trades.Trades.col_arr")
  * [Trades.col_mapper](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.col_mapper "vectorbt.portfolio.trades.Trades.col_mapper")
  * [Trades.config](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.config "vectorbt.portfolio.trades.Trades.config")
  * [Trades.direction](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.direction "vectorbt.portfolio.trades.Trades.direction")
  * [Trades.duration](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.duration "vectorbt.portfolio.trades.Trades.duration")
  * [Trades.end_idx](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.end_idx "vectorbt.portfolio.trades.Trades.end_idx")
  * [Trades.entry_fees](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.entry_fees "vectorbt.portfolio.trades.Trades.entry_fees")
  * [Trades.entry_idx](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.entry_idx "vectorbt.portfolio.trades.Trades.entry_idx")
  * [Trades.entry_price](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.entry_price "vectorbt.portfolio.trades.Trades.entry_price")
  * [Trades.exit_fees](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.exit_fees "vectorbt.portfolio.trades.Trades.exit_fees")
  * [Trades.exit_idx](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.exit_idx "vectorbt.portfolio.trades.Trades.exit_idx")
  * [Trades.exit_price](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.exit_price "vectorbt.portfolio.trades.Trades.exit_price")
  * [Trades.expectancy()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.expectancy "vectorbt.portfolio.trades.Trades.expectancy")
  * [Trades.from_ts()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.from_ts "vectorbt.portfolio.trades.Trades.from_ts")
  * [Trades.id](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.id "vectorbt.portfolio.trades.Trades.id")
  * [Trades.id_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.id_arr "vectorbt.portfolio.trades.Trades.id_arr")
  * [Trades.idx_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.idx_arr "vectorbt.portfolio.trades.Trades.idx_arr")
  * [Trades.iloc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.iloc "vectorbt.portfolio.trades.Trades.iloc")
  * [Trades.indexing_func()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.indexing_func "vectorbt.portfolio.trades.Trades.indexing_func")
  * [Trades.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.indexing_kwargs "vectorbt.portfolio.trades.Trades.indexing_kwargs")
  * [Trades.loc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.loc "vectorbt.portfolio.trades.Trades.loc")
  * [Trades.long](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.long "vectorbt.portfolio.trades.Trades.long")
  * [Trades.losing](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.losing "vectorbt.portfolio.trades.Trades.losing")
  * [Trades.losing_streak](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.losing_streak "vectorbt.portfolio.trades.Trades.losing_streak")
  * [Trades.open](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.open "vectorbt.portfolio.trades.Trades.open")
  * [Trades.parent_id](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.parent_id "vectorbt.portfolio.trades.Trades.parent_id")
  * [Trades.plot()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.plot "vectorbt.portfolio.trades.Trades.plot")
  * [Trades.plot_pnl()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.plot_pnl "vectorbt.portfolio.trades.Trades.plot_pnl")
  * [Trades.plots_defaults](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.plots_defaults "vectorbt.portfolio.trades.Trades.plots_defaults")
  * [Trades.pnl](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.pnl "vectorbt.portfolio.trades.Trades.pnl")
  * [Trades.profit_factor()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.profit_factor "vectorbt.portfolio.trades.Trades.profit_factor")
  * [Trades.records](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records "vectorbt.portfolio.trades.Trades.records")
  * [Trades.records_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records_arr "vectorbt.portfolio.trades.Trades.records_arr")
  * [Trades.records_readable](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records_readable "vectorbt.portfolio.trades.Trades.records_readable")
  * [Trades.returns](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.returns "vectorbt.portfolio.trades.Trades.returns")
  * [Trades.self_aliases](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.self_aliases "vectorbt.portfolio.trades.Trades.self_aliases")
  * [Trades.short](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.short "vectorbt.portfolio.trades.Trades.short")
  * [Trades.size](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.size "vectorbt.portfolio.trades.Trades.size")
  * [Trades.sqn()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.sqn "vectorbt.portfolio.trades.Trades.sqn")
  * [Trades.start_idx](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.start_idx "vectorbt.portfolio.trades.Trades.start_idx")
  * [Trades.stats_defaults](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.stats_defaults "vectorbt.portfolio.trades.Trades.stats_defaults")
  * [Trades.status](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.status "vectorbt.portfolio.trades.Trades.status")
  * [Trades.ts](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.ts "vectorbt.portfolio.trades.Trades.ts")
  * [Trades.values](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.values "vectorbt.portfolio.trades.Trades.values")
  * [Trades.win_rate()](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.win_rate "vectorbt.portfolio.trades.Trades.win_rate")
  * [Trades.winning](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.winning "vectorbt.portfolio.trades.Trades.winning")
  * [Trades.winning_streak](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.winning_streak "vectorbt.portfolio.trades.Trades.winning_streak")
  * [Trades.wrapper](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.wrapper "vectorbt.portfolio.trades.Trades.wrapper")
  * [Trades.writeable_attrs](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.writeable_attrs "vectorbt.portfolio.trades.Trades.writeable_attrs")
  * [Wrapping.regroup()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.regroup "vectorbt.portfolio.trades.Trades.regroup")
  * [Wrapping.resolve_self()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.resolve_self "vectorbt.portfolio.trades.Trades.resolve_self")
  * [Wrapping.select_one()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one "vectorbt.portfolio.trades.Trades.select_one")
  * [Wrapping.select_one_from_obj()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one_from_obj "vectorbt.portfolio.trades.Trades.select_one_from_obj")



* * *

### from_trades class method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L1591-L1601 "Jump to source")¶
    
    
    Positions.from_trades(
        trades,
        close=None,
        attach_close=True,
        **kwargs
    )
    

Build [Positions](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Positions "vectorbt.portfolio.trades.Positions") from [Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades "vectorbt.portfolio.trades.Trades").

* * *

## Trades class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L605-L1452 "Jump to source")¶
    
    
    Trades(
        wrapper,
        records_arr,
        close,
        **kwargs
    )
    

Extends [Ranges](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges "vectorbt.generic.ranges.Ranges") for working with trade-like records, such as entry trades, exit trades, and positions.

**Superclasses**

  * [AttrResolver](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver "vectorbt.utils.attr_.AttrResolver")
  * [Configured](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured "vectorbt.utils.config.Configured")
  * [Documented](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented "vectorbt.utils.docs.Documented")
  * [IndexingBase](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.IndexingBase "vectorbt.base.indexing.IndexingBase")
  * [PandasIndexer](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer "vectorbt.base.indexing.PandasIndexer")
  * [Pickleable](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable "vectorbt.utils.config.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin "vectorbt.generic.plots_builder.PlotsBuilderMixin")
  * [Ranges](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges "vectorbt.generic.ranges.Ranges")
  * [Records](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records "vectorbt.records.base.Records")
  * [RecordsWithFields](https://vectorbt.dev/api/records/base/#vectorbt.records.base.RecordsWithFields "vectorbt.records.base.RecordsWithFields")
  * [StatsBuilderMixin](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin "vectorbt.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping "vectorbt.base.array_wrapper.Wrapping")



**Inherited members**

  * [AttrResolver.deep_getattr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.deep_getattr "vectorbt.generic.ranges.Ranges.deep_getattr")
  * [AttrResolver.post_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.post_resolve_attr "vectorbt.generic.ranges.Ranges.post_resolve_attr")
  * [AttrResolver.pre_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.pre_resolve_attr "vectorbt.generic.ranges.Ranges.pre_resolve_attr")
  * [AttrResolver.resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.resolve_attr "vectorbt.generic.ranges.Ranges.resolve_attr")
  * [Configured.copy()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.copy "vectorbt.generic.ranges.Ranges.copy")
  * [Configured.dumps()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.dumps "vectorbt.generic.ranges.Ranges.dumps")
  * [Configured.loads()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.loads "vectorbt.generic.ranges.Ranges.loads")
  * [Configured.to_doc()](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented.to_doc "vectorbt.generic.ranges.Ranges.to_doc")
  * [Configured.update_config()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.update_config "vectorbt.generic.ranges.Ranges.update_config")
  * [PandasIndexer.xs()](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.xs "vectorbt.generic.ranges.Ranges.xs")
  * [Pickleable.load()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.load "vectorbt.generic.ranges.Ranges.load")
  * [Pickleable.save()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.save "vectorbt.generic.ranges.Ranges.save")
  * [PlotsBuilderMixin.build_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbt.generic.ranges.Ranges.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbt.generic.ranges.Ranges.override_subplots_doc")
  * [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.generic.ranges.Ranges.plots")
  * [Ranges.avg_duration()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.avg_duration "vectorbt.generic.ranges.Ranges.avg_duration")
  * [Ranges.closed](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.closed "vectorbt.generic.ranges.Ranges.closed")
  * [Ranges.col](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.col "vectorbt.generic.ranges.Ranges.col")
  * [Ranges.col_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.col_arr "vectorbt.generic.ranges.Ranges.col_arr")
  * [Ranges.col_mapper](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.col_mapper "vectorbt.generic.ranges.Ranges.col_mapper")
  * [Ranges.config](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.config "vectorbt.generic.ranges.Ranges.config")
  * [Ranges.coverage()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.coverage "vectorbt.generic.ranges.Ranges.coverage")
  * [Ranges.duration](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.duration "vectorbt.generic.ranges.Ranges.duration")
  * [Ranges.end_idx](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.end_idx "vectorbt.generic.ranges.Ranges.end_idx")
  * [Ranges.from_ts()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.from_ts "vectorbt.generic.ranges.Ranges.from_ts")
  * [Ranges.id](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.id "vectorbt.generic.ranges.Ranges.id")
  * [Ranges.id_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.id_arr "vectorbt.generic.ranges.Ranges.id_arr")
  * [Ranges.idx_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.idx_arr "vectorbt.generic.ranges.Ranges.idx_arr")
  * [Ranges.iloc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.iloc "vectorbt.generic.ranges.Ranges.iloc")
  * [Ranges.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.indexing_kwargs "vectorbt.generic.ranges.Ranges.indexing_kwargs")
  * [Ranges.loc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.loc "vectorbt.generic.ranges.Ranges.loc")
  * [Ranges.max_duration()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.max_duration "vectorbt.generic.ranges.Ranges.max_duration")
  * [Ranges.open](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.open "vectorbt.generic.ranges.Ranges.open")
  * [Ranges.records](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records "vectorbt.generic.ranges.Ranges.records")
  * [Ranges.records_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records_arr "vectorbt.generic.ranges.Ranges.records_arr")
  * [Ranges.records_readable](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records_readable "vectorbt.generic.ranges.Ranges.records_readable")
  * [Ranges.self_aliases](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.self_aliases "vectorbt.generic.ranges.Ranges.self_aliases")
  * [Ranges.start_idx](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.start_idx "vectorbt.generic.ranges.Ranges.start_idx")
  * [Ranges.status](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.status "vectorbt.generic.ranges.Ranges.status")
  * [Ranges.to_mask()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.to_mask "vectorbt.generic.ranges.Ranges.to_mask")
  * [Ranges.ts](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.ts "vectorbt.generic.ranges.Ranges.ts")
  * [Ranges.values](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.values "vectorbt.generic.ranges.Ranges.values")
  * [Ranges.wrapper](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.wrapper "vectorbt.generic.ranges.Ranges.wrapper")
  * [Ranges.writeable_attrs](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.writeable_attrs "vectorbt.generic.ranges.Ranges.writeable_attrs")
  * [Records.apply()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.apply "vectorbt.generic.ranges.Ranges.apply")
  * [Records.apply_mask()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.apply_mask "vectorbt.generic.ranges.Ranges.apply_mask")
  * [Records.build_field_config_doc()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.build_field_config_doc "vectorbt.generic.ranges.Ranges.build_field_config_doc")
  * [Records.count()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.count "vectorbt.generic.ranges.Ranges.count")
  * [Records.get_apply_mapping_arr()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_apply_mapping_arr "vectorbt.generic.ranges.Ranges.get_apply_mapping_arr")
  * [Records.get_by_col_idxs()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_by_col_idxs "vectorbt.generic.ranges.Ranges.get_by_col_idxs")
  * [Records.get_field_arr()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_arr "vectorbt.generic.ranges.Ranges.get_field_arr")
  * [Records.get_field_mapping()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_mapping "vectorbt.generic.ranges.Ranges.get_field_mapping")
  * [Records.get_field_name()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_name "vectorbt.generic.ranges.Ranges.get_field_name")
  * [Records.get_field_setting()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_setting "vectorbt.generic.ranges.Ranges.get_field_setting")
  * [Records.get_field_title()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_title "vectorbt.generic.ranges.Ranges.get_field_title")
  * [Records.get_map_field()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_map_field "vectorbt.generic.ranges.Ranges.get_map_field")
  * [Records.get_map_field_to_index()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_map_field_to_index "vectorbt.generic.ranges.Ranges.get_map_field_to_index")
  * [Records.indexing_func_meta()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.indexing_func_meta "vectorbt.generic.ranges.Ranges.indexing_func_meta")
  * [Records.is_sorted()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.is_sorted "vectorbt.generic.ranges.Ranges.is_sorted")
  * [Records.map()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map "vectorbt.generic.ranges.Ranges.map")
  * [Records.map_array()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map_array "vectorbt.generic.ranges.Ranges.map_array")
  * [Records.map_field()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map_field "vectorbt.generic.ranges.Ranges.map_field")
  * [Records.override_field_config_doc()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.override_field_config_doc "vectorbt.generic.ranges.Ranges.override_field_config_doc")
  * [Records.replace()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.replace "vectorbt.generic.ranges.Ranges.replace")
  * [Records.sort()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.sort "vectorbt.generic.ranges.Ranges.sort")
  * [StatsBuilderMixin.build_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbt.generic.ranges.Ranges.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbt.generic.ranges.Ranges.override_metrics_doc")
  * [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.generic.ranges.Ranges.stats")
  * [Wrapping.regroup()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.regroup "vectorbt.generic.ranges.Ranges.regroup")
  * [Wrapping.resolve_self()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.resolve_self "vectorbt.generic.ranges.Ranges.resolve_self")
  * [Wrapping.select_one()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one "vectorbt.generic.ranges.Ranges.select_one")
  * [Wrapping.select_one_from_obj()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one_from_obj "vectorbt.generic.ranges.Ranges.select_one_from_obj")



**Subclasses**

  * [EntryTrades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.EntryTrades "vectorbt.portfolio.trades.EntryTrades")
  * [ExitTrades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.ExitTrades "vectorbt.portfolio.trades.ExitTrades")
  * [Positions](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Positions "vectorbt.portfolio.trades.Positions")



* * *

### close property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L643-L646 "Jump to source")¶

Reference price such as close (optional).

* * *

### direction method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `direction`.

* * *

### entry_fees method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `entry_fees`.

* * *

### entry_idx method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `entry_idx`.

* * *

### entry_price method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `entry_price`.

* * *

### exit_fees method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `exit_fees`.

* * *

### exit_idx method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `exit_idx`.

* * *

### exit_price method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `exit_price`.

* * *

### expectancy method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L706-L721 "Jump to source")¶
    
    
    Trades.expectancy(
        group_by=None,
        wrap_kwargs=None
    )
    

Average profitability.

* * *

### field_config class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py "Jump to source")¶

Field config of [Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades "vectorbt.portfolio.trades.Trades").
    
    
    Config({
        "dtype": {
            "id": "int64",
            "col": "int64",
            "size": "float64",
            "entry_idx": "int64",
            "entry_price": "float64",
            "entry_fees": "float64",
            "exit_idx": "int64",
            "exit_price": "float64",
            "exit_fees": "float64",
            "pnl": "float64",
            "return": "float64",
            "direction": "int64",
            "status": "int64",
            "parent_id": "int64"
        },
        "settings": {
            "id": {
                "name": "id",
                "title": "Trade Id"
            },
            "col": {
                "name": "col",
                "title": "Column",
                "mapping": "columns"
            },
            "idx": {
                "name": "exit_idx",
                "title": "Timestamp",
                "mapping": "index"
            },
            "start_idx": {
                "title": "Start Timestamp",
                "mapping": "index",
                "name": "entry_idx"
            },
            "end_idx": {
                "title": "End Timestamp",
                "mapping": "index",
                "name": "exit_idx"
            },
            "status": {
                "title": "Status",
                "mapping": {
                    "Open": 0,
                    "Closed": 1
                }
            },
            "size": {
                "title": "Size"
            },
            "entry_idx": {
                "title": "Entry Timestamp",
                "mapping": "index"
            },
            "entry_price": {
                "title": "Avg Entry Price"
            },
            "entry_fees": {
                "title": "Entry Fees"
            },
            "exit_idx": {
                "title": "Exit Timestamp",
                "mapping": "index"
            },
            "exit_price": {
                "title": "Avg Exit Price"
            },
            "exit_fees": {
                "title": "Exit Fees"
            },
            "pnl": {
                "title": "PnL"
            },
            "return": {
                "title": "Return"
            },
            "direction": {
                "title": "Direction",
                "mapping": {
                    "Long": 0,
                    "Short": 1
                }
            },
            "parent_id": {
                "title": "Position Id"
            }
        }
    })
    

* * *

### indexing_func method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L629-L641 "Jump to source")¶
    
    
    Trades.indexing_func(
        pd_indexing_func,
        **kwargs
    )
    

Perform indexing on [Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades "vectorbt.portfolio.trades.Trades").

* * *

### long method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Records filtered by `direction == 0`.

* * *

### losing method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Losing trades.

* * *

### losing_streak method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Losing streak at each trade in the current column.

See [trade_losing_streak_nb()](https://vectorbt.dev/api/portfolio/nb/#vectorbt.portfolio.nb.trade_losing_streak_nb "vectorbt.portfolio.nb.trade_losing_streak_nb").

* * *

### metrics class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py "Jump to source")¶

Metrics supported by [Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades "vectorbt.portfolio.trades.Trades").
    
    
    Config({
        "start": {
            "title": "Start",
            "calc_func": "<function Trades.<lambda> at 0x7f957f5d7880>",
            "agg_func": null,
            "tags": "wrapper"
        },
        "end": {
            "title": "End",
            "calc_func": "<function Trades.<lambda> at 0x7f957f5d7920>",
            "agg_func": null,
            "tags": "wrapper"
        },
        "period": {
            "title": "Period",
            "calc_func": "<function Trades.<lambda> at 0x7f957f5d79c0>",
            "apply_to_timedelta": true,
            "agg_func": null,
            "tags": "wrapper"
        },
        "first_trade_start": {
            "title": "First Trade Start",
            "calc_func": "entry_idx.nth",
            "n": 0,
            "wrap_kwargs": {
                "to_index": true
            },
            "tags": [
                "trades",
                "index"
            ]
        },
        "last_trade_end": {
            "title": "Last Trade End",
            "calc_func": "exit_idx.nth",
            "n": -1,
            "wrap_kwargs": {
                "to_index": true
            },
            "tags": [
                "trades",
                "index"
            ]
        },
        "coverage": {
            "title": "Coverage",
            "calc_func": "coverage",
            "overlapping": false,
            "normalize": false,
            "apply_to_timedelta": true,
            "tags": [
                "ranges",
                "coverage"
            ]
        },
        "overlap_coverage": {
            "title": "Overlap Coverage",
            "calc_func": "coverage",
            "overlapping": true,
            "normalize": false,
            "apply_to_timedelta": true,
            "tags": [
                "ranges",
                "coverage"
            ]
        },
        "total_records": {
            "title": "Total Records",
            "calc_func": "count",
            "tags": "records"
        },
        "total_long_trades": {
            "title": "Total Long Trades",
            "calc_func": "long.count",
            "tags": [
                "trades",
                "long"
            ]
        },
        "total_short_trades": {
            "title": "Total Short Trades",
            "calc_func": "short.count",
            "tags": [
                "trades",
                "short"
            ]
        },
        "total_closed_trades": {
            "title": "Total Closed Trades",
            "calc_func": "closed.count",
            "tags": [
                "trades",
                "closed"
            ]
        },
        "total_open_trades": {
            "title": "Total Open Trades",
            "calc_func": "open.count",
            "tags": [
                "trades",
                "open"
            ]
        },
        "open_trade_pnl": {
            "title": "Open Trade PnL",
            "calc_func": "open.pnl.sum",
            "tags": [
                "trades",
                "open"
            ]
        },
        "win_rate": {
            "title": "Win Rate [%]",
            "calc_func": "closed.win_rate",
            "post_calc_func": "<function Trades.<lambda> at 0x7f957f5d7a60>",
            "tags": "RepEval(expression=\"['trades', *incl_open_tags]\", mapping={})"
        },
        "winning_streak": {
            "title": "Max Win Streak",
            "calc_func": "RepEval(expression=\"'winning_streak.max' if incl_open else 'closed.winning_streak.max'\", mapping={})",
            "wrap_kwargs": {
                "dtype": "Int64"
            },
            "tags": "RepEval(expression=\"['trades', *incl_open_tags, 'streak']\", mapping={})"
        },
        "losing_streak": {
            "title": "Max Loss Streak",
            "calc_func": "RepEval(expression=\"'losing_streak.max' if incl_open else 'closed.losing_streak.max'\", mapping={})",
            "wrap_kwargs": {
                "dtype": "Int64"
            },
            "tags": "RepEval(expression=\"['trades', *incl_open_tags, 'streak']\", mapping={})"
        },
        "best_trade": {
            "title": "Best Trade [%]",
            "calc_func": "RepEval(expression=\"'returns.max' if incl_open else 'closed.returns.max'\", mapping={})",
            "post_calc_func": "<function Trades.<lambda> at 0x7f957f5d7b00>",
            "tags": "RepEval(expression=\"['trades', *incl_open_tags]\", mapping={})"
        },
        "worst_trade": {
            "title": "Worst Trade [%]",
            "calc_func": "RepEval(expression=\"'returns.min' if incl_open else 'closed.returns.min'\", mapping={})",
            "post_calc_func": "<function Trades.<lambda> at 0x7f957f5d7ba0>",
            "tags": "RepEval(expression=\"['trades', *incl_open_tags]\", mapping={})"
        },
        "avg_winning_trade": {
            "title": "Avg Winning Trade [%]",
            "calc_func": "RepEval(expression=\"'winning.returns.mean' if incl_open else 'closed.winning.returns.mean'\", mapping={})",
            "post_calc_func": "<function Trades.<lambda> at 0x7f957f5d7c40>",
            "tags": "RepEval(expression=\"['trades', *incl_open_tags, 'winning']\", mapping={})"
        },
        "avg_losing_trade": {
            "title": "Avg Losing Trade [%]",
            "calc_func": "RepEval(expression=\"'losing.returns.mean' if incl_open else 'closed.losing.returns.mean'\", mapping={})",
            "post_calc_func": "<function Trades.<lambda> at 0x7f957f5d7ce0>",
            "tags": "RepEval(expression=\"['trades', *incl_open_tags, 'losing']\", mapping={})"
        },
        "avg_winning_trade_duration": {
            "title": "Avg Winning Trade Duration",
            "calc_func": "RepEval(expression=\"'winning.avg_duration' if incl_open else 'closed.winning.avg_duration'\", mapping={})",
            "fill_wrap_kwargs": true,
            "tags": "RepEval(expression=\"['trades', *incl_open_tags, 'winning', 'duration']\", mapping={})"
        },
        "avg_losing_trade_duration": {
            "title": "Avg Losing Trade Duration",
            "calc_func": "RepEval(expression=\"'losing.avg_duration' if incl_open else 'closed.losing.avg_duration'\", mapping={})",
            "fill_wrap_kwargs": true,
            "tags": "RepEval(expression=\"['trades', *incl_open_tags, 'losing', 'duration']\", mapping={})"
        },
        "profit_factor": {
            "title": "Profit Factor",
            "calc_func": "RepEval(expression=\"'profit_factor' if incl_open else 'closed.profit_factor'\", mapping={})",
            "tags": "RepEval(expression=\"['trades', *incl_open_tags]\", mapping={})"
        },
        "expectancy": {
            "title": "Expectancy",
            "calc_func": "RepEval(expression=\"'expectancy' if incl_open else 'closed.expectancy'\", mapping={})",
            "tags": "RepEval(expression=\"['trades', *incl_open_tags]\", mapping={})"
        },
        "sqn": {
            "title": "SQN",
            "calc_func": "RepEval(expression=\"'sqn' if incl_open else 'closed.sqn'\", mapping={})",
            "tags": "RepEval(expression=\"['trades', *incl_open_tags]\", mapping={})"
        }
    })
    

Returns `Trades._metrics`, which gets (deep) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `Trades._metrics`.

* * *

### parent_id method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `parent_id`.

* * *

### plot method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L1099-L1414 "Jump to source")¶
    
    
    Trades.plot(
        column=None,
        plot_zones=True,
        close_trace_kwargs=None,
        entry_trace_kwargs=None,
        exit_trace_kwargs=None,
        exit_profit_trace_kwargs=None,
        exit_loss_trace_kwargs=None,
        active_trace_kwargs=None,
        profit_shape_kwargs=None,
        loss_shape_kwargs=None,
        add_trace_kwargs=None,
        xref='x',
        yref='y',
        fig=None,
        **layout_kwargs
    )
    

Plot orders.

**Args**

**`column`** : `str`
    Name of the column to plot.
**`plot_zones`** : `bool`
    

Whether to plot zones.

Set to False if there are many trades within one position.

**`close_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for [Trades.close](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.close "vectorbt.portfolio.trades.Trades.close").
**`entry_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Entry" markers.
**`exit_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Exit" markers.
**`exit_profit_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Exit - Profit" markers.
**`exit_loss_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Exit - Loss" markers.
**`active_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Active" markers.
**`profit_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for profit zones.
**`loss_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for loss zones.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`xref`** : `str`
    X coordinate axis.
**`yref`** : `str`
    Y coordinate axis.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    >>> import pandas as pd
    >>> from datetime import datetime, timedelta
    >>> import vectorbt as vbt
    
    >>> price = pd.Series([1., 2., 3., 4., 3., 2., 1.], name='Price')
    >>> price.index = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(len(price))]
    >>> orders = pd.Series([1., -0.5, -0.5, 2., -0.5, -0.5, -0.5])
    >>> pf = vbt.Portfolio.from_orders(price, orders)
    >>> pf.trades.plot()
    

* * *

### plot_pnl method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L910-L1097 "Jump to source")¶
    
    
    Trades.plot_pnl(
        column=None,
        pct_scale=True,
        marker_size_range=(7, 14),
        opacity_range=(0.75, 0.9),
        closed_profit_trace_kwargs=None,
        closed_loss_trace_kwargs=None,
        open_trace_kwargs=None,
        hline_shape_kwargs=None,
        add_trace_kwargs=None,
        xref='x',
        yref='y',
        fig=None,
        **layout_kwargs
    )
    

Plot trade PnL and returns.

**Args**

**`column`** : `str`
    Name of the column to plot.
**`pct_scale`** : `bool`
    Whether to set y-axis to [Trades.returns](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.returns "vectorbt.portfolio.trades.Trades.returns"), otherwise to [Trades.pnl](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades.pnl "vectorbt.portfolio.trades.Trades.pnl").
**`marker_size_range`** : `tuple`
    Range of marker size.
**`opacity_range`** : `tuple`
    Range of marker opacity.
**`closed_profit_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Closed - Profit" markers.
**`closed_loss_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Closed - Loss" markers.
**`open_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Open" markers.
**`hline_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for zeroline.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`xref`** : `str`
    X coordinate axis.
**`yref`** : `str`
    Y coordinate axis.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    >>> import pandas as pd
    >>> from datetime import datetime, timedelta
    >>> import vectorbt as vbt
    
    >>> price = pd.Series([1., 2., 3., 4., 3., 2., 1.])
    >>> price.index = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(len(price))]
    >>> orders = pd.Series([1., -0.5, -0.5, 2., -0.5, -0.5, -0.5])
    >>> pf = vbt.Portfolio.from_orders(price, orders)
    >>> pf.trades.plot_pnl()
    

* * *

### plots_defaults property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L1416-L1428 "Jump to source")¶

Defaults for [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.portfolio.trades.Trades.plots").

Merges [Ranges.plots_defaults](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.plots_defaults "vectorbt.generic.ranges.Ranges.plots_defaults") and `trades.plots` from [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings").

* * *

### pnl method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `pnl`.

* * *

### profit_factor method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L689-L704 "Jump to source")¶
    
    
    Trades.profit_factor(
        group_by=None,
        wrap_kwargs=None
    )
    

Profit factor.

* * *

### returns method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `return`.

* * *

### short method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Records filtered by `direction == 1`.

* * *

### size method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `size`.

* * *

### sqn method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L723-L732 "Jump to source")¶
    
    
    Trades.sqn(
        group_by=None,
        wrap_kwargs=None
    )
    

System Quality Number (SQN).

* * *

### stats_defaults property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L736-L748 "Jump to source")¶

Defaults for [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.portfolio.trades.Trades.stats").

Merges [Ranges.stats_defaults](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.stats_defaults "vectorbt.generic.ranges.Ranges.stats_defaults") and `trades.stats` from [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings").

* * *

### subplots class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py "Jump to source")¶

Subplots supported by [Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades "vectorbt.portfolio.trades.Trades").
    
    
    Config({
        "plot": {
            "title": "Trades",
            "yaxis_kwargs": {
                "title": "Price"
            },
            "check_is_not_grouped": true,
            "plot_func": "plot",
            "tags": "trades"
        },
        "plot_pnl": {
            "title": "Trade PnL",
            "yaxis_kwargs": {
                "title": "Trade PnL"
            },
            "check_is_not_grouped": true,
            "plot_func": "plot_pnl",
            "tags": "trades"
        }
    })
    

Returns `Trades._subplots`, which gets (deep) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change subplots, you can either change the config in-place, override this property, or overwrite the instance variable `Trades._subplots`.

* * *

### win_rate method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/trades.py#L678-L687 "Jump to source")¶
    
    
    Trades.win_rate(
        group_by=None,
        wrap_kwargs=None
    )
    

Rate of winning trades.

* * *

### winning method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Winning trades.

* * *

### winning_streak method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Winning streak at each trade in the current column.

See [trade_winning_streak_nb()](https://vectorbt.dev/api/portfolio/nb/#vectorbt.portfolio.nb.trade_winning_streak_nb "vectorbt.portfolio.nb.trade_winning_streak_nb").

* * *

[ ](https://github.com/sponsors/polakowo "Become a sponsor")

* * *
