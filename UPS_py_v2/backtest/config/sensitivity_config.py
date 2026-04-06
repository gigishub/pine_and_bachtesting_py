"""Sensitivity analysis configuration — Phase 2 of the robustness workflow.

PURPOSE
-------
Phase 1 (grid_search via simple_config.py) finds parameter combinations that
perform well across multiple markets and timeframes.

Phase 2 (sensitivity) asks: "Is that performance stable, or does it cliff-edge?"

For each top-N result from Phase 1, the sensitivity analysis:
  1. Takes the winning parameter set.
  2. Perturbs each numeric parameter by ±perturbation_pct (e.g. ±15%).
  3. Re-runs the backtest for every perturbed version.
  4. Checks whether performance degrades gradually (robust) or drops sharply
     at small perturbations (overfit / fragile).

USAGE
-----
Not yet implemented. When ready:
  python -m UPS_py_v2.backtest.backtesting_py.run_sensitivity
  python -m UPS_py_v2.backtest.vectorbt.run_sensitivity

CONFIGURATION (to fill in when implementing)
---------------------------------------------
Example fields:

    source_results_dir: Path     # output dir from a completed Phase 1 run
    top_n: int = 10              # how many Phase 1 winners to test
    perturbation_pct: float = 0.15  # ±15% around each numeric parameter
    perturbation_steps: int = 3  # e.g. -15%, 0%, +15%
    engine: str = "vbt"          # which engine to use for the sensitivity run
"""

from __future__ import annotations
