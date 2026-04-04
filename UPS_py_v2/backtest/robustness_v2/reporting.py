from __future__ import annotations

import pandas as pd

from .config import DEFAULT_OPTIMIZATION_CONFIG, OptimizationConfig
from .models import OptimizationArtifacts
from .pipeline import (
    STEP_CONSISTENCY,
    STEP_DATASETS,
    STEP_DATASET_SEARCH,
    STEP_INTERSECTION,
    STEP_MASTER_WINNERS,
    STEP_OUT_OF_SAMPLE,
)


def _section(title: str) -> str:
    return f"\n{'=' * 80}\n{title}\n{'=' * 80}"


def _format_table(df: pd.DataFrame, columns: list[str]) -> str:
    if df.empty:
        return "No rows to display."
    printable = df[columns].copy()
    if "# Trades" in printable.columns:
        printable["# Trades"] = printable["# Trades"].astype(int)
    return printable.to_string(index=False, justify="left")


def render_plan(config: OptimizationConfig = DEFAULT_OPTIMIZATION_CONFIG) -> str:
    lines = [
        _section("OPTIMIZER V2 PLAN"),
        f"Assets:              {', '.join(config.symbols)}",
        f"Timeframes:          {', '.join(config.timeframes)}",
        f"Top N per dataset:   {config.top_n}",
        f"In-sample ratio:     {config.in_sample_ratio:.0%}",
        f"Start time:          {config.start_time}",
        f"Parameters:          {', '.join(config.parameter_names) if config.parameter_names else 'baseline only'}",
    ]
    if config.end_time:
        lines.append(f"End time:            {config.end_time}")
    for name in config.parameter_names:
        values = ', '.join(str(value) for value in config.parameter_ranges[name])
        lines.append(f"  {name}: {values}")
    return "\n".join(lines)


def render_dataset_splits(artifacts: OptimizationArtifacts) -> str:
    rows = [
        {
            "Dataset": split.dataset.dataset_key,
            "In Sample Bars": len(split.in_sample),
            "Out Of Sample Bars": len(split.out_of_sample),
        }
        for split in artifacts.dataset_splits.values()
    ]
    return _section("DATASET SPLITS") + "\n" + _format_table(pd.DataFrame(rows), ["Dataset", "In Sample Bars", "Out Of Sample Bars"])


def render_dataset_results(artifacts: OptimizationArtifacts, config: OptimizationConfig) -> str:
    columns = [
        "Dataset",
        "Rank",
        "Expectancy [%]",
        "Return [%]",
        "Profit Factor",
        "# Trades",
        *list(config.parameter_names),
    ]
    summary = artifacts.dataset_results.loc[artifacts.dataset_results["Rank"] <= config.top_n]
    return _section("TOP RESULTS BY DATASET") + "\n" + _format_table(summary, columns)


def render_master_winners(artifacts: OptimizationArtifacts, config: OptimizationConfig) -> str:
    columns = [
        "Dataset",
        "Rank",
        "Expectancy [%]",
        "Return [%]",
        "Profit Factor",
        "# Trades",
        *list(config.parameter_names),
    ]
    return _section("MASTER WINNERS") + "\n" + _format_table(artifacts.master_winners, columns)


def render_intersection(artifacts: OptimizationArtifacts, config: OptimizationConfig) -> str:
    if artifacts.intersection_winners.empty:
        return _section("INTERSECTION") + "\nNo configuration reached the majority threshold."
    columns = [
        "Top N Hits",
        "Required Hits",
        "Avg Winner Rank",
        "Avg Winner Expectancy [%]",
        "Avg Winner Return [%]",
        *list(config.parameter_names),
    ]
    return _section("INTERSECTION") + "\n" + _format_table(artifacts.intersection_winners, columns)


def render_consistency(artifacts: OptimizationArtifacts, config: OptimizationConfig) -> str:
    if artifacts.consistent_winners.empty:
        return _section("CONSISTENCY") + "\nNo candidate kept positive expectancy across the full matrix."
    columns = [
        "Coverage",
        "Avg Expectancy [%]",
        "Min Expectancy [%]",
        "Avg Return [%]",
        "Min Return [%]",
        "Avg Profit Factor",
        "Avg # Trades",
        *list(config.parameter_names),
    ]
    return _section("CONSISTENCY") + "\n" + _format_table(artifacts.consistent_winners, columns)


def render_out_of_sample(artifacts: OptimizationArtifacts, config: OptimizationConfig) -> str:
    if artifacts.out_of_sample_results.empty:
        return _section("OUT OF SAMPLE") + "\nNo out-of-sample run was produced."
    columns = [
        "Dataset",
        "Expectancy [%]",
        "Return [%]",
        "Profit Factor",
        "# Trades",
        *list(config.parameter_names),
    ]
    table = _format_table(artifacts.out_of_sample_results, columns)
    averages = [
        "",
        "Holdout averages:",
        f"Avg Expectancy [%]: {artifacts.out_of_sample_results['Expectancy [%]'].mean():.2f}",
        f"Avg Return [%]:     {artifacts.out_of_sample_results['Return [%]'].mean():.2f}",
        f"Avg # Trades:       {artifacts.out_of_sample_results['# Trades'].mean():.2f}",
    ]
    return _section("OUT OF SAMPLE") + "\n" + table + "\n" + "\n".join(averages)


def render_pipeline_report(
    artifacts: OptimizationArtifacts,
    config: OptimizationConfig = DEFAULT_OPTIMIZATION_CONFIG,
) -> str:
    sections = [render_plan(config)]
    if artifacts.completed_step in {STEP_DATASETS, STEP_DATASET_SEARCH, STEP_MASTER_WINNERS, STEP_INTERSECTION, STEP_CONSISTENCY, STEP_OUT_OF_SAMPLE}:
        sections.append(render_dataset_splits(artifacts))
    if artifacts.completed_step in {STEP_DATASET_SEARCH, STEP_MASTER_WINNERS, STEP_INTERSECTION, STEP_CONSISTENCY, STEP_OUT_OF_SAMPLE}:
        sections.append(render_dataset_results(artifacts, config))
    if artifacts.completed_step in {STEP_MASTER_WINNERS, STEP_INTERSECTION, STEP_CONSISTENCY, STEP_OUT_OF_SAMPLE}:
        sections.append(render_master_winners(artifacts, config))
    if artifacts.completed_step in {STEP_INTERSECTION, STEP_CONSISTENCY, STEP_OUT_OF_SAMPLE}:
        sections.append(render_intersection(artifacts, config))
    if artifacts.completed_step in {STEP_CONSISTENCY, STEP_OUT_OF_SAMPLE}:
        sections.append(render_consistency(artifacts, config))
    if artifacts.completed_step == STEP_OUT_OF_SAMPLE:
        sections.append(render_out_of_sample(artifacts, config))
    return "\n".join(sections)
