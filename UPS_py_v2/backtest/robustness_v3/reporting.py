from __future__ import annotations

import pandas as pd

from .config import DEFAULT_OPTIMIZATION_CONFIG_V3, OptimizationConfigV3
from .models import RobustnessArtifactsV3
from .pipeline import STEP_DATASET_RUNS, STEP_PARAMETER_GRID


def _section(title: str) -> str:
    return f"\n{'=' * 80}\n{title}\n{'=' * 80}"


def _format_table(df: pd.DataFrame, columns: list[str]) -> str:
    if df.empty:
        return "No rows to display."
    printable = df[columns].copy()
    if "# Trades" in printable.columns:
        printable["# Trades"] = printable["# Trades"].astype(int)
    return printable.to_string(index=False, justify="left")


def render_plan(config: OptimizationConfigV3 = DEFAULT_OPTIMIZATION_CONFIG_V3) -> str:
    lines = [
        _section("ROBUSTNESS V3 PLAN"),
        "Step 1: define the Boolean filter + risk:reward optimization grid.",
        "Step 2: run that same grid on each symbol/timeframe independently.",
        f"Assets:              {', '.join(config.validation_symbols)}",
        f"Timeframes:          {', '.join(config.validation_timeframes)}",
        f"Risk:Reward values:  {', '.join(str(value) for value in config.risk_reward_range)}",
        f"Top rows shown:      {config.top_n}",
        f"Start time:          {config.start_time}",
        f"Core filters:        {', '.join(config.boolean_filter_ranges.keys())}",
    ]
    if config.end_time:
        lines.append(f"End time:            {config.end_time}")
    if config.optional_parameter_ranges:
        lines.append("Optional parameter ranges:")
        for name, values in config.optional_parameter_ranges.items():
            lines.append(f"  {name}: {', '.join(str(value) for value in values)}")
    return "\n".join(lines)


def render_parameter_grid(artifacts: RobustnessArtifactsV3, config: OptimizationConfigV3) -> str:
    lines = [
        _section("STEP 1 PARAMETER GRID"),
        f"Grid size:           {artifacts.parameter_grid_size}",
        f"Boolean filters:     {', '.join(config.boolean_filter_ranges.keys())}",
        f"Risk:Reward values:  {', '.join(str(value) for value in config.risk_reward_range)}",
    ]
    return "\n".join(lines)


def render_dataset_results(artifacts: RobustnessArtifactsV3, config: OptimizationConfigV3) -> str:
    if artifacts.dataset_results.empty:
        return _section("STEP 2 DATASET RUNS") + "\nNo dataset results were produced."

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
    return _section("STEP 2 DATASET RUNS") + "\n" + _format_table(summary, columns)


def render_pipeline_report(
    artifacts: RobustnessArtifactsV3,
    config: OptimizationConfigV3 = DEFAULT_OPTIMIZATION_CONFIG_V3,
) -> str:
    sections = [render_plan(config)]
    if artifacts.completed_step in {STEP_PARAMETER_GRID, STEP_DATASET_RUNS}:
        sections.append(render_parameter_grid(artifacts, config))
    if artifacts.completed_step == STEP_DATASET_RUNS:
        sections.append(render_dataset_results(artifacts, config))
    return "\n".join(sections)