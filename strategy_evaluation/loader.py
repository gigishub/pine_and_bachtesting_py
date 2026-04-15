"""Load VBT backtest result directories into a single DataFrame.

Expected directory layout (produced by the AMS vectorbt runner):
  <run_dir>/
    BTCUSDT_1H.csv
    BTCUSDT_4H.csv
    ...
    trades/           ← trade logs with EntryTime/ExitTime columns
    *.log             ← ignored
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from strategy_evaluation.config import RobustnessConfig

logger = logging.getLogger(__name__)


def validate_columns(df: pd.DataFrame, cfg: RobustnessConfig) -> dict[str, bool]:
    """Check that *df* contains the columns the evaluation pipeline expects.

    Required columns produce a WARNING when absent (analysis will degrade or
    fail).  Optional columns produce an INFO message when absent (analysis
    continues with graceful fallback).

    Returns a mapping of column name → present (bool).
    """
    required = {
        cfg.col_sqn, cfg.col_pf, cfg.col_trades,
        cfg.col_win_rate, cfg.col_sharpe, cfg.col_return,
    }
    optional = {cfg.col_max_drawdown, cfg.col_expectancy, cfg.col_calmar}

    present: dict[str, bool] = {}
    for col in sorted(required | optional):
        found = col in df.columns
        present[col] = found
        if not found:
            if col in required:
                logger.warning("Required column missing from results CSV: '%s'", col)
            else:
                logger.info("Optional column not in results CSV (skipped): '%s'", col)

    return present


def load_run_dir(run_dir: str | Path) -> pd.DataFrame:
    """Read all per-symbol CSV files and return a combined DataFrame.

    Parameters
    ----------
    run_dir:
        Path to a VBT backtest results directory.

    Returns
    -------
    pd.DataFrame
        All combinations from every CSV, with consistent dtypes.

    Raises
    ------
    FileNotFoundError
        If *run_dir* does not exist.
    ValueError
        If no usable CSV files are found.
    """
    run_dir = Path(run_dir)
    if not run_dir.exists():
        raise FileNotFoundError(f"Run directory not found: {run_dir}")

    csv_files = [
        f for f in run_dir.glob("*.csv")
        if f.name != "trades" and "log" not in f.name.lower()
    ]
    if not csv_files:
        raise ValueError(f"No CSV files found in {run_dir}")

    frames: list[pd.DataFrame] = []
    for csv_path in sorted(csv_files):
        try:
            df = pd.read_csv(csv_path)
            if df.empty:
                logger.debug("Skipping empty file: %s", csv_path.name)
                continue
            frames.append(df)
        except Exception:
            logger.warning("Failed to read %s — skipping", csv_path.name, exc_info=True)

    if not frames:
        raise ValueError(f"All CSV files in {run_dir} were empty or unreadable")

    combined = pd.concat(frames, ignore_index=True)
    logger.info("Loaded %d combinations from %d files in %s", len(combined), len(frames), run_dir.name)
    return combined


def load_data_period(run_dir: str | Path) -> tuple[str, str] | None:
    """Derive the tested data period from trade log CSVs in the trades/ sub-folder.

    Returns a (start, end) tuple of date strings (YYYY-MM-DD), or None if no
    trade logs are found.  The start is the earliest EntryTime and the end is
    the latest ExitTime across all trade logs.
    """
    trades_dir = Path(run_dir) / "trades"
    if not trades_dir.exists():
        return None

    trade_files = list(trades_dir.glob("*.csv"))
    if not trade_files:
        return None

    earliest: pd.Timestamp | None = None
    latest: pd.Timestamp | None = None

    for path in trade_files:
        try:
            df = pd.read_csv(path, usecols=lambda c: c in {"EntryTime", "ExitTime"})
            if df.empty:
                continue
            if "EntryTime" in df.columns:
                t = pd.to_datetime(df["EntryTime"], utc=True).min()
                if earliest is None or t < earliest:
                    earliest = t
            if "ExitTime" in df.columns:
                t = pd.to_datetime(df["ExitTime"], utc=True).max()
                if latest is None or t > latest:
                    latest = t
        except Exception:
            logger.debug("Could not read trade log %s for period extraction", path.name, exc_info=True)

    if earliest is None or latest is None:
        return None

    return earliest.strftime("%Y-%m-%d"), latest.strftime("%Y-%m-%d")
