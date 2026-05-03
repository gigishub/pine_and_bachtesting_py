"""Population masks for Setup 2 – Trigger 4: positional filters (held state, not crossovers).

Baseline: regime AND kde_upper (4h). All populations are strict subsets.

All six signals are condition-based (held state) — they remain True while
the momentum structure stays bearish, not just on a crossover event.

No-lookahead guarantee:
    The aligned 4h kde_upper gate originates from runner.py where the 4h KDE
    output is .shift(1) before merge_asof alignment.
    All conditions use direct comparisons (no forward-looking data).

Signal definitions
──────────────────
rsi_below_50    : RSI(period) < rsi_threshold (default 50) — held state
mfi_below_50    : MFI(period) < mfi_threshold (default 50) — held state
rsi_ma_below_50 : RSI_MA(period) < rsi_ma_threshold (default 50) — held state
rsi_and_mfi     : RSI(period) < rsi_threshold AND MFI(period) < mfi_threshold — both held
rsi_ma_declining: RSI_MA < RSI_MA[1] — slope condition, trend reversal
mfi_ma_declining: MFI_MA < MFI_MA[1] — slope condition, trend reversal
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_2_trigger_4_check.config import TestConfig


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
    v  = df["Volume"]

    # ------------------------------------------------------------------
    # 1. RSI held below threshold (positional filter)
    # ------------------------------------------------------------------
    rsi            = _compute_rsi(c, config.rsi_period)
    rsi_below_50   = rsi < config.rsi_threshold

    # ------------------------------------------------------------------
    # 2. MFI held below threshold (positional filter)
    # ------------------------------------------------------------------
    mfi            = _compute_mfi(h, lo, c, v, config.mfi_period)
    mfi_below_50   = mfi < config.mfi_threshold

    # ------------------------------------------------------------------
    # 3. RSI's MA held below threshold (positional filter)
    # ------------------------------------------------------------------
    if config.rsi_ma_type == "sma":
        rsi_ma = rsi.rolling(config.rsi_ma_period, min_periods=config.rsi_ma_period).mean()
    else:
        rsi_ma = rsi.ewm(span=config.rsi_ma_period, adjust=False).mean()

    rsi_ma_below_50 = rsi_ma < config.rsi_ma_threshold

    # ------------------------------------------------------------------
    # 4. RSI AND MFI both held below threshold (confluence)
    # ------------------------------------------------------------------
    rsi_and_mfi = rsi_below_50 & mfi_below_50

    # ------------------------------------------------------------------
    # 5. RSI's MA declining (slope condition)
    # ------------------------------------------------------------------
    rsi_ma_declining = rsi_ma < rsi_ma.shift(1)

    # ------------------------------------------------------------------
    # 6. MFI's MA declining (slope condition)
    # ------------------------------------------------------------------
    if config.rsi_ma_type == "sma":
        mfi_ma = mfi.rolling(config.rsi_ma_period, min_periods=config.rsi_ma_period).mean()
    else:
        mfi_ma = mfi.ewm(span=config.rsi_ma_period, adjust=False).mean()

    mfi_ma_declining = mfi_ma < mfi_ma.shift(1)

    return {
        "kde_upper_baseline": baseline,
        "rsi_below_50":       baseline & rsi_below_50,
        "mfi_below_50":       baseline & mfi_below_50,
        "rsi_ma_below_50":    baseline & rsi_ma_below_50,
        "rsi_and_mfi":        baseline & rsi_and_mfi,
        "rsi_ma_declining":   baseline & rsi_ma_declining,
        "mfi_ma_declining":   baseline & mfi_ma_declining,
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
