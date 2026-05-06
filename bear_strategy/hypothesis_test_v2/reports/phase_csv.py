"""
Phase comparison CSV writer.

Appends one row per (idea × symbol × entry_tf) to:
    results/phase_comparison.csv

Columns
-------
phase, idea_name, symbol, entry_tf, start_date, end_date,
candidate_n, candidate_wr, candidate_pf, candidate_coverage,
baseline_label, baseline_n, baseline_wr, baseline_pf,
pf_lift, wr_lift, decision
"""

from __future__ import annotations

import csv
from pathlib import Path

from bear_strategy.hypothesis_test_v2.engine.outcome_engine import OutcomeResult


_COLUMNS = [
    "phase", "idea_name", "symbol", "entry_tf",
    "start_date", "end_date",
    "candidate_n", "candidate_wr", "candidate_pf", "candidate_coverage", "candidate_avg_dur",
    "baseline_label", "baseline_n", "baseline_wr", "baseline_pf", "baseline_avg_dur",
    "pf_lift", "wr_lift",
    "decision",
]


def append_row(
    csv_path: Path,
    *,
    phase: str,
    idea_name: str,
    symbol: str,
    entry_tf: str,
    start_date: str,
    end_date: str,
    result: OutcomeResult,
    baseline_label: str,
    decision: str = "PENDING",
) -> None:
    """
    Append one result row to *csv_path*.  Creates the file with a header if it
    does not yet exist.

    Parameters
    ----------
    csv_path:       Full path to the comparison CSV.
    phase:          "regime", "setup", or "trigger".
    idea_name:      Human-readable idea label, e.g. "close_below_ema_50".
    symbol:         Trading pair, e.g. "BTCUSDT".
    entry_tf:       Entry timeframe, e.g. "15m".
    start_date:     ISO date string matching the data window.
    end_date:       ISO date string matching the data window.
    result:         OutcomeResult from compute_outcomes().
    baseline_label: Short name describing the baseline population (for display).
    decision:       "PENDING", "PROMOTED", or "REJECTED".
    """
    write_header = not csv_path.exists()
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=_COLUMNS)
        if write_header:
            writer.writeheader()
        writer.writerow({
            "phase":               phase,
            "idea_name":           idea_name,
            "symbol":              symbol,
            "entry_tf":            entry_tf,
            "start_date":          start_date,
            "end_date":            end_date,
            "candidate_n":         result.candidate_n,
            "candidate_wr":        result.candidate_wr,
            "candidate_pf":        result.candidate_pf,
            "candidate_coverage":  result.candidate_coverage,
            "candidate_avg_dur":   result.candidate_avg_dur,
            "baseline_label":      baseline_label,
            "baseline_n":          result.baseline_n,
            "baseline_wr":         result.baseline_wr,
            "baseline_pf":         result.baseline_pf,
            "baseline_avg_dur":    result.baseline_avg_dur,
            "pf_lift":             result.pf_lift,
            "wr_lift":             result.wr_lift,
            "decision":            decision,
        })
