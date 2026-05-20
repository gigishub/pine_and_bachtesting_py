"""vectorbt grid-search pipeline for the Bear Strategy.

RELATIONSHIP TO AMS vectorbt pipeline
--------------------------------------
This module mirrors adaptive_momentum_strategy/backtest/vectorbt/pipeline.py
with three key differences:
  1. Uses BearGridConfig and BearDataset instead of MomentumGridConfig / DatasetConfig.
  2. Worker state carries a TUPLE of 3 DataFrames (df_1h, df_1d, funding_df), not a
     single df.
  3. run_backtest_vbt is replaced by make_runner(fees, init_cash) → BacktestRunner
     so fees/init_cash are bound at pipeline setup time via closure.

PARALLEL EXECUTION
------------------
  n_jobs == 1  → sequential (default; safest for multi-source data)
  n_jobs == -1 → all CPU cores
  n_jobs > 1   → that many workers

Each worker receives data_tuple once via _worker_init (pickled once per worker).
NUMBA_NUM_THREADS=1 prevents nested numba thread contention.
"""

from __future__ import annotations

import logging
import math
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from itertools import product
from typing import Any, Callable

import pandas as pd

from bear_strategy.strategy.parameters import Parameters
from .bear_grid_config import BearGridConfig
from .metrics import extract_stats
from .runner import run

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Boolean flag groups for valid-combo filtering
# ---------------------------------------------------------------------------

_TRIGGER_FLAGS = ("use_vp_trigger",)
_EXIT_FLAGS    = ("use_fixed_tp", "use_rsi_exit", "use_macd_exit",
                  "use_rsi_oversold_exit", "use_ema_reclaim_exit", "use_funding_exit",
                  "use_ema_above_exit", "use_vwap_exit", "use_vwma_exit",
                  "use_engulfing_exit", "use_hammer_exit",
                  "use_bb_mean_reversion_exit", "use_atr_reversal_exit",
                  "use_vbt_sl_trail")   # trailing SL alone is a valid exit

_EXCLUSIVE_LAYER_MAP: dict[str, tuple[str, ...]] = {
    "trigger": _TRIGGER_FLAGS,
    "exit":    _EXIT_FLAGS,
}


def _is_valid_combo(params: dict[str, Any]) -> bool:
    """Return False if all triggers are False OR all exits are False."""
    triggers_active = any(bool(params.get(f, False)) for f in _TRIGGER_FLAGS)
    exits_active    = any(bool(params.get(f, False)) for f in _EXIT_FLAGS)
    return triggers_active and exits_active


def _is_exclusive_combo(
    params: dict[str, Any],
    exclusive_layers: frozenset[str],
) -> bool:
    """Return False if any exclusive layer has more than one active flag.

    When a layer is in exclusive_layers, exactly one of its flags may be True.
    """
    for layer in exclusive_layers:
        flags  = _EXCLUSIVE_LAYER_MAP[layer]
        active = sum(bool(params.get(f, False)) for f in flags)
        if active != 1:
            return False
    return True


# ---------------------------------------------------------------------------
# Dataset descriptor
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BearDataset:
    """Immutable descriptor for one symbol/timeframe set to backtest."""

    symbol: str
    start_date: str
    end_date: str
    data_dir: str = "crypto_data/data"

    @property
    def condition_key(self) -> str:
        """Filesystem-safe key, e.g. 'BTCUSDT_1H'."""
        return f"{self.symbol}_1H"

    @property
    def dataset_key(self) -> str:
        return self.condition_key


# ---------------------------------------------------------------------------
# BacktestRunner type alias
# ---------------------------------------------------------------------------

BacktestRunner = Callable[
    [tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame], dict[str, Any]],
    pd.Series,
]


# ---------------------------------------------------------------------------
# Process-pool worker state  (carries 3 DataFrames + bound runner)
# ---------------------------------------------------------------------------

_worker_data_tuple: tuple | None = None
_worker_runner: BacktestRunner | None = None


def _worker_init(
    data_tuple: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
    runner: BacktestRunner,
) -> None:
    global _worker_data_tuple, _worker_runner
    os.environ["NUMBA_NUM_THREADS"] = "1"
    _worker_data_tuple = data_tuple
    _worker_runner     = runner


def _worker_run_one(params: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
    try:
        stats = _worker_runner(_worker_data_tuple, params)  # type: ignore[misc]
        return stats, ""
    except Exception as exc:
        return None, str(exc)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_datasets(
    dataset: BearDataset,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load 1h OHLCV, 1d OHLCV, and funding rate data for one symbol."""
    from bear_strategy.hypothesis_test_v2.engine.data_loader import load_ohlcv, load_funding

    df_1h      = load_ohlcv(dataset.symbol, "1h", dataset.start_date, dataset.end_date, dataset.data_dir)
    df_1d      = load_ohlcv(dataset.symbol, "1d", dataset.start_date, dataset.end_date, dataset.data_dir)
    funding_df = load_funding(dataset.symbol, dataset.start_date, dataset.end_date, dataset.data_dir)
    return df_1h, df_1d, funding_df


def ensure_min_bars(
    df_1h: pd.DataFrame,
    *,
    dataset: BearDataset,
    min_bars: int,
) -> pd.DataFrame:
    if len(df_1h) < min_bars:
        raise ValueError(
            f"Need at least {min_bars} bars for {dataset.dataset_key}, got {len(df_1h)}"
        )
    return df_1h


# ---------------------------------------------------------------------------
# BacktestRunner factory
# ---------------------------------------------------------------------------

def make_runner(fees: float, init_cash: float) -> BacktestRunner:
    """Return a BacktestRunner that forwards fees/init_cash to the bear runner."""
    import dataclasses as _dc

    def _run(
        data_tuple: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
        params: dict[str, Any],
    ) -> pd.Series:
        df_1h, df_1d, funding_df = data_tuple
        valid = {f.name for f in _dc.fields(Parameters)}
        p     = Parameters(**{k: v for k, v in params.items() if k in valid})
        pf    = run(df_1h, df_1d, funding_df, p, fees=fees, init_cash=init_cash)
        return extract_stats(pf)

    return _run


def get_trade_log(
    data_tuple: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
    params: dict[str, Any],
    *,
    rank: int,
    sig: str,
    condition: str,
    symbol: str,
    fees: float,
    init_cash: float,
) -> pd.DataFrame:
    """Re-run one combo and return its trade records as a tidy DataFrame."""
    import dataclasses as _dc

    df_1h, df_1d, funding_df = data_tuple
    valid = {f.name for f in _dc.fields(Parameters)}
    p     = Parameters(**{k: v for k, v in params.items() if k in valid})
    pf    = run(df_1h, df_1d, funding_df, p, fees=fees, init_cash=init_cash)

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
    config: BearGridConfig,
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
    config: BearGridConfig,
) -> list[dict[str, Any]]:
    parameter_names = config.parameter_names
    ranges          = [config.parameter_ranges[name] for name in parameter_names]
    grid: list[dict[str, Any]] = []
    seen: set[str] = set()

    exclusive_layers: frozenset[str] = frozenset(
        layer
        for layer, field_name in [
            ("trigger", "trigger_exclusive"),
            ("exit",    "exit_exclusive"),
        ]
        if getattr(config, field_name, False)
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
    dataset: BearDataset,
    params: dict[str, Any],
    parameter_names: tuple[str, ...],
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "Symbol":              dataset.symbol,
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
    data_tuple: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
    dataset: BearDataset,
    config: BearGridConfig,
    *,
    backtest_runner: BacktestRunner,
) -> pd.DataFrame:
    """Run the full deduplicated parameter grid on one symbol."""
    baseline_params = config.build_baseline_params()
    grid            = build_parameter_grid(baseline_params, config)

    if config.n_jobs == 1:
        rows = _run_sequential(data_tuple, dataset, config, grid, backtest_runner)
    else:
        n_workers = os.cpu_count() if config.n_jobs == -1 else config.n_jobs
        rows      = _run_parallel(data_tuple, dataset, config, grid, backtest_runner, n_workers)

    if not rows:
        raise RuntimeError(f"No results produced for {dataset.condition_key}")

    return _rank_results(pd.DataFrame(rows))


def _run_sequential(
    data_tuple: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
    dataset: BearDataset,
    config: BearGridConfig,
    grid: list[dict[str, Any]],
    backtest_runner: BacktestRunner,
) -> list[dict[str, Any]]:
    from tqdm import tqdm

    rows: list[dict[str, Any]] = []
    best_exp = 0.0

    pbar = tqdm(grid, desc=dataset.condition_key, unit="combo", leave=False)
    for params in pbar:
        try:
            stats = backtest_runner(data_tuple, params)
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
    data_tuple: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
    dataset: BearDataset,
    config: BearGridConfig,
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
        initargs=(data_tuple, backtest_runner),
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
