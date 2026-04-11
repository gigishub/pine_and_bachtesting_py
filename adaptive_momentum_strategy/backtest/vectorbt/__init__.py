"""vectorbt engine for the Adaptive Momentum Strategy.

Entry points:
    from adaptive_momentum_strategy.backtest.vectorbt.runner import run
    from adaptive_momentum_strategy.backtest.vectorbt.run import main
"""

from .runner import run

__all__ = ["run"]
