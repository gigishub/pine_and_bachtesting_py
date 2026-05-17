"""Load run_grid per-symbol CSV results into a combined DataFrame.

Expected layout (produced by sequencer.run_sequential):
  <results_dir>/
    BTCUSDT_1H.csv
    ETHUSDT_1H.csv
    ...
    trades/              ← optional trade logs (not loaded here)
    run_manifest.txt     ← skipped
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

_REQUIRED_COLS: frozenset[str] = frozenset({
    "Symbol", "Parameter Signature",
    "SQN", "Profit Factor", "# Trades", "Win Rate [%]", "Return [%]",
})

# Filenames that appear in results dirs but are NOT per-symbol data
_SKIP_STEMS: frozenset[str] = frozenset({
    "config", "summary", "sweep_summary", "base_config", "run_manifest",
    "analysis_ranked", "analysis_ranked_all", "analysis_ranked_passing",
    "analysis_per_pair",
})


def load_run_dir(run_dir: str | Path) -> pd.DataFrame:
    """Load all per-symbol CSVs from a run_grid results directory.

    Raises
    ------
    FileNotFoundError : directory does not exist.
    ValueError : no usable per-symbol CSVs found.
    """
    run_dir = Path(run_dir)
    if not run_dir.exists():
        raise FileNotFoundError(f"Run directory not found: {run_dir}")

    csv_files = [
        f for f in run_dir.glob("*.csv")
        if f.stem not in _SKIP_STEMS
        and not f.stem.startswith("pivot_")
        and not f.stem.startswith("analysis_")
    ]
    if not csv_files:
        raise ValueError(f"No per-symbol CSVs in {run_dir}")

    frames: list[pd.DataFrame] = []
    for path in sorted(csv_files):
        try:
            df = pd.read_csv(path)
            if not df.empty:
                frames.append(df)
        except Exception:
            logger.warning("Skipping unreadable CSV: %s", path.name, exc_info=True)

    if not frames:
        raise ValueError(f"All CSVs in {run_dir} empty or unreadable")

    combined = pd.concat(frames, ignore_index=True)
    missing = _REQUIRED_COLS - set(combined.columns)
    if missing:
        logger.warning("Missing expected columns in '%s': %s", run_dir.name, missing)

    logger.info(
        "Loaded %d rows from %d files in '%s'",
        len(combined), len(frames), run_dir.name,
    )
    return combined


def list_run_dirs(results_root: str | Path) -> list[Path]:
    """Return available run directories under results_root, newest first."""
    root = Path(results_root)
    if not root.exists():
        return []
    return sorted(
        [d for d in root.iterdir() if d.is_dir() and not d.name.startswith(".")],
        reverse=True,
    )


def detect_toggle_cols(df: pd.DataFrame) -> list[str]:
    """Return columns starting with 'use_' whose values are strictly 0 or 1."""
    result = []
    for col in df.columns:
        if not col.startswith("use_"):
            continue
        uniq = set(df[col].dropna().astype(float).unique())
        if uniq.issubset({0.0, 1.0}):
            result.append(col)
    return result


def sig_short_label(sig: str) -> str:
    """Shorten a parameter signature to active flags + key numeric params.

    Examples
    --------
    "use_fixed_tp=1|use_rsi_exit=0"          → "fixed_tp"
    "use_fixed_tp=1|stop_atr_mult=2.0000"    → "fixed_tp | sl=2.0"
    ""                                        → "(baseline)"
    """
    if not sig:
        return "(baseline)"

    flag_parts: list[str] = []
    num_parts:  list[str] = []

    for item in sig.split("|"):
        k, _, v = item.partition("=")
        if k.startswith("use_"):
            if v in ("1", "True", "true"):
                short = k.replace("use_", "").replace("_exit", "").replace("_trigger", "")
                flag_parts.append(short)
        else:
            label = (
                k.replace("stop_atr_mult",   "sl")
                 .replace("target_atr_mult", "tp")
                 .replace("exit_rsi_level",  "rsi_lvl")
                 .replace("rsi_oversold_level", "os_lvl")
                 .replace("exit_ema_period", "ema")
                 .replace("macd_fast_period","macd_f")
                 .replace("macd_slow_period","macd_s")
            )
            try:
                num_parts.append(f"{label}={float(v):.4g}")
            except ValueError:
                num_parts.append(f"{label}={v}")

    parts: list[str] = []
    if flag_parts:
        parts.append("+".join(flag_parts))
    if num_parts:
        parts.append(" ".join(num_parts))
    return " | ".join(parts) if parts else sig[:50]
