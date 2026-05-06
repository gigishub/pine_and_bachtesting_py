"""
Vectorised short-trade outcome engine.

For each bar where *entry_mask* is True, simulates a short trade:
  - Stop loss:   entry_price + stop_atr_mult  * ATR
  - Take profit: entry_price - target_atr_mult * ATR

The forward scan looks bar-by-bar until the trade hits stop, hits target,
or the data ends (open trade → excluded from stats so neither side is penalised).
There is intentionally NO bar timeout — both candidate and baseline are evaluated
under identical conditions so the comparison is fair.

Typical usage
-------------
    result = compute_outcomes(
        df            = ltf_df,
        entry_mask    = regime_mask,
        baseline_mask = all_bars_mask,
        atr_period    = 7,
        stop_mult     = 2.0,
        target_mult   = 3.0,
    )
    print(result.candidate_pf, result.baseline_pf, result.pf_lift)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd


@dataclass
class OutcomeResult:
    """Aggregated statistics for a candidate vs its baseline."""

    # Candidate (the indicator under test)
    candidate_n:       int   = 0
    candidate_wins:    int   = 0
    candidate_losses:  int   = 0
    candidate_wr:      float = 0.0
    candidate_pf:      float = 0.0
    candidate_coverage: float = 0.0  # fraction of baseline bars
    candidate_avg_dur: float = 0.0   # avg bars held per resolved trade

    # Baseline (random entries on the baseline population)
    baseline_n:       int   = 0
    baseline_wins:    int   = 0
    baseline_losses:  int   = 0
    baseline_wr:      float = 0.0
    baseline_pf:      float = 0.0
    baseline_avg_dur: float = 0.0    # avg bars held per resolved trade

    # Lift (candidate vs baseline)
    pf_lift:  float = 0.0
    wr_lift:  float = 0.0

    raw_entries: pd.Series = field(default_factory=pd.Series)  # entry timestamps


def compute_atr(close: pd.Series, high: pd.Series, low: pd.Series, period: int) -> pd.Series:
    """Wilder ATR (same result as most charting platforms).

    Parameters
    ----------
    close:  Closing prices.
    high:   High prices.
    low:    Low prices.
    period: Smoothing window (e.g. 7, 14).

    Returns
    -------
    pd.Series of ATR values (NaN for warm-up bars).
    """
    prev_close = close.shift(1)
    tr = pd.concat(
        [
            high - low,
            (high - prev_close).abs(),
            (low  - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()


def _simulate_trades(
    close: np.ndarray,
    high:  np.ndarray,
    low:   np.ndarray,
    atr:   np.ndarray,
    entry_indices: np.ndarray,
    stop_mult:   float,
    target_mult: float,
) -> tuple[list[float], list[float], list[int]]:
    """
    Forward-scan simulator for short trades.

    Scans forward from each entry until stop or target is hit, or data ends.
    Trades still open at end of data are excluded (no artificial timeout).

    Returns (gross_wins, gross_losses, durations_bars) where durations_bars is
    the number of bars each resolved trade was held.
    """
    wins:      list[float] = []
    losses:    list[float] = []
    durations: list[int]   = []
    n = len(close)

    for idx in entry_indices:
        entry_price = close[idx]
        atr_val     = atr[idx]
        if np.isnan(atr_val) or entry_price <= 0:
            continue

        stop_price   = entry_price + stop_mult   * atr_val
        target_price = entry_price - target_mult * atr_val

        for j in range(idx + 1, n):
            bar_high = high[j]
            bar_low  = low[j]

            hit_stop   = bar_high >= stop_price
            hit_target = bar_low  <= target_price

            if hit_target and hit_stop:
                # Ambiguous bar — conservative: count as loss.
                losses.append(stop_mult)
                durations.append(j - idx)
                break
            elif hit_target:
                wins.append(target_mult)
                durations.append(j - idx)
                break
            elif hit_stop:
                losses.append(stop_mult)
                durations.append(j - idx)
                break
        # Data ended before resolution → open trade, excluded from stats.

    return wins, losses, durations


def _profit_factor(wins: list[float], losses: list[float]) -> float:
    total_loss = sum(losses)
    return round(sum(wins) / total_loss, 3) if total_loss > 0 else float("inf")


def _win_rate(wins: list[float], losses: list[float]) -> float:
    total = len(wins) + len(losses)
    return round(len(wins) / total, 4) if total > 0 else 0.0


def compute_outcomes(
    df:            pd.DataFrame,
    entry_mask:    pd.Series,
    baseline_mask: pd.Series,
    atr_period:    int   = 7,
    stop_mult:     float = 2.0,
    target_mult:   float = 3.0,
) -> OutcomeResult:
    """
    Compute candidate vs baseline outcome statistics.

    Parameters
    ----------
    df:             OHLCV DataFrame with columns open/high/low/close.
    entry_mask:     Boolean Series — True where the candidate indicator fires.
    baseline_mask:  Boolean Series — True for the baseline population (e.g. all
                    bars for the regime phase, regime-only bars for setup phase).
    atr_period:     ATR smoothing period (warm-up bars are excluded as entries).
    stop_mult:      ATR multiples for stop loss.
    target_mult:    ATR multiples for take-profit target.

    Returns
    -------
    OutcomeResult with candidate and baseline statistics plus lift metrics.
    Trades still open at the end of data are excluded from both sides equally.
    """
    atr = compute_atr(df["close"], df["high"], df["low"], atr_period)

    # Warm-up mask: exclude bars where ATR is still NaN.
    warm = atr.notna()

    candidate_mask_clean = entry_mask    & warm
    baseline_mask_clean  = baseline_mask & warm

    close = df["close"].values
    high  = df["high"].values
    low   = df["low"].values
    atr_v = atr.values

    cand_idx = np.where(candidate_mask_clean.values)[0]
    base_idx = np.where(baseline_mask_clean.values)[0]

    c_wins, c_losses, c_durs = _simulate_trades(close, high, low, atr_v, cand_idx, stop_mult, target_mult)
    b_wins, b_losses, b_durs = _simulate_trades(close, high, low, atr_v, base_idx, stop_mult, target_mult)

    cand_n = len(c_wins) + len(c_losses)
    base_n = len(b_wins) + len(b_losses)

    c_pf = _profit_factor(c_wins, c_losses)
    b_pf = _profit_factor(b_wins, b_losses)
    c_wr = _win_rate(c_wins, c_losses)
    b_wr = _win_rate(b_wins, b_losses)

    c_avg_dur = round(sum(c_durs) / len(c_durs), 1) if c_durs else 0.0
    b_avg_dur = round(sum(b_durs) / len(b_durs), 1) if b_durs else 0.0

    coverage = round(candidate_mask_clean.sum() / baseline_mask_clean.sum(), 4) if baseline_mask_clean.sum() > 0 else 0.0

    return OutcomeResult(
        candidate_n        = cand_n,
        candidate_wins     = len(c_wins),
        candidate_losses   = len(c_losses),
        candidate_wr       = c_wr,
        candidate_pf       = c_pf,
        candidate_coverage = coverage,
        candidate_avg_dur  = c_avg_dur,
        baseline_n         = base_n,
        baseline_wins      = len(b_wins),
        baseline_losses    = len(b_losses),
        baseline_wr        = b_wr,
        baseline_pf        = b_pf,
        baseline_avg_dur   = b_avg_dur,
        pf_lift            = round(c_pf - b_pf, 3) if b_pf != float("inf") else 0.0,
        wr_lift            = round(c_wr - b_wr, 4),
        raw_entries        = df.index[candidate_mask_clean],
    )
