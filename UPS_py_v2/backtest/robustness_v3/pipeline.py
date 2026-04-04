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
    build_primary_dataset,
    build_validation_datasets,
)
from .models import RobustnessArtifactsV3

logger = logging.getLogger(__name__)

STEP_PRIMARY_SEARCH = "primary_search"
STEP_MATRIX_VALIDATION = "matrix_validation"
ALL_STEPS = {STEP_PRIMARY_SEARCH, STEP_MATRIX_VALIDATION}

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


def run_primary_search(
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
            logger.warning("Primary search failed for %s %s", dataset.dataset_key, exc)
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


def select_primary_candidates(primary_results: pd.DataFrame, top_n: int) -> pd.DataFrame:
    return primary_results.loc[primary_results["Rank"] <= top_n].copy().reset_index(drop=True)


def summarize_validation_results(
    validation_results: pd.DataFrame,
    *,
    expected_datasets: int,
    parameter_names: tuple[str, ...],
) -> pd.DataFrame:
    if validation_results.empty:
        return pd.DataFrame()

    rows: list[dict[str, Any]] = []
    for signature, frame in validation_results.groupby("Parameter Signature", dropna=False):
        first = frame.iloc[0]
        row: dict[str, Any] = {
            "Parameter Signature": signature,
            "Coverage": int(frame["Dataset"].nunique()),
            "Expected Coverage": expected_datasets,
            "Positive Expectancy Hits": int((frame["Expectancy [%]"] > 0).sum()),
            "Positive Return Hits": int((frame["Return [%]"] > 0).sum()),
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

    summary = pd.DataFrame(rows)
    return summary.sort_values(
        by=[
            "Positive Expectancy Hits",
            "Avg Expectancy [%]",
            "Min Expectancy [%]",
            "Avg Return [%]",
            "Min Return [%]",
        ],
        ascending=[False, False, False, False, False],
    ).reset_index(drop=True)


def run_matrix_validation(
    baseline_params: dict[str, Any],
    primary_candidates: pd.DataFrame,
    config: OptimizationConfigV3 = DEFAULT_OPTIMIZATION_CONFIG_V3,
    *,
    data_loader: DataLoader = load_dataset,
    backtest_runner: BacktestRunner = run_backtest,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if primary_candidates.empty:
        return pd.DataFrame(), pd.DataFrame()

    parameter_lookup = {
        build_parameter_signature(params, config.parameter_names): params
        for params in build_parameter_grid(baseline_params, config)
    }
    validation_rows: list[dict[str, Any]] = []
    datasets = build_validation_datasets(config)

    for dataset in datasets:
        df = ensure_min_bars(data_loader(dataset), dataset=dataset, min_bars=config.min_bars)
        for signature in primary_candidates["Parameter Signature"]:
            params = parameter_lookup[signature]
            try:
                stats = backtest_runner(df, params)
            except Exception as exc:
                logger.warning("Matrix validation failed for %s %s", dataset.dataset_key, exc)
                continue
            validation_rows.append(
                _metric_row(
                    stats,
                    dataset=dataset,
                    params=params,
                    parameter_names=config.parameter_names,
                )
            )

    validation_results = rank_results(pd.DataFrame(validation_rows)) if validation_rows else pd.DataFrame()
    validation_summary = summarize_validation_results(
        validation_results,
        expected_datasets=len(datasets),
        parameter_names=config.parameter_names,
    )
    return validation_results, validation_summary


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
    primary_dataset = build_primary_dataset(config)
    primary_df = ensure_min_bars(data_loader(primary_dataset), dataset=primary_dataset, min_bars=config.min_bars)

    artifacts.primary_results = run_primary_search(
        primary_df,
        primary_dataset,
        baseline_params,
        config,
        backtest_runner=backtest_runner,
    )
    artifacts.primary_candidates = select_primary_candidates(artifacts.primary_results, config.top_n)
    artifacts.completed_step = STEP_PRIMARY_SEARCH
    if stop_after == STEP_PRIMARY_SEARCH:
        return artifacts

    artifacts.validation_results, artifacts.validation_summary = run_matrix_validation(
        baseline_params,
        artifacts.primary_candidates,
        config,
        data_loader=data_loader,
        backtest_runner=backtest_runner,
    )
    if not artifacts.validation_summary.empty:
        artifacts.finalist_params = {
            name: artifacts.validation_summary.iloc[0][name]
            for name in config.parameter_names
        }
    artifacts.completed_step = STEP_MATRIX_VALIDATION
    return artifacts