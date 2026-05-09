"""
Lookahead / bias sanity check for bull_strategy hypothesis_test_v2.

Run with:
    python -m bull_strategy.hypothesis_test_v2.sanity_check

Three tests are performed on BTCUSDT / 15m:

1. Future shuffle
   Shuffles the entire price series randomly and runs compute_outcomes on all bars.
   Expected: PF ≈ 1.0  (no structural edge when prices are scrambled).
   A high PF here means the outcome engine has a lookahead bug.

2. Shifted entry (pure future signal)
   Enters N bars *before* a signal fires — the entry bar cannot possibly know
   about the future signal, so this should perform at or below random.
   Expected: PF_shifted ≤ PF_real  (real signal should be >= shifted noise).

3. Cache vs recomputed baseline
   Reads the cached all_candles baseline for BTCUSDT/15m and recomputes it fresh.
   Expected: values match within 0.001.
"""

from __future__ import annotations

import logging
import sys

import numpy as np
import pandas as pd

from bull_strategy.hypothesis_test_v2.config import SHARED
from bull_strategy.hypothesis_test_v2.engine.data_loader import load_ohlcv
from bull_strategy.hypothesis_test_v2.engine.outcome_engine import compute_atr, compute_outcomes
from bull_strategy.hypothesis_test_v2.engine.baseline_cache import get_or_compute_baseline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

SYMBOL    = "BTCUSDT"
ENTRY_TF  = "15m"
SHIFT_N   = 100   # bars to shift forward for the shifted-entry test
TOLERANCE = 0.001


def _passes(label: str, ok: bool, detail: str) -> bool:
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {label}: {detail}")
    return ok


def test_future_shuffle(df: pd.DataFrame) -> bool:
    """Shuffle prices randomly → PF should be near 1.0."""
    log.info("Test 1 — Future shuffle …")
    rng = np.random.default_rng(42)

    shuffled = df.copy()
    idx = rng.permutation(len(df))
    for col in ("open", "high", "low", "close"):
        shuffled[col] = df[col].values[idx]

    # Reorder high/low so high >= low (shuffle may swap them)
    h = shuffled[["high", "low"]].max(axis=1)
    l = shuffled[["high", "low"]].min(axis=1)
    shuffled["high"] = h
    shuffled["low"]  = l

    baseline = pd.Series(True, index=shuffled.index)
    result   = compute_outcomes(shuffled, baseline, baseline,
                                atr_period=SHARED["atr_period"],
                                stop_mult=SHARED["stop_atr_mult"],
                                target_mult=SHARED["target_atr_mult"])
    pf = result.baseline_pf
    ok = 0.85 <= pf <= 1.20
    return _passes(
        "Future shuffle baseline PF",
        ok,
        f"{pf:.3f}  (expected 0.85–1.20 when prices are random)",
    )


def test_shifted_entry(df: pd.DataFrame) -> bool:
    """Shift a signal N bars into the future — should not beat the real signal."""
    log.info("Test 2 — Shifted-entry vs real-entry …")

    # Use close > 200-bar EMA as a simple bullish regime signal
    atr    = compute_atr(df["close"], df["high"], df["low"], SHARED["atr_period"])
    warm   = atr.notna()
    ema200 = df["close"].ewm(span=200, adjust=False).mean()

    real_signal    = (df["close"] > ema200) & warm
    shifted_signal = real_signal.shift(-SHIFT_N).fillna(False).astype(bool) & warm

    baseline = pd.Series(True, index=df.index) & warm

    res_real    = compute_outcomes(df, real_signal, baseline,
                                   atr_period=SHARED["atr_period"],
                                   stop_mult=SHARED["stop_atr_mult"],
                                   target_mult=SHARED["target_atr_mult"])
    res_shifted = compute_outcomes(df, shifted_signal, baseline,
                                   atr_period=SHARED["atr_period"],
                                   stop_mult=SHARED["stop_atr_mult"],
                                   target_mult=SHARED["target_atr_mult"])

    pf_real    = res_real.candidate_pf
    pf_shifted = res_shifted.candidate_pf

    # Shifted entries look N bars into the future — they should not be dramatically
    # better than the real signal.  A pathological lookahead would show shifted >> real.
    ok = pf_shifted <= pf_real * 1.10  # allow 10% tolerance for statistical noise
    return _passes(
        "Shifted-entry PF vs real-entry PF",
        ok,
        f"real={pf_real:.3f}  shifted={pf_shifted:.3f}  "
        f"({'OK — shifted not better than real' if ok else 'WARN — future shift is beating real signal'})",
    )


def test_cache_vs_recomputed(df: pd.DataFrame, cache_dir: str) -> bool:
    """Cached baseline must match a fresh recomputation."""
    log.info("Test 3 — Cache vs recomputed baseline …")
    from pathlib import Path

    cache_path = Path(cache_dir)
    baseline   = pd.Series(True, index=df.index)

    cached_pf, cached_wr = get_or_compute_baseline(
        df             = df,
        baseline_mask  = baseline,
        baseline_label = "all_candles",
        symbol         = SYMBOL,
        entry_tf       = ENTRY_TF,
        start          = SHARED["start"],
        end            = SHARED["end"],
        cache_dir      = cache_path,
        atr_period     = SHARED["atr_period"],
        stop_mult      = SHARED["stop_atr_mult"],
        target_mult    = SHARED["target_atr_mult"],
    )

    # Recompute from scratch by temporarily removing the cached file
    import glob as _glob, os
    cache_files = _glob.glob(str(cache_path / f"baseline_{SYMBOL}_{ENTRY_TF}_all_candles_*.csv"))
    backed_up: list[tuple[str, str]] = []
    for f in cache_files:
        bak = f + ".bak"
        os.rename(f, bak)
        backed_up.append((f, bak))

    try:
        fresh_pf, fresh_wr = get_or_compute_baseline(
            df             = df,
            baseline_mask  = baseline,
            baseline_label = "all_candles",
            symbol         = SYMBOL,
            entry_tf       = ENTRY_TF,
            start          = SHARED["start"],
            end            = SHARED["end"],
            cache_dir      = cache_path,
            atr_period     = SHARED["atr_period"],
            stop_mult      = SHARED["stop_atr_mult"],
            target_mult    = SHARED["target_atr_mult"],
        )
    finally:
        for orig, bak in backed_up:
            if os.path.exists(orig):
                os.remove(orig)
            os.rename(bak, orig)

    pf_diff = abs(cached_pf - fresh_pf)
    ok      = pf_diff <= TOLERANCE
    return _passes(
        "Cache vs recomputed",
        ok,
        f"cached={cached_pf:.4f}  recomputed={fresh_pf:.4f}  diff={pf_diff:.4f}",
    )


def main() -> None:
    print("\n═══════════════════════════════════════════════════")
    print("  bull_strategy hypothesis_test_v2 — Lookahead / Bias Sanity Check")
    print(f"  Symbol: {SYMBOL}  TF: {ENTRY_TF}  "
          f"Window: {SHARED['start']} → {SHARED['end']}")
    print("═══════════════════════════════════════════════════\n")

    df = load_ohlcv(
        symbol     = SYMBOL,
        timeframe  = ENTRY_TF,
        start_date = SHARED["start"],
        end_date   = SHARED["end"],
        data_dir   = SHARED["data_dir"],
    )
    log.info("Loaded %d bars for %s/%s", len(df), SYMBOL, ENTRY_TF)

    cache_dir = "bull_strategy/hypothesis_test_v2/regime/results/baseline_cache"

    results = [
        test_future_shuffle(df),
        test_shifted_entry(df),
        test_cache_vs_recomputed(df, cache_dir),
    ]

    print()
    passed = sum(results)
    total  = len(results)
    print(f"{'═'*51}")
    print(f"  Result: {passed}/{total} tests passed")
    print(f"{'═'*51}\n")

    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
