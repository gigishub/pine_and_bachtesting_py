"""Bear Strategy — vectorbt grid config registry.

Each .py file in this directory (except ``__init__.py`` and ``default.py``)
is a named grid config.  Pass its filename stem (without ``.py``) to the
grid runner via ``--config``:

    python -m bear_strategy.backtest.vectorbt.run_grid --config exit_isolation
    python -m bear_strategy.backtest.vectorbt.run_grid --config full_combo

Built-in named configs
----------------------
  default             — baseline single-run (fixed TP on, all others off)
  exit_isolation      — test each exit indicator alone (exit_exclusive=True)
  exit_value_sweep    — all exits on, sweep numeric params + SL/TP multiples
  regime_value_sweep  — sweep RSI bear-zone and funding guard thresholds
  full_combo          — full Cartesian: all exit flags × SL/TP multiples

Adding a new named config
-------------------------
1. Create ``configs/my_config.py``.
2. Import ``build_config`` from ``default`` for the baseline.
3. Override only what you need with ``dataclasses.replace()``.
4. Define ``build_config() -> BearGridConfig`` (same function name as default).
5. Run with ``--config my_config``.

Example skeleton
~~~~~~~~~~~~~~~~
.. code-block:: python

    import dataclasses
    from bear_strategy.backtest.vectorbt.configs.default import build_config as _base

    def build_config():
        return dataclasses.replace(
            _base(),
            symbols=["BTCUSDT", "ETHUSDT"],
            sl_mult_range=(1.5, 2.0, 2.5),
        )
"""

from __future__ import annotations

import importlib
from pathlib import Path

from bear_strategy.backtest.vectorbt.bear_grid_config import BearGridConfig

# Files that are infrastructure, not named grid configs
_SKIP = {"__init__"}


def load_config(name: str) -> BearGridConfig:
    """Import a named grid config by filename stem and return its BearGridConfig.

    Parameters
    ----------
    name:
        Module filename without ``.py``, e.g. ``"exit_isolation"`` or
        ``"full_combo"``.

    Raises
    ------
    ValueError
        If the name does not match any file in this directory.
    AttributeError
        If the module does not define ``build_config()``.
    """
    module_path = f"bear_strategy.backtest.vectorbt.configs.{name}"
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        available = [
            p.stem
            for p in Path(__file__).parent.glob("*.py")
            if p.stem not in _SKIP
        ]
        raise ValueError(
            f"Grid config '{name}' not found.  Available: {available}"
        ) from exc

    build_fn = getattr(module, "build_config", None)
    if build_fn is None:
        raise AttributeError(
            f"Config module '{name}' must define ``build_config() -> BearGridConfig``."
        )
    cfg = build_fn()
    if not isinstance(cfg, BearGridConfig):
        raise TypeError(
            f"build_config() in '{name}' must return a BearGridConfig, "
            f"got {type(cfg).__name__}"
        )
    return cfg
