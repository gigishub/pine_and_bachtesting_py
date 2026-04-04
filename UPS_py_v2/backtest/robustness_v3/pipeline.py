from __future__ import annotations

from itertools import product
import logging
import math
from typing import Any, Callable

import pandas as pd
from backtesting.lib import FractionalBacktest

from ...data.fetch import load_ohlcv
from ..strategy import UPSStrategy
from .config import (
    DEFAULT_OPTIMIZATION_CONFIG_V3,
    DatasetConfig,
    OptimizationConfigV3,
    build_validation_datasets,
)
from .models import RobustnessArtifactsV3

logger = logging.getLogger(__name__)

STEP_PARAMETER_GRID = "parameter_grid"
STEP_DATASET_RUNS = "dataset_runs"
ALL_STEPS = {STEP_PARAMETER_GRID, STEP_DATASET_RUNS}

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


def ensure_min_bars(df: pd.DataFrame, *, dataset: DatasetConfig, min_bars: int) -> pd.DataFrame:
    if len(df) < min_bars:
        raise ValueError(f"Need at least {min_bars} bars for {dataset.dataset_key}, got {len(df)}")
    return df


def run_backtest(df: pd.DataFrame, params: dict[str, Any]) -> pd.Series:
    backtest = build_backtest(df)
    return backtest.run(**params)


def normalize_params(
    params: dict[str, Any],
    baseline_params: dict[str, Any],
    config: OptimizationConfigV3,
) -> dict[str, Any]:
    normalized = params.copy()
    for name in config.parameter_names:
        required_flags = config.feature_dependencies.get(name, ())
        if required_flags and not all(bool(normalized.get(flag, False)) for flag in required_flags):
            normalized[name] = baseline_params.get(name)
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
    config: OptimizationConfigV3 = DEFAULT_OPTIMIZATION_CONFIG_V3,
) -> list[dict[str, Any]]:
    parameter_names = config.parameter_names
    ranges = [config.parameter_ranges[name] for name in parameter_names]
    grid: list[dict[str, Any]] = []
    seen_signatures: set[str] = set()

    for values in product(*ranges):
        candidate = baseline_params.copy()
        candidate.update(dict(zip(parameter_names, values)))
        candidate = normalize_params(candidate, baseline_params, config)
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
    if results.empty:
        return results

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
    config: OptimizationConfigV3 = DEFAULT_OPTIMIZATION_CONFIG_V3,
    *,
    backtest_runner: BacktestRunner = run_backtest,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for params in build_parameter_grid(baseline_params, config):
        try:
            stats = backtest_runner(df, params)
        except Exception as exc:
            logger.warning("Dataset search failed for %s %s", dataset.dataset_key, exc)
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


def run_matrix_datasets(
    baseline_params: dict[str, Any],
    config: OptimizationConfigV3 = DEFAULT_OPTIMIZATION_CONFIG_V3,
    *,
    data_loader: DataLoader = load_dataset,
    backtest_runner: BacktestRunner = run_backtest,
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    datasets = build_validation_datasets(config)

    for dataset in datasets:
        df = ensure_min_bars(data_loader(dataset), dataset=dataset, min_bars=config.min_bars)
        frames.append(
            run_dataset_search(
                df,
                dataset,
                baseline_params,
                config,
                backtest_runner=backtest_runner,
            )
        )

    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def run_robustness_pipeline(
    config: OptimizationConfigV3 = DEFAULT_OPTIMIZATION_CONFIG_V3,
    *,
    stop_after: str | None = None,
    data_loader: DataLoader = load_dataset,
    backtest_runner: BacktestRunner = run_backtest,
) -> RobustnessArtifactsV3:
    if stop_after is not None and stop_after not in ALL_STEPS:
        raise ValueError(f"Unsupported stop_after step: {stop_after}")

    artifacts = RobustnessArtifactsV3()
    baseline_params = config.build_baseline_params()
    artifacts.parameter_grid_size = len(build_parameter_grid(baseline_params, config))
    artifacts.completed_step = STEP_PARAMETER_GRID
    if stop_after == STEP_PARAMETER_GRID:
        return artifacts

    artifacts.dataset_results = run_matrix_datasets(
        baseline_params,
        config,
        data_loader=data_loader,
        backtest_runner=backtest_runner,
    )
    artifacts.completed_step = STEP_DATASET_RUNS
    return artifacts