"""Aggregate analysis results into a single robustness verdict."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from strategy_evaluation.config import RobustnessConfig


@dataclass
class RobustnessResult:
    verdict: str                          # "ROBUST" | "MARGINAL" | "WEAK"
    symbol_pass_rates: dict[str, float]   # symbol → 0.0 or 1.0
    tf_pass_rates: dict[str, float]       # timeframe → 0.0–1.0
    toggle_frequency: dict[str, int]      # toggle → count in top combos
    decay_df: pd.DataFrame                # per-symbol/TF decay comparison
    avg_sqn_short: float
    avg_sqn_long: float
    symbol_rate: float                    # fraction of symbols that pass
    tf_rate: float                        # fraction of TFs that pass
    decay_flag_count: int
    notes: list[str] = field(default_factory=list)


def aggregate_verdict(
    symbol_rates: dict[str, float],
    tf_rates: dict[str, float],
    toggle_freq: dict[str, int],
    decay_df: pd.DataFrame,
    short_df: pd.DataFrame,
    long_df: pd.DataFrame,
    cfg: RobustnessConfig,
) -> RobustnessResult:
    """Combine all analysis outputs into a RobustnessResult with a verdict."""
    symbol_rate = sum(symbol_rates.values()) / len(symbol_rates) if symbol_rates else 0.0
    tf_rate = sum(tf_rates.values()) / len(tf_rates) if tf_rates else 0.0

    avg_sqn_short = _safe_mean_top1(short_df, cfg)
    avg_sqn_long = _safe_mean_top1(long_df, cfg)

    decay_flag_count = int(decay_df["decayed"].sum()) if not decay_df.empty else 0
    total_pairs = len(decay_df) if not decay_df.empty else 1
    decay_rate = decay_flag_count / total_pairs

    notes: list[str] = []

    # ── WEAK ────────────────────────────────────────────────────────────────
    is_weak = (
        symbol_rate < cfg.weak_symbol_rate
        or avg_sqn_long < cfg.weak_avg_sqn
        or decay_rate > 0.50  # majority of symbol/TF pairs show decay
    )

    # ── ROBUST ──────────────────────────────────────────────────────────────
    is_robust = (
        symbol_rate >= cfg.robust_symbol_rate
        and tf_rate >= cfg.robust_tf_rate
        and avg_sqn_long >= cfg.robust_avg_sqn
        and decay_rate <= 0.25
    )

    if is_weak:
        verdict = "WEAK"
        if symbol_rate < cfg.weak_symbol_rate:
            notes.append(f"Symbol pass rate {symbol_rate:.0%} is below weak threshold ({cfg.weak_symbol_rate:.0%}).")
        if avg_sqn_long < cfg.weak_avg_sqn:
            notes.append(f"Average SQN ({avg_sqn_long:.2f}) is below weak threshold ({cfg.weak_avg_sqn}).")
        if decay_rate > 0.50:
            notes.append(f"{decay_flag_count}/{total_pairs} symbol-TF pairs show performance decay.")
    elif is_robust:
        verdict = "ROBUST"
        notes.append("Strategy meets all robustness thresholds.")
    else:
        verdict = "MARGINAL"
        if symbol_rate < cfg.robust_symbol_rate:
            notes.append(f"Symbol pass rate {symbol_rate:.0%} below robust threshold ({cfg.robust_symbol_rate:.0%}).")
        if tf_rate < cfg.robust_tf_rate:
            notes.append(f"Timeframe pass rate {tf_rate:.0%} below robust threshold ({cfg.robust_tf_rate:.0%}).")
        if avg_sqn_long < cfg.robust_avg_sqn:
            notes.append(f"Average SQN ({avg_sqn_long:.2f}) below robust threshold ({cfg.robust_avg_sqn}).")
        if decay_rate > 0.25:
            notes.append(f"{decay_flag_count}/{total_pairs} symbol-TF pairs show performance decay.")

    return RobustnessResult(
        verdict=verdict,
        symbol_pass_rates=symbol_rates,
        tf_pass_rates=tf_rates,
        toggle_frequency=toggle_freq,
        decay_df=decay_df,
        avg_sqn_short=avg_sqn_short,
        avg_sqn_long=avg_sqn_long,
        symbol_rate=symbol_rate,
        tf_rate=tf_rate,
        decay_flag_count=decay_flag_count,
        notes=notes,
    )


def _safe_mean(df: pd.DataFrame, col: str) -> float:
    if col not in df.columns:
        return float("nan")
    series = pd.to_numeric(df[col], errors="coerce")
    return float(series.mean()) if not series.isna().all() else float("nan")


def _safe_mean_top1(df: pd.DataFrame, cfg: RobustnessConfig) -> float:
    """Average SQN of the best qualifying combo per (symbol, timeframe).

    Only combos that pass all thresholds (``_passes=True``) are considered so
    that low-trade outliers with inflated Expectancy do not inflate the average.
    Falls back to the full dataframe if ``_passes`` is not present.
    """
    source = df[df["_passes"]].copy() if "_passes" in df.columns else df.copy()
    if source.empty:
        return float("nan")
    key = [cfg.col_symbol, cfg.col_timeframe]
    top1 = (
        source.sort_values(cfg.col_rank)
        .groupby(key, as_index=False)
        .first()
    )
    return _safe_mean(top1, cfg.col_sqn)
