"""Backtest config phases for Adaptive Momentum Strategy.

Each file in this package represents one phase in the standard testing pipeline.
Pass the filename (without .py) to the runner via --config:

    python -m adaptive_momentum_strategy.backtest.vectorbt.run --config phase1_broad_sweep
    python -m adaptive_momentum_strategy.backtest.vectorbt.run --config phase2_4h_cleanup
    python -m adaptive_momentum_strategy.backtest.vectorbt.run --config phase3_numeric_sweep

Standard phase progression
---------------------------
Phase 1  broad_sweep       All toggles, all timeframes, exclusive mode (isolation).
                            Goal: find which indicators have positive signal.
                            Next step: run robustness report; identify best TF and
                            which toggles hurt (negative OLS coefficient).

Phase 2  cleanup            Pin negatives OFF, pin positives ON, best TF only,
                            combination mode (exclusive=False).
                            Goal: confirm SQN lifts when bad toggles are removed.
                            Next step: if avg SQN >= 1.5, unlock numeric sweeps.

Phase 3  numeric_sweep      Same toggle config as phase 2, but sweep key numeric
                            params (e.g. cmf_threshold, chandelier_atr_mult).
                            Goal: fine-tune the surviving indicators.
                            Next step: walk-forward validation.
"""

from __future__ import annotations

import importlib
from pathlib import Path

from adaptive_momentum_strategy.backtest.config import MomentumGridConfig


def load_config(name: str, output_dir: Path | None = None) -> MomentumGridConfig:
    """Import a phase config by name and return a MomentumGridConfig.

    Parameters
    ----------
    name:
        Config module name without the .py suffix, e.g. 'phase1_broad_sweep'.
    output_dir:
        Forwarded to the config builder.
    """
    module_path = f"adaptive_momentum_strategy.backtest.configs.{name}"
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        available = [
            p.stem for p in Path(__file__).parent.glob("phase*.py")
        ]
        raise ValueError(
            f"Config '{name}' not found. Available: {available}"
        ) from exc

    build_fn = getattr(module, "build_config", None)
    if build_fn is None:
        raise AttributeError(
            f"Config module '{name}' must define a build_config(output_dir) function."
        )
    return build_fn(output_dir=output_dir)
