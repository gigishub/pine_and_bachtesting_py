"""
Volume Profile utility — computes POC, HVN, LVN, VAL, VAH using a fixed rolling window.

No look-ahead: profile at bar i uses only bars [i-window, i-1].

Performance: global log-uniform price grid + cumulative-sum trick + fully vectorised
percentile computation.  No Python loop over bars.  Expected ~0.5 s on 13k-bar 4h series.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def compute_volume_profile(
    df: pd.DataFrame,
    window: int = 168,
    price_bins: int = 100,
) -> dict[str, pd.Series]:
    """
    Rolling fixed-range volume profile.

    At bar i the profile is built from bars [i-window, i-1] — no look-ahead.

    Uses a log-uniform global price grid (equal %-resolution across wide price ranges)
    and the cumsum trick so rolling window volumes are O(price_bins) per bar rather
    than O(window × price_bins).  All aggregations are fully vectorised — no Python
    bar loop.

    Returns dict of Series (poc, hvn_high, hvn_low, lvn_high, lvn_low, vah, val).
    NaN for bars before the first full window.
    """
    n      = len(df)
    high   = df["high"].values
    low    = df["low"].values
    close  = df["close"].values
    volume = df["volume"].values

    # ── Global log-uniform price grid ─────────────────────────────────────────
    p_min       = max(float(low.min()), 1e-9)
    p_max       = float(high.max())
    log_edges   = np.linspace(np.log(p_min) - 1e-9, np.log(p_max) + 1e-9, price_bins + 1)
    bin_centers = np.exp((log_edges[:-1] + log_edges[1:]) / 2)

    # Assign each bar's typical price to a bin (vectorised, O(n))
    typical  = np.maximum((high + low + close) / 3, 1e-9)
    bar_bins = np.clip(
        np.searchsorted(log_edges, np.log(typical), side="right") - 1,
        0, price_bins - 1,
    )

    # Sparse volume matrix: vol_matrix[i, bar_bins[i]] = volume[i], else 0
    vol_matrix           = np.zeros((n, price_bins))
    vol_matrix[np.arange(n), bar_bins] = volume

    # Prefix-sum.  cum_vol[k+1] = vol_matrix[0:k+1].sum(axis=0)
    cum_vol     = np.zeros((n + 1, price_bins))
    cum_vol[1:] = vol_matrix.cumsum(axis=0)

    # Rolling window volumes via cumsum difference.
    # win_vol[j] = cum_vol[j+window] - cum_vol[j]  for j = 0 .. n-window-1,
    # corresponding to bar index i = j + window.
    # Lookahead: bar i sees bars [i-window, i-1] only. ✓
    win_vol = (cum_vol[window:] - cum_vol[:n + 1 - window])[:n - window]
    # shape: (m, price_bins) where m = n - window
    m = win_vol.shape[0]

    total_vols = win_vol.sum(axis=1)            # (m,)
    n_nz       = (win_vol > 0).sum(axis=1)     # non-zero bin count per row
    row_valid  = (total_vols > 0) & (n_nz >= 4)

    # ── POC (fully vectorised) ────────────────────────────────────────────────
    poc_idx  = np.argmax(win_vol, axis=1)
    poc_vals = np.where(row_valid, bin_centers[poc_idx], np.nan)

    # ── HVN / LVN percentile thresholds (vectorised via sorted rows) ──────────
    # Sort each row ascending: zero bins go first, then non-zeros.
    sorted_vol = np.sort(win_vol, axis=1)       # (m, price_bins) ascending

    # Position of first non-zero element in each sorted row
    nz_start = price_bins - n_nz               # (m,)

    def _pct_pos(pct: float) -> np.ndarray:
        """Column index in sorted_vol for the given percentile over non-zero bins."""
        within = np.floor(pct / 100.0 * np.maximum(n_nz - 1, 0)).astype(int)
        return np.clip(nz_start + within, 0, price_bins - 1)

    row_idx  = np.arange(m)
    lvn_thr  = sorted_vol[row_idx, _pct_pos(25)]   # 25th pct of non-zeros
    hvn_thr  = sorted_vol[row_idx, _pct_pos(75)]   # 75th pct of non-zeros

    # ── HVN / LVN bin masks ───────────────────────────────────────────────────
    nz_mask  = win_vol > 0
    hvn_mask = nz_mask & (win_vol >= hvn_thr[:, np.newaxis])
    lvn_mask = nz_mask & (win_vol <= lvn_thr[:, np.newaxis])

    bin_bc   = np.arange(price_bins)[np.newaxis, :]  # (1, price_bins)

    hvn_hi_idx = np.where(hvn_mask, bin_bc, -1).max(axis=1)
    hvn_lo_idx = np.where(hvn_mask, bin_bc, price_bins).min(axis=1)
    lvn_hi_idx = np.where(lvn_mask, bin_bc, -1).max(axis=1)
    lvn_lo_idx = np.where(lvn_mask, bin_bc, price_bins).min(axis=1)

    def _safe(idx: np.ndarray, sentinel: int) -> np.ndarray:
        ok = (idx != sentinel) & row_valid
        return np.where(ok, bin_centers[np.clip(idx, 0, price_bins - 1)], np.nan)

    hvn_high_m = _safe(hvn_hi_idx, -1)
    hvn_low_m  = _safe(hvn_lo_idx, price_bins)
    lvn_high_m = _safe(lvn_hi_idx, -1)
    lvn_low_m  = _safe(lvn_lo_idx, price_bins)

    # ── Value Area (vectorised) ───────────────────────────────────────────────
    # Accumulate bins top-down until 70% of total volume is covered.
    sorted_desc_idx = np.argsort(win_vol, axis=1)[:, ::-1]
    sorted_desc_vol = np.take_along_axis(win_vol, sorted_desc_idx, axis=1)
    cumsums         = sorted_desc_vol.cumsum(axis=1)
    target          = (total_vols * 0.70)[:, np.newaxis]
    va_cutoff       = (cumsums >= target).argmax(axis=1)   # first col >= 70%

    pos_idx      = np.arange(price_bins)[np.newaxis, :]
    in_va_sorted = pos_idx <= va_cutoff[:, np.newaxis]
    in_va_orig   = np.zeros((m, price_bins), dtype=bool)
    np.put_along_axis(in_va_orig, sorted_desc_idx, in_va_sorted, axis=1)

    rv_bc  = row_valid[:, np.newaxis]
    vah_idx = np.where(in_va_orig & rv_bc, bin_bc, -1).max(axis=1)
    val_idx = np.where(in_va_orig & rv_bc, bin_bc, price_bins).min(axis=1)
    vah_m   = _safe(vah_idx, -1)
    val_m   = _safe(val_idx, price_bins)

    # ── Pad to full-length Series ─────────────────────────────────────────────
    def _pad(arr: np.ndarray) -> pd.Series:
        full = np.full(n, np.nan)
        full[window:] = arr
        return pd.Series(full, index=df.index)

    return {
        "poc":      _pad(poc_vals),
        "hvn_high": _pad(hvn_high_m),
        "hvn_low":  _pad(hvn_low_m),
        "lvn_high": _pad(lvn_high_m),
        "lvn_low":  _pad(lvn_low_m),
        "vah":      _pad(vah_m),
        "val":      _pad(val_m),
    }
