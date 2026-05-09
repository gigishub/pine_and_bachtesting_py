"""
OOS batch runner.

For each strategy in STRATEGIES, AND-s all filter signals to build a compound
entry mask, then compares against a random baseline (all warmed candles).

This is intentionally separate from batch_runner.py — OOS has different
semantics: no phase concept, no baseline cache, always random comparison.
"""

from __future__ import annotations

import importlib
import logging
from pathlib import Path

import pandas as pd

from bear_strategy.hypothesis_test_v2.engine.alignment import align_htf_series
from bear_strategy.hypothesis_test_v2.engine.data_loader import load_ohlcv
from bear_strategy.hypothesis_test_v2.engine.outcome_engine import compute_outcomes
from bear_strategy.hypothesis_test_v2.oss_test.oss_report import write_oss_report
from bear_strategy.hypothesis_test_v2.reports.phase_csv import append_row

log = logging.getLogger(__name__)

# Within-run HTF data cache: avoids reloading the same symbol/tf multiple times.
_htf_cache: dict[tuple[str, str], pd.DataFrame] = {}


def _get_htf_df(symbol: str, context_tf: str, shared: dict) -> pd.DataFrame:
    key = (symbol, context_tf)
    if key not in _htf_cache:
        _htf_cache[key] = load_ohlcv(
            symbol, context_tf, shared["start"], shared["end"], shared["data_dir"]
        )
    return _htf_cache[key]


def _compute_filter(
    entry_df: pd.DataFrame,
    filt: dict,
    symbol: str,
    shared: dict,
) -> pd.Series:
    """
    Compute a single filter signal, with optional HTF alignment.

    Parameters
    ----------
    entry_df:  OHLCV DataFrame for the entry timeframe.
    filt:      Filter dict with keys ``module``, ``params``, and optionally
               ``context_tf``.
    symbol:    Trading pair (injected into params for aux-data indicators).
    shared:    OOS_SHARED dict.
    """
    mod = importlib.import_module(filt["module"])
    augmented = {
        **filt["params"],
        "_symbol":   symbol,
        "_data_dir": shared.get("data_dir", "crypto_data/data"),
    }
    context_tf = filt.get("context_tf")
    if context_tf:
        htf_df     = _get_htf_df(symbol, context_tf, shared)
        htf_signal = mod.signal(htf_df, augmented)
        return align_htf_series(htf_df.index, htf_signal, entry_df.index, shift=True)
    return mod.signal(entry_df, augmented)


def _run_strategy_pair(
    *,
    symbol: str,
    entry_tf: str,
    strategy: dict,
    shared: dict,
    csv_path: Path,
) -> None:
    try:
        df = load_ohlcv(
            symbol, entry_tf, shared["start"], shared["end"], shared["data_dir"]
        )
    except (FileNotFoundError, ValueError) as exc:
        log.warning("Skipping %s/%s — %s", symbol, entry_tf, exc)
        return

    # Random baseline: every warmed candle (no filters).
    baseline_mask = pd.Series(True, index=df.index)

    # Compound signal: AND every filter in order.
    candidate_mask = baseline_mask.copy()
    for filt in strategy["filters"]:
        try:
            sig = _compute_filter(df, filt, symbol, shared)
            candidate_mask = candidate_mask & sig
        except Exception:
            log.exception(
                "Error computing filter %s for %s — skipping strategy",
                filt["module"], symbol,
            )
            return

    result = compute_outcomes(
        df            = df,
        entry_mask    = candidate_mask,
        baseline_mask = baseline_mask,
        atr_period    = shared["atr_period"],
        stop_mult     = shared["stop_atr_mult"],
        target_mult   = shared["target_atr_mult"],
    )

    append_row(
        csv_path,
        phase          = "oss_test",
        idea_name      = strategy["name"],
        symbol         = symbol,
        entry_tf       = entry_tf,
        start_date     = shared["start"],
        end_date       = shared["end"],
        result         = result,
        baseline_label = "random_all_candles",
        decision       = "OOS_PENDING",
    )

    log.info(
        "  [OOS] %s %s/%s → PF %.3f (base %.3f  lift %+.3f)  WR %.1f%%  n=%d  cov %.1f%%",
        strategy["name"], symbol, entry_tf,
        result.candidate_pf, result.baseline_pf, result.pf_lift,
        result.candidate_wr * 100, result.candidate_n,
        result.candidate_coverage * 100,
    )


def run_oss(
    *,
    strategies: list[dict],
    entry_timeframes: list[str],
    shared: dict,
    results_dir: Path,
    thresholds: dict,
) -> None:
    """
    Run all strategies for every symbol × entry_tf combination.

    Deletes and regenerates oss_comparison.csv and oss_report_entry*.md on
    every run so results are always a clean slate.

    Parameters
    ----------
    strategies:       STRATEGIES list from oss_test/config.py.
    entry_timeframes: ENTRY_TIMEFRAMES from oss_test/config.py.
    shared:           OOS_SHARED merged with ``pairs`` from config.
    results_dir:      Path to oss_test/results/.
    thresholds:       THRESHOLDS from oss_test/config.py.
    """
    results_dir.mkdir(parents=True, exist_ok=True)
    _htf_cache.clear()

    csv_path = results_dir / "oss_comparison.csv"
    if csv_path.exists():
        csv_path.unlink()
    for old_md in results_dir.glob("oss_report_entry*.md"):
        old_md.unlink()

    for symbol in shared["pairs"]:
        for entry_tf in entry_timeframes:
            for strategy in strategies:
                if not strategy.get("enabled", True):
                    log.info("Skipping disabled strategy: %s", strategy["name"])
                    continue
                log.info(
                    "OOS [%s] on %s/%s …", strategy["name"], symbol, entry_tf
                )
                _run_strategy_pair(
                    symbol    = symbol,
                    entry_tf  = entry_tf,
                    strategy  = strategy,
                    shared    = shared,
                    csv_path  = csv_path,
                )

    write_oss_report(csv_path, results_dir, thresholds)
    log.info("OOS test complete. Results in %s", results_dir)
