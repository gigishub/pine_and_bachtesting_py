"""Population masks for Setup 2 Trigger: KDE Upper (4h) + Level/RVOL on 15m.

Baseline: regime AND kde_upper (4h structural gate).
All populations are strict subsets of this baseline.
Lift is measured vs kde_upper_baseline PF.

Populations:
    kde_upper_baseline  -- regime + kde_upper on 15m bars
    vwap_only           -- near daily VWAP (above close, within dist_threshold)
    vpvr_only           -- near VPVR HVN (1d), same proximity rule
    near_setup          -- near VWAP OR near VPVR
    rvol_only           -- Volume > rvol_threshold × rolling_mean(Vol, rvol_window)
    vwap_and_rvol       -- near VWAP AND rvol_above
    vpvr_and_rvol       -- near VPVR AND rvol_above
    near_and_rvol       -- near either AND rvol_above

All signals are computed on 15m bars.
dist_threshold = setup_distance_atr × ATR(15m, period)

No-lookahead guarantee:
    kde_upper from 4h bars, shifted 1 completed 4h bar, forward-filled to 15m.
    VPVR from 1d bars, shifted 1 day, forward-filled to 15m.
    Daily VWAP accumulates from midnight through bar t — fully causal.
    RVOL rolling mean is purely historical.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_tests.setup_2_trigger_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: 15m DataFrame with regime signal, atr, vpvr_hvn_1d, kde_upper
            columns (4h KDE already shifted and aligned to 15m), and OHLCV.
        config: TestConfig instance.

    Returns:
        dict of boolean pd.Series aligned to df's index.
    """
    _require_columns(
        df,
        [
            config.regime_col,
            "Open", "High", "Low", "Close", "Volume",
            "atr", "vpvr_hvn_1d", "kde_upper",
        ],
    )

    regime = df[config.regime_col].astype(bool)
    close = df["Close"]
    atr = df["atr"]
    vpvr = df["vpvr_hvn_1d"]

    kde_upper = df["kde_upper"].infer_objects(copy=False).fillna(False).astype(bool)

    daily_vwap = _compute_daily_vwap(df)

    threshold = config.setup_distance_atr * atr

    near_vwap = (
        daily_vwap.notna()
        & atr.notna()
        & (daily_vwap > close)
        & ((daily_vwap - close) <= threshold)
    )
    near_vpvr = (
        vpvr.notna()
        & atr.notna()
        & (vpvr > close)
        & ((vpvr - close) <= threshold)
    )
    near_either = near_vwap | near_vpvr

    # RVOL on 15m bars: 96-bar window = 24h baseline by default
    vol_mean = df["Volume"].rolling(config.rvol_window, min_periods=config.rvol_window).mean()
    rvol_above = (df["Volume"] / vol_mean) > config.rvol_threshold

    kde_ready = df["kde_upper"].notna()
    baseline = regime & kde_upper & atr.notna() & kde_ready

    return {
        "kde_upper_baseline": baseline,
        "vwap_only": baseline & near_vwap,
        "vpvr_only": baseline & near_vpvr,
        "near_setup": baseline & near_either,
        "rvol_only": baseline & rvol_above,
        "vwap_and_rvol": baseline & near_vwap & rvol_above,
        "vpvr_and_rvol": baseline & near_vpvr & rvol_above,
        "near_and_rvol": baseline & near_either & rvol_above,
    }


# ---------------------------------------------------------------------------
# Daily VWAP helper
# ---------------------------------------------------------------------------


def _compute_daily_vwap(df: pd.DataFrame) -> pd.Series:
    """Daily-anchored VWAP on entry-TF bars. Resets at UTC midnight."""
    typical = (df["High"] + df["Low"] + df["Close"]) / 3.0
    tp_vol = typical * df["Volume"]
    anchor_key = df.index.tz_localize(None).to_period("D")
    cum_tp_vol = tp_vol.groupby(anchor_key).cumsum()
    cum_vol = df["Volume"].groupby(anchor_key).cumsum()
    return (cum_tp_vol / cum_vol).rename("daily_vwap")


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Ensure runner._process_pair() attaches all signals first."
        )
