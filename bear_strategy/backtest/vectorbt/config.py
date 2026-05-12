"""Re-export shim — canonical config lives in configs/default.py.

Per the project structure, engine-specific configs belong in
``backtest/vectorbt/configs/``.  Import from there directly or use this
module for backward compatibility.
"""

from bear_strategy.backtest.vectorbt.configs.default import (  # noqa: F401
    VbtRunConfig,
    build_config,
)
