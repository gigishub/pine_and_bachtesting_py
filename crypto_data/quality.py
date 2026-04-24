from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

# Minutes per timeframe — used to estimate the expected row count
_TF_MINUTES: dict[str, int] = {
    "1m": 1,
    "5m": 5,
    "15m": 15,
    "30m": 30,
    "1h": 60,
    "4h": 240,
    "1d": 1440,
}


def _expected_rows(tf: str, start: pd.Timestamp, end: pd.Timestamp) -> int:
    minutes = _TF_MINUTES.get(tf)
    if minutes is None:
        return 0
    total_minutes = (end - start).total_seconds() / 60
    # +1 to include both the start and end candle
    return max(1, int(total_minutes / minutes) + 1)


def check_quality(df: pd.DataFrame, symbol: str, tf: str) -> dict[str, Any]:
    """Run quality checks on an OHLCV DataFrame and log any warnings.

    Returns a dict of quality metrics for the given symbol + timeframe.
    """
    ohlcv_cols = ["Open", "High", "Low", "Close", "Volume"]
    nan_count = int(df[ohlcv_cols].isna().sum().sum())
    dup_count = int(df.index.duplicated().sum())

    start = df.index.min()
    end = df.index.max()
    expected = _expected_rows(tf, start, end)
    gap_count = max(0, expected - len(df))

    # High must be >= Open, Close, and Low on every candle
    ohlc_violations = int(
        (
            (df["High"] < df["Low"])
            | (df["High"] < df["Close"])
            | (df["High"] < df["Open"])
        ).sum()
    )

    completeness_pct = round(len(df) / expected * 100, 2) if expected > 0 else 0.0

    if nan_count:
        logger.warning("[%s %s] %d NaN value(s) detected", symbol, tf, nan_count)
    if dup_count:
        logger.warning("[%s %s] %d duplicate timestamp(s)", symbol, tf, dup_count)
    if gap_count:
        logger.warning(
            "[%s %s] %d missing row(s) — expected %d, got %d",
            symbol, tf, gap_count, expected, len(df),
        )
    if ohlc_violations:
        logger.warning(
            "[%s %s] %d OHLC sanity violation(s) (High < Open/Close/Low)",
            symbol, tf, ohlc_violations,
        )

    return {
        "symbol": symbol,
        "timeframe": tf,
        "rows": len(df),
        "expected_rows": expected,
        "nan_count": nan_count,
        "duplicate_timestamps": dup_count,
        "gap_count": gap_count,
        "ohlc_violations": ohlc_violations,
        "completeness_pct": completeness_pct,
        "start": str(start),
        "end": str(end),
    }


def save_quality_report(
    coin_dir: Path,
    symbol: str,
    tf_results: dict[str, dict[str, Any]],
) -> None:
    """Write (or overwrite) a Markdown quality report for all timeframes of a coin."""
    report_path = coin_dir / f"{symbol}_quality_report.md"
    coin_dir.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines: list[str] = [
        f"# Quality Report — {symbol}",
        f"",
        f"Generated: {generated_at}",
        f"",
        "| Timeframe | Rows | Expected | Completeness % | NaN | Duplicates | Gaps | OHLC Violations | Start | End |",
        "|-----------|-----:|---------:|---------------:|----:|-----------:|-----:|----------------:|-------|-----|",
    ]

    for tf, r in sorted(tf_results.items()):
        lines.append(
            f"| {r['timeframe']} "
            f"| {r['rows']:,} "
            f"| {r['expected_rows']:,} "
            f"| {r['completeness_pct']:.2f} "
            f"| {r['nan_count']} "
            f"| {r['duplicate_timestamps']} "
            f"| {r['gap_count']} "
            f"| {r['ohlc_violations']} "
            f"| {r['start'][:10]} "
            f"| {r['end'][:10]} |"
        )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    logger.info("Quality report saved: %s", report_path)
