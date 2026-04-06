from __future__ import annotations

import logging
import math
from contextlib import contextmanager
from itertools import product
from typing import Any, Callable, Generator

import backtesting.backtesting as _bt_module  # needed to monkey-patch its tqdm reference
import pandas as pd
from backtesting.lib import FractionalBacktest
from tqdm import tqdm

from ...data.fetch import load_ohlcv
from ..strategy import UPSStrategy
from .config import DatasetConfig, RobustnessConfigV4
from .models import METRIC_COLUMNS

logger = logging.getLogger(__name__)

# Type aliases for injectable dependencies — lets tests replace data loading and backtesting.
DataLoader = Callable[[DatasetConfig], pd.DataFrame]
BacktestRunner = Callable[[pd.DataFrame, dict[str, Any]], pd.Series]


# ---------------------------------------------------------------------------
# Backtest construction
# ---------------------------------------------------------------------------

def build_backtest(df: pd.DataFrame) -> FractionalBacktest:
    """Create a backtest instance with fixed engine settings.

    To change cash, commission, or sizing mode, edit here — not in run_backtest().
    """
    return FractionalBacktest(
        df,
        UPSStrategy,
        cash=10_000,
        commission=0.001,       # 0.1% round-trip — adjust for spot vs futures fees
        exclusive_orders=True,  # no simultaneous long+short
        finalize_trades=True,   # close open trades at end of data
    )


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


def run_backtest(df: pd.DataFrame, params: dict[str, Any]) -> pd.Series:
    """Run one backtest with a given parameter set. Returns backtesting.py stats Series."""
    return build_backtest(df).run(**params)


def ensure_min_bars(df: pd.DataFrame, *, dataset: DatasetConfig, min_bars: int) -> pd.DataFrame:
    """Guard against datasets too short to produce meaningful statistics.

    Raise early with a clear message rather than silently returning bad results.
    """
    if len(df) < min_bars:
        raise ValueError(
            f"Need at least {min_bars} bars for {dataset.dataset_key}, got {len(df)}"
        )
    return df


@contextmanager
def _suppress_backtest_progress() -> Generator[None, None, None]:
    """Monkey-patch backtesting.py's internal tqdm reference to disable per-run bars.

    Without this, each of the 192 grid runs prints its own progress bar, flooding
    the terminal. We replace it for the duration of the grid loop, then restore it.
    backtesting.backtesting._tqdm is the module-level tqdm alias used by Backtest.run().
    """
    original = _bt_module._tqdm
    _bt_module._tqdm = lambda *args, **kwargs: original(*args, **{**kwargs, "disable": True})
    try:
        yield
    finally:
        _bt_module._tqdm = original  # always restore, even on exception


# ---------------------------------------------------------------------------
# Parameter grid construction
# ---------------------------------------------------------------------------

def _normalize_params(
    params: dict[str, Any],
    baseline_params: dict[str, Any],
    config: RobustnessConfigV4,
) -> dict[str, Any]:
    """Collapse child parameters to their baseline value when their parent feature is off.

    This is the deduplication step: if use_iq_filter=False, there is no point testing
    iq_lookback=10 vs 20 — the IQ code path is skipped entirely by the strategy.
    By collapsing to baseline we ensure build_parameter_signature() produces an identical
    string for both, and the `seen` set in build_parameter_grid() skips the duplicate.
    """
    normalized = params.copy()
    for name in config.parameter_names:
        required_flags = config.feature_dependencies.get(name, ())
        # If any required parent flag is False/missing, this child param has no effect.
        if required_flags and not all(bool(normalized.get(flag, False)) for flag in required_flags):
            normalized[name] = baseline_params.get(name)
    return normalized


def build_parameter_signature(params: dict[str, Any], parameter_names: tuple[str, ...]) -> str:
    """Encode a parameter set as a single pipe-separated string.

    Used as: (1) deduplication key during grid construction, (2) cross-condition
    join key in the robustness summary, (3) human-readable label in CSVs/Streamlit.
    Bools are rendered as 0/1 so the string is short and diff-friendly.
    """
    parts: list[str] = []
    for name in parameter_names:
        value = params[name]
        if isinstance(value, bool):
            rendered = str(int(value))       # True→"1", False→"0"
        elif isinstance(value, float):
            rendered = f"{value:.4f}"        # fixed 4dp for stable string comparison
        else:
            rendered = str(value)
        parts.append(f"{name}={rendered}")
    return "|".join(parts)


def build_parameter_grid(
    baseline_params: dict[str, Any],
    config: RobustnessConfigV4,
) -> list[dict[str, Any]]:
    """Build the full deduplicated parameter grid.

    Steps:
      1. Cartesian product of all parameter ranges.
      2. Normalize each candidate (collapse inactive child params to baseline).
      3. Skip if the normalized signature has already been seen.

    Result: every dict in the list is a unique, runnable parameter set.
    Grid size < theoretical max because of deduplication (e.g. 192 vs 256 for 6 booleans+4 RR).
    """
    parameter_names = config.parameter_names
    ranges = [config.parameter_ranges[name] for name in parameter_names]
    grid: list[dict[str, Any]] = []
    seen: set[str] = set()  # signature strings of already-added combinations

    for values in product(*ranges):
        candidate = baseline_params.copy()
        candidate.update(dict(zip(parameter_names, values)))
        candidate = _normalize_params(candidate, baseline_params, config)
        sig = build_parameter_signature(candidate, parameter_names)
        if sig in seen:
            continue  # duplicate after normalization — skip
        seen.add(sig)
        grid.append(candidate)

    return grid


# ---------------------------------------------------------------------------
# Metric extraction helpers
# ---------------------------------------------------------------------------

def _safe_float(value: Any) -> float:
    """Convert backtesting stat values to float; return NaN on missing/invalid."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def _safe_int(value: Any) -> int:
    """Convert to int; return 0 on missing/invalid (e.g. 0 trades is a valid result)."""
    v = _safe_float(value)
    return 0 if math.isnan(v) else int(v)


def _build_row(
    stats: pd.Series,
    *,
    dataset: DatasetConfig,
    params: dict[str, Any],
    parameter_names: tuple[str, ...],
) -> dict[str, Any]:
    """Flatten one backtest result into a flat dict ready for a DataFrame row.

    Includes identity columns, all individual parameter values (so you can filter
    by e.g. use_iq_filter=True in Excel/Streamlit), core metrics, and extended stats.
    To add a new metric, add a key here and in models.METRIC_COLUMNS if it needs aggregation.
    """
    row: dict[str, Any] = {
        "Symbol": dataset.symbol,
        "Timeframe": dataset.timeframe,
        "Condition": dataset.condition_key,  # e.g. "BTC_1H"
        "Parameter Signature": build_parameter_signature(params, parameter_names),
    }
    # Individual parameter values — allows grouping/filtering by any single parameter.
    for name in parameter_names:
        row[name] = params[name]

    # Core metrics — these drive ranking and consistency scoring.
    row.update({
        "Return [%]": _safe_float(stats.get("Return [%]")),
        "Expectancy [%]": _safe_float(stats.get("Expectancy [%]")),   # primary sort key
        "Profit Factor": _safe_float(stats.get("Profit Factor")),
        "Win Rate [%]": _safe_float(stats.get("Win Rate [%]")),
        "Max Drawdown [%]": _safe_float(stats.get("Max. Drawdown [%]")),  # note backtesting's key has a dot
        "# Trades": _safe_int(stats.get("# Trades")),
        "SQN": _safe_float(stats.get("SQN")),
    })
    # Extended stats — saved in CSV for manual inspection; not used in ranking.
    row.update({
        "Avg Trade [%]": _safe_float(stats.get("Avg. Trade [%]")),
        "Best Trade [%]": _safe_float(stats.get("Best Trade [%]")),
        "Worst Trade [%]": _safe_float(stats.get("Worst Trade [%]")),
        "Avg Win Trade [%]": _safe_float(stats.get("Avg. Win Trade [%]")),
        "Avg Loss Trade [%]": _safe_float(stats.get("Avg. Loss Trade [%]")),
        "Max Drawdown Duration": str(stats.get("Max. Drawdown Duration", "")),
        "Exposure Time [%]": _safe_float(stats.get("Exposure Time [%]")),
        "Sharpe Ratio": _safe_float(stats.get("Sharpe Ratio")),
        "Calmar Ratio": _safe_float(stats.get("Calmar Ratio")),
    })
    return row


# ---------------------------------------------------------------------------
# Ranking
# ---------------------------------------------------------------------------

def _rank_results(results: pd.DataFrame) -> pd.DataFrame:
    """Sort all results by a priority cascade and assign Rank (1 = best).

    Priority order (all descending except drawdown):
      1. Expectancy — primary signal; average edge per trade
      2. Return     — total return as tiebreaker
      3. Profit Factor
      4. # Trades   — prefer setups that actually trade
      5. Max Drawdown — ascending; smaller drawdown wins ties
    To change ranking logic, edit the sort_values() call below.
    """
    if results.empty:
        return results

    ranked = results.copy()
    # Prefix with _rank_ so they're easy to drop afterwards.
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
    backtest_runner: BacktestRunner = run_backtest,
) -> pd.DataFrame:
    """Run the full deduplicated parameter grid on one pair/timeframe.

    Returns a ranked DataFrame — every unique parameter combination is a row.
    Nothing is filtered out here; the sequencer saves the full result to CSV.
    The Rank column lets callers decide their own top-N cutoff later.
    """
    baseline_params = config.build_baseline_params()
    grid = build_parameter_grid(baseline_params, config)
    rows: list[dict[str, Any]] = []

    # Suppress backtesting's per-run bars so our grid bar is the only thing visible.
    with _suppress_backtest_progress():
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
            rows.append(
                _build_row(
                    stats,
                    dataset=dataset,
                    params=params,
                    parameter_names=config.parameter_names,
                )
            )
            # Live postfix: highest expectancy seen so far + completed count.
            if rows:
                best_exp = max(
                    (r["Expectancy [%]"] for r in rows if not math.isnan(r["Expectancy [%]"])),
                    default=0.0,
                )
                pbar.set_postfix({"best_exp": f"{best_exp:.2f}%", "done": len(rows)})

    if not rows:
        raise RuntimeError(f"No results produced for {dataset.condition_key}")

    return _rank_results(pd.DataFrame(rows))
