"""Sequential run loop for the Adaptive Momentum vectorbt engine.

Mirrors UPS_py_v2/backtest/vectorbt/sequencer.py.
Each condition is independent — a failure on one does not stop the rest.
Results are saved as one CSV per condition with checkpoint-resume support.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from ..config import DatasetConfig, MomentumGridConfig
from .pipeline import (
    BacktestRunner,
    load_dataset,
    ensure_min_bars,
    run_backtest_vbt,
    run_condition,
    get_trade_log,
    build_parameter_signature,
)

logger = logging.getLogger(__name__)


def _save_trade_logs(
    df: pd.DataFrame,
    results: pd.DataFrame,
    dataset: DatasetConfig,
    config: MomentumGridConfig,
    output_dir: Path,
) -> None:
    trades_dir = output_dir / "trades"
    trades_dir.mkdir(exist_ok=True)
    trade_log_path = trades_dir / f"{dataset.condition_key}_trade_log.csv"

    if trade_log_path.exists():
        return

    top_rows = results.head(config.trade_logs_top_n)
    trade_dfs: list[pd.DataFrame] = []

    for _, row in top_rows.iterrows():
        params = {name: row[name] for name in config.parameter_names}
        rank = int(row["Rank"])
        sig  = str(row["Parameter Signature"])
        try:
            tdf = get_trade_log(
                df, params,
                rank=rank, sig=sig,
                condition=dataset.condition_key,
                symbol=dataset.symbol,
            )
            if not tdf.empty:
                trade_dfs.append(tdf)
        except Exception as exc:
            logger.warning("Trade log failed for %s rank %d: %s", dataset.condition_key, rank, exc)

    if trade_dfs:
        combined = pd.concat(trade_dfs, ignore_index=True)
        combined.to_csv(trade_log_path, index=False)
        logger.info(
            "Trade log saved → %s (%d trades across top-%d combos)",
            trade_log_path.name, len(combined), len(trade_dfs),
        )


def run_sequential(
    config: MomentumGridConfig,
    output_dir: Path | None = None,
    *,
    stop_after: str | None = None,
    data_loader=load_dataset,
    backtest_runner: BacktestRunner = run_backtest_vbt,
) -> list[Path]:
    """Run the full grid sequentially, saving one CSV per condition.

    Args:
        config:          MomentumGridConfig with symbols, timeframes, and modes.
        output_dir:      Where to save CSVs. Overrides config.output_dir when provided.
        stop_after:      Condition key to stop after (e.g. "SOLUSDT_1H") for early review.
        data_loader:     Swappable for testing without hitting the network.
        backtest_runner: Swappable for testing without running real backtests.

    Returns:
        List of Paths to the saved CSV files (one per completed condition).
    """
    resolved_dir = Path(output_dir or config.output_dir)
    resolved_dir.mkdir(parents=True, exist_ok=True)

    datasets = config.build_datasets()
    saved: list[Path] = []
    condition_times: list[float] = []

    outer = tqdm(datasets, desc="Momentum Grid (vbt)", unit="condition", position=0)

    for dataset in outer:
        outer.set_postfix({"current": dataset.condition_key})

        csv_path = resolved_dir / f"{dataset.condition_key}.csv"
        if csv_path.exists():
            outer.write(f"  ✓ Already done: {dataset.condition_key}")
            saved.append(csv_path)
            continue

        t_start = time.monotonic()

        try:
            df = ensure_min_bars(
                data_loader(dataset),
                dataset=dataset,
                min_bars=config.min_bars,
            )
        except ValueError as exc:
            logger.warning("Skipping %s — %s", dataset.condition_key, exc)
            outer.write(f"  ⚠ Skipped {dataset.condition_key}: {exc}")
            continue

        try:
            results = run_condition(df, dataset, config, backtest_runner=backtest_runner)
        except RuntimeError as exc:
            logger.warning("Skipping %s — %s", dataset.condition_key, exc)
            outer.write(f"  ⚠ Skipped {dataset.condition_key}: {exc}")
            continue

        elapsed = time.monotonic() - t_start
        condition_times.append(elapsed)

        results.to_csv(csv_path, index=False)
        saved.append(csv_path)

        if config.save_trade_logs:
            _save_trade_logs(df, results, dataset, config, resolved_dir)

        outer.write(
            f"  ✓ {dataset.condition_key}  "
            f"{len(results)} combos  "
            f"{elapsed:.0f}s  →  {csv_path.name}"
        )

        if stop_after and dataset.condition_key == stop_after:
            outer.write(f"Stopping after {stop_after} as requested.")
            break

    outer.close()
    avg_time = sum(condition_times) / len(condition_times) if condition_times else 0
    tqdm.write(
        f"\nDone. {len(saved)} condition(s) saved to {resolved_dir}  "
        f"(avg {avg_time:.0f}s/condition)"
    )
    return saved
