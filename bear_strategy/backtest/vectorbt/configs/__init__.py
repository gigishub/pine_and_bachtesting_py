"""Bear Strategy — vectorbt sweep config registry.

Each .py file in this directory (except ``__init__.py``, ``default.py``, and
``sweep.py``) is a self-contained named sweep.  Pass its filename (without
``.py``) to the sweep runner via ``--config``:

    python -m bear_strategy.backtest.vectorbt.sweep_run --config is_broad
    python -m bear_strategy.backtest.vectorbt.sweep_run --config oos_broad
    python -m bear_strategy.backtest.vectorbt.sweep_run --config rsi_exit_sweep

Adding a new named sweep
------------------------
1. Create a new file here, e.g. ``tight_sl_sweep.py``.
2. Import ``build_config`` from ``default.py`` for the shared baseline.
3. Only change what you need — leave everything else untouched.
4. Define ``build_sweep_config() -> SweepConfig`` and return your config.
5. Run with ``--config tight_sl_sweep``.

Example skeleton
~~~~~~~~~~~~~~~~
.. code-block:: python

    import dataclasses
    from bear_strategy.backtest.vectorbt.configs.default import build_config
    from bear_strategy.backtest.vectorbt.configs.sweep import SweepConfig

    def build_sweep_config() -> SweepConfig:
        base = build_config()
        base = dataclasses.replace(base, pairs=["BTCUSDT", "ETHUSDT"])
        return SweepConfig(
            base     = base,
            sl_mults = (1.0, 1.5, 2.0),
            tp_mults = (2.0, 3.0, 4.0),
        )
"""

from __future__ import annotations

import importlib
from pathlib import Path

from bear_strategy.backtest.vectorbt.configs.sweep import SweepConfig

# Files that are infrastructure, not named sweep configs
_SKIP = {"__init__", "default", "sweep"}


def load_sweep_config(name: str) -> SweepConfig:
    """Import a named sweep config by filename stem and return its SweepConfig.

    Parameters
    ----------
    name:
        Module filename without ``.py``, e.g. ``"is_broad"`` or
        ``"rsi_exit_sweep"``.

    Raises
    ------
    ValueError
        If the name does not match any file in this directory.
    AttributeError
        If the module does not define ``build_sweep_config()``.
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
            f"Sweep config '{name}' not found.  Available: {available}"
        ) from exc

    build_fn = getattr(module, "build_sweep_config", None)
    if build_fn is None:
        raise AttributeError(
            f"Config module '{name}' must define "
            f"``build_sweep_config() -> SweepConfig``."
        )
    return build_fn()
