"""Population masks for the KDE + Level Proximity Combined Check.

Populations tested (against regime_only baseline):

  KDE signals (4h, standalone):
    kde_upper        - open > kde_peak  (mean-reversion short from above POC)
    kde_lower_fresh  - close < kde_peak AND counter <= kde_lower_duration

  Level signals (1d reference, standalone):
    vwap_only        - price within dist_threshold of daily VWAP
    vpvr_only        - price within dist_threshold of VPVR HVN (1d)
    near_setup       - near VWAP OR near VPVR

  Intersections (KDE direction x level):
    kde_upper_and_vwap    - kde_upper AND vwap_only
    kde_upper_and_vpvr    - kde_upper AND vpvr_only
    kde_upper_and_near    - kde_upper AND near_setup
    kde_lower_and_vwap    - kde_lower_fresh AND vwap_only
    kde_lower_and_vpvr    - kde_lower_fresh AND vpvr_only
    kde_lower_and_near    - kde_lower_fresh AND near_setup

dist_threshold = setup_distance_atr * ATR_1h

No-lookahead guarantee:
    KDE signals computed on 4h bars, shifted 1 completed bar, aligned to 1h.
    Daily VWAP accumulates from midnight to bar t on 1h data (causal).
    VPVR HVN from 1d bars, shifted 1 bar, forward-filled to 1h.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_tests.setup_kde_level_combined_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: 1h DataFrame with regime signal, atr, vpvr_hvn_1d, kde_upper,
            kde_lower_fresh columns (4h KDE already shifted and aligned),
            and OHLCV columns.
        config: TestConfig instance.

    Returns:
        dict of boolean pd.Series aligned to df's index.
    """
    _require_columns(
        df,
        [
            config.regime_col,
            "Open", "High", "Low", "Close", "Volume",
            "atr", "vpvr_hvn_1d", "kde_upper", "kde_lower_fresh",
        ],
    )

    regime = df[config.regime_col].astype(bool)
    close = df["Close"]
    atr = df["atr"]
    vpvr = df["vpvr_hvn_1d"]

    # KDE signals: pre-computed on 4h bars, already aligned to 1h by runner
    kde_upper = df["kde_upper"].infer_objects(copy=False).fillna(False).astype(bool)
    kde_lower = df["kde_lower_fresh"].infer_objects(copy=False).fillna(False).astype(bool)

    # Daily VWAP (resets at UTC midnight, causal within each day)
    daily_vwap = _compute_daily_vwap(df)

    # Near-level proximity: level is above close AND within threshold
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
    kde_gate = kde_upper | kde_lower

    near_either = near_vwap | near_vpvr

    # Eligibility: regime bar, ATR warmed, KDE column populated (4h warmup done)
    kde_ready = df["kde_upper"].notna()
    eligible = regime & atr.notna() & kde_ready

    return {
        # Baseline
        "regime_only": eligible,
        # KDE combined gate (OR) and split directions
        "kde_gate": eligible & kde_gate,
        "kde_upper": eligible & kde_upper,
        "kde_lower_fresh": eligible & kde_lower,
        # Level signals standalone
        "vwap_only": eligible & near_vwap,
        "vpvr_only": eligible & near_vpvr,
        "near_setup": eligible & near_either,
        # Intersections: kde_gate x level
        "kde_gate_and_vwap": eligible & kde_gate & near_vwap,
        "kde_gate_and_vpvr": eligible & kde_gate & near_vpvr,
        "kde_gate_and_near": eligible & kde_gate & near_either,
        # Intersections: kde_upper x level
        "kde_upper_and_vwap": eligible & kde_upper & near_vwap,
        "kde_upper_and_vpvr": eligible & kde_upper & near_vpvr,
        "kde_upper_and_near": eligible & kde_upper & near_either,
        # Intersections: kde_lower_fresh x level
        "kde_lower_and_vwap": eligible & kde_lower & near_vwap,
        "kde_lower_and_vpvr": eligible & kde_lower & near_vpvr,
        "kde_lower_and_near": eligible & kde_lower & near_either,
    }


# ---------------------------------------------------------------------------
# Daily VWAP helper
# ---------------------------------------------------------------------------


def _compute_daily_vwap(df: pd.DataFrame) -> pd.Series:
    """Compute daily-anchored VWAP on the entry-TF DataFrame.

    Resets at UTC midnight each day. Value at bar t accumulates from
    the first bar of the same calendar day through bar t -- no lookahead.
    """
    typical = (df["High"] + df["Low"] + df["Close"]) / 3.0
    tp_vol = typical * df["Volume"]

    # suppress pandas timezone-to-period UserWarning (expected, no data loss)
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
