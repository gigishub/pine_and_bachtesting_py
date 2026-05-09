"""Session-based Volume Profile utility.

This implementation uses the previous completed session profile for the current
session bars, which avoids look-ahead and keeps levels stable intraday.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def compute_session_volume_profile(
    df: pd.DataFrame,
    price_bins: int = 100,
) -> dict[str, pd.Series]:
    """
    Compute volume profile metrics per UTC daily session.
    
    Returns dict with:
    - poc: Point of Control (price level with most volume in session)
    - hvn_high/hvn_low: High Volume Node zone (top 25% volume)
    - lvn_high/lvn_low: Low Volume Node zone (bottom 25% volume)
    - vah/val: Value Area High/Low (70% volume range)
    
    Levels for a session are sourced from the previous completed session,
    so there is no same-session look-ahead.
    """
    n = len(df)
    poc = np.full(n, np.nan)
    hvn_high = np.full(n, np.nan)
    hvn_low = np.full(n, np.nan)
    lvn_high = np.full(n, np.nan)
    lvn_low = np.full(n, np.nan)
    vah = np.full(n, np.nan)
    val = np.full(n, np.nan)
    
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    volume = df["volume"].values
    
    def _profile_for_indices(indices: np.ndarray) -> tuple[float, float, float, float, float, float, float]:
        if len(indices) == 0:
            return (np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)

        p_high = high[indices].max()
        p_low = low[indices].min()
        if p_high == p_low:
            return (np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)

        bin_edges = np.linspace(p_low, p_high, price_bins + 1)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bin_volumes = np.zeros(price_bins)

        for j in indices:
            typical_price = (high[j] + low[j] + close[j]) / 3
            bin_idx = np.searchsorted(bin_edges, typical_price, side="right") - 1
            if bin_idx < 0:
                bin_idx = 0
            elif bin_idx >= price_bins:
                bin_idx = price_bins - 1
            bin_volumes[bin_idx] += volume[j]

        total_vol = bin_volumes.sum()
        if total_vol <= 0:
            return (np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)

        non_zero_mask = bin_volumes > 0
        n_nonzero = int(non_zero_mask.sum())

        # Need at least 4 non-zero bins to compute meaningful HVN/LVN percentiles.
        # With 100 bins and only 6 bars (4h session), <10 bins ever get volume,
        # so np.percentile(all_bins, 25) == 0 and the (> 0) & (<= 0) filter is always empty.
        if n_nonzero < 4:
            return (np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)

        poc_idx = int(np.argmax(bin_volumes))
        poc_val = float(bin_centers[poc_idx])

        # HVN: top-25% of non-zero bins by volume
        hvn_threshold = np.percentile(bin_volumes[non_zero_mask], 75)
        hvn_bins = np.where(non_zero_mask & (bin_volumes >= hvn_threshold))[0]
        hvn_high_val = float(bin_centers[hvn_bins.max()]) if len(hvn_bins) > 0 else np.nan
        hvn_low_val = float(bin_centers[hvn_bins.min()]) if len(hvn_bins) > 0 else np.nan

        # LVN: bottom-25% of non-zero bins by volume (percentile among non-zero only).
        # Using all bins causes the 25th percentile to be 0, making the > 0 & <= 0 filter empty.
        lvn_threshold = np.percentile(bin_volumes[non_zero_mask], 25)
        lvn_bins = np.where(non_zero_mask & (bin_volumes <= lvn_threshold))[0]
        lvn_high_val = float(bin_centers[lvn_bins.max()]) if len(lvn_bins) > 0 else np.nan
        lvn_low_val = float(bin_centers[lvn_bins.min()]) if len(lvn_bins) > 0 else np.nan

        sorted_idx = np.argsort(bin_volumes)[::-1]
        cumsum_vol = 0.0
        va_bins: list[int] = []
        for idx in sorted_idx:
            cumsum_vol += float(bin_volumes[idx])
            va_bins.append(int(idx))
            if cumsum_vol >= total_vol * 0.70:
                break

        vah_val = float(bin_centers[max(va_bins)]) if va_bins else np.nan
        val_val = float(bin_centers[min(va_bins)]) if va_bins else np.nan
        return (poc_val, hvn_high_val, hvn_low_val, lvn_high_val, lvn_low_val, vah_val, val_val)

    sessions = df.index.normalize()
    session_labels = pd.Index(sessions.unique())
    session_indices = [np.where(sessions == s)[0] for s in session_labels]

    prior_profile: tuple[float, float, float, float, float, float, float] | None = None
    for idx, cur_indices in enumerate(session_indices):
        if prior_profile is not None:
            for j in cur_indices:
                poc[j] = prior_profile[0]
                hvn_high[j] = prior_profile[1]
                hvn_low[j] = prior_profile[2]
                lvn_high[j] = prior_profile[3]
                lvn_low[j] = prior_profile[4]
                vah[j] = prior_profile[5]
                val[j] = prior_profile[6]

        prior_profile = _profile_for_indices(cur_indices)
    
    return {
        "poc": pd.Series(poc, index=df.index),
        "hvn_high": pd.Series(hvn_high, index=df.index),
        "hvn_low": pd.Series(hvn_low, index=df.index),
        "lvn_high": pd.Series(lvn_high, index=df.index),
        "lvn_low": pd.Series(lvn_low, index=df.index),
        "vah": pd.Series(vah, index=df.index),
        "val": pd.Series(val, index=df.index),
    }
