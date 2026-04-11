"""Entry-point for the Adaptive Momentum vectorbt grid-search.

Usage (from project root):
    source .venv/bin/activate && python -m adaptive_momentum_strategy.backtest.vectorbt.run
    python -m adaptive_momentum_strategy.backtest.vectorbt.run --config phase2_4h_cleanup
    python -m adaptive_momentum_strategy.backtest.vectorbt.run --config phase3_numeric_sweep

Config phases live in backtest/configs/ — each file documents its purpose,
what to look for in the robustness report, and what the next step is.
Default: phase1_broad_sweep (backward compatible).

Results are saved to:
    adaptive_momentum_strategy/backtest/results/results_vbt/<YYYY-MM-DD_HHMM_AMS>/

One CSV per condition (symbol x timeframe), with one row per parameter combo.
Each CSV is ranked by Expectancy [%] descending.

Optional trade logs (top-5 combos per condition):
    adaptive_momentum_strategy/backtest/results/results_vbt/<run>/trades/
"""

from __future__ import annotations

import logging
import sys
from math import prod
from pathlib import Path

# Allow running from project root without installing as a package.
_ROOT = Path(__file__).parents[4]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from adaptive_momentum_strategy.backtest.configs import load_config
from adaptive_momentum_strategy.backtest.reporting.output import build_output_dir
from adaptive_momentum_strategy.backtest.vectorbt.sequencer import run_sequential
from adaptive_momentum_strategy.backtest.vectorbt.pipeline import build_parameter_grid

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Adaptive Momentum vectorbt grid-search.")
    parser.add_argument(
        "--config",
        default="phase1_broad_sweep",
        help="Config phase to run (e.g. phase1_broad_sweep, phase2_4h_cleanup, phase3_numeric_sweep).",
    )
    args, _ = parser.parse_known_args()

    print(f"Adaptive Momentum -- initializing (config: {args.config}, loading libraries, this may take ~30s)...")
    output_dir = build_output_dir("AMS")
    config = load_config(args.config, output_dir=output_dir)

    log_path = output_dir / "run_vbt.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_path, mode="a"),
        ],
    )

    datasets = config.build_datasets()

    # Total combos before invalid-combo filtering
    total_combos = prod(len(r) for r in config.parameter_ranges.values()) if config.parameter_ranges else 1

    # Valid combos after filtering (computed once here for the display)
    baseline_params = config.build_baseline_params()
    valid_grid = build_parameter_grid(baseline_params, config)

    # Flags included in the sweep (range has > 1 value)
    swept_flags = [
        name
        for name, rng in config.boolean_filter_ranges.items()
        if len(rng) > 1
    ]

    print("\nAdaptive Momentum -- vectorbt Grid Search")
    print(f"  Symbols:    {', '.join(config.symbols)}")
    print(f"  Timeframes: {', '.join(config.timeframes)}")
    print(f"  Conditions: {len(datasets)}")
    print(f"  Flags in grid: {', '.join(swept_flags)}")
    print(f"  Grid size:  {len(valid_grid)} valid / {total_combos} total combos per condition")
    print(f"  Workers:    {config.n_jobs} (1 = sequential)")
    print(f"  Output dir: {output_dir}")
    print(f"  Log file:   {log_path}\n")

    saved = run_sequential(config)

    print(f"\nAll conditions complete. {len(saved)} CSV(s) saved to {output_dir}")
    print("Tip: inspect CSVs with pandas or open in Excel to compare all flag combinations.")
