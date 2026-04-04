from __future__ import annotations

from itertools import product
import logging
import math
from typing import Any, Callable

import pandas as pd
from backtesting.lib import FractionalBacktest

from ...data.fetch import load_ohlcv
from ..strategy import UPSStrategy
from .config import DEFAULT_OPTIMIZATION_CONFIG, DatasetConfig, OptimizationConfig, build_datasets, is_parameter_active
from .models import DatasetSplit, OptimizationArtifacts

logger = logging.getLogger(__name__)

STEP_DATASETS = "dataset_splits"
STEP_DATASET_SEARCH = "dataset_search"
STEP_MASTER_WINNERS = "master_winners"
STEP_INTERSECTION = "intersection"
STEP_CONSISTENCY = "consistency"
STEP_OUT_OF_SAMPLE = "out_of_sample"
ALL_STEPS = {
    STEP_DATASETS,
    STEP_DATASET_SEARCH,
    STEP_MASTER_WINNERS,
    STEP_INTERSECTION,
    STEP_CONSISTENCY,
    STEP_OUT_OF_SAMPLE,
}

METRIC_COLUMNS = [
    "Return [%]",
    "Expectancy [%]",
    "Profit Factor",
    "Win Rate [%]",
    "Max Drawdown [%]",
    "# Trades",
    "SQN",
]


DataLoader = Callable[[DatasetConfig], pd.DataFrame]
BacktestRunner = Callable[[pd.DataFrame, dict[str, Any]], pd.Series]


def build_backtest(df: pd.DataFrame) -> FractionalBacktest:
    return FractionalBacktest(
        df,
        UPSStrategy,
        cash=10_000,
        commission=0.001,
        exclusive_orders=True,
        finalize_trades=True,
    )


def load_dataset(dataset: DatasetConfig) -> pd.DataFrame:
    return load_ohlcv(
        source=dataset.source,
        symbol=dataset.symbol,
        market_type=dataset.market_type,
        timeframe=dataset.timeframe,
        start_time=dataset.start_time,
        end_time=dataset.end_time,
    )


def run_backtest(df: pd.DataFrame, params: dict[str, Any]) -> pd.Series:
    backtest = build_backtest(df)
    return backtest.run(**params)


def split_dataset(
    df: pd.DataFrame,
    *,
    in_sample_ratio: float,
    min_bars: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not 0 < in_sample_ratio < 1:
        raise ValueError("in_sample_ratio must be between 0 and 1")
    if len(df) < min_bars:
        raise ValueError(f"Need at least {min_bars} bars, got {len(df)}")

    split_index = int(len(df) * in_sample_ratio)
    split_index = max(1, min(split_index, len(df) - 1))
    in_sample = df.iloc[:split_index].copy()
    out_of_sample = df.iloc[split_index:].copy()
    if out_of_sample.empty:
        raise ValueError("Out-of-sample slice is empty")
    return in_sample, out_of_sample


def normalize_params(params: dict[str, Any], config: OptimizationConfig) -> dict[str, Any]:
    normalized = params.copy()
    for name in config.parameter_names:
        if name in normalized and not is_parameter_active(name, normalized, config.feature_dependencies):
            normalized[name] = False
    return normalized


def build_parameter_signature(params: dict[str, Any], parameter_names: tuple[str, ...]) -> str:
    parts: list[str] = []
    for name in parameter_names:
        value = params[name]
        if isinstance(value, bool):
            rendered = str(int(value))
        elif isinstance(value, float):
            rendered = f"{value:.4f}"
        else:
            rendered = str(value)
        parts.append(f"{name}={rendered}")
    return "|".join(parts)


def build_parameter_grid(
    baseline_params: dict[str, Any],
    config: OptimizationConfig = DEFAULT_OPTIMIZATION_CONFIG,
) -> list[dict[str, Any]]:
    parameter_names = config.parameter_names
    if not parameter_names:
        return [baseline_params.copy()]

    ranges = [config.parameter_ranges[name] for name in parameter_names]
    grid: list[dict[str, Any]] = []
    seen_signatures: set[str] = set()

    for values in product(*ranges):
        candidate = baseline_params.copy()
        candidate.update(dict(zip(parameter_names, values)))
        candidate = normalize_params(candidate, config)
        signature = build_parameter_signature(candidate, parameter_names)
        if signature in seen_signatures:
            continue
        seen_signatures.add(signature)
        grid.append(candidate)

    return grid


def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def _safe_int(value: Any) -> int:
    numeric_value = _safe_float(value)
    if math.isnan(numeric_value):
        return 0
    return int(numeric_value)


def _metric_row(
    stats: pd.Series,
    *,
    dataset: DatasetConfig,
    params: dict[str, Any],
    parameter_names: tuple[str, ...],
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "Dataset": dataset.dataset_key,
        "Symbol": dataset.symbol,
        "Timeframe": dataset.timeframe,
        "Parameter Signature": build_parameter_signature(params, parameter_names),
    }
    for name in parameter_names:
        row[name] = params[name]
    row.update(
        {
            "Return [%]": _safe_float(stats.get("Return [%]")),
            "Expectancy [%]": _safe_float(stats.get("Expectancy [%]")),
            "Profit Factor": _safe_float(stats.get("Profit Factor")),
            "Win Rate [%]": _safe_float(stats.get("Win Rate [%]")),
            "Max Drawdown [%]": _safe_float(stats.get("Max. Drawdown [%]")),
            "# Trades": _safe_int(stats.get("# Trades")),
            "SQN": _safe_float(stats.get("SQN")),
        }
    )
    return row


def rank_results(results: pd.DataFrame) -> pd.DataFrame:
    ranking = results.copy()
    ranking["_rank_expectancy"] = ranking["Expectancy [%]"].fillna(float("-inf"))
    ranking["_rank_return"] = ranking["Return [%]"].fillna(float("-inf"))
    ranking["_rank_profit_factor"] = ranking["Profit Factor"].fillna(float("-inf"))
    ranking["_rank_trades"] = ranking["# Trades"].fillna(0)
    ranking["_rank_drawdown"] = ranking["Max Drawdown [%]"].fillna(float("inf"))
    ranking = ranking.sort_values(
        by=[
            "_rank_expectancy",
            "_rank_return",
            "_rank_profit_factor",
            "_rank_trades",
            "_rank_drawdown",
        ],
        ascending=[False, False, False, False, True],
    ).reset_index(drop=True)
    ranking["Rank"] = ranking.index + 1
    return ranking.drop(
        columns=[
            "_rank_expectancy",
            "_rank_return",
            "_rank_profit_factor",
            "_rank_trades",
            "_rank_drawdown",
        ]
    )


def run_dataset_search(
    df: pd.DataFrame,
    dataset: DatasetConfig,
    baseline_params: dict[str, Any],
    config: OptimizationConfig = DEFAULT_OPTIMIZATION_CONFIG,
    *,
    backtest_runner: BacktestRunner = run_backtest,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for params in build_parameter_grid(baseline_params, config):
        try:
            stats = backtest_runner(df, params)
        except Exception as exc:
            logger.warning("Backtest failed for %s %s", dataset.dataset_key, exc)
            continue
        rows.append(
            _metric_row(
                stats,
                dataset=dataset,
                params=params,
                parameter_names=config.parameter_names,
            )
        )
    if not rows:
        raise RuntimeError(f"No optimization results produced for {dataset.dataset_key}")
    return rank_results(pd.DataFrame(rows))


def build_dataset_splits(
    config: OptimizationConfig = DEFAULT_OPTIMIZATION_CONFIG,
    *,
    data_loader: DataLoader = load_dataset,
) -> dict[str, DatasetSplit]:
    splits: dict[str, DatasetSplit] = {}
    for dataset in build_datasets(config):
        raw_df = data_loader(dataset)
        in_sample, out_of_sample = split_dataset(
            raw_df,
            in_sample_ratio=config.in_sample_ratio,
            min_bars=config.min_bars,
        )
        splits[dataset.dataset_key] = DatasetSplit(
            dataset=dataset,
            in_sample=in_sample,
            out_of_sample=out_of_sample,
        )
    return splits


def run_all_dataset_searches(
    dataset_splits: dict[str, DatasetSplit],
    baseline_params: dict[str, Any],
    config: OptimizationConfig = DEFAULT_OPTIMIZATION_CONFIG,
    *,
    backtest_runner: BacktestRunner = run_backtest,
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for split in dataset_splits.values():
        frames.append(
            run_dataset_search(
                split.in_sample,
                split.dataset,
                baseline_params,
                config,
                backtest_runner=backtest_runner,
            )
        )
    if not frames:
        raise RuntimeError("No dataset results were generated")
    return pd.concat(frames, ignore_index=True)


def select_master_winners(dataset_results: pd.DataFrame, top_n: int) -> pd.DataFrame:
    return dataset_results.loc[dataset_results["Rank"] <= top_n].copy().reset_index(drop=True)


def find_intersection_winners(
    master_winners: pd.DataFrame,
    *,
    total_datasets: int,
    parameter_names: tuple[str, ...],
) -> pd.DataFrame:
    required_hits = (total_datasets // 2) + 1
    grouped = master_winners.groupby("Parameter Signature", dropna=False)
    rows: list[dict[str, Any]] = []

    for signature, frame in grouped:
        first = frame.iloc[0]
        row: dict[str, Any] = {
            "Parameter Signature": signature,
            "Top N Hits": int(frame["Dataset"].nunique()),
            "Required Hits": required_hits,
            "Avg Winner Rank": float(frame["Rank"].mean()),
            "Avg Winner Expectancy [%]": float(frame["Expectancy [%]"].mean()),
            "Avg Winner Return [%]": float(frame["Return [%]"].mean()),
        }
        for name in parameter_names:
            row[name] = first[name]
        rows.append(row)

    intersections = pd.DataFrame(rows)
    if intersections.empty:
        return intersections
    intersections = intersections.loc[intersections["Top N Hits"] >= required_hits]
    if intersections.empty:
        return intersections
    return intersections.sort_values(
        by=["Top N Hits", "Avg Winner Expectancy [%]", "Avg Winner Return [%]", "Avg Winner Rank"],
        ascending=[False, False, False, True],
    ).reset_index(drop=True)


def filter_consistent_winners(
    dataset_results: pd.DataFrame,
    candidate_signatures: set[str],
    *,
    total_datasets: int,
    parameter_names: tuple[str, ...],
) -> pd.DataFrame:
    if not candidate_signatures:
        return pd.DataFrame()

    candidate_rows = dataset_results.loc[dataset_results["Parameter Signature"].isin(candidate_signatures)]
    grouped = candidate_rows.groupby("Parameter Signature", dropna=False)
    rows: list[dict[str, Any]] = []

    for signature, frame in grouped:
        if frame["Dataset"].nunique() != total_datasets:
            continue
        if not bool((frame["# Trades"] > 0).all()):
            continue
        if not bool((frame["Expectancy [%]"] > 0).all()):
            continue

        first = frame.iloc[0]
        row: dict[str, Any] = {
            "Parameter Signature": signature,
            "Coverage": int(frame["Dataset"].nunique()),
            "Avg Expectancy [%]": float(frame["Expectancy [%]"].mean()),
            "Min Expectancy [%]": float(frame["Expectancy [%]"].min()),
            "Avg Return [%]": float(frame["Return [%]"].mean()),
            "Min Return [%]": float(frame["Return [%]"].min()),
            "Avg Profit Factor": float(frame["Profit Factor"].fillna(0.0).mean()),
            "Avg # Trades": float(frame["# Trades"].mean()),
        }
        for name in parameter_names:
            row[name] = first[name]
        rows.append(row)

    consistent = pd.DataFrame(rows)
    if consistent.empty:
        return consistent
    return consistent.sort_values(
        by=["Avg Expectancy [%]", "Min Expectancy [%]", "Avg Return [%]", "Min Return [%]"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)


def run_out_of_sample_validation(
    dataset_splits: dict[str, DatasetSplit],
    finalist_params: dict[str, Any],
    config: OptimizationConfig = DEFAULT_OPTIMIZATION_CONFIG,
    *,
    backtest_runner: BacktestRunner = run_backtest,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for split in dataset_splits.values():
        try:
            stats = backtest_runner(split.out_of_sample, finalist_params)
        except Exception as exc:
            logger.warning("Out-of-sample validation failed for %s %s", split.dataset.dataset_key, exc)
            continue
        rows.append(
            _metric_row(
                stats,
                dataset=split.dataset,
                params=finalist_params,
                parameter_names=config.parameter_names,
            )
        )
    return rank_results(pd.DataFrame(rows)) if rows else pd.DataFrame()


def run_optimizer_pipeline(
    config: OptimizationConfig = DEFAULT_OPTIMIZATION_CONFIG,
    *,
    stop_after: str | None = None,
    data_loader: DataLoader = load_dataset,
    backtest_runner: BacktestRunner = run_backtest,
) -> OptimizationArtifacts:
    if stop_after is not None and stop_after not in ALL_STEPS:
        raise ValueError(f"Unsupported stop_after step: {stop_after}")

    artifacts = OptimizationArtifacts()
    baseline_params = config.build_baseline_params()
    artifacts.dataset_splits = build_dataset_splits(config, data_loader=data_loader)
    artifacts.completed_step = STEP_DATASETS
    if stop_after == STEP_DATASETS:
        return artifacts

    artifacts.dataset_results = run_all_dataset_searches(
        artifacts.dataset_splits,
        baseline_params,
        config,
        backtest_runner=backtest_runner,
    )
    artifacts.completed_step = STEP_DATASET_SEARCH
    if stop_after == STEP_DATASET_SEARCH:
        return artifacts

    artifacts.master_winners = select_master_winners(artifacts.dataset_results, config.top_n)
    artifacts.completed_step = STEP_MASTER_WINNERS
    if stop_after == STEP_MASTER_WINNERS:
        return artifacts

    artifacts.intersection_winners = find_intersection_winners(
        artifacts.master_winners,
        total_datasets=len(artifacts.dataset_splits),
        parameter_names=config.parameter_names,
    )
    artifacts.completed_step = STEP_INTERSECTION
    if stop_after == STEP_INTERSECTION:
        return artifacts

    artifacts.consistent_winners = filter_consistent_winners(
        artifacts.dataset_results,
        set(artifacts.intersection_winners["Parameter Signature"]) if not artifacts.intersection_winners.empty else set(),
        total_datasets=len(artifacts.dataset_splits),
        parameter_names=config.parameter_names,
    )
    artifacts.completed_step = STEP_CONSISTENCY
    if stop_after == STEP_CONSISTENCY:
        return artifacts

    if not artifacts.consistent_winners.empty:
        finalist_signature = str(artifacts.consistent_winners.iloc[0]["Parameter Signature"])
        finalist_grid = {
            build_parameter_signature(params, config.parameter_names): params
            for params in build_parameter_grid(baseline_params, config)
        }
        artifacts.finalist_params = finalist_grid[finalist_signature]
        artifacts.out_of_sample_results = run_out_of_sample_validation(
            artifacts.dataset_splits,
            artifacts.finalist_params,
            config,
            backtest_runner=backtest_runner,
        )
    artifacts.completed_step = STEP_OUT_OF_SAMPLE
    return artifacts
