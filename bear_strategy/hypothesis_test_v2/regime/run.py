#!/usr/bin/env python
"""
Run the REGIME phase hypothesis tests.

Usage (from project root with .venv active):
    python -m bear_strategy.hypothesis_test_v2.regime.run
    # or
    python bear_strategy/hypothesis_test_v2/regime/run.py

What it does
------------
Tests each idea in IDEAS against an unrestricted random-entry baseline (every
warmed bar). This correctly measures whether a regime gate selects higher-quality
short opportunities than chance.

Outputs (in regime/results/)
-----------------------------
  phase_comparison.csv  — one row per idea × symbol × timeframe
  active_board.md       — ranked active/pending ideas
  rejected_archive.md   — rejected ideas with metrics
  baseline_cache/       — cached baseline statistics (auto-reused on re-runs)
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Allow running as a script from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from bear_strategy.hypothesis_test_v2.batch_runner import run_phase
from bear_strategy.hypothesis_test_v2.config import SHARED
from bear_strategy.hypothesis_test_v2.regime.config import BASELINE, ENTRY_TIMEFRAMES, IDEAS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)

RESULTS_DIR = Path(__file__).parent / "results"


def main() -> None:
    run_phase(
        phase            = "regime",
        ideas            = IDEAS,
        baseline_cfg     = BASELINE,
        entry_timeframes = ENTRY_TIMEFRAMES,
        shared           = SHARED,
        results_dir      = RESULTS_DIR,
    )


if __name__ == "__main__":
    main()
