from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from .models import METRIC_COLUMNS

logger = logging.getLogger(__name__)

# The summary file is always written to the same results_dir as the per-condition CSVs.
SUMMARY_FILENAME = "ROBUSTNESS_SUMMARY.csv"


def load_condition_results(results_dir: Path) -> dict[str, pd.DataFrame]:
    """Load all per-condition CSVs from results_dir into a name→DataFrame dict.

    Skips ROBUSTNESS_SUMMARY.csv so it's safe to call after a summary already exists.
    Keys are the condition names (CSV stem), e.g. {"BTC_1H": df, "ETH_4H": df}.
    """
    frames: dict[str, pd.DataFrame] = {}
    for csv_path in sorted(results_dir.glob("*.csv")):
        if csv_path.name == SUMMARY_FILENAME:
            continue
        try:
            df = pd.read_csv(csv_path)
            frames[csv_path.stem] = df
        except Exception as exc:
            logger.warning("Could not load %s: %s", csv_path.name, exc)
    return frames


def _top_n_signatures(df: pd.DataFrame, top_n: int) -> set[str]:
    """Return the set of parameter signatures that made the top N in this condition.

    Used to count how many conditions a given setup appeared in the top N (consistency).
    Returns empty set if the DataFrame has no Rank column or is empty.
    """
    if "Rank" not in df.columns or df.empty:
        return set()
    return set(df.loc[df["Rank"] <= top_n, "Parameter Signature"].dropna())


def build_robustness_summary(
    results_dir: Path,
    *,
    consistency_top_n: int = 20,
    save: bool = True,
) -> pd.DataFrame:
    """Aggregate all per-condition CSVs into a single robustness summary.

    For each unique parameter signature across all conditions, computes:
      - Consistency Score: count of conditions where it ranked in top N
        → high score = robust; low score = likely a one-condition fluke
      - Consistency [%]: score as a percentage of total conditions run
      - Mean of each metric across ALL conditions (not just top N)
        → gives a complete picture even for conditions where it wasn't top N
      - Std of each metric across conditions
        → low Std + high Consistency = stable and robust
        → high Std = good average but performs very differently by condition
      - Conditions Appeared In: which conditions had this setup in their top N

    Sort order: Consistency Score desc → Expectancy Mean desc.
    Robustness Rank 1 = most consistent AND highest average expectancy.

    Args:
        results_dir:       Folder containing per-condition CSVs (output of sequencer).
        consistency_top_n: Top N cutoff used to determine whether a setup "made it"
                           in each condition. Match this to config.consistency_top_n.
        save:              Write ROBUSTNESS_SUMMARY.csv to results_dir when True.

    Returns:
        Summary DataFrame — one row per unique parameter signature.
    """
    condition_frames = load_condition_results(results_dir)
    if not condition_frames:
        logger.warning("No condition CSVs found in %s", results_dir)
        return pd.DataFrame()

    # Combine all conditions into one frame for cross-condition aggregation.
    all_data = pd.concat(condition_frames.values(), ignore_index=True)
    total_conditions = len(condition_frames)

    # Pre-compute top-N signature sets per condition once — avoids repeated filtering.
    top_n_per_condition: dict[str, set[str]] = {
        condition: _top_n_signatures(df, consistency_top_n)
        for condition, df in condition_frames.items()
    }

    all_signatures = all_data["Parameter Signature"].dropna().unique()

    rows: list[dict] = []
    for sig in all_signatures:
        # All rows for this signature across every condition.
        sig_data = all_data[all_data["Parameter Signature"] == sig]

        # Which conditions had this signature in their top N?
        appeared_in = [
            condition
            for condition, top_sigs in top_n_per_condition.items()
            if sig in top_sigs
        ]
        consistency_score = len(appeared_in)

        row: dict = {
            "Parameter Signature": sig,
            "Consistency Score": consistency_score,
            "Consistency [%]": round(consistency_score / total_conditions * 100, 1),
            "Conditions Appeared In": ", ".join(sorted(appeared_in)),
        }

        # Aggregate each metric across all conditions for this signature.
        # Using ALL conditions (not just top-N appearances) gives a complete picture.
        for metric in METRIC_COLUMNS:
            if metric not in sig_data.columns:
                continue
            col = pd.to_numeric(sig_data[metric], errors="coerce")
            if metric == "# Trades":
                row[f"{metric} Mean"] = round(col.mean(), 1)  # no Std for trade count
            else:
                row[f"{metric} Mean"] = round(col.mean(), 4)
                row[f"{metric} Std"] = round(col.std(), 4)

        rows.append(row)

    summary = pd.DataFrame(rows)
    if summary.empty:
        return summary

    summary = summary.sort_values(
        by=["Consistency Score", "Expectancy [%] Mean"],
        ascending=[False, False],
    ).reset_index(drop=True)

    # Insert Robustness Rank as the first column for quick reading.
    summary.insert(0, "Robustness Rank", summary.index + 1)

    if save:
        out_path = results_dir / SUMMARY_FILENAME
        summary.to_csv(out_path, index=False)
        logger.info(
            "Robustness summary saved → %s (%d signatures, %d conditions)",
            out_path,
            len(summary),
            total_conditions,
        )

    return summary
