"""
Baseline computation and on-disk cache.

Cache key
---------
baseline_{symbol}_{entry_tf}_{baseline_type}_{start}_{end}.csv

*baseline_type* encodes what population was used:
  - "all"           : unrestricted (every warmed bar) — regime phase
  - "regime_<name>" : regime-filtered bars — setup phase
  - "regime_<n>_setup_<n>" : regime + setup — trigger phase

If the file exists, it is loaded and returned directly.
If not, it is computed via compute_outcomes and saved.

Public API
----------
    from engine.baseline_cache import get_or_compute_baseline
    b_pf, b_wr = get_or_compute_baseline(...)
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path

import pandas as pd

from bull_strategy.hypothesis_test_v2.engine.outcome_engine import (
    OutcomeResult,
    compute_atr,
    _simulate_trades,
    _profit_factor,
    _win_rate,
)

log = logging.getLogger(__name__)


def _cache_filename(
    symbol: str,
    entry_tf: str,
    baseline_label: str,
    start: str,
    end: str,
) -> str:
    safe = baseline_label.replace("/", "_").replace(" ", "_")
    return f"baseline_{symbol}_{entry_tf}_{safe}_{start}_{end}.csv"


def _compute_baseline_from_mask(
    df: pd.DataFrame,
    baseline_mask: pd.Series,
    atr_period: int,
    stop_mult: float,
    target_mult: float,
) -> tuple[list[float], list[float]]:
    import numpy as np

    atr  = compute_atr(df["close"], df["high"], df["low"], atr_period)
    warm = atr.notna()
    mask = baseline_mask & warm

    idx = mask.values.nonzero()[0]
    wins, losses, _ = _simulate_trades(
        df["close"].values, df["high"].values, df["low"].values,
        atr.values, idx, stop_mult, target_mult,
    )
    return wins, losses


def get_or_compute_baseline(
    df: pd.DataFrame,
    baseline_mask: pd.Series,
    baseline_label: str,
    symbol: str,
    entry_tf: str,
    start: str,
    end: str,
    cache_dir: Path,
    atr_period: int,
    stop_mult: float,
    target_mult: float,
) -> tuple[float, float]:
    """
    Return (baseline_pf, baseline_wr) for *baseline_mask* on *df*.

    Loads from cache if available; otherwise computes and persists.

    Parameters
    ----------
    df:             OHLCV DataFrame (entry timeframe).
    baseline_mask:  Boolean Series marking which bars form the baseline population.
    baseline_label: Human-readable string used in the cache filename.
    symbol:         Trading pair, e.g. "BTCUSDT".
    entry_tf:       Entry timeframe string, e.g. "15m".
    start / end:    Date range (for cache filename only; df is already sliced).
    cache_dir:      Directory where cache CSVs live.
    atr_period, stop_mult, target_mult: Exit parameters.

    Returns
    -------
    (baseline_pf, baseline_wr) floats.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    fname = _cache_filename(symbol, entry_tf, baseline_label, start, end)
    cache_path = cache_dir / fname

    if cache_path.exists():
        _df = pd.read_csv(cache_path, skipinitialspace=True)
        _df.columns = [c.strip() for c in _df.columns]
        row = _df.iloc[0]
        log.debug("Loaded baseline from cache: %s", fname)
        return float(row["baseline_pf"]), float(row["baseline_wr"])

    log.info("Computing baseline [%s] for %s/%s …", baseline_label, symbol, entry_tf)
    wins, losses = _compute_baseline_from_mask(
        df, baseline_mask, atr_period, stop_mult, target_mult
    )
    pf = _profit_factor(wins, losses)
    wr = _win_rate(wins, losses)

    with open(cache_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["baseline_label", "baseline_pf", "baseline_wr", "n", "start_date", "end_date"])
        writer.writeheader()
        writer.writerow({
            "baseline_label": baseline_label,
            "baseline_pf":    pf,
            "baseline_wr":    wr,
            "n":              len(wins) + len(losses),
            "start_date":     start,
            "end_date":       end,
        })

    log.info("Baseline [%s] %s/%s: PF=%.3f  WR=%.3f  n=%d", baseline_label, symbol, entry_tf, pf, wr, len(wins) + len(losses))
    return pf, wr
