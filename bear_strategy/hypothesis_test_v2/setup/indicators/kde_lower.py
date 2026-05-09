"""
kde_lower — Setup indicator.

What it measures
----------------
Uses a rolling Kernel Density Estimate to locate the lower-density peak of
recent closes and identifies the first bars where price closes below that
lower KDE level.

Signal contract
---------------
Returns True for the first *max_bars* bars after price closes below the
rolling KDE lower peak.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


def compute_kde_lower(
    closes: pd.Series,
    bandwidth: float = 0.15,
    lookback_bars: int = 200,
) -> pd.Series:
    """Rolling KDE lower-peak price level."""
    try:
        from scipy.stats import gaussian_kde
    except ImportError as exc:
        raise ImportError("scipy is required for kde_lower; install with: pip install scipy") from exc

    peaks = pd.Series(index=closes.index, dtype=float)

    for i in range(lookback_bars, len(closes)):
        window = closes.iloc[i - lookback_bars : i].dropna().values
        if len(window) < 10:
            continue

        price_range = window.max() - window.min()
        if price_range == 0:
            continue

        bw = bandwidth * price_range
        try:
            kde = gaussian_kde(window, bw_method=bw / window.std())
        except Exception:
            continue

        xs = np.linspace(window.min(), window.max(), 200)
        dens = kde(xs)
        median_price = np.median(window)

        lower_mask = xs <= median_price
        if not lower_mask.any():
            continue

        lower_peak_price = xs[lower_mask][np.argmax(dens[lower_mask])]
        peaks.iloc[i] = lower_peak_price

    return peaks


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    bandwidth = float(params.get("bandwidth", 0.15))
    lookback_bars = int(params.get("lookback_bars", 200))
    max_bars = int(params.get("max_bars", 5))

    lower_peak = compute_kde_lower(
        df["close"],
        bandwidth=bandwidth,
        lookback_bars=lookback_bars,
    )

    below_lower = (df["close"] < lower_peak).fillna(False)
    run_id = below_lower.ne(below_lower.shift()).cumsum()
    run_index = below_lower.groupby(run_id).cumcount()

    return (below_lower & (run_index < max_bars)).fillna(False)
