"""Independent, thorough OHLCV data quality audit.

Runs a comprehensive set of checks beyond the lightweight quality.py inline
checks that run during download.  Produces a detailed Markdown report saved
to the coin's directory.

Per-file checks (run_audit / audit_coin)
-----------------------------------------
1.  Completeness     — actual vs expected row count; exact gap locations
2.  Duplicates       — duplicate timestamps
3.  Price integrity  — zero or negative OHLC values
4.  OHLC logic       — High≥Low, High≥Open, High≥Close, Low≤Open, Low≤Close
5.  Price spikes     — single-candle log-return exceeds a tf-aware threshold
6.  Stale prices     — N consecutive identical Close values (frozen data)
7.  Volume health    — zero-volume candles; volume spikes vs rolling median
8.  Return profile   — log-return mean, std, skew, kurtosis (statistical flag)

Cross-timeframe consistency (cross_timeframe_check)
----------------------------------------------------
Uses 1m candles as ground truth.  Each higher-TF file is compared against
the 1m data resampled up — any OHLCV mismatch beyond floating-point noise
indicates a data integrity problem in the higher-TF download.

Each per-file check returns a CheckResult with PASS / WARN / FAIL status,
affected row count, percentage, and (where useful) a sample of flagged rows.

A weighted trust score (0–100) is computed across all per-file checks.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

from .config import DEFAULT_SYMBOLS, OUTPUT_DIR, TIMEFRAMES
from .fetcher import normalize_timeframe
from .storage import load_parquet

logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────

# Max acceptable absolute log-return per candle before flagging as a spike
_SPIKE_THRESHOLD: dict[str, float] = {
    "1m": 0.10,
    "5m": 0.15,
    "15m": 0.20,
    "30m": 0.25,
    "1h": 0.30,
    "4h": 0.40,
    "1d": 0.50,
}
_DEFAULT_SPIKE_THRESHOLD = 0.30

# N or more consecutive identical Close values → stale/frozen feed
_STALE_REPEAT_MIN = 5

# Volume spike = volume > this multiple of the 30-period rolling median
_VOLUME_SPIKE_MULTIPLIER = 10

# Zero-volume candles above this % of total rows triggers a WARN
_ZERO_VOLUME_WARN_PCT = 1.0

_TF_MINUTES: dict[str, int] = {
    "1m": 1,
    "5m": 5,
    "15m": 15,
    "30m": 30,
    "1h": 60,
    "4h": 240,
    "1d": 1440,
}

# Trust-score penalty weights (max deduction per check, out of 100)
_WEIGHTS: dict[str, float] = {
    "ohlc_logic": 30.0,
    "price_integrity": 20.0,
    "completeness": 20.0,
    "duplicates": 10.0,
    "stale_prices": 10.0,
    "price_spikes": 5.0,
    "zero_volume": 3.0,
    "volume_spikes": 2.0,
}

_SAMPLE_ROWS = 10  # max flagged rows shown in the report


# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class CheckResult:
    name: str
    status: str              # "PASS" | "WARN" | "FAIL"
    affected: int
    total: int
    detail: str = ""
    flagged: pd.DataFrame = field(default_factory=pd.DataFrame)

    @property
    def pct(self) -> float:
        return round(self.affected / self.total * 100, 3) if self.total else 0.0

    @property
    def icon(self) -> str:
        return {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}.get(self.status, "?")


# ── Individual check functions ────────────────────────────────────────────────

def check_completeness(df: pd.DataFrame, tf: str) -> CheckResult:
    """Measure how many expected candles are missing and locate the gaps."""
    minutes = _TF_MINUTES.get(tf)
    if not minutes:
        return CheckResult("Completeness", "WARN", 0, len(df), detail=f"Unknown timeframe '{tf}'")

    freq = f"{minutes}min"
    full_idx = pd.date_range(df.index.min(), df.index.max(), freq=freq, tz="UTC")
    missing = full_idx.difference(df.index)
    pct_complete = round((1 - len(missing) / len(full_idx)) * 100, 3) if len(full_idx) else 100.0

    if len(missing) == 0:
        status = "PASS"
        detail = f"100% complete ({len(df):,} rows)"
    elif pct_complete >= 99.0:
        status = "WARN"
        detail = f"{pct_complete}% complete — {len(missing):,} missing candle(s)"
    else:
        status = "FAIL"
        detail = f"{pct_complete}% complete — {len(missing):,} missing candle(s)"

    # Build a sample gap table: show start/end of each contiguous gap block
    gap_df = pd.DataFrame()
    if len(missing) > 0:
        gaps: list[dict] = []
        block_start = missing[0]
        block_end = missing[0]
        for ts in missing[1:]:
            if ts - block_end <= pd.Timedelta(minutes=minutes):
                block_end = ts
            else:
                gaps.append({"gap_start": block_start, "gap_end": block_end,
                              "missing_candles": int((block_end - block_start).total_seconds() / 60 / minutes) + 1})
                block_start = block_end = ts
        gaps.append({"gap_start": block_start, "gap_end": block_end,
                     "missing_candles": int((block_end - block_start).total_seconds() / 60 / minutes) + 1})
        gap_df = pd.DataFrame(gaps).head(_SAMPLE_ROWS)

    return CheckResult("Completeness", status, len(missing), len(full_idx), detail=detail, flagged=gap_df)


def check_duplicates(df: pd.DataFrame) -> CheckResult:
    mask = df.index.duplicated(keep="first")
    affected = int(mask.sum())
    status = "FAIL" if affected else "PASS"
    flagged = df[mask].head(_SAMPLE_ROWS)[["Open", "High", "Low", "Close", "Volume"]] if affected else pd.DataFrame()
    return CheckResult("Duplicate timestamps", status, affected, len(df),
                       detail=f"{affected} duplicate timestamp(s)", flagged=flagged)


def check_price_integrity(df: pd.DataFrame) -> CheckResult:
    """Flag zero or negative values in any OHLC column."""
    ohlc = df[["Open", "High", "Low", "Close"]]
    mask = (ohlc <= 0).any(axis=1)
    affected = int(mask.sum())
    status = "FAIL" if affected else "PASS"
    flagged = df[mask].head(_SAMPLE_ROWS)[["Open", "High", "Low", "Close", "Volume"]] if affected else pd.DataFrame()
    return CheckResult("Zero / negative prices", status, affected, len(df),
                       detail=f"{affected} candle(s) with zero or negative OHLC", flagged=flagged)


def check_ohlc_logic(df: pd.DataFrame) -> CheckResult:
    """All five OHLC consistency constraints."""
    h, l, o, c = df["High"], df["Low"], df["Open"], df["Close"]
    mask = (h < l) | (h < o) | (h < c) | (l > o) | (l > c)
    affected = int(mask.sum())
    status = "FAIL" if affected else "PASS"
    flagged = df[mask].head(_SAMPLE_ROWS)[["Open", "High", "Low", "Close"]] if affected else pd.DataFrame()
    return CheckResult("OHLC logic", status, affected, len(df),
                       detail=f"{affected} violation(s) (High<Low/Open/Close or Low>Open/Close)",
                       flagged=flagged)


def check_price_spikes(df: pd.DataFrame, tf: str) -> CheckResult:
    """Flag candles where the absolute log-return exceeds the tf threshold."""
    if len(df) < 2:
        return CheckResult("Price spikes", "PASS", 0, len(df), detail="Insufficient data")

    threshold = _SPIKE_THRESHOLD.get(tf, _DEFAULT_SPIKE_THRESHOLD)
    log_ret = np.log(df["Close"] / df["Close"].shift(1)).abs()
    mask = log_ret > threshold
    affected = int(mask.sum())

    status = "PASS" if affected == 0 else ("WARN" if affected / len(df) < 0.01 else "FAIL")
    flagged = pd.DataFrame()
    if affected:
        tmp = df[mask].copy()
        tmp["abs_log_return"] = log_ret[mask].round(4)
        flagged = tmp.head(_SAMPLE_ROWS)[["Open", "High", "Low", "Close", "abs_log_return"]]

    return CheckResult(
        f"Price spikes (|log-ret| > {threshold:.0%})",
        status, affected, len(df),
        detail=f"{affected} spike(s) above {threshold:.0%} threshold",
        flagged=flagged,
    )


def check_stale_prices(df: pd.DataFrame) -> CheckResult:
    """Detect runs of N+ consecutive identical Close values (frozen feed)."""
    close = df["Close"]
    # Encode run-length: each change in close resets the group
    groups = (close != close.shift()).cumsum()
    run_lengths = groups.map(groups.value_counts())
    mask = run_lengths >= _STALE_REPEAT_MIN
    affected = int(mask.sum())
    status = "FAIL" if affected else "PASS"
    flagged = df[mask].head(_SAMPLE_ROWS)[["Open", "High", "Low", "Close", "Volume"]] if affected else pd.DataFrame()
    return CheckResult(
        f"Stale prices (≥{_STALE_REPEAT_MIN} repeats)",
        status, affected, len(df),
        detail=f"{affected} candle(s) inside a frozen-price run",
        flagged=flagged,
    )


def check_zero_volume(df: pd.DataFrame) -> CheckResult:
    mask = df["Volume"] == 0
    affected = int(mask.sum())
    pct = affected / len(df) * 100 if len(df) else 0
    status = "PASS" if pct == 0 else ("WARN" if pct <= _ZERO_VOLUME_WARN_PCT else "FAIL")
    flagged = df[mask].head(_SAMPLE_ROWS)[["Open", "High", "Low", "Close", "Volume"]] if affected else pd.DataFrame()
    return CheckResult("Zero volume", status, affected, len(df),
                       detail=f"{affected} zero-volume candle(s) ({pct:.2f}%)", flagged=flagged)


def check_volume_spikes(df: pd.DataFrame) -> CheckResult:
    """Flag candles where volume exceeds N× the 30-period rolling median."""
    if len(df) < 31:
        return CheckResult("Volume spikes", "PASS", 0, len(df), detail="Insufficient data for rolling median")

    rolling_med = df["Volume"].rolling(30, min_periods=10).median()
    # Avoid division by zero on zero-median windows
    safe_med = rolling_med.replace(0, np.nan)
    ratio = df["Volume"] / safe_med
    mask = ratio > _VOLUME_SPIKE_MULTIPLIER
    affected = int(mask.sum())
    status = "PASS" if not affected else "WARN"
    flagged = pd.DataFrame()
    if affected:
        tmp = df[mask].copy()
        tmp["volume_ratio"] = ratio[mask].round(1)
        flagged = tmp.head(_SAMPLE_ROWS)[["Open", "High", "Low", "Close", "Volume", "volume_ratio"]]
    return CheckResult(
        f"Volume spikes (>{_VOLUME_SPIKE_MULTIPLIER}× rolling median)",
        status, affected, len(df),
        detail=f"{affected} spike(s) above {_VOLUME_SPIKE_MULTIPLIER}× rolling median",
        flagged=flagged,
    )


def check_return_profile(df: pd.DataFrame) -> CheckResult:
    """Compute log-return statistics and flag extreme skew / kurtosis."""
    if len(df) < 10:
        return CheckResult("Return profile", "WARN", 0, len(df), detail="Insufficient data")

    log_ret = np.log(df["Close"] / df["Close"].shift(1)).dropna()
    mean = float(log_ret.mean())
    std = float(log_ret.std())
    skew = float(log_ret.skew())
    kurt = float(log_ret.kurtosis())  # excess kurtosis

    issues = []
    if abs(skew) > 3:
        issues.append(f"high skew ({skew:.2f})")
    if kurt > 20:
        issues.append(f"extreme kurtosis ({kurt:.1f})")

    status = "WARN" if issues else "PASS"
    detail = (
        f"mean={mean:.5f}  std={std:.5f}  skew={skew:.2f}  excess-kurt={kurt:.1f}"
        + (f"  ⚠ {', '.join(issues)}" if issues else "")
    )
    return CheckResult("Return profile", status, len(issues), len(df), detail=detail)


# ── Composite audit ───────────────────────────────────────────────────────────

def run_audit(df: pd.DataFrame, symbol: str, tf: str) -> List[CheckResult]:
    """Run all checks and return an ordered list of CheckResult objects."""
    return [
        check_completeness(df, tf),
        check_duplicates(df),
        check_price_integrity(df),
        check_ohlc_logic(df),
        check_price_spikes(df, tf),
        check_stale_prices(df),
        check_zero_volume(df),
        check_volume_spikes(df),
        check_return_profile(df),
    ]


def compute_trust_score(results: List[CheckResult]) -> float:
    """Weighted trust score 0–100 based on check outcomes.

    Each check has a max deduction.  The deduction scales proportionally with
    the fraction of affected rows (so 1 bad candle out of 10,000 barely dents
    the score), except for FAIL statuses on critical checks which apply the
    full deduction immediately.
    """
    score = 100.0
    check_weights = {
        "OHLC logic": _WEIGHTS["ohlc_logic"],
        "Zero / negative prices": _WEIGHTS["price_integrity"],
        "Completeness": _WEIGHTS["completeness"],
        "Duplicate timestamps": _WEIGHTS["duplicates"],
        f"Stale prices (≥{_STALE_REPEAT_MIN} repeats)": _WEIGHTS["stale_prices"],
    }
    spike_key = next((r.name for r in results if r.name.startswith("Price spikes")), None)
    vol_key = next((r.name for r in results if r.name.startswith("Volume spikes")), None)
    zvol_key = "Zero volume"

    if spike_key:
        check_weights[spike_key] = _WEIGHTS["price_spikes"]
    if vol_key:
        check_weights[vol_key] = _WEIGHTS["volume_spikes"]
    check_weights[zvol_key] = _WEIGHTS["zero_volume"]

    for r in results:
        max_ded = check_weights.get(r.name, 0.0)
        if max_ded == 0.0:
            continue
        if r.status == "PASS":
            continue
        # Proportional deduction: fraction affected × max weight, but FAIL on
        # critical checks deducts the full weight immediately.
        fraction = r.pct / 100.0
        if r.status == "FAIL" and r.name in ("OHLC logic", "Zero / negative prices"):
            deduction = max_ded if fraction > 0 else 0.0
        else:
            deduction = max_ded * min(1.0, fraction * 10)  # amplify small %
        score -= deduction

    return round(max(0.0, score), 1)


# ── Report writer ─────────────────────────────────────────────────────────────

def save_audit_report(
    coin_dir: Path,
    symbol: str,
    tf: str,
    results: List[CheckResult],
    trust_score: float,
    source_file: str = "",
) -> Path:
    """Write a per-tf Markdown audit report to <coin_dir>/<symbol>_<tf>_audit_report.md."""
    coin_dir.mkdir(parents=True, exist_ok=True)
    report_path = coin_dir / f"{symbol}_{tf}_audit_report.md"
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    total_rows = results[0].total if results else 0
    score_emoji = "🟢" if trust_score >= 90 else ("🟡" if trust_score >= 70 else "🔴")

    lines: list[str] = [
        f"# Audit Report — {symbol} {tf}",
        "",
        f"Generated : {generated_at}",
        f"Source    : {source_file or 'n/a'}",
        f"Rows      : {total_rows:,}",
        "",
        f"## {score_emoji} Trust Score: {trust_score:.1f} / 100",
        "",
        "## Summary",
        "",
        "| Check | Status | Affected | % of rows |",
        "|-------|--------|:--------:|----------:|",
    ]

    for r in results:
        lines.append(
            f"| {r.name} | {r.icon} {r.status} | {r.affected:,} | {r.pct:.3f}% |"
        )

    lines += ["", "---", "", "## Check Details", ""]

    for r in results:
        lines += [f"### {r.icon} {r.name}", "", f"{r.detail}", ""]
        if not r.flagged.empty:
            lines += [
                f"_First {min(_SAMPLE_ROWS, len(r.flagged))} flagged rows:_",
                "",
                r.flagged.to_markdown(),
                "",
            ]

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    logger.info("Audit report saved: %s  (trust score: %.1f)", report_path, trust_score)
    return report_path


# ── Convenience entry points ──────────────────────────────────────────────────

def audit_coin(
    symbol: str,
    tf: str,
    output_dir: Path = OUTPUT_DIR,
) -> float:
    """Load the latest parquet for symbol+tf, run the full audit, save report.

    Returns the trust score (0–100).
    """
    tf_norm = normalize_timeframe(tf)
    coin_dir = output_dir / symbol
    matches = sorted(coin_dir.glob(f"{symbol}_{tf_norm}_start_*_end_*.parquet"))
    if not matches:
        raise FileNotFoundError(f"No data found for {symbol} {tf_norm} in {coin_dir}")

    parquet_path = matches[-1]
    df = load_parquet(parquet_path)
    results = run_audit(df, symbol, tf_norm)
    trust_score = compute_trust_score(results)
    save_audit_report(coin_dir, symbol, tf_norm, results, trust_score, source_file=parquet_path.name)
    return trust_score


def audit_all(
    symbols: list[str] = DEFAULT_SYMBOLS,
    timeframes: list[str] = TIMEFRAMES,
    output_dir: Path = OUTPUT_DIR,
) -> dict[tuple[str, str], float]:
    """Run audit_coin for every symbol × timeframe that has data on disk.

    Returns a dict mapping (symbol, tf) → trust_score.
    """
    scores: dict[tuple[str, str], float] = {}
    for symbol in symbols:
        for tf in timeframes:
            tf_norm = normalize_timeframe(tf)
            try:
                score = audit_coin(symbol, tf_norm, output_dir)
                scores[(symbol, tf_norm)] = score
            except FileNotFoundError:
                logger.debug("No data for %s %s — skipping audit", symbol, tf_norm)
            except Exception as exc:
                logger.error("Audit failed for %s %s: %s", symbol, tf_norm, exc)
    return scores


# ── Cross-timeframe consistency check ────────────────────────────────────────

# pandas resample rule for each TF (1m is ground truth, not resampled)
_RESAMPLE_RULES: dict[str, str] = {
    "5m": "5min",
    "15m": "15min",
    "30m": "30min",
    "1h": "1h",
    "4h": "4h",
    "1d": "1D",
}


@dataclass
class TFMismatch:
    """Result of comparing one higher-TF file against resampled 1m data."""

    tf: str
    common_candles: int
    mismatches: int
    by_column: dict[str, int]
    flagged: pd.DataFrame = field(default_factory=pd.DataFrame)

    @property
    def mismatch_pct(self) -> float:
        if self.common_candles == 0:
            return 0.0
        return round(self.mismatches / self.common_candles * 100, 3)

    @property
    def status(self) -> str:
        if self.mismatches == 0:
            return "PASS"
        # <0.1% mismatches: only warn (boundary-millisecond edge cases are possible)
        if self.mismatch_pct < 0.1:
            return "WARN"
        return "FAIL"

    @property
    def icon(self) -> str:
        return {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}.get(self.status, "?")


def _resample_1m_to(df_1m: pd.DataFrame, tf: str) -> pd.DataFrame:
    """Resample 1-minute OHLCV DataFrame to the target timeframe."""
    rule = _RESAMPLE_RULES.get(tf)
    if rule is None:
        raise ValueError(f"No resample rule defined for timeframe '{tf}'")
    resampled = (
        df_1m.resample(rule, closed="left", label="left")
        .agg({"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"})
        .dropna(subset=["Open"])
    )
    return resampled


def _compare_candles(
    resampled: pd.DataFrame,
    actual: pd.DataFrame,
    tf: str,
    ohlc_rtol: float,
    vol_rtol: float,
) -> TFMismatch:
    """Compare resampled 1m data against the actual downloaded TF file."""
    common_idx = resampled.index.intersection(actual.index)
    zero_result = TFMismatch(tf, 0, 0, {c: 0 for c in ["Open", "High", "Low", "Close", "Volume"]})
    if common_idx.empty:
        return zero_result

    r = resampled.loc[common_idx]
    a = actual.loc[common_idx]

    mismatch_rows: list[dict] = []
    by_column: dict[str, int] = {}

    for col in ["Open", "High", "Low", "Close", "Volume"]:
        rtol = vol_rtol if col == "Volume" else ohlc_rtol
        matches = np.isclose(r[col].values, a[col].values, rtol=rtol, atol=0)
        col_mismatches = int((~matches).sum())
        by_column[col] = col_mismatches

        if col_mismatches:
            bad_idx = common_idx[~matches]
            for ts in bad_idx[:_SAMPLE_ROWS]:
                r_val = float(r.at[ts, col])
                a_val = float(a.at[ts, col])
                denom = max(abs(a_val), 1e-10)
                mismatch_rows.append(
                    {
                        "timestamp": ts,
                        "column": col,
                        "from_1m": r_val,
                        "actual": a_val,
                        "rel_diff_pct": round(abs(r_val - a_val) / denom * 100, 6),
                    }
                )

    total_mismatches = sum(by_column.values())
    flagged = pd.DataFrame(mismatch_rows) if mismatch_rows else pd.DataFrame()
    return TFMismatch(tf, len(common_idx), total_mismatches, by_column, flagged)


def cross_timeframe_check(
    symbol: str,
    output_dir: Path = OUTPUT_DIR,
    ohlc_rtol: float = 1e-6,
    vol_rtol: float = 1e-4,
) -> list[TFMismatch]:
    """Validate higher-TF candle files against 1m data resampled upward.

    Loads the 1m parquet for *symbol* as ground truth, resamples it to every
    other TF that has a parquet on disk in the same coin directory, and
    compares OHLCV column by column with the requested tolerances.

    Saves ``{symbol}_cross_tf_audit_report.md`` in the coin directory.

    Args:
        symbol:     Coin symbol, e.g. ``"BTCUSDT"``.
        output_dir: Root of the data directory (parent of coin directories).
        ohlc_rtol:  Relative tolerance for price columns (default 1e-6 ≈ exact).
        vol_rtol:   Relative tolerance for Volume (default 1e-4 = 0.01%).

    Returns:
        List of :class:`TFMismatch` objects, one per checked timeframe.

    Raises:
        FileNotFoundError: If no 1m parquet exists for *symbol*.
    """
    coin_dir = output_dir / symbol
    matches_1m = sorted(coin_dir.glob(f"{symbol}_1m_start_*_end_*.parquet"))
    if not matches_1m:
        raise FileNotFoundError(f"No 1m data found for {symbol} in {coin_dir}")

    df_1m = load_parquet(matches_1m[-1])
    logger.info("Loaded 1m data: %d rows for %s", len(df_1m), symbol)

    results: list[TFMismatch] = []
    for tf in list(_RESAMPLE_RULES.keys()):
        tf_files = sorted(coin_dir.glob(f"{symbol}_{tf}_start_*_end_*.parquet"))
        if not tf_files:
            logger.debug("No %s data for %s — skipping cross-TF check", tf, symbol)
            continue

        df_actual = load_parquet(tf_files[-1])
        try:
            df_resampled = _resample_1m_to(df_1m, tf)
        except ValueError as exc:
            logger.warning("Cannot resample 1m to %s: %s", tf, exc)
            continue

        mismatch = _compare_candles(df_resampled, df_actual, tf, ohlc_rtol, vol_rtol)
        results.append(mismatch)

        if mismatch.mismatches:
            logger.warning(
                "[%s] Cross-TF: %d/%d candles mismatch on %s vs resampled 1m",
                symbol,
                mismatch.mismatches,
                mismatch.common_candles,
                tf,
            )
        else:
            logger.info("[%s] Cross-TF: %s ✓ (%d candles match)", symbol, tf, mismatch.common_candles)

    save_cross_tf_report(coin_dir, symbol, results, df_1m)
    return results


def save_cross_tf_report(
    coin_dir: Path,
    symbol: str,
    results: list[TFMismatch],
    df_1m: pd.DataFrame,
) -> Path:
    """Write ``{symbol}_cross_tf_audit_report.md`` to *coin_dir*."""
    coin_dir.mkdir(parents=True, exist_ok=True)
    report_path = coin_dir / f"{symbol}_cross_tf_audit_report.md"
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    any_fail = any(r.status == "FAIL" for r in results)
    any_warn = any(r.status == "WARN" for r in results)
    overall = "❌ ISSUES FOUND" if any_fail else ("⚠️ WARNINGS" if any_warn else "✅ ALL PASS")

    lines: list[str] = [
        f"# Cross-Timeframe Consistency Report — {symbol}",
        "",
        f"Generated   : {generated_at}",
        f"Ground truth: 1m  ({len(df_1m):,} rows, "
        f"{df_1m.index.min().date()} → {df_1m.index.max().date()})",
        "",
        f"## {overall}",
        "",
        "> Each higher-TF candle is reconstructed by resampling the 1m data.",
        "> Mismatches between the reconstructed and downloaded candles indicate data errors.",
        "> Small volume differences (<0.01%) at period boundaries can be legitimate (WARN).",
        "",
        "## Summary",
        "",
        "| TF | Candles compared | Mismatches | % | Open | High | Low | Close | Volume | Status |",
        "|----|:----------------:|:----------:|:-:|:----:|:----:|:---:|:-----:|:------:|--------|",
    ]

    for r in results:
        bc = r.by_column
        lines.append(
            f"| {r.tf} "
            f"| {r.common_candles:,} "
            f"| {r.mismatches:,} "
            f"| {r.mismatch_pct:.3f}% "
            f"| {bc.get('Open', 0)} "
            f"| {bc.get('High', 0)} "
            f"| {bc.get('Low', 0)} "
            f"| {bc.get('Close', 0)} "
            f"| {bc.get('Volume', 0)} "
            f"| {r.icon} {r.status} |"
        )

    lines += ["", "---", "", "## Mismatch Details", ""]

    has_details = False
    for r in results:
        if r.flagged.empty:
            continue
        has_details = True
        lines += [
            f"### {r.icon} {r.tf} — {r.mismatches} mismatch(es)",
            "",
            f"_First {min(_SAMPLE_ROWS, len(r.flagged))} discrepancies:_",
            "",
            r.flagged.to_markdown(index=False),
            "",
        ]

    if not has_details:
        lines += ["_No mismatches found — all timeframes are consistent with the 1m ground truth._", ""]

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    logger.info("Cross-TF report saved: %s", report_path)
    return report_path


# ── Standalone runner ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import logging as _logging

    _logging.basicConfig(
        level=_logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    scores = audit_all()
    if scores:
        print("\n── Audit Summary ─────────────────────────────────")
        for (sym, tf), score in sorted(scores.items()):
            emoji = "🟢" if score >= 90 else ("🟡" if score >= 70 else "🔴")
            print(f"  {emoji}  {sym:12s} {tf:4s}  trust score: {score:.1f}")
    else:
        print("No data files found. Run main.py to download data first.")
