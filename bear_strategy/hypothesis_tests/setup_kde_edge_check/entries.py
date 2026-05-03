"""Population masks for the KDE Price Cluster Edge Check.

──────────────────────────────────────────────────────────────────────
KDE Signal Computation
──────────────────────────────────────────────────────────────────────

At each bar i, a rolling window of the last `window` Close prices is
fitted with scipy's gaussian_kde using Scott's rule bandwidth scaled by
`bandwidth_mult`.  The KDE curve is evaluated at `kde_n_points` evenly-
spaced prices between the window min and max.

Point of Control (POC / kde_peak):
    The price with the highest KDE density — the most-traded level
    over the lookback window.

Value Area (VA):
    The tightest price band around the POC containing `value_area_pct`
    (default 70%) of the total KDE density.  Computed by expanding
    outward from the peak index, greedily adding whichever adjacent
    side adds more density first.

Cluster count (n_clusters):
    Number of local maxima of the KDE curve, found via sign changes of
    the numerical derivative.  n_clusters == 1 means a single dominant
    price cluster; higher values indicate a fragmented, multi-modal
    distribution.

Peak height (kde_peak_height):
    The raw KDE density at the POC.  A tall, narrow peak means price
    has been pinned to that level for a long time — a structurally
    significant cluster.

──────────────────────────────────────────────────────────────────────
Filter Conditions (matching the spec)
──────────────────────────────────────────────────────────────────────

    setup_active_upper: open > kde_peak
        Price opens above the most-traded level.  In a bear regime this
        is a potential mean-reversion short setup against cluster resistance.

    setup_active_lower: close < kde_peak AND counter ≤ lower_duration
        Price closes below the POC AND it is within the first
        `lower_duration` bars since the breach began.  Counter resets
        whenever close returns above kde_peak.

──────────────────────────────────────────────────────────────────────
Populations
──────────────────────────────────────────────────────────────────────

    regime_only    — bear regime + ATR warm + KDE window full.
    kde_upper      — regime_only AND open > kde_peak  (setup_active_upper).
    kde_lower      — regime_only AND close < kde_peak (any duration).
    kde_lower_fresh— regime_only AND close < kde_peak AND counter ≤ lower_duration
                     (setup_active_lower).
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

from bear_strategy.hypothesis_tests.setup_kde_edge_check.config import TestConfig

logger = logging.getLogger(__name__)


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population, plus KDE metadata columns.

    Args:
        df: Entry-TF DataFrame with regime signal and ATR column attached.
        config: TestConfig instance.

    Returns:
        dict with keys: ``regime_only``, ``kde_upper``, ``kde_lower``,
        ``kde_lower_fresh``.
        All values are boolean pd.Series aligned to df's index.
    """
    _require_columns(df, [config.regime_col, "Close", "Open", "atr"])

    regime = df[config.regime_col].astype(bool)
    atr_ready = df["atr"].notna()

    # Check if KDE signals are already attached (from aligned higher TF)
    kde_signals_precomputed = (
        "setup_active_upper" in df.columns
        and "is_below_peak" in df.columns
        and "setup_active_lower" in df.columns
        and "kde_peak" in df.columns
    )

    if kde_signals_precomputed:
        # Use pre-computed signals (from aligned 4h KDE on 1h bars)
        kde_signals = {
            "kde_peak": df["kde_peak"],
            "setup_active_upper": df["setup_active_upper"],
            "is_below_peak": df["is_below_peak"],
            "setup_active_lower": df["setup_active_lower"],
        }
    else:
        # Compute KDE on entry-TF data (for testing entry_tf alone)
        kde_signals = _compute_kde_signals(
            close=df["Close"].to_numpy(dtype=float),
            open_=df["Open"].to_numpy(dtype=float),
            window=config.window,
            bandwidth_mult=config.bandwidth_mult,
            kde_n_points=config.kde_n_points,
            value_area_pct=config.value_area_pct,
            lower_duration=config.lower_duration,
            index=df.index,
        )

    kde_ready = kde_signals["kde_peak"].notna()
    eligible = regime & atr_ready & kde_ready

    return {
        "regime_only": eligible,
        "kde_upper": eligible & kde_signals["setup_active_upper"],
        "kde_lower": eligible & kde_signals["is_below_peak"],
        "kde_lower_fresh": eligible & kde_signals["setup_active_lower"],
    }


# ---------------------------------------------------------------------------
# KDE signal computation
# ---------------------------------------------------------------------------


def _compute_kde_signals(
    close: np.ndarray,
    open_: np.ndarray,
    window: int,
    bandwidth_mult: float,
    kde_n_points: int,
    value_area_pct: float,
    lower_duration: int,
    index: pd.Index,
) -> dict[str, pd.Series]:
    """Compute rolling KDE signals for every bar.

    Returns a dict of pd.Series (all indexed by `index`) with keys:
        kde_peak            — POC price (NaN before warm-up).
        kde_peak_height     — KDE density at the POC.
        value_area_low      — lower bound of the Value Area.
        value_area_high     — upper bound of the Value Area.
        n_clusters          — number of local density maxima.
        is_above_peak       — open > kde_peak.
        is_below_peak       — close < kde_peak.
        lower_counter       — consecutive bars close has been below kde_peak.
        setup_active_upper  — is_above_peak (open > kde_peak).
        setup_active_lower  — is_below_peak AND lower_counter ≤ lower_duration.
    """
    n = len(close)

    kde_peak_arr = np.full(n, np.nan)
    kde_peak_height_arr = np.full(n, np.nan)
    va_low_arr = np.full(n, np.nan)
    va_high_arr = np.full(n, np.nan)
    n_clusters_arr = np.zeros(n, dtype=int)
    is_above_peak = np.zeros(n, dtype=bool)
    is_below_peak = np.zeros(n, dtype=bool)
    lower_counter_arr = np.zeros(n, dtype=int)

    # --- Rolling KDE per bar -------------------------------------------
    for i in range(window - 1, n):
        window_closes = close[i - window + 1 : i + 1]
        x_min, x_max = window_closes.min(), window_closes.max()

        if x_max - x_min < 1e-10:
            # Degenerate window (all prices equal) — skip.
            continue

        try:
            bw_factor = bandwidth_mult
            kde_func = gaussian_kde(
                window_closes,
                bw_method=lambda k, f=bw_factor: k.scotts_factor() * f,
            )
        except Exception as exc:
            logger.debug("KDE fit failed at bar %d: %s", i, exc)
            continue

        x_space = np.linspace(x_min, x_max, kde_n_points)
        density = kde_func(x_space)

        # POC
        peak_idx = int(np.argmax(density))
        kde_peak_arr[i] = x_space[peak_idx]
        kde_peak_height_arr[i] = density[peak_idx]

        # Value Area — expand outward from peak until target density covered
        total = density.sum()
        target = value_area_pct * total
        lo = hi = peak_idx
        accumulated = density[peak_idx]
        while accumulated < target:
            lo_val = density[lo - 1] if lo > 0 else 0.0
            hi_val = density[hi + 1] if hi < kde_n_points - 1 else 0.0
            if lo_val == 0.0 and hi_val == 0.0:
                break
            if lo_val >= hi_val and lo > 0:
                lo -= 1
                accumulated += density[lo]
            elif hi < kde_n_points - 1:
                hi += 1
                accumulated += density[hi]
            else:
                lo -= 1
                accumulated += density[lo]
        va_low_arr[i] = x_space[lo]
        va_high_arr[i] = x_space[hi]

        # Cluster count via derivative sign changes (+ to - = local maximum)
        d_density = np.gradient(density, x_space)
        sign_chg = np.diff(np.sign(d_density))
        n_clusters_arr[i] = int(np.sum(sign_chg < 0))

        # Bar-level filter conditions
        is_above_peak[i] = open_[i] > kde_peak_arr[i]
        is_below_peak[i] = close[i] < kde_peak_arr[i]

    # --- Lower counter (state machine, independent pass) ------------------
    # Increment when close < kde_peak; reset to 0 when close ≥ kde_peak.
    for i in range(n):
        if np.isnan(kde_peak_arr[i]):
            continue
        prev = lower_counter_arr[i - 1] if i > 0 else 0
        lower_counter_arr[i] = (prev + 1) if is_below_peak[i] else 0

    setup_active_upper = is_above_peak
    setup_active_lower = is_below_peak & (lower_counter_arr <= lower_duration)

    def s(arr: np.ndarray) -> pd.Series:
        return pd.Series(arr, index=index)

    return {
        "kde_peak": s(kde_peak_arr),
        "kde_peak_height": s(kde_peak_height_arr),
        "value_area_low": s(va_low_arr),
        "value_area_high": s(va_high_arr),
        "n_clusters": s(n_clusters_arr),
        "is_above_peak": s(is_above_peak),
        "is_below_peak": s(is_below_peak),
        "lower_counter": s(lower_counter_arr),
        "setup_active_upper": s(setup_active_upper),
        "setup_active_lower": s(setup_active_lower),
    }


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Ensure runner._process_pair() has attached regime signals and ATR."
        )
