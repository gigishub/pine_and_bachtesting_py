"""vectorbt robustness pipeline — grid building, backtest execution, and result ranking.

RELATIONSHIP TO backtest/robustness_v4/pipeline.py
----------------------------------------------------
This module is structurally identical to backtest/robustness_v4/pipeline.py with
three targeted changes:

  1. REMOVED: FractionalBacktest / UPSStrategy imports (backtesting.py engine)
  2. REMOVED: _suppress_backtest_progress() context manager (backtesting.py internal)
  3. REPLACED: run_backtest() → run_backtest_vbt()
               Uses run() from runner.py + extract_stats() from metrics.py
               instead of calling FractionalBacktest.run().

Everything else — parameter grid building, deduplication, _normalize_params(),
build_parameter_signature(), _build_row(), _rank_results(), run_condition() —
is unchanged and produces the same CSV column format.

SHARED IMPORT
-------------
RobustnessConfigV4 and DatasetConfig are imported from backtest/robustness_v4/config.py.
These are pure dataclasses with zero engine dependency — they describe WHAT to test
(symbols, timeframes, parameter ranges) but have no knowledge of HOW to simulate.
This is the only cross-package import; no engine code from backtest/ is used.

PARALLEL EXECUTION
------------------
When config.n_jobs != 1, the grid is split across worker processes:
  n_jobs > 1  → that many workers
  n_jobs == -1 → all available CPU cores

Each worker gets the DataFrame once via the pool initialiser (_worker_init),
so it is only pickled once per worker rather than once per combo.
NUMBA_NUM_THREADS=1 is set in each worker to prevent nested parallelism
(vectorbt uses numba internally, which itself spawns threads).
"""

from __future__ import annotations

import logging
import math
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import product
from typing import Any, Callable

import pandas as pd

from ..backtest.robustness_v4.config import DatasetConfig, RobustnessConfigV4
from ..data.fetch import load_ohlcv
from ..strategy.strategy_parameters import StrategySettings
from .metrics import extract_stats
from .runner import run

logger = logging.getLogger(__name__)

# Type alias — same contract as BacktestRunner in backtest/robustness_v4/pipeline.py
BacktestRunner = Callable[[pd.DataFrame, dict[str, Any]], pd.Series]

# ---------------------------------------------------------------------------
# Process-pool worker state
# ---------------------------------------------------------------------------
# Populated once per worker via _worker_init() so df is only pickled once
# per worker process, not once per combo call.

_worker_df: pd.DataFrame | None = None
_worker_runner: BacktestRunner | None = None


def _worker_init(df: pd.DataFrame, runner: BacktestRunner) -> None:
    """Pool initialiser: store df and runner as process-local globals.

    Sets NUMBA_NUM_THREADS=1 to prevent nested thread contention:
    vectorbt uses numba internally, which spawns its own thread pool.
    Without this, each worker would spawn os.cpu_count() numba threads,
    creating cpu_count² threads total.
    """
    global _worker_df, _worker_runner
    os.environ["NUMBA_NUM_THREADS"] = "1"
    _worker_df = df
    _worker_runner = runner


def _worker_run_one(params: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
    """Run one backtest combo in a worker process.

    Returns (stats_series, error_message). stats_series is None on failure
    so the main process can log the warning without a shared logger.
    """
    try:
        stats = _worker_runner(_worker_df, params)  # type: ignore[misc]
        return stats, ""
    except Exception as exc:
        return None, str(exc)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_dataset(dataset: DatasetConfig) -> pd.DataFrame:
    """Default data loader — fetches OHLCV via the project's data layer."""
    return load_ohlcv(
        source=dataset.source,
        symbol=dataset.symbol,
        market_type=dataset.market_type,
        timeframe=dataset.timeframe,
        start_time=dataset.start_time,
        end_time=dataset.end_time,
    )


def ensure_min_bars(df: pd.DataFrame, *, dataset: DatasetConfig, min_bars: int) -> pd.DataFrame:
    """Raise early if the dataset is too short for meaningful statistics."""
    if len(df) < min_bars:
        raise ValueError(
            f"Need at least {min_bars} bars for {dataset.dataset_key}, got {len(df)}"
        )
    return df


# ---------------------------------------------------------------------------
# vectorbt backtest entry point
# ---------------------------------------------------------------------------

def run_backtest_vbt(df: pd.DataFrame, params: dict[str, Any]) -> pd.Series:
    """Run one backtest with a given parameter set using vectorbt.

    Has the same signature as BacktestRunner so it slots into run_condition()
    and run_sequential() as a drop-in replacement.

    Args:
        df:     OHLCV DataFrame.
        params: Full strategy parameter dict (baseline + grid overrides).

    Returns:
        pd.Series keyed with the same metric names as backtesting.py results.
    """
    settings = StrategySettings(**params)
    pf = run(df, settings)
    return extract_stats(pf)


# ---------------------------------------------------------------------------
# Parameter grid construction  (identical logic to backtest/robustness_v4/pipeline.py)
# ---------------------------------------------------------------------------

def _normalize_params(
    params: dict[str, Any],
    baseline_params: dict[str, Any],
    config: RobustnessConfigV4,
) -> dict[str, Any]:
    """Collapse child parameters to baseline when their parent feature flag is off."""
    normalized = params.copy()
    for name in config.parameter_names:
        required_flags = config.feature_dependencies.get(name, ())
        if required_flags and not all(bool(normalized.get(flag, False)) for flag in required_flags):
            normalized[name] = baseline_params.get(name)
    return normalized


def build_parameter_signature(params: dict[str, Any], parameter_names: tuple[str, ...]) -> str:
    """Encode a parameter set as a pipe-separated string for deduplication and CSV output."""
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
    config: RobustnessConfigV4,
) -> list[dict[str, Any]]:
    """Build the full deduplicated parameter grid via Cartesian product."""
    parameter_names = config.parameter_names
    ranges = [config.parameter_ranges[name] for name in parameter_names]
    grid: list[dict[str, Any]] = []
    seen: set[str] = set()

    for values in product(*ranges):
        candidate = baseline_params.copy()
        candidate.update(dict(zip(parameter_names, values)))
        candidate = _normalize_params(candidate, baseline_params, config)
        sig = build_parameter_signature(candidate, parameter_names)
        if sig in seen:
            continue
        seen.add(sig)
        grid.append(candidate)

    return grid


# ---------------------------------------------------------------------------
# Metric helpers
# ---------------------------------------------------------------------------

def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def _safe_int(value: Any) -> int:
    v = _safe_float(value)
    return 0 if math.isnan(v) else int(v)


def _build_row(
    stats: pd.Series,
    *,
    dataset: DatasetConfig,
    params: dict[str, Any],
    parameter_names: tuple[str, ...],
) -> dict[str, Any]:
    """Flatten one backtest result into a flat dict ready for a DataFrame row."""
    row: dict[str, Any] = {
        "Symbol": dataset.symbol,
        "Timeframe": dataset.timeframe,
        "Condition": dataset.condition_key,
        "Parameter Signature": build_parameter_signature(params, parameter_names),
    }
    for name in parameter_names:
        row[name] = params[name]

    row.update({
        "Return [%]":       _safe_float(stats.get("Return [%]")),
        "Expectancy [%]":   _safe_float(stats.get("Expectancy [%]")),
        "Profit Factor":    _safe_float(stats.get("Profit Factor")),
        "Win Rate [%]":     _safe_float(stats.get("Win Rate [%]")),
        "Max Drawdown [%]": _safe_float(stats.get("Max. Drawdown [%]")),
        "# Trades":         _safe_int(stats.get("# Trades")),
        "SQN":              _safe_float(stats.get("SQN")),
    })
    row.update({
        "Avg Trade [%]":         _safe_float(stats.get("Avg. Trade [%]")),
        "Best Trade [%]":        _safe_float(stats.get("Best Trade [%]")),
        "Worst Trade [%]":       _safe_float(stats.get("Worst Trade [%]")),
        "Avg Win Trade [%]":     _safe_float(stats.get("Avg. Win Trade [%]")),
        "Avg Loss Trade [%]":    _safe_float(stats.get("Avg. Loss Trade [%]")),
        "Max Drawdown Duration": str(stats.get("Max. Drawdown Duration", "")),
        "Exposure Time [%]":     _safe_float(stats.get("Exposure Time [%]")),
        "Sharpe Ratio":          _safe_float(stats.get("Sharpe Ratio")),
        "Calmar Ratio":          _safe_float(stats.get("Calmar Ratio")),
    })
    return row


# ---------------------------------------------------------------------------
# Ranking
# ---------------------------------------------------------------------------

def _rank_results(results: pd.DataFrame) -> pd.DataFrame:
    """Sort all results by a priority cascade and assign Rank (1 = best)."""
    if results.empty:
        return results

    ranked = results.copy()
    ranked["_rank_expectancy"] = ranked["Expectancy [%]"].fillna(float("-inf"))
    ranked["_rank_return"] = ranked["Return [%]"].fillna(float("-inf"))
    ranked["_rank_profit_factor"] = ranked["Profit Factor"].fillna(float("-inf"))
    ranked["_rank_trades"] = ranked["# Trades"].fillna(0)
    ranked["_rank_drawdown"] = ranked["Max Drawdown [%]"].fillna(float("inf"))

    ranked = ranked.sort_values(
        by=[
            "_rank_expectancy",
            "_rank_return",
            "_rank_profit_factor",
            "_rank_trades",
            "_rank_drawdown",
        ],
        ascending=[False, False, False, False, True],
    ).reset_index(drop=True)

    ranked["Rank"] = ranked.index + 1
    return ranked.drop(columns=[c for c in ranked.columns if c.startswith("_rank_")])


# ---------------------------------------------------------------------------
# Public entry point: run one condition
# ---------------------------------------------------------------------------

def run_condition(
    df: pd.DataFrame,
    dataset: DatasetConfig,
    config: RobustnessConfigV4,
    *,
    backtest_runner: BacktestRunner = run_backtest_vbt,
) -> pd.DataFrame:
    """Run the full deduplicated parameter grid on one pair/timeframe.

    Dispatches to sequential or parallel execution based on config.n_jobs:
      n_jobs == 1  → sequential (safe for debugging, no process overhead)
      n_jobs == -1 → all CPU cores
      n_jobs > 1   → that many workers

    Returns a ranked DataFrame — every unique parameter combination is a row.
    """
    baseline_params = config.build_baseline_params()
    grid = build_parameter_grid(baseline_params, config)

    if config.n_jobs == 1:
        rows = _run_sequential(df, dataset, config, grid, backtest_runner)
    else:
        n_workers = os.cpu_count() if config.n_jobs == -1 else config.n_jobs
        rows = _run_parallel(df, dataset, config, grid, backtest_runner, n_workers)

    if not rows:
        raise RuntimeError(f"No results produced for {dataset.condition_key}")

    return _rank_results(pd.DataFrame(rows))


def _run_sequential(
    df: pd.DataFrame,
    dataset: DatasetConfig,
    config: RobustnessConfigV4,
    grid: list[dict[str, Any]],
    backtest_runner: BacktestRunner,
) -> list[dict[str, Any]]:
    """Sequential grid loop — one combo at a time with a live progress bar."""
    from tqdm import tqdm

    rows: list[dict[str, Any]] = []
    best_exp = 0.0  # running max — avoids O(n²) scan on every iteration

    pbar = tqdm(grid, desc=dataset.condition_key, unit="combo", leave=False)
    for params in pbar:
        try:
            stats = backtest_runner(df, params)
        except Exception as exc:
            logger.warning(
                "Backtest failed for %s params=%s: %s",
                dataset.condition_key,
                build_parameter_signature(params, config.parameter_names),
                exc,
            )
            continue

        row = _build_row(stats, dataset=dataset, params=params, parameter_names=config.parameter_names)
        rows.append(row)

        exp = row["Expectancy [%]"]
        if not math.isnan(exp) and exp > best_exp:
            best_exp = exp
        pbar.set_postfix({"best_exp": f"{best_exp:.2f}%", "done": len(rows)})

    return rows


def _run_parallel(
    df: pd.DataFrame,
    dataset: DatasetConfig,
    config: RobustnessConfigV4,
    grid: list[dict[str, Any]],
    backtest_runner: BacktestRunner,
    n_workers: int,
) -> list[dict[str, Any]]:
    """Parallel grid loop using a process pool.

    Each worker receives df once via the pool initialiser so it is only
    pickled once per worker, not once per combo.
    """
    from tqdm import tqdm

    rows: list[dict[str, Any]] = []
    best_exp = 0.0  # running max

    pbar = tqdm(
        total=len(grid),
        desc=f"{dataset.condition_key} ×{n_workers}",
        unit="combo",
        leave=False,
    )

    with ProcessPoolExecutor(
        max_workers=n_workers,
        initializer=_worker_init,
        initargs=(df, backtest_runner),
    ) as pool:
        futures = {pool.submit(_worker_run_one, params): params for params in grid}
        for future in as_completed(futures):
            params = futures[future]
            try:
                stats, error = future.result()
            except Exception as exc:
                logger.warning(
                    "Worker error for %s params=%s: %s",
                    dataset.condition_key,
                    build_parameter_signature(params, config.parameter_names),
                    exc,
                )
                pbar.update(1)
                continue

            if stats is None:
                logger.warning(
                    "Backtest failed for %s params=%s: %s",
                    dataset.condition_key,
                    build_parameter_signature(params, config.parameter_names),
                    error,
                )
                pbar.update(1)
                continue

            row = _build_row(stats, dataset=dataset, params=params, parameter_names=config.parameter_names)
            rows.append(row)

            exp = row["Expectancy [%]"]
            if not math.isnan(exp) and exp > best_exp:
                best_exp = exp
            pbar.update(1)
            pbar.set_postfix({"best_exp": f"{best_exp:.2f}%", "done": len(rows)})

    pbar.close()
    return rows
