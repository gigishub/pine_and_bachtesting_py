#!/usr/bin/env python
"""
Run the TRIGGER phase hypothesis tests.

Usage (from project root with .venv active):
    python -m bull_strategy.hypothesis_test_v2.trigger.run
    # or
    python bull_strategy/hypothesis_test_v2/trigger/run.py

What it does
------------
Tests each trigger idea against the BASELINE defined in trigger/config.py.
After promoting both regime and setup indicators, update BASELINE to combine
them — trigger ideas are then measured against the joint regime+setup population.

Outputs (in trigger/results/)
------------------------------
  phase_comparison.csv  — one row per idea × symbol × timeframe
  active_board.md       — ranked active/pending ideas
  rejected_archive.md   — rejected ideas with metrics
  baseline_cache/       — cached baseline statistics
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from bull_strategy.hypothesis_test_v2.batch_runner import run_phase
from bull_strategy.hypothesis_test_v2.config import SHARED
from bull_strategy.hypothesis_test_v2.trigger.config import BASELINE, ENTRY_TIMEFRAMES, IDEAS, PAIRS, THRESHOLDS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)

RESULTS_DIR = Path(__file__).parent / "results"


def main() -> None:
    run_phase(
        phase            = "trigger",
        ideas            = IDEAS,
        baseline_cfg     = BASELINE,
        entry_timeframes = ENTRY_TIMEFRAMES,
        shared           = {**SHARED, "pairs": PAIRS},
        results_dir      = RESULTS_DIR,
        thresholds       = THRESHOLDS,
    )


if __name__ == "__main__":
    main()
