"""vectorbt grid-search pipeline for the Adaptive Momentum Strategy.

RELATIONSHIP TO UPS vectorbt pipeline
--------------------------------------
This module mirrors UPS_py_v2/backtest/vectorbt/pipeline.py with three changes:
  1. Imports DatasetConfig and MomentumGridConfig from this strategy's config.
  2. run_backtest_vbt() constructs Parameters (not StrategySettings).
  3. Supports long-only, short-only, or both directions via use_long/use_short flags.

Everything else (grid building, deduplication, _normalize_params, _build_row,
_rank_results, run_condition, parallel execution) is structurally identical.

PARALLEL EXECUTION
------------------
  n_jobs == 1  → sequential (safe for debugging)
  n_jobs == -1 → all CPU cores
  n_jobs > 1   → that many workers

Each worker gets df once via _worker_init (pickled once per worker, not per combo).
NUMBA_NUM_THREADS=1 prevents nested numba thread contention.
"""

from __future__ import annotations

import logging
import math
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import product
from typing import Any, Callable

import pandas as pd

from ..config import DatasetConfig, MomentumGridConfig
from ...strategy.parameters import Parameters
from .metrics import extract_stats
from .runner import run

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Boolean flag groups for valid-combo filtering
# ---------------------------------------------------------------------------

_REGIME_FLAGS  = ("use_adx", "use_ema_ribbon")
_SETUP_FLAGS   = ("use_donchian", "use_volume_profile")
_TRIGGER_FLAGS = ("use_cmf", "use_power_candle")
_EXIT_FLAGS    = ("use_chandelier", "use_psar", "use_bbands", "use_trailing_stop")

_SHORT_REGIME_FLAGS  = ("use_adx", "use_ema_ribbon_short")
_SHORT_SETUP_FLAGS   = ("use_donchian_short", "use_volume_profile_short")
_SHORT_TRIGGER_FLAGS = ("use_cmf_short", "use_power_candle_short")
_SHORT_EXIT_FLAGS    = ("use_chandelier_short", "use_psar_short", "use_bbands_short", "use_trailing_stop_short")


def _is_valid_combo(params: dict[str, Any]) -> bool:
    """Return False if any active direction has an empty flag group.

    Mirrors the _validate_flags logic in compute_signals / compute_short_signals
    but applied before running the backtest so invalid combos are skipped.
    """
    use_long  = bool(params.get("use_long",  True))
    use_short = bool(params.get("use_short", False))

    if not use_long and not use_short:
        return False

    if use_long:
        long_groups = [_REGIME_FLAGS, _SETUP_FLAGS, _TRIGGER_FLAGS, _EXIT_FLAGS]
        if not all(
            any(bool(params.get(flag, False)) for flag in group)
            for group in long_groups
        ):
            return False

    if use_short:
        short_groups = [
            _SHORT_REGIME_FLAGS, _SHORT_SETUP_FLAGS,
            _SHORT_TRIGGER_FLAGS, _SHORT_EXIT_FLAGS,
        ]
        if not all(
            any(bool(params.get(flag, False)) for flag in group)
            for group in short_groups
        ):
            return False

    return True


_EXCLUSIVE_LAYER_MAP: dict[str, tuple[str, ...]] = {
    "regime":        _REGIME_FLAGS,
    "setup":         _SETUP_FLAGS,
    "trigger":       _TRIGGER_FLAGS,
    "exit":          _EXIT_FLAGS,
    "short_regime":  _SHORT_REGIME_FLAGS,
    "short_setup":   _SHORT_SETUP_FLAGS,
    "short_trigger": _SHORT_TRIGGER_FLAGS,
    "short_exit":    _SHORT_EXIT_FLAGS,
}


def _is_exclusive_combo(
    params: dict[str, Any],
    exclusive_layers: frozenset[str],
) -> bool:
    """Return False if any exclusive layer has more than one active flag.

    When a layer is in exclusive_layers, exactly one of its flags may be True.
    This is used to test indicators in isolation rather than in combination.
    Layers not in exclusive_layers are unconstrained.
    """
    for layer in exclusive_layers:
        flags = _EXCLUSIVE_LAYER_MAP[layer]
        active = sum(bool(params.get(f, False)) for f in flags)
        if active != 1:
            return False
    return True


BacktestRunner = Callable[[pd.DataFrame, dict[str, Any]], pd.Series]

# ---------------------------------------------------------------------------
# Process-pool worker state
# ---------------------------------------------------------------------------

_worker_df: pd.DataFrame | None = None
_worker_runner: BacktestRunner | None = None


def _worker_init(df: pd.DataFrame, runner: BacktestRunner) -> None:
    global _worker_df, _worker_runner
    os.environ["NUMBA_NUM_THREADS"] = "1"
    _worker_df = df
    _worker_runner = runner


def _worker_run_one(params: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
    try:
        stats = _worker_runner(_worker_df, params)  # type: ignore[misc]
        return stats, ""
    except Exception as exc:
        return None, str(exc)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_dataset(dataset: DatasetConfig) -> pd.DataFrame:
    """Fetch OHLCV data via the shared data layer."""
    import sys
    from pathlib import Path
    _root = Path(__file__).parents[4]
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))

    from UPS_py_v2.data.fetch import load_ohlcv
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
        raise ValueError(
            f"Need at least {min_bars} bars for {dataset.dataset_key}, got {len(df)}"
        )
    return df


# ---------------------------------------------------------------------------
# vectorbt backtest entry point
# ---------------------------------------------------------------------------

def run_backtest_vbt(df: pd.DataFrame, params: dict[str, Any]) -> pd.Series:
    """Run one backtest combo using vectorbt.  Signature matches BacktestRunner."""
    # Filter params to only those accepted by Parameters to handle extra grid keys.
    import dataclasses
    valid_fields = {f.name for f in dataclasses.fields(Parameters)}
    p = Parameters(**{k: v for k, v in params.items() if k in valid_fields})
    pf = run(df, p)
    return extract_stats(pf)


def get_trade_log(
    df: pd.DataFrame,
    params: dict[str, Any],
    *,
    rank: int,
    sig: str,
    condition: str,
    symbol: str,
) -> pd.DataFrame:
    """Re-run one combo and return its trade records as a tidy DataFrame."""
    import dataclasses
    valid_fields = {f.name for f in dataclasses.fields(Parameters)}
    p = Parameters(**{k: v for k, v in params.items() if k in valid_fields})
    pf = run(df, p)

    try:
        tlog = pf.trades.records_readable.copy()
    except Exception:
        return pd.DataFrame()

    if tlog.empty:
        return pd.DataFrame()

    col_map = {
        "Entry Timestamp": "EntryTime",
        "Exit Timestamp":  "ExitTime",
        "Avg Entry Price": "EntryPrice",
        "Avg Exit Price":  "ExitPrice",
        "Entry Fees":      "EntryFees",
        "Exit Fees":       "ExitFees",
        "Size":            "Size",
        "PnL":             "PnL",
        "Return":          "Return [%]",
        "Direction":       "Direction",
        "Status":          "Status",
    }
    available = [c for c in col_map if c in tlog.columns]
    tlog = tlog[available].rename(columns=col_map)

    if "Return [%]" in tlog.columns:
        tlog["Return [%]"] = (tlog["Return [%]"] * 100).round(4)

    tlog.insert(0, "Condition",           condition)
    tlog.insert(0, "Symbol",              symbol)
    tlog.insert(0, "Rank",                rank)
    tlog.insert(0, "Parameter Signature", sig)
    return tlog.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Parameter grid construction
# ---------------------------------------------------------------------------

def _normalize_params(
    params: dict[str, Any],
    baseline_params: dict[str, Any],
    config: MomentumGridConfig,
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
    config: MomentumGridConfig,
) -> list[dict[str, Any]]:
    parameter_names = config.parameter_names
    ranges = [config.parameter_ranges[name] for name in parameter_names]
    grid: list[dict[str, Any]] = []
    seen: set[str] = set()

    exclusive_layers: frozenset[str] = frozenset(
        layer
        for layer, field in [
            ("regime",        "regime_exclusive"),
            ("setup",         "setup_exclusive"),
            ("trigger",       "trigger_exclusive"),
            ("exit",          "exit_exclusive"),
            # Short exclusive layers are only meaningful when short is enabled
            *([
                ("short_regime",  "short_regime_exclusive"),
                ("short_setup",   "short_setup_exclusive"),
                ("short_trigger", "short_trigger_exclusive"),
                ("short_exit",    "short_exit_exclusive"),
            ] if config.enable_short else []),
        ]
        if getattr(config, field, False)
    )

    for values in product(*ranges):
        candidate = baseline_params.copy()
        candidate.update(dict(zip(parameter_names, values)))
        candidate = _normalize_params(candidate, baseline_params, config)
        sig = build_parameter_signature(candidate, parameter_names)
        if not _is_valid_combo(candidate):
            continue
        if exclusive_layers and not _is_exclusive_combo(candidate, exclusive_layers):
            continue
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
    row: dict[str, Any] = {
        "Symbol":              dataset.symbol,
        "Timeframe":           dataset.timeframe,
        "Condition":           dataset.condition_key,
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
    if results.empty:
        return results

    ranked = results.copy()
    ranked["_rank_expectancy"]    = ranked["Expectancy [%]"].fillna(float("-inf"))
    ranked["_rank_return"]        = ranked["Return [%]"].fillna(float("-inf"))
    ranked["_rank_profit_factor"] = ranked["Profit Factor"].fillna(float("-inf"))
    ranked["_rank_trades"]        = ranked["# Trades"].fillna(0)
    ranked["_rank_drawdown"]      = ranked["Max Drawdown [%]"].fillna(float("inf"))

    ranked = ranked.sort_values(
        by=["_rank_expectancy", "_rank_return", "_rank_profit_factor",
            "_rank_trades", "_rank_drawdown"],
        ascending=[False, False, False, False, True],
    ).reset_index(drop=True)

    ranked["Rank"] = ranked.index + 1
    return ranked.drop(columns=[c for c in ranked.columns if c.startswith("_rank_")])


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_condition(
    df: pd.DataFrame,
    dataset: DatasetConfig,
    config: MomentumGridConfig,
    *,
    backtest_runner: BacktestRunner = run_backtest_vbt,
) -> pd.DataFrame:
    """Run the full deduplicated parameter grid on one pair/timeframe."""
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
    config: MomentumGridConfig,
    grid: list[dict[str, Any]],
    backtest_runner: BacktestRunner,
) -> list[dict[str, Any]]:
    from tqdm import tqdm

    rows: list[dict[str, Any]] = []
    best_exp = 0.0

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
    config: MomentumGridConfig,
    grid: list[dict[str, Any]],
    backtest_runner: BacktestRunner,
    n_workers: int,
) -> list[dict[str, Any]]:
    from tqdm import tqdm

    rows: list[dict[str, Any]] = []
    best_exp = 0.0

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
