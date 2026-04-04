from __future__ import annotations

import pandas as pd

from .config import DEFAULT_MATRIX_CONFIG, MatrixConfig
from .engine import MatrixSearchArtifacts


def _section(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def _print_table(df: pd.DataFrame, columns: list[str]) -> None:
    if df.empty:
        print("No rows to display.")
        return

    printable = df[columns].copy()
    if "# Trades" in printable.columns:
        printable["# Trades"] = printable["# Trades"].astype(int)
    print(printable.to_string(index=False, justify="left"))


def print_matrix_plan(matrix_config: MatrixConfig = DEFAULT_MATRIX_CONFIG) -> None:
    _section("FILTER MATRIX PLAN")
    print(f"Assets:              {', '.join(matrix_config.symbols)}")
    print(f"Timeframes:          {', '.join(matrix_config.timeframes)}")
    print(f"Risk:Reward values:  {', '.join(str(value) for value in matrix_config.risk_reward_choices)}")
    print(f"Top N per dataset:   {matrix_config.top_n}")
    print(f"In-sample ratio:     {matrix_config.in_sample_ratio:.0%}")
    print(f"Start time:          {matrix_config.start_time}")
    if matrix_config.end_time:
        print(f"End time:            {matrix_config.end_time}")
    print(f"Boolean filters:     {', '.join(matrix_config.filter_names)}")


def print_dataset_summary(artifacts: MatrixSearchArtifacts, top_n: int) -> None:
    _section("TOP RESULTS BY DATASET")
    summary = artifacts.dataset_results.loc[artifacts.dataset_results["Rank"] <= top_n]
    _print_table(
        summary,
        [
            "Dataset",
            "Rank",
            "Expectancy [%]",
            "Return [%]",
            "Profit Factor",
            "# Trades",
            "risk_reward_multiplier",
        ],
    )


def print_master_winners_report(artifacts: MatrixSearchArtifacts) -> None:
    _section("MASTER WINNER REPORT")
    _print_table(
        artifacts.master_winners,
        [
            "Dataset",
            "Rank",
            "Expectancy [%]",
            "Return [%]",
            "Profit Factor",
            "# Trades",
            "risk_reward_multiplier",
            "use_iq_filter",
            "use_sq_boost",
            "enable_ec",
            "enable_bullish_engulfing",
            "enable_shooting_star",
            "enable_hammer",
        ],
    )


def print_intersection_report(artifacts: MatrixSearchArtifacts) -> None:
    _section("INTERSECTION SEARCH")
    if artifacts.intersection_winners.empty:
        print("No configuration reached the majority threshold inside the Top 10 lists.")
        return

    _print_table(
        artifacts.intersection_winners,
        [
            "Top 10 Hits",
            "Required Hits",
            "Avg Winner Rank",
            "Avg Winner Expectancy [%]",
            "Avg Winner Return [%]",
            "risk_reward_multiplier",
            "use_iq_filter",
            "use_sq_boost",
            "enable_ec",
            "enable_bullish_engulfing",
            "enable_shooting_star",
            "enable_hammer",
        ],
    )


def print_consistency_report(artifacts: MatrixSearchArtifacts) -> None:
    _section("CONSISTENCY FILTER")
    if artifacts.consistent_winners.empty:
        print("No intersection winner kept positive expectancy across the full matrix.")
        return

    _print_table(
        artifacts.consistent_winners,
        [
            "Coverage",
            "Avg Expectancy [%]",
            "Min Expectancy [%]",
            "Avg Return [%]",
            "Min Return [%]",
            "Avg Profit Factor",
            "Avg # Trades",
            "risk_reward_multiplier",
            "use_iq_filter",
            "use_sq_boost",
            "enable_ec",
            "enable_bullish_engulfing",
            "enable_shooting_star",
            "enable_hammer",
        ],
    )


def print_out_of_sample_report(artifacts: MatrixSearchArtifacts) -> None:
    _section("OUT-OF-SAMPLE FINALIST")
    if artifacts.out_of_sample_results.empty:
        print("No out-of-sample run was produced because no consistent finalist survived.")
        return

    _print_table(
        artifacts.out_of_sample_results,
        [
            "Dataset",
            "Expectancy [%]",
            "Return [%]",
            "Profit Factor",
            "# Trades",
            "risk_reward_multiplier",
            "use_iq_filter",
            "use_sq_boost",
            "enable_ec",
            "enable_bullish_engulfing",
            "enable_shooting_star",
            "enable_hammer",
        ],
    )

    print("\nHoldout averages:")
    print(f"Avg Expectancy [%]: {artifacts.out_of_sample_results['Expectancy [%]'].mean():.2f}")
    print(f"Avg Return [%]:     {artifacts.out_of_sample_results['Return [%]'].mean():.2f}")
    print(f"Avg # Trades:       {artifacts.out_of_sample_results['# Trades'].mean():.2f}")