"""Population masks for Trigger Search 2: close_below_bb base + refinement signals.

Baseline stack
--------------
    kde_upper_baseline : regime AND kde_upper (Setup 1 gate)   [reference]
    rsi_ma_baseline    : kde_upper_baseline AND RSI_MA < threshold  [base]

Three entry timing triggers tested — each fires on ONE specific bar — subsets of rsi_ma_baseline:

1. close_below_bb        : close < lower Bollinger Band (previously confirmed)
2. bearish_candle_size   : bar range within 0.7–1.2 × ATR (medium-sized bar)
3. ema_cross_price       : price crosses below EMA(n, default 10) (event)

No-lookahead guarantee:
    4h kde_upper is .shift(1) before merge_asof in runner.py.
    All crossover checks use .shift(1) for prior-bar values — no lookahead.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.trigger_search_1.config import TestConfig


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

    o  = df["Open"]
    h  = df["High"]
    lo = df["Low"]
    c  = df["Close"]

    # ------------------------------------------------------------------
    # RSI MA — baked into the reinforced baseline
    # ------------------------------------------------------------------
    rsi = _compute_rsi(c, config.rsi_period)
    if config.rsi_ma_type == "sma":
        rsi_ma = rsi.rolling(config.rsi_ma_period, min_periods=config.rsi_ma_period).mean()
    else:
        rsi_ma = rsi.ewm(span=config.rsi_ma_period, adjust=False).mean()

    rsi_ma_baseline = kde_upper_baseline & (rsi_ma < config.rsi_ma_threshold)

    # ------------------------------------------------------------------
    # 1. Close below lower Bollinger Band (CONFIRMED BASE TRIGGER)
    # ------------------------------------------------------------------
    bb_mid   = c.rolling(config.bb_period, min_periods=config.bb_period).mean()
    bb_std_  = c.rolling(config.bb_period, min_periods=config.bb_period).std(ddof=1)
    lower_bb = bb_mid - config.bb_std * bb_std_
    close_below_bb = c < lower_bb

    # ------------------------------------------------------------------
    # 2. Bearish candle size — range in 0.7–1.2 × ATR (medium bar)
    # ------------------------------------------------------------------
    bar_range = h - lo
    bearish_candle_size = (bar_range >= config.atr_candle_min * atr) & (bar_range <= config.atr_candle_max * atr) & (c < o)

    # ------------------------------------------------------------------
    # 3. Price crosses below EMA(n, default 10)
    # ------------------------------------------------------------------
    ema_n = c.ewm(span=config.ema_cross_period, adjust=False).mean()
    ema_cross_price = (c.shift(1) >= ema_n.shift(1)) & (c < ema_n)

    return {
        "kde_upper_baseline": kde_upper_baseline,
        "rsi_ma_baseline":    rsi_ma_baseline,
        "close_below_bb":     rsi_ma_baseline & close_below_bb,
        "bearish_candle_size": rsi_ma_baseline & bearish_candle_size,
        "ema_cross_price":    rsi_ma_baseline & ema_cross_price,
    }


# ---------------------------------------------------------------------------
# Indicator helpers
# ---------------------------------------------------------------------------


def _compute_rsi(close: pd.Series, period: int) -> pd.Series:
    """Wilder-smoothed RSI."""
    delta    = close.diff()
    gain     = delta.clip(lower=0)
    loss     = (-delta).clip(lower=0)
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100.0 - (100.0 / (1.0 + rs))


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Ensure runner._process_pair() attaches all signals first."
        )
