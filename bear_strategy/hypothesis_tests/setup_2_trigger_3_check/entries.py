"""Population masks for Setup 2 – Trigger 3: oscillator-level and band-expansion signals.

Baseline: regime AND kde_upper (4h). All populations are strict subsets.

All four signals are purely vectorised — no state machine required.
They fire on the bar where the crossover or expansion condition occurs.

No-lookahead guarantee:
    The aligned 4h kde_upper gate originates from runner.py where the 4h KDE
    output is .shift(1) before merge_asof alignment.
    All crossover conditions use .shift(1) on the prior-bar value — no
    forward-looking data is accessed.

Signal definitions
──────────────────
rsi_cross_50    : RSI(period) crosses below rsi_threshold (default 50)
mfi_cross_50    : MFI(period) crosses below mfi_threshold (default 50)
rsi_cross_ma    : RSI crosses below its own MA (EMA default, configurable)
bb_expand_down  : BB lower band expands downward + close < midband + bearish bar
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_2_trigger_3_check.config import TestConfig


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

    o  = df["Open"]
    h  = df["High"]
    lo = df["Low"]
    c  = df["Close"]
    v  = df["Volume"]

    # ------------------------------------------------------------------
    # 1. RSI crosses below threshold (default 50)
    # ------------------------------------------------------------------
    rsi          = _compute_rsi(c, config.rsi_period)
    rsi_cross_50 = (rsi < config.rsi_threshold) & (rsi.shift(1) >= config.rsi_threshold)

    # ------------------------------------------------------------------
    # 2. MFI crosses below threshold (default 50)
    # ------------------------------------------------------------------
    mfi          = _compute_mfi(h, lo, c, v, config.mfi_period)
    mfi_cross_50 = (mfi < config.mfi_threshold) & (mfi.shift(1) >= config.mfi_threshold)

    # ------------------------------------------------------------------
    # 3. RSI crosses below its own moving average
    # ------------------------------------------------------------------
    if config.rsi_ma_type == "sma":
        rsi_ma = rsi.rolling(config.rsi_ma_period, min_periods=config.rsi_ma_period).mean()
    else:
        rsi_ma = rsi.ewm(span=config.rsi_ma_period, adjust=False).mean()

    rsi_cross_ma = (rsi < rsi_ma) & (rsi.shift(1) >= rsi_ma.shift(1))

    # ------------------------------------------------------------------
    # 4. BB lower band expands downward
    #    lower band moved further down + close below midband + bearish
    # ------------------------------------------------------------------
    bb_mid   = c.rolling(config.bb_period, min_periods=config.bb_period).mean()
    bb_std   = c.rolling(config.bb_period, min_periods=config.bb_period).std(ddof=1)
    bb_lower = bb_mid - config.bb_std * bb_std

    bb_expand_down = (
        (bb_lower < bb_lower.shift(1))   # lower band expanded down this bar
        & (c < bb_mid)                   # price is below the mean
        & (c < o)                        # bearish close
    )

    # ------------------------------------------------------------------
    # 5. EMA cross with elevated relative volume
    # ------------------------------------------------------------------
    ema          = c.ewm(span=config.ema_rvol_period, adjust=False).mean()
    rvol         = v / v.rolling(config.ema_rvol_lookback, min_periods=config.ema_rvol_lookback).mean()
    ema_rvol_cross = (
        (c < ema)
        & (c.shift(1) >= ema.shift(1))
        & (rvol > config.ema_rvol_threshold)
    )

    return {
        "kde_upper_baseline": baseline,
        "rsi_cross_50":       baseline & rsi_cross_50,
        "mfi_cross_50":       baseline & mfi_cross_50,
        "rsi_cross_ma":       baseline & rsi_cross_ma,
        "bb_expand_down":     baseline & bb_expand_down,
        "ema_rvol_cross":     baseline & ema_rvol_cross,
    }


# ---------------------------------------------------------------------------
# Indicator helpers
# ---------------------------------------------------------------------------


def _compute_rsi(close: pd.Series, period: int) -> pd.Series:
    """Wilder-smoothed RSI (standard definition)."""
    delta  = close.diff()
    gain   = delta.clip(lower=0)
    loss   = (-delta).clip(lower=0)
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100.0 - (100.0 / (1.0 + rs))


def _compute_mfi(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    volume: pd.Series,
    period: int,
) -> pd.Series:
    """Money Flow Index: volume-weighted RSI on typical price."""
    tp = (high + low + close) / 3.0
    rmf = tp * volume  # raw money flow

    # Positive/negative MF based on typical price direction
    tp_up   = (tp > tp.shift(1)).astype(float)
    tp_down = (tp < tp.shift(1)).astype(float)

    pos_mf = (rmf * tp_up).rolling(period, min_periods=period).sum()
    neg_mf = (rmf * tp_down).rolling(period, min_periods=period).sum()

    mfr = pos_mf / neg_mf.replace(0, np.nan)
    return 100.0 - (100.0 / (1.0 + mfr))


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Ensure runner._process_pair() attaches all signals first."
        )
