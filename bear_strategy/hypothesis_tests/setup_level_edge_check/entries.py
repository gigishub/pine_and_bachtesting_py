"""Population masks for the setup level edge check (Step 2).

Classifies regime-confirmed 1-hour bars into near-setup and
away-from-setup populations given a df_1h that already carries the
following columns (aligned from 4H, all shifted by 1 bar in the runner):

    ema_below_50_regime   — bool: Step 1 winning regime filter
    atr_4h                — float: 4H ATR (shifted, NaN until warm)
    vpvr_hvn              — float: nearest HVN above 4H close (NaN until warm)
    anchored_vwap         — float: VWAP from last confirmed swing high (NaN
                            until first swing high confirmed)
    atr                   — float: 1h ATR (used for stop sizing, not here)

Near-setup definition (either condition):
  1. vpvr_hvn is not NaN, vpvr_hvn > close_1h, and
     (vpvr_hvn - close_1h) <= setup_distance_atr × atr_4h
  2. anchored_vwap is not NaN, anchored_vwap > close_1h, and
     (anchored_vwap - close_1h) <= setup_distance_atr × atr_4h

Only bars where at least one indicator is initialised (vpvr_hvn or
anchored_vwap is not NaN, and atr_4h is not NaN) count as eligible so
that warmup bars do not contaminate the away-from-setup baseline.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_tests.setup_level_edge_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: 1h DataFrame enriched with regime and aligned 4H signals.
        config: TestConfig providing ``regime_col`` and
            ``setup_distance_atr``.

    Returns:
        dict with keys:
            ``all_regime``, ``near_setup``, ``away_from_setup``,
            ``vpvr_only``, ``vwap_only``.
        All values are boolean pd.Series aligned to df's index.
    """
    _require_columns(df, [config.regime_col, "atr_4h", "vpvr_hvn", "anchored_vwap", "Close"])

    regime = df[config.regime_col].astype(bool)
    close = df["Close"]
    atr_4h = df["atr_4h"]
    vpvr = df["vpvr_hvn"]
    avwap = df["anchored_vwap"]

    threshold = config.setup_distance_atr * atr_4h

    vpvr_valid = vpvr.notna() & atr_4h.notna()
    avwap_valid = avwap.notna() & atr_4h.notna()

    near_vpvr = vpvr_valid & (vpvr > close) & ((vpvr - close) <= threshold)
    near_vwap = avwap_valid & (avwap > close) & ((avwap - close) <= threshold)

    # Eligible: regime bar where at least one indicator is initialised.
    # Bars where both are NaN are excluded from both near and away so that
    # warmup periods do not bias the control group.
    eligible = regime & (vpvr_valid | avwap_valid)

    return {
        "all_regime": regime,
        "near_setup": eligible & (near_vpvr | near_vwap),
        "away_from_setup": eligible & ~(near_vpvr | near_vwap),
        "vpvr_only": eligible & near_vpvr,
        "vwap_only": eligible & near_vwap,
    }


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Run runner._process_pair() to attach all signals before calling "
            "build_population_masks()."
        )
