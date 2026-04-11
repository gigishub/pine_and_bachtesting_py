"""Relative Strength setup indicator (Setup Option C).

Compares an asset's 24-hour return against a benchmark (typically BTC/USDT)
to identify assets showing disproportionate capital inflow.  Only assets that
are 'leading' the benchmark qualify for entry, increasing the probability of
outsized gains during a broad market rally.

Mathematical condition:
    Token_Returns(24h) > BTC_Returns(24h) × multiplier
    AND Token/BTC ratio is above its `ratio_sma_period`-bar SMA.

Reference: Pring, M. J. (2002). Technical Analysis Explained.
"""

from __future__ import annotations

import pandas as pd


def compute_returns(close: pd.Series, period: int = 24) -> pd.Series:
    """Percentage return over the last `period` bars."""
    return close.pct_change(period).astype(float)


def compute_ratio_sma(
    close: pd.Series,
    benchmark_close: pd.Series,
    sma_period: int = 20,
) -> tuple[pd.Series, pd.Series]:
    """Return (token/benchmark ratio, SMA of that ratio).

    Both series share the index of `close`.
    """
    ratio = (close / benchmark_close.reindex(close.index, method="ffill")).astype(float)
    ratio_sma = ratio.rolling(sma_period).mean()
    return ratio, ratio_sma


def setup_is_relatively_strong(
    close: pd.Series,
    benchmark_close: pd.Series,
    period: int = 24,
    multiplier: float = 1.5,
    ratio_sma_period: int = 20,
) -> pd.Series:
    """True when the asset shows relative strength vs. the benchmark.

    Args:
        close:            OHLCV close for the asset being traded.
        benchmark_close:  Close for the benchmark (e.g. BTC/USDT), aligned
                          to the same DatetimeIndex.
        period:           Look-back bars for the return comparison.
        multiplier:       Token return must exceed benchmark × this value.
        ratio_sma_period: Bars for the token/benchmark ratio SMA.
    """
    token_ret = compute_returns(close, period)
    bench_ret = compute_returns(benchmark_close.reindex(close.index, method="ffill"), period)

    excess_strength = token_ret > (bench_ret * multiplier)

    ratio, ratio_sma = compute_ratio_sma(close, benchmark_close, ratio_sma_period)
    ratio_above_sma = ratio > ratio_sma

    return (excess_strength & ratio_above_sma).fillna(False)
