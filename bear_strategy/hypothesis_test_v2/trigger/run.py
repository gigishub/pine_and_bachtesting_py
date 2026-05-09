#!/usr/bin/env python
"""
Run the TRIGGER phase hypothesis tests.

Usage (from project root with .venv active):
    python -m bear_strategy.hypothesis_test_v2.trigger.run
    # or
    python bear_strategy/hypothesis_test_v2/trigger/run.py

What it does
------------
Tests each trigger idea against the BASELINE defined in trigger/config.py.
The baseline should be updated to the promoted regime + setup combination
before running trigger tests.

Outputs (in trigger/results/)
------------------------------
  phase_comparison.csv  — one row per idea × symbol × timeframe
  active_board.md       — ranked active/pending ideas
  rejected_archive.md   — rejected ideas with metrics
  baseline_cache/       — cached baseline statistics
"""

from __future__ import annotations

import argparse
import importlib
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from bear_strategy.hypothesis_test_v2.batch_runner import run_phase
from bear_strategy.hypothesis_test_v2.config import SHARED

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)

RESULTS_DIR = Path(__file__).parent / "results"


def _load_trigger_config(config_module: str):
    mod = importlib.import_module(config_module)
    required = ("BASELINE", "ENTRY_TIMEFRAMES", "IDEAS", "PAIRS", "THRESHOLDS")
    missing = [name for name in required if not hasattr(mod, name)]
    if missing:
        raise ImportError(
            f"Config module '{config_module}' is missing required symbols: {', '.join(missing)}"
        )
    return mod


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run trigger-phase hypothesis tests")
    parser.add_argument(
        "--config-module",
        default="bear_strategy.hypothesis_test_v2.trigger.config",
        help="Python module path for trigger config",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    cfg = _load_trigger_config(args.config_module)

    run_phase(
        phase            = "trigger",
        ideas            = cfg.IDEAS,
        baseline_cfg     = cfg.BASELINE,
        entry_timeframes = cfg.ENTRY_TIMEFRAMES,
        shared           = {**SHARED, "pairs": cfg.PAIRS},
        results_dir      = RESULTS_DIR,
        thresholds       = cfg.THRESHOLDS,
    )


if __name__ == "__main__":
    main()
