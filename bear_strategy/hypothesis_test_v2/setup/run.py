#!/usr/bin/env python
"""
Run the SETUP phase hypothesis tests.

Usage (from project root with .venv active):
    python -m bear_strategy.hypothesis_test_v2.setup.run
    # or
    python bear_strategy/hypothesis_test_v2/setup/run.py

What it does
------------
Tests each setup idea against the BASELINE defined in setup/config.py.
Once the regime phase has promoted a regime filter, update BASELINE in
setup/config.py to that indicator — setup ideas will then be compared
against regime-only bars (correctly measuring added edge).

Outputs (in setup/results/)
----------------------------
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

from bear_strategy.hypothesis_test_v2.batch_runner import run_phase
from bear_strategy.hypothesis_test_v2.config import SHARED
from bear_strategy.hypothesis_test_v2.setup.config import BASELINE, ENTRY_TIMEFRAMES, IDEAS, PAIRS, THRESHOLDS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)

RESULTS_DIR = Path(__file__).parent / "results"


def main() -> None:
    run_phase(
        phase            = "setup",
        ideas            = IDEAS,
        baseline_cfg     = BASELINE,
        entry_timeframes = ENTRY_TIMEFRAMES,
        shared           = {**SHARED, "pairs": PAIRS},
        results_dir      = RESULTS_DIR,
        thresholds       = THRESHOLDS,
    )


if __name__ == "__main__":
    main()
