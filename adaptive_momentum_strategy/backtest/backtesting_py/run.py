"""Entry point for a single backtesting.py run of the Adaptive Momentum Strategy.

Usage (from project root):
    source .venv/bin/activate
    python -m adaptive_momentum_strategy.backtest.backtesting_py.run
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Allow running from project root without installing as a package.
_ROOT = Path(__file__).parents[4]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")

from adaptive_momentum_strategy.backtest.backtesting_py.runner import run_backtest

if __name__ == "__main__":
    run_backtest()
