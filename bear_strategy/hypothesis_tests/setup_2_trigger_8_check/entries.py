"""Population masks for Setup 2 – Trigger 8: rsi_ma_below_50 reinforced baseline.

Baseline stack:
    kde_upper_baseline : regime AND kde_upper (Setup 1 gate)
    rsi_ma_baseline    : kde_upper_baseline AND RSI_MA < rsi_ma_threshold

All seven test populations are strict subsets of rsi_ma_baseline.
Verdicts are measured as lift over rsi_ma_baseline PF, not kde_upper_baseline.

No-lookahead guarantee:
    The aligned 4h kde_upper gate originates from runner.py where the 4h KDE
    output is .shift(1) before merge_asof alignment.
    All conditions use direct comparisons (no forward-looking data).

Signal definitions
──────────────────
1. rsi_below_50       : RSI(period) < rsi_threshold — held state
2. mfi_below_50       : MFI(period) < mfi_threshold — held state
3. rsi_and_mfi        : RSI < threshold AND MFI < threshold simultaneously
4. close_below_ema    : Close < EMA(ema_slow) — price below macro trend average
5. ema_bearish_order  : EMA(ema_fast) < EMA(ema_slow) — fast below slow
6. macd_signal_wall   : MACD line < 0 AND MACD line < signal line
7. lower_bb_declining : lower_bb < lower_bb[1] — floor actively falling
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_2_trigger_8_check.config import TestConfig


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

    kde_upper_baseline = regime & kde_upper & atr.notna()

    c  = df["Close"]
    h  = df["High"]
    lo = df["Low"]
    v  = df["Volume"]

    # ------------------------------------------------------------------
    # RSI MA — baked into the reinforced baseline
    # ------------------------------------------------------------------
    rsi = _compute_rsi(c, config.rsi_period)
    if config.rsi_ma_type == "sma":
        rsi_ma = rsi.rolling(config.rsi_ma_period, min_periods=config.rsi_ma_period).mean()
    else:
        rsi_ma = rsi.ewm(span=config.rsi_ma_period, adjust=False).mean()

    rsi_ma_below_threshold = rsi_ma < config.rsi_ma_threshold

    # Reinforced baseline: kde_upper_baseline AND RSI_MA below threshold
    rsi_ma_baseline = kde_upper_baseline & rsi_ma_below_threshold

    # ------------------------------------------------------------------
    # 1. RSI held below threshold
    # ------------------------------------------------------------------
    rsi_below_50 = rsi < config.rsi_threshold

    # ------------------------------------------------------------------
    # 2. MFI held below threshold
    # ------------------------------------------------------------------
    mfi         = _compute_mfi(h, lo, c, v, config.mfi_period)
    mfi_below_50 = mfi < config.mfi_threshold

    # ------------------------------------------------------------------
    # 3. RSI AND MFI both held below threshold (confluence)
    # ------------------------------------------------------------------
    rsi_and_mfi = rsi_below_50 & mfi_below_50

    # ------------------------------------------------------------------
    # 4. Close below slow EMA (price below macro trend average)
    # ------------------------------------------------------------------
    slow_ema        = c.ewm(span=config.ema_slow, adjust=False).mean()
    close_below_ema = c < slow_ema

    # ------------------------------------------------------------------
    # 5. Fast EMA below slow EMA (bearish MA order, held state)
    # ------------------------------------------------------------------
    fast_ema          = c.ewm(span=config.ema_fast, adjust=False).mean()
    ema_bearish_order = fast_ema < slow_ema

    # ------------------------------------------------------------------
    # 6. MACD signal wall: MACD line < 0 AND MACD line < signal line
    # ------------------------------------------------------------------
    ema_f       = c.ewm(span=config.macd_fast, adjust=False).mean()
    ema_s       = c.ewm(span=config.macd_slow, adjust=False).mean()
    macd_line   = ema_f - ema_s
    signal_line = macd_line.ewm(span=config.macd_signal, adjust=False).mean()
    macd_signal_wall = (macd_line < 0) & (macd_line < signal_line)

    # ------------------------------------------------------------------
    # 7. Lower Bollinger Band declining (floor falling, directional)
    # ------------------------------------------------------------------
    bb_mid  = c.rolling(config.bb_period, min_periods=config.bb_period).mean()
    bb_std_ = c.rolling(config.bb_period, min_periods=config.bb_period).std(ddof=1)
    lower_bb          = bb_mid - config.bb_std * bb_std_
    lower_bb_declining = lower_bb < lower_bb.shift(1)

    return {
        "kde_upper_baseline":  kde_upper_baseline,
        "rsi_ma_baseline":     rsi_ma_baseline,
        "rsi_below_50":        rsi_ma_baseline & rsi_below_50,
        "mfi_below_50":        rsi_ma_baseline & mfi_below_50,
        "rsi_and_mfi":         rsi_ma_baseline & rsi_and_mfi,
        "close_below_ema":     rsi_ma_baseline & close_below_ema,
        "ema_bearish_order":   rsi_ma_baseline & ema_bearish_order,
        "macd_signal_wall":    rsi_ma_baseline & macd_signal_wall,
        "lower_bb_declining":  rsi_ma_baseline & lower_bb_declining,
    }


# ---------------------------------------------------------------------------
# Indicator helpers
# ---------------------------------------------------------------------------


def _compute_rsi(close: pd.Series, period: int) -> pd.Series:
    """Wilder-smoothed RSI (standard definition)."""
    delta    = close.diff()
    gain     = delta.clip(lower=0)
    loss     = (-delta).clip(lower=0)
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
    tp  = (high + low + close) / 3.0
    rmf = tp * volume

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
