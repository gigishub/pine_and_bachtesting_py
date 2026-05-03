"""Population masks for Setup 2 Candle Trigger: KDE Upper (4h) + 15m bar quality.

Baseline: regime AND kde_upper. All populations are strict subsets.
Lift is measured vs kde_upper_baseline PF.

Signal definitions (all on 15m bars):

  bearish_rvol
    close < open  AND  volume / rolling_mean(volume, N) > threshold
    Confirms bearish intent with above-average participation.

  upper_wick_rejection
    upper_wick / bar_range > wick_ratio_threshold
    upper_wick = high - max(open, close)
    Buyers tried to push up but were rejected by sellers. No bearish-bar
    requirement — a doji or even bullish bar with a large upper wick counts.

  breakdown_bar
    close < open  AND  (close - low) / (high - low) < breakdown_close_pct
    Bar closes in the bottom portion of its range. Strong directional follow-
    through from sellers with no recovery.

  roc_negative
    (close - close.shift(roc_period)) / close.shift(roc_period) < 0
    Price is lower than N bars ago — momentum is pointing down.

  bearish_engulf
    Current bar: close < open (bearish body)
    Previous bar: close[1] > open[1] (bullish body)
    open >= close[1]  (current open at or above prior close)
    close <= open[1]  (current close at or below prior open)
    Classic bearish engulfing — current body completely swallows prior body.

No-lookahead guarantee:
    All signals use only current and prior bar data (no future values).
    kde_upper from 4h bars shifted 1 bar, forward-filled to 15m.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_2_candle_trigger_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: 15m DataFrame with regime, atr, kde_upper, and OHLCV columns.
        config: TestConfig instance.

    Returns:
        dict mapping population name -> boolean pd.Series on df's index.
    """
    _require_columns(
        df,
        [
            config.regime_col,
            "Open", "High", "Low", "Close", "Volume",
            "atr", "kde_upper",
        ],
    )

    regime = df[config.regime_col].astype(bool)
    o = df["Open"]
    h = df["High"]
    lo = df["Low"]
    c = df["Close"]
    vol = df["Volume"]

    kde_upper = df["kde_upper"].infer_objects(copy=False).fillna(False).astype(bool)
    kde_ready = df["kde_upper"].notna()

    baseline = regime & kde_upper & df["atr"].notna() & kde_ready

    # ------------------------------------------------------------------
    # 1. bearish_rvol
    # ------------------------------------------------------------------
    vol_mean = vol.rolling(config.rvol_window, min_periods=config.rvol_window).mean()
    rvol_above = (vol / vol_mean) > config.rvol_threshold
    bearish_rvol = (c < o) & rvol_above

    # ------------------------------------------------------------------
    # 2. upper_wick_rejection
    # ------------------------------------------------------------------
    bar_range = h - lo
    upper_wick = h - pd.concat([o, c], axis=1).max(axis=1)
    # Avoid division by zero on doji-range bars; treat as no signal
    wick_ratio = upper_wick.where(bar_range > 0, other=np.nan) / bar_range.where(bar_range > 0, other=np.nan)
    upper_wick_rejection = wick_ratio > config.wick_ratio_threshold

    # ------------------------------------------------------------------
    # 3. breakdown_bar
    # ------------------------------------------------------------------
    close_pos = (c - lo).where(bar_range > 0, other=np.nan) / bar_range.where(bar_range > 0, other=np.nan)
    breakdown_bar = (c < o) & (close_pos < config.breakdown_close_pct)

    # ------------------------------------------------------------------
    # 4. roc_negative
    # ------------------------------------------------------------------
    prior_close = c.shift(config.roc_period)
    roc = (c - prior_close) / prior_close
    roc_negative = roc < 0

    # ------------------------------------------------------------------
    # 5. bearish_engulf
    # ------------------------------------------------------------------
    prev_o = o.shift(1)
    prev_c = c.shift(1)
    curr_bearish = c < o
    prev_bullish = prev_c > prev_o
    body_engulfs = (o >= prev_c) & (c <= prev_o)
    bearish_engulf = curr_bearish & prev_bullish & body_engulfs

    return {
        "kde_upper_baseline": baseline,
        "bearish_rvol": baseline & bearish_rvol,
        "upper_wick_rejection": baseline & upper_wick_rejection,
        "breakdown_bar": baseline & breakdown_bar,
        "roc_negative": baseline & roc_negative,
        "bearish_engulf": baseline & bearish_engulf,
    }


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Ensure runner._process_pair() attaches all signals first."
        )
