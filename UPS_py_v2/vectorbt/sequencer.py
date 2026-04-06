"""Sequential robustness run loop for the vectorbt engine.

Mirrors backtest/robustness_v4/sequencer.py but drives the vectorbt pipeline.
Each condition is independent — a failure on one does not stop the rest.
Results are saved as one CSV per condition with checkpoint-resume support.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from ..backtest.robustness_v4.config import DatasetConfig, RobustnessConfigV4
from .pipeline import (
    BacktestRunner,
    load_dataset,
    ensure_min_bars,
    run_backtest_vbt,
    run_condition,
)

logger = logging.getLogger(__name__)


def run_sequential(
    config: RobustnessConfigV4,
    output_dir: Path | None = None,
    *,
    stop_after: str | None = None,
    data_loader=load_dataset,
    backtest_runner: BacktestRunner = run_backtest_vbt,
) -> list[Path]:
    """Run the full robustness grid sequentially, saving one CSV per condition.

    Args:
        config:          V4 config with symbols, timeframes, and parameter ranges.
        output_dir:      Where to save CSVs. Overrides config.output_dir when provided.
        stop_after:      Condition key to stop after (e.g. "BTC_1H") for early review.
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

    outer = tqdm(datasets, desc="Robustness (vbt)", unit="condition", position=0)

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
