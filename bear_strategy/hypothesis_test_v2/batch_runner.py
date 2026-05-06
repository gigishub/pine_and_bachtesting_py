"""
Batch runner — shared engine used by every phase's run.py.

Baseline types (set in each phase's config.py)
-----------------------------------------------
type = "all_candles"
    Every warmed bar is an entry — unrestricted random-entry baseline.
    Used in the REGIME phase.

type = "indicator"
    Bars filtered by a single promoted indicator from a prior phase.
    Optional "context_tf" key — signal is computed on that TF then
    shift(1) + merge_asof-aligned to the entry TF (no lookahead).

type = "indicators"
    Bars filtered by ALL listed indicators (logical AND).
    Each item may also carry a "context_tf" key.

Multi-timeframe (context_tf) support
--------------------------------------
Any idea OR baseline item can include "context_tf" to compute the signal
on a higher/different timeframe and align it to the entry bars:

    {
        "name":             "close_below_ema_50_1d",
        "indicator_module": "...close_below_ema",
        "params":           {"period": 50},
        "context_tf":       "1d",   # compute on 1d, align to entry_tf
    }

Example BASELINE dicts
----------------------
    # Regime phase
    BASELINE = {"type": "all_candles", "label": "all_candles"}

    # Setup phase — promoted regime on 1d
    BASELINE = {
        "type":       "indicator",
        "label":      "close_below_ema_50_1d",
        "module":     "bear_strategy.hypothesis_test_v2.regime.indicators.close_below_ema",
        "params":     {"period": 50},
        "context_tf": "1d",
    }

    # Trigger phase — regime + setup
    BASELINE = {
        "type":  "indicators",
        "label": "ema50_1d_rsi_range",
        "list": [
            {"module": "...close_below_ema", "params": {"period": 50}, "context_tf": "1d"},
            {"module": "...rsi_range",        "params": {"period": 14, "low": 40, "high": 65}},
        ],
    }
"""

from __future__ import annotations

import importlib
import logging
import sys
from pathlib import Path

import pandas as pd

from bear_strategy.hypothesis_test_v2.engine.alignment import align_htf_series
from bear_strategy.hypothesis_test_v2.engine.baseline_cache import get_or_compute_baseline
from bear_strategy.hypothesis_test_v2.engine.data_loader import (
    assert_date_range_consistent,
    load_ohlcv,
)
from bear_strategy.hypothesis_test_v2.engine.outcome_engine import compute_outcomes
from bear_strategy.hypothesis_test_v2.reports.active_board import write_active_boards
from bear_strategy.hypothesis_test_v2.reports.phase_csv import append_row
from bear_strategy.hypothesis_test_v2.reports.rejected_archive import append_rejected_by_tf

log = logging.getLogger(__name__)

# Within-run cache: avoids reloading the same symbol/tf pair multiple times.
_htf_cache: dict[tuple[str, str], pd.DataFrame] = {}


def _get_htf_df(symbol: str, context_tf: str, shared: dict) -> pd.DataFrame:
    key = (symbol, context_tf)
    if key not in _htf_cache:
        _htf_cache[key] = load_ohlcv(
            symbol, context_tf, shared["start"], shared["end"], shared["data_dir"]
        )
    return _htf_cache[key]


# ── Single-indicator signal (with optional HTF alignment) ────────────────────

def _compute_signal(
    entry_df: pd.DataFrame,
    module_path: str,
    params: dict,
    context_tf: str | None,
    symbol: str,
    shared: dict,
) -> pd.Series:
    """
    Compute a boolean signal, optionally on a higher TF then aligned.

    When context_tf is set:
        1. Load that TF's OHLCV.
        2. Call signal(htf_df, params) → HTF boolean Series.
        3. shift(1) on HTF index so the current forming bar is excluded.
        4. merge_asof(backward) onto entry_df.index — no lookahead.

    When context_tf is None:
        Call signal(entry_df, params) directly.
    """
    mod = importlib.import_module(module_path)
    if context_tf:
        htf_df = _get_htf_df(symbol, context_tf, shared)
        htf_signal = mod.signal(htf_df, params)
        return align_htf_series(htf_df.index, htf_signal, entry_df.index, shift=True)
    return mod.signal(entry_df, params)


# ── Baseline mask ─────────────────────────────────────────────────────────────

def _build_baseline_mask(
    df: pd.DataFrame,
    baseline_cfg: dict,
    symbol: str = "",
    shared: dict | None = None,
) -> pd.Series:
    btype = baseline_cfg["type"]
    if btype == "all_candles":
        return pd.Series(True, index=df.index)
    elif btype == "indicator":
        return _compute_signal(
            df, baseline_cfg["module"], baseline_cfg["params"],
            baseline_cfg.get("context_tf"), symbol, shared or {},
        )
    elif btype == "indicators":
        mask = pd.Series(True, index=df.index)
        for item in baseline_cfg["list"]:
            mask = mask & _compute_signal(
                df, item["module"], item["params"],
                item.get("context_tf"), symbol, shared or {},
            )
        return mask
    raise ValueError(f"Unknown baseline type: {btype!r}")


# ── Candidate mask ────────────────────────────────────────────────────────────

def _build_candidate_mask(
    df: pd.DataFrame,
    idea: dict,
    baseline_mask: pd.Series,
    symbol: str,
    shared: dict,
) -> pd.Series:
    """Candidate is always a subset of baseline_mask."""
    sig = _compute_signal(
        df, idea["indicator_module"], idea.get("params", {}),
        idea.get("context_tf"), symbol, shared,
    )
    return baseline_mask & sig


# ── Per-pair / per-TF inner loop ──────────────────────────────────────────────

def _run_single(
    *,
    symbol: str,
    entry_tf: str,
    ideas: list[dict],
    baseline_cfg: dict,
    shared: dict,
    phase: str,
    results_dir: Path,
) -> None:
    try:
        df = load_ohlcv(symbol, entry_tf, shared["start"], shared["end"], shared["data_dir"])
    except (FileNotFoundError, ValueError) as exc:
        log.warning("Skipping %s/%s — %s", symbol, entry_tf, exc)
        return

    baseline_mask = _build_baseline_mask(df, baseline_cfg, symbol=symbol, shared=shared)
    cache_dir     = results_dir / "baseline_cache"

    baseline_pf, baseline_wr = get_or_compute_baseline(
        df            = df,
        baseline_mask = baseline_mask,
        baseline_label= baseline_cfg["label"],
        symbol        = symbol,
        entry_tf      = entry_tf,
        start         = shared["start"],
        end           = shared["end"],
        cache_dir     = cache_dir,
        atr_period    = shared["atr_period"],
        stop_mult     = shared["stop_atr_mult"],
        target_mult   = shared["target_atr_mult"],
    )

    csv_path = results_dir / "phase_comparison.csv"

    for idea in ideas:
        if not idea.get("enabled", True):
            log.info("Skipping disabled idea: %s", idea["name"])
            continue

        log.info("Testing [%s] on %s/%s …", idea["name"], symbol, entry_tf)
        try:
            candidate_mask = _build_candidate_mask(df, idea, baseline_mask, symbol, shared)
        except Exception:
            log.exception("Error computing signal for idea %s", idea["name"])
            continue

        result = compute_outcomes(
            df            = df,
            entry_mask    = candidate_mask,
            baseline_mask = baseline_mask,
            atr_period    = shared["atr_period"],
            stop_mult     = shared["stop_atr_mult"],
            target_mult   = shared["target_atr_mult"],
        )
        result.baseline_pf = baseline_pf
        result.baseline_wr = baseline_wr

        append_row(
            csv_path,
            phase          = phase,
            idea_name      = idea["name"],
            symbol         = symbol,
            entry_tf       = entry_tf,
            start_date     = shared["start"],
            end_date       = shared["end"],
            result         = result,
            baseline_label = baseline_cfg["label"],
            decision       = idea.get("decision", "PENDING"),
        )

        log.info(
            "  -> PF %.3f (base %.3f, lift %+.3f)  WR %.2f%%  n=%d  coverage=%.2f%%",
            result.candidate_pf, baseline_pf, result.pf_lift,
            result.candidate_wr * 100, result.candidate_n,
            result.candidate_coverage * 100,
        )


# ── Public entrypoint ─────────────────────────────────────────────────────────

def run_phase(
    *,
    phase: str,
    ideas: list[dict],
    baseline_cfg: dict,
    entry_timeframes: list[str],
    shared: dict,
    results_dir: Path,
) -> None:
    """
    Run all *ideas* for every symbol × entry_tf combination.

    Idempotent: phase_comparison.csv and active-board MDs are deleted and
    regenerated on every run so results are never duplicated.

    Parameters
    ----------
    phase:            "regime", "setup", or "trigger".
    ideas:            IDEAS list from the phase config.
    baseline_cfg:     BASELINE dict from the phase config.
    entry_timeframes: Timeframes to test entries on, e.g. ["15m", "1h"].
    shared:           SHARED dict from the global config.py.
    results_dir:      Path to the phase results/ directory.
    """
    results_dir.mkdir(parents=True, exist_ok=True)
    _htf_cache.clear()

    try:
        assert_date_range_consistent(results_dir, shared["start"], shared["end"])
    except Exception as exc:
        log.error("Date range mismatch — aborting: %s", exc)
        sys.exit(1)

    # Delete stale outputs so each run is a clean slate.
    csv_path = results_dir / "phase_comparison.csv"
    if csv_path.exists():
        csv_path.unlink()
    for old_md in results_dir.glob(f"phase_{phase}_entry*_active.md"):
        old_md.unlink()

    for symbol in shared["pairs"]:
        for entry_tf in entry_timeframes:
            _run_single(
                symbol       = symbol,
                entry_tf     = entry_tf,
                ideas        = ideas,
                baseline_cfg = baseline_cfg,
                shared       = shared,
                phase        = phase,
                results_dir  = results_dir,
            )

    write_active_boards(csv_path, results_dir, phase)
    append_rejected_by_tf(csv_path, results_dir, phase)
    log.info("Phase [%s] complete. Results in %s", phase, results_dir)
