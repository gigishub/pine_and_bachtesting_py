"""Population masks for Setup 2 – Trigger 5: BB + Keltner Channel signals.

Baseline: regime AND kde_upper (4h). All populations are strict subsets.

All six signals are condition-based (held state) — they remain True while
the volatility or price structure meets the criteria.

No-lookahead guarantee:
    The aligned 4h kde_upper gate originates from runner.py where the 4h KDE
    output is .shift(1) before merge_asof alignment.
    All conditions use direct comparisons on prior values where applicable.

Signal definitions
──────────────────
momentum_close         : Close < Lower_Band
falling_tunnel         : Lower_Band < Lower_Band[1] AND Upper_Band < Upper_Band[1]
volatility_velocity    : (BB_Width - BB_Width[1]) > Average_Width_Delta
squeeze_snap           : BB_Width == Lowest(BB_Width, squeeze_lookback) & Lower_Band < Lower_Band[1]
lower_expansion        : Lower_Band < Lower_Band[1]
keltner_squeeze_release: Lower_BB < Lower_Keltner_Channel
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_2_trigger_5_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return one boolean mask per population.

    Args:
        df: Entry-TF DataFrame with regime, atr, kde_upper (bool), and OHLCV.
        config: TestConfig instance.

    Returns:
        dict mapping population name -> boolean pd.Series on df's index.
    """
    _require_columns(
        df,
        [config.regime_col, "Open", "High", "Low", "Close", "Volume", "atr", "kde_upper"],
    )

    regime    = df[config.regime_col].astype(bool)
    kde_upper = df["kde_upper"].infer_objects(copy=False).fillna(False).astype(bool)
    atr       = df["atr"]

    baseline = regime & kde_upper & atr.notna()

    h  = df["High"]
    lo = df["Low"]
    c  = df["Close"]

    # ------------------------------------------------------------------
    # 1. Momentum Close — price closes below lower BB
    # ------------------------------------------------------------------
    bb_mid   = c.rolling(config.bb_period, min_periods=config.bb_period).mean()
    bb_std   = c.rolling(config.bb_period, min_periods=config.bb_period).std(ddof=1)
    bb_lower = bb_mid - config.bb_std * bb_std
    bb_upper = bb_mid + config.bb_std * bb_std

    momentum_close = c < bb_lower

    # ------------------------------------------------------------------
    # 2. Falling Tunnel — both bands moving down
    # ------------------------------------------------------------------
    falling_tunnel = (
        (bb_lower < bb_lower.shift(1))
        & (bb_upper < bb_upper.shift(1))
    )

    # ------------------------------------------------------------------
    # 3. Volatility Velocity — expansion rate accelerating
    # ------------------------------------------------------------------
    bb_width = bb_upper - bb_lower
    bb_width_delta = bb_width - bb_width.shift(1)
    avg_width_delta = bb_width_delta.rolling(
        config.vol_vel_lookback, min_periods=config.vol_vel_lookback
    ).mean()
    volatility_velocity = bb_width_delta > avg_width_delta

    # ------------------------------------------------------------------
    # 4. Squeeze & Snap — contraction then expansion
    # ------------------------------------------------------------------
    bb_width_min = bb_width.rolling(config.squeeze_lookback, min_periods=config.squeeze_lookback).min()
    squeeze_snap = (
        (bb_width == bb_width_min)
        & (bb_lower < bb_lower.shift(1))
    )

    # ------------------------------------------------------------------
    # 5. Lower Expansion — floor dropping
    # ------------------------------------------------------------------
    lower_expansion = bb_lower < bb_lower.shift(1)

    # ------------------------------------------------------------------
    # 6. Keltner Squeeze Release — BB lower drops below KC lower
    # ------------------------------------------------------------------
    tr = pd.concat(
        [h - lo, (h - c.shift(1)).abs(), (lo - c.shift(1)).abs()], axis=1
    ).max(axis=1)
    atr_series = tr.ewm(span=config.kc_period, adjust=False).mean()
    kc_mid = c.rolling(config.kc_period, min_periods=config.kc_period).mean()
    kc_lower = kc_mid - config.kc_atr_mult * atr_series

    keltner_squeeze_release = bb_lower < kc_lower

    return {
        "kde_upper_baseline":        baseline,
        "momentum_close":            baseline & momentum_close,
        "falling_tunnel":            baseline & falling_tunnel,
        "volatility_velocity":       baseline & volatility_velocity,
        "squeeze_snap":              baseline & squeeze_snap,
        "lower_expansion":           baseline & lower_expansion,
        "keltner_squeeze_release":   baseline & keltner_squeeze_release,
    }


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Ensure runner._process_pair() attaches all signals first."
        )
