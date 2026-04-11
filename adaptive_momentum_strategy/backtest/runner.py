"""Backward-compatibility shim.

The backtesting.py runner has moved to:
    adaptive_momentum_strategy.backtest.backtesting_py.runner

To run a single backtest use:
    python -m adaptive_momentum_strategy.backtest.backtesting_py.run
"""

from adaptive_momentum_strategy.backtest.backtesting_py.strategy import AdaptiveMomentumStrategy
from adaptive_momentum_strategy.backtest.backtesting_py.runner import load_data, run_backtest

__all__ = ["AdaptiveMomentumStrategy", "load_data", "run_backtest"]

if __name__ == "__main__":
    run_backtest()
