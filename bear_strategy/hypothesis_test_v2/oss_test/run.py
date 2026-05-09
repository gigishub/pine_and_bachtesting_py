#!/usr/bin/env python
"""
Run the out-of-sample (OOS) hypothesis test for the promoted bear strategy.

Usage (from project root with .venv active):
    python -m bear_strategy.hypothesis_test_v2.oss_test.run
    # or
    python bear_strategy/hypothesis_test_v2/oss_test/run.py

What it does
------------
Tests the PROMOTED full strategy stack (regime + setup + trigger) against
completely unseen data (2023-11-02 onwards).  Compares against a random
baseline (every warmed candle) to assess real-world generalisability.

Outputs (in oss_test/results/)
-------------------------------
  oss_comparison.csv         — one row per strategy × symbol × timeframe
  oss_report_entry{tf}.md    — human-readable OOS verdict
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from bear_strategy.hypothesis_test_v2.oss_test.config import (
    ENTRY_TIMEFRAMES,
    OOS_SHARED,
    PAIRS,
    STRATEGIES,
    THRESHOLDS,
)
from bear_strategy.hypothesis_test_v2.oss_test.oss_runner import run_oss

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)

RESULTS_DIR = Path(__file__).parent / "results"


def main() -> None:
    run_oss(
        strategies       = STRATEGIES,
        entry_timeframes = ENTRY_TIMEFRAMES,
        shared           = {**OOS_SHARED, "pairs": PAIRS},
        results_dir      = RESULTS_DIR,
        thresholds       = THRESHOLDS,
    )


if __name__ == "__main__":
    main()
