"""Sequential run loop for the Bear Strategy AMS-style vectorbt engine.

Each symbol is treated as one independent condition.  A failure on one
symbol does not stop the rest.  Results are saved as one CSV per condition
with checkpoint-resume support (skip if CSV already exists).
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from .bear_grid_config import BearGridConfig
from .pipeline import (
    BacktestRunner,
    BearDataset,
    load_datasets,
    ensure_min_bars,
    make_runner,
    run_condition,
    get_trade_log,
    build_parameter_signature,
)

logger = logging.getLogger(__name__)


def _save_trade_logs(
    data_tuple: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
    results: pd.DataFrame,
    dataset: BearDataset,
    config: BearGridConfig,
    output_dir: Path,
) -> None:
    trades_dir = output_dir / "trades"
    trades_dir.mkdir(exist_ok=True)
    trade_log_path = trades_dir / f"{dataset.condition_key}_trade_log.csv"

    if trade_log_path.exists():
        return

    top_rows   = results.head(config.trade_logs_top_n)
    baseline   = config.build_baseline_params()
    trade_dfs: list[pd.DataFrame] = []

    for _, row in top_rows.iterrows():
        params = {**baseline, **{name: row[name] for name in config.parameter_names}}
        rank   = int(row["Rank"])
        sig    = str(row["Parameter Signature"])
        try:
            tdf = get_trade_log(
                data_tuple,
                params,
                rank=rank,
                sig=sig,
                condition=dataset.condition_key,
                symbol=dataset.symbol,
                fees=config.fees,
                init_cash=config.initial_cash,
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
    config: BearGridConfig,
    output_dir: Path | None = None,
    *,
    stop_after: str | None = None,
) -> list[Path]:
    """Run the full grid sequentially, saving one CSV per symbol.

    Args:
        config:      BearGridConfig with symbols, date range, and param ranges.
        output_dir:  Where to save CSVs. Overrides config.output_dir when provided.
        stop_after:  Condition key to stop after (e.g. "BTCUSDT_1H") for early review.

    Returns:
        List of Paths to the saved CSV files (one per completed condition).
    """
    config.validate_coverage()

    resolved_dir = Path(output_dir or config.output_dir)
    resolved_dir.mkdir(parents=True, exist_ok=True)

    # Save audit manifest before any CSVs are written
    from .audit_config import build_manifest
    config_name   = resolved_dir.name
    manifest_text = build_manifest(config, config_name)
    manifest_path = resolved_dir / "run_manifest.txt"
    manifest_path.write_text(manifest_text, encoding="utf-8")
    logger.info("Run manifest saved → %s", manifest_path)
    logger.info("\n%s", manifest_text)

    runner  = make_runner(config.fees, config.initial_cash)
    datasets = [
        BearDataset(
            symbol=symbol,
            start_date=config.start_date,
            end_date=config.end_date,
            data_dir=config.data_dir,
        )
        for symbol in config.symbols
    ]
    saved: list[Path] = []
    condition_times: list[float] = []

    outer = tqdm(datasets, desc="Bear Grid (vbt)", unit="condition", position=0)

    for dataset in outer:
        outer.set_postfix({"current": dataset.condition_key})

        csv_path = resolved_dir / f"{dataset.condition_key}.csv"
        if csv_path.exists():
            outer.write(f"  ✓ Already done: {dataset.condition_key}")
            saved.append(csv_path)
            continue

        t_start = time.monotonic()

        try:
            df_1h, df_1d, funding_df = load_datasets(dataset)
            ensure_min_bars(df_1h, dataset=dataset, min_bars=config.min_bars)
        except (ValueError, OSError, RuntimeError, FileNotFoundError) as exc:
            logger.warning("Skipping %s — %s", dataset.condition_key, exc)
            outer.write(f"  ⚠ Skipped {dataset.condition_key}: {exc}")
            continue

        data_tuple = (df_1h, df_1d, funding_df)

        try:
            results = run_condition(data_tuple, dataset, config, backtest_runner=runner)
        except RuntimeError as exc:
            logger.warning("Skipping %s — %s", dataset.condition_key, exc)
            outer.write(f"  ⚠ Skipped {dataset.condition_key}: {exc}")
            continue

        elapsed = time.monotonic() - t_start
        condition_times.append(elapsed)

        results.to_csv(csv_path, index=False)
        saved.append(csv_path)

        if config.save_trade_logs:
            _save_trade_logs(data_tuple, results, dataset, config, resolved_dir)

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
