from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import logging
import math
from typing import Any

import pandas as pd
from backtesting.lib import FractionalBacktest

from ...data.fetch import load_ohlcv
from ..strategy import UPSStrategy
from .config import DEFAULT_MATRIX_CONFIG, DataConfig, MatrixConfig, build_matrix_datasets, is_parameter_active

logger = logging.getLogger(__name__)

METRIC_COLUMNS = [
    "Return [%]",
    "Expectancy [%]",
    "Profit Factor",
    "Win Rate [%]",
    "Max Drawdown [%]",
    "# Trades",
    "SQN",
]


@dataclass(frozen=True)
class MatrixSearchArtifacts:
    dataset_results: pd.DataFrame
    master_winners: pd.DataFrame
    intersection_winners: pd.DataFrame
    consistent_winners: pd.DataFrame
    out_of_sample_results: pd.DataFrame


def build_backtest(df: pd.DataFrame) -> FractionalBacktest:
    return FractionalBacktest(
        df,
        UPSStrategy,
        cash=10_000,
        commission=0.001,
        exclusive_orders=True,
        finalize_trades=True,
    )


def load_data(data_config: DataConfig) -> pd.DataFrame:
    return load_ohlcv(
        source=data_config.source,
        symbol=data_config.symbol,
        market_type=data_config.market_type,
        timeframe=data_config.timeframe,
        start_time=data_config.start_time,
        end_time=data_config.end_time,
    )


def run_backtest(df: pd.DataFrame, params: dict[str, Any]) -> pd.Series:
    bt = build_backtest(df)
    return bt.run(**params)


def split_in_sample_out_of_sample(
    df: pd.DataFrame,
    *,
    in_sample_ratio: float,
    min_bars: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split a dataset so the holdout segment stays untouched during optimization."""
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


def normalize_filter_params(params: dict[str, Any], filter_names: tuple[str, ...]) -> dict[str, Any]:
    """Force dependent booleans off when their parent feature is disabled."""
    normalized = params.copy()
    for filter_name in filter_names:
        if filter_name in normalized and not is_parameter_active(filter_name, normalized):
            normalized[filter_name] = False
    return normalized


def build_parameter_signature(params: dict[str, Any], filter_names: tuple[str, ...]) -> str:
    signature_parts = [f"{name}={int(bool(params[name]))}" for name in filter_names]
    signature_parts.append(f"ma_length={int(params['ma_length'])}")
    signature_parts.append(f"risk_reward_multiplier={float(params['risk_reward_multiplier']):.2f}")
    return "|".join(signature_parts)


def build_parameter_grid(
    baseline_params: dict[str, Any],
    matrix_config: MatrixConfig = DEFAULT_MATRIX_CONFIG,
) -> list[dict[str, Any]]:
    """Build the boolean filter x ma_length x risk:reward search space."""
    grid: list[dict[str, Any]] = []
    seen_signatures: set[str] = set()

    filter_names = matrix_config.filter_names
    for ma_value in matrix_config.ma_length_choices:
        for rr_value in matrix_config.risk_reward_choices:
            for filter_values in product((False, True), repeat=len(filter_names)):
                candidate = baseline_params.copy()
                for filter_name, filter_value in zip(filter_names, filter_values):
                    candidate[filter_name] = filter_value

                candidate["ma_length"] = int(ma_value)
                candidate["risk_reward_multiplier"] = float(rr_value)
                candidate = normalize_filter_params(candidate, filter_names)
                signature = build_parameter_signature(candidate, filter_names)
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
    dataset: DataConfig,
    params: dict[str, Any],
    filter_names: tuple[str, ...],
) -> dict[str, Any]:
    row = {
        "Dataset": dataset.dataset_key,
        "Symbol": dataset.symbol,
        "Timeframe": dataset.timeframe,
        "Parameter Signature": build_parameter_signature(params, filter_names),
        "risk_reward_multiplier": float(params["risk_reward_multiplier"]),
    }
    for filter_name in filter_names:
        row[filter_name] = bool(params[filter_name])

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


def rank_dataset_results(results: pd.DataFrame) -> pd.DataFrame:
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
    dataset: DataConfig,
    baseline_params: dict[str, Any],
    matrix_config: MatrixConfig = DEFAULT_MATRIX_CONFIG,
) -> pd.DataFrame:
    """Evaluate the full boolean + ratio grid on one in-sample dataset."""
    rows: list[dict[str, Any]] = []
    for params in build_parameter_grid(baseline_params, matrix_config):
        try:
            stats = run_backtest(df, params)
        except Exception as exc:
            logger.warning("Backtest failed for %s %s", dataset.dataset_key, exc)
            continue

        rows.append(
            _metric_row(
                stats,
                dataset=dataset,
                params=params,
                filter_names=matrix_config.filter_names,
            )
        )

    if not rows:
        raise RuntimeError(f"No optimization results produced for {dataset.dataset_key}")

    return rank_dataset_results(pd.DataFrame(rows))


def find_intersection_winners(
    master_winners: pd.DataFrame,
    *,
    total_datasets: int,
    filter_names: tuple[str, ...],
) -> pd.DataFrame:
    """Find configs that appear in the Top N across a majority of datasets."""
    required_hits = (total_datasets // 2) + 1
    grouped = master_winners.groupby("Parameter Signature", dropna=False)
    rows: list[dict[str, Any]] = []

    for signature, frame in grouped:
        first = frame.iloc[0]
        row = {
            "Parameter Signature": signature,
            "Top 10 Hits": int(frame["Dataset"].nunique()),
            "Required Hits": required_hits,
            "Avg Winner Rank": float(frame["Rank"].mean()),
            "Avg Winner Expectancy [%]": float(frame["Expectancy [%]"].mean()),
            "Avg Winner Return [%]": float(frame["Return [%]"].mean()),
        }
        for filter_name in filter_names:
            row[filter_name] = bool(first[filter_name])
        row["risk_reward_multiplier"] = float(first["risk_reward_multiplier"])
        rows.append(row)

    intersections = pd.DataFrame(rows)
    if intersections.empty:
        return intersections

    intersections = intersections.loc[intersections["Top 10 Hits"] >= required_hits]
    if intersections.empty:
        return intersections

    return intersections.sort_values(
        by=["Top 10 Hits", "Avg Winner Expectancy [%]", "Avg Winner Return [%]", "Avg Winner Rank"],
        ascending=[False, False, False, True],
    ).reset_index(drop=True)


def filter_consistent_winners(
    dataset_results: pd.DataFrame,
    candidate_signatures: set[str],
    *,
    total_datasets: int,
    filter_names: tuple[str, ...],
) -> pd.DataFrame:
    """Keep only configs with positive expectancy on every dataset in the matrix."""
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
        row = {
            "Parameter Signature": signature,
            "Coverage": int(frame["Dataset"].nunique()),
            "Avg Expectancy [%]": float(frame["Expectancy [%]"].mean()),
            "Min Expectancy [%]": float(frame["Expectancy [%]"].min()),
            "Avg Return [%]": float(frame["Return [%]"].mean()),
            "Min Return [%]": float(frame["Return [%]"].min()),
            "Avg Profit Factor": float(frame["Profit Factor"].fillna(0.0).mean()),
            "Avg # Trades": float(frame["# Trades"].mean()),
        }
        for filter_name in filter_names:
            row[filter_name] = bool(first[filter_name])
        row["risk_reward_multiplier"] = float(first["risk_reward_multiplier"])
        rows.append(row)

    consistent = pd.DataFrame(rows)
    if consistent.empty:
        return consistent

    return consistent.sort_values(
        by=["Avg Expectancy [%]", "Min Expectancy [%]", "Avg Return [%]", "Min Return [%]"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)


def run_out_of_sample_validation(
    holdout_data: dict[str, tuple[DataConfig, pd.DataFrame]],
    finalist_params: dict[str, Any],
    *,
    filter_names: tuple[str, ...],
) -> pd.DataFrame:
    """Run the chosen finalist on untouched holdout slices for every dataset."""
    rows: list[dict[str, Any]] = []
    for dataset_key, (dataset, df) in holdout_data.items():
        try:
            stats = run_backtest(df, finalist_params)
        except Exception as exc:
            logger.warning("Out-of-sample validation failed for %s %s", dataset_key, exc)
            continue

        rows.append(_metric_row(stats, dataset=dataset, params=finalist_params, filter_names=filter_names))

    return rank_dataset_results(pd.DataFrame(rows)) if rows else pd.DataFrame()


def run_filter_matrix_search(
    baseline_params: dict[str, Any],
    matrix_config: MatrixConfig = DEFAULT_MATRIX_CONFIG,
) -> MatrixSearchArtifacts:
    """Run the full six-step filter search across a multi-asset, multi-timeframe matrix."""
    dataset_frames: list[pd.DataFrame] = []
    master_winner_frames: list[pd.DataFrame] = []
    holdout_data: dict[str, tuple[DataConfig, pd.DataFrame]] = {}
    parameter_lookup = {
        build_parameter_signature(params, matrix_config.filter_names): params
        for params in build_parameter_grid(baseline_params, matrix_config)
    }

    datasets = build_matrix_datasets(matrix_config)
    for dataset in datasets:
        raw_df = load_data(dataset)
        in_sample, out_of_sample = split_in_sample_out_of_sample(
            raw_df,
            in_sample_ratio=matrix_config.in_sample_ratio,
            min_bars=matrix_config.min_bars,
        )
        dataset_results = run_dataset_search(in_sample, dataset, baseline_params, matrix_config)
        dataset_frames.append(dataset_results)
        master_winner_frames.append(dataset_results.head(matrix_config.top_n).copy())
        holdout_data[dataset.dataset_key] = (dataset, out_of_sample)

    if not dataset_frames:
        raise RuntimeError("No dataset results were generated")

    combined_results = pd.concat(dataset_frames, ignore_index=True)
    master_winners = pd.concat(master_winner_frames, ignore_index=True)
    intersection_winners = find_intersection_winners(
        master_winners,
        total_datasets=len(datasets),
        filter_names=matrix_config.filter_names,
    )
    consistent_winners = filter_consistent_winners(
        combined_results,
        set(intersection_winners["Parameter Signature"]) if not intersection_winners.empty else set(),
        total_datasets=len(datasets),
        filter_names=matrix_config.filter_names,
    )

    out_of_sample_results = pd.DataFrame()
    if not consistent_winners.empty:
        finalist_signature = str(consistent_winners.iloc[0]["Parameter Signature"])
        finalist_params = parameter_lookup[finalist_signature]
        out_of_sample_results = run_out_of_sample_validation(
            holdout_data,
            finalist_params,
            filter_names=matrix_config.filter_names,
        )

    return MatrixSearchArtifacts(
        dataset_results=combined_results,
        master_winners=master_winners,
        intersection_winners=intersection_winners,
        consistent_winners=consistent_winners,
        out_of_sample_results=out_of_sample_results,
    )