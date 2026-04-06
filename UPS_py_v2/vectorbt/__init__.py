"""UPS Strategy — vectorbt backtest engine.

This package is fully independent from UPS_py_v2.backtest.
The only shared dependencies are:
  - UPS_py_v2.strategy  (signals, indicators, risk helpers, StrategySettings)
  - UPS_py_v2.data      (data loading)

Trailing stops are not supported in this engine path.
Use UPS_py_v2.backtest for trail_stop=True.
"""
