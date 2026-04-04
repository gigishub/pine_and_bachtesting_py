from __future__ import annotations

import pandas as pd

from .config import DEFAULT_OPTIMIZATION_CONFIG_V3, OptimizationConfigV3
from .models import RobustnessArtifactsV3
from .pipeline import STEP_MATRIX_VALIDATION, STEP_PRIMARY_SEARCH


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
        "Step 1: optimize Boolean filters + risk:reward set on the primary dataset.",
        "Step 2: validate the Step 1 candidates across the asset/timeframe matrix.",
        f"Primary dataset:     {config.primary_symbol} {config.primary_timeframe}",
        f"Validation assets:   {', '.join(config.validation_symbols)}",
        f"Validation frames:   {', '.join(config.validation_timeframes)}",
        f"Risk:Reward values:  {', '.join(str(value) for value in config.risk_reward_range)}",
        f"Top candidates:      {config.top_n}",
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


def render_primary_results(artifacts: RobustnessArtifactsV3, config: OptimizationConfigV3) -> str:
    columns = [
        "Dataset",
        "Rank",
        "Expectancy [%]",
        "Return [%]",
        "Profit Factor",
        "# Trades",
        *list(config.parameter_names),
    ]
    summary = artifacts.primary_results.loc[artifacts.primary_results["Rank"] <= config.top_n]
    return _section("STEP 1 PRIMARY SEARCH") + "\n" + _format_table(summary, columns)


def render_matrix_summary(artifacts: RobustnessArtifactsV3, config: OptimizationConfigV3) -> str:
    if artifacts.validation_summary.empty:
        return _section("STEP 2 MATRIX VALIDATION") + "\nNo validation results were produced."

    columns = [
        "Coverage",
        "Expected Coverage",
        "Positive Expectancy Hits",
        "Positive Return Hits",
        "Avg Expectancy [%]",
        "Min Expectancy [%]",
        "Avg Return [%]",
        "Min Return [%]",
        "Avg Profit Factor",
        "Avg # Trades",
        *list(config.parameter_names),
    ]
    return _section("STEP 2 MATRIX VALIDATION") + "\n" + _format_table(artifacts.validation_summary, columns)


def render_pipeline_report(
    artifacts: RobustnessArtifactsV3,
    config: OptimizationConfigV3 = DEFAULT_OPTIMIZATION_CONFIG_V3,
) -> str:
    sections = [render_plan(config)]
    if artifacts.completed_step in {STEP_PRIMARY_SEARCH, STEP_MATRIX_VALIDATION}:
        sections.append(render_primary_results(artifacts, config))
    if artifacts.completed_step == STEP_MATRIX_VALIDATION:
        sections.append(render_matrix_summary(artifacts, config))
    return "\n".join(sections)