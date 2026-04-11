"""Volume Profile Value Area High (VAH) setup indicator (Setup Option B).

Volume Profile organises trading activity by price level rather than time.
The Value Area represents the range where `value_area_pct` (default 70%) of
session volume occurred.  Price trading above the Value Area High (VAH)
signals institutional acceptance of higher prices.

This module approximates the full Volume Profile from OHLCV data by binning
volume against the close price within each rolling lookback window.

Reference: Steidlmayer, J. P. (1991). Steidlmayer on Markets.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _vah_for_window(
    close_arr: np.ndarray,
    high_arr: np.ndarray,
    low_arr: np.ndarray,
    volume_arr: np.ndarray,
    n_bins: int,
    value_area_pct: float,
) -> float:
    """Compute the Value Area High for a single OHLCV window."""
    price_min = low_arr.min()
    price_max = high_arr.max()
    if price_max <= price_min or volume_arr.sum() == 0:
        return float("nan")

    bin_edges = np.linspace(price_min, price_max, n_bins + 1)
    vol_by_bin = np.zeros(n_bins)

    for i in range(len(close_arr)):
        # Distribute bar volume to the bin containing its close price.
        bin_idx = int(np.searchsorted(bin_edges[1:], close_arr[i]))
        bin_idx = min(bin_idx, n_bins - 1)
        vol_by_bin[bin_idx] += volume_arr[i]

    total_vol = vol_by_bin.sum()
    # Add bins highest-volume-first until the value area is filled.
    sorted_bin_idx = np.argsort(vol_by_bin)[::-1]
    cumvol = 0.0
    value_area_bins: list[int] = []
    for idx in sorted_bin_idx:
        cumvol += vol_by_bin[idx]
        value_area_bins.append(int(idx))
        if cumvol >= total_vol * value_area_pct:
            break

    vah_bin = max(value_area_bins)
    return float(bin_edges[vah_bin + 1])


def _val_for_window(
    close_arr: np.ndarray,
    high_arr: np.ndarray,
    low_arr: np.ndarray,
    volume_arr: np.ndarray,
    n_bins: int,
    value_area_pct: float,
) -> float:
    """Compute the Value Area Low for a single OHLCV window."""
    price_min = low_arr.min()
    price_max = high_arr.max()
    if price_max <= price_min or volume_arr.sum() == 0:
        return float("nan")

    bin_edges = np.linspace(price_min, price_max, n_bins + 1)
    vol_by_bin = np.zeros(n_bins)

    for i in range(len(close_arr)):
        bin_idx = int(np.searchsorted(bin_edges[1:], close_arr[i]))
        bin_idx = min(bin_idx, n_bins - 1)
        vol_by_bin[bin_idx] += volume_arr[i]

    total_vol = vol_by_bin.sum()
    sorted_bin_idx = np.argsort(vol_by_bin)[::-1]
    cumvol = 0.0
    value_area_bins: list[int] = []
    for idx in sorted_bin_idx:
        cumvol += vol_by_bin[idx]
        value_area_bins.append(int(idx))
        if cumvol >= total_vol * value_area_pct:
            break

    val_bin = min(value_area_bins)
    return float(bin_edges[val_bin])


def compute_vah_series(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    volume: pd.Series,
    session_bars: int = 24,
    lookback_sessions: int = 3,
    n_bins: int = 20,
    value_area_pct: float = 0.70,
) -> pd.Series:
    """Compute a rolling Value Area High series.

    For each bar, the VAH is derived from the last
    `session_bars × lookback_sessions` bars.

    Args:
        session_bars:       Bars per session (e.g. 24 for a 24-hour session at 1h).
        lookback_sessions:  How many full sessions to include in the profile.
        n_bins:             Price bins for the volume histogram.
        value_area_pct:     Fraction of volume that defines the Value Area.
    """
    lookback = session_bars * lookback_sessions
    vah = pd.Series(float("nan"), index=close.index, dtype=float)

    h_arr = high.to_numpy(dtype=float)
    l_arr = low.to_numpy(dtype=float)
    c_arr = close.to_numpy(dtype=float)
    v_arr = volume.to_numpy(dtype=float)

    for i in range(lookback - 1, len(c_arr)):
        s = i - lookback + 1
        vah.iloc[i] = _vah_for_window(
            c_arr[s : i + 1],
            h_arr[s : i + 1],
            l_arr[s : i + 1],
            v_arr[s : i + 1],
            n_bins,
            value_area_pct,
        )

    return vah


def compute_val_series(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    volume: pd.Series,
    session_bars: int = 24,
    lookback_sessions: int = 3,
    n_bins: int = 20,
    value_area_pct: float = 0.70,
) -> pd.Series:
    """Compute a rolling Value Area Low series.

    Short-side mirror of compute_vah_series().  For each bar, the VAL is
    the lower edge of the lowest high-volume bin within the lookback window.

    Args:
        session_bars:       Bars per session (e.g. 24 for a 24-hour session at 1h).
        lookback_sessions:  How many full sessions to include in the profile.
        n_bins:             Price bins for the volume histogram.
        value_area_pct:     Fraction of volume that defines the Value Area.
    """
    lookback = session_bars * lookback_sessions
    val = pd.Series(float("nan"), index=close.index, dtype=float)

    h_arr = high.to_numpy(dtype=float)
    l_arr = low.to_numpy(dtype=float)
    c_arr = close.to_numpy(dtype=float)
    v_arr = volume.to_numpy(dtype=float)

    for i in range(lookback - 1, len(c_arr)):
        s = i - lookback + 1
        val.iloc[i] = _val_for_window(
            c_arr[s : i + 1],
            h_arr[s : i + 1],
            l_arr[s : i + 1],
            v_arr[s : i + 1],
            n_bins,
            value_area_pct,
        )

    return val


def setup_is_below_val(
    close: pd.Series,
    val: pd.Series,
    consecutive_bars: int = 2,
) -> pd.Series:
    """True when close has been below the VAL for `consecutive_bars` bars.

    Price trading below the Value Area Low signals that the market has rejected
    fair value and is searching for liquidity at lower levels — a bearish
    structural confirmation for short entries.
    """
    below = (close < val).astype(int)
    return (below.rolling(consecutive_bars).min() == 1).fillna(False)


def setup_is_above_vah(
    close: pd.Series,
    vah: pd.Series,
    consecutive_bars: int = 2,
) -> pd.Series:
    """True when close has been above the VAH for `consecutive_bars` bars.

    Requiring two consecutive closes above the VAH filters out single-bar
    false breakouts ("bull traps") — as specified in the strategy description.
    """
    above = (close > vah).astype(int)
    # Rolling min over consecutive_bars: True only if ALL recent bars are above.
    return (above.rolling(consecutive_bars).min() == 1).fillna(False)
