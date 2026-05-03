"""Population masks for Setup 2 – Trigger 7: exhaustion / momentum-fade signals.

Baseline: regime AND kde_upper (4h). All populations are strict subsets.

Four exhaustion signals, all condition-based (held state or single-bar).

No-lookahead guarantee:
    The aligned 4h kde_upper gate originates from runner.py where the 4h KDE
    output is .shift(1) before merge_asof alignment.
    All conditions use .shift(n) for prior values; no forward-looking data.

Signal definitions
──────────────────
price_rsi_divergence  : Price HH but RSI LH over lookback (hollow upmove)
shrinking_impulse     : High-to-high gain shrinking + long upper wick (buyers struggling)
bb_rounding           : Was near upper BB, now pulling to midline + upper BB flattening
ema_tightening        : |fast EMA - slow EMA| narrowing while fast < slow (momentum loss)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_2_trigger_7_check.config import TestConfig


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

    h = df["High"]
    lo = df["Low"]
    c = df["Close"]
    o = df["Open"]

    # ------------------------------------------------------------------
    # 1. Price-RSI divergence
    #    Price makes Higher High over lookback but RSI makes Lower High.
    # ------------------------------------------------------------------
    rsi = _compute_rsi(c, config.rsi_period)
    lb  = config.divergence_lookback

    prev_high = h.shift(lb)
    prev_rsi  = rsi.shift(lb)

    price_higher_high = h > prev_high
    rsi_lower_high    = rsi < prev_rsi
    price_rsi_divergence = price_higher_high & rsi_lower_high

    # ------------------------------------------------------------------
    # 2. Shrinking impulse
    #    Latest high-to-high gain < prior high-to-high gain AND bar has
    #    a long upper wick (signals buyers failing to hold extensions).
    # ------------------------------------------------------------------
    lb_i = config.impulse_lookback

    prev_h1 = h.shift(lb_i)       # one cycle ago
    prev_h2 = h.shift(lb_i * 2)   # two cycles ago

    current_impulse = h - prev_h1
    prior_impulse   = prev_h1 - prev_h2

    # impulse is shrinking (both positive to avoid noise from down swings)
    impulse_shrinking = (
        (current_impulse < prior_impulse)
        & (current_impulse > 0)
        & (prior_impulse > 0)
    )

    # long upper wick: top wick > wick_ratio * bar range
    bar_range   = (h - lo).replace(0, np.nan)
    upper_wick  = h - c.where(c >= o, o)  # wick from body top to high
    long_wick   = upper_wick > config.wick_ratio * bar_range

    shrinking_impulse = impulse_shrinking & long_wick

    # ------------------------------------------------------------------
    # 3. BB rounding
    #    bb_lookback bars ago close was near upper BB;
    #    now close is pulling toward midline AND upper BB is flattening.
    # ------------------------------------------------------------------
    rolling_mean = c.rolling(config.bb_period, min_periods=config.bb_period).mean()
    rolling_std  = c.rolling(config.bb_period, min_periods=config.bb_period).std(ddof=0)
    upper_bb     = rolling_mean + config.bb_std * rolling_std

    lb_b = config.bb_lookback
    # was near upper band
    was_near_upper = c.shift(lb_b) >= upper_bb.shift(lb_b) * (1.0 - config.bb_proximity_pct)
    # now closer to midline than upper band
    pulling_to_mid = c < (rolling_mean + (upper_bb - rolling_mean) * 0.5)
    # upper band flattening or curling down
    bb_flattening  = upper_bb <= upper_bb.shift(1)

    bb_rounding = was_near_upper & pulling_to_mid & bb_flattening

    # ------------------------------------------------------------------
    # 4. EMA tightening
    #    |fast_ema - slow_ema| shrinking while fast EMA < slow EMA
    #    (bearish side — fast EMA lagging below slow EMA and converging).
    # ------------------------------------------------------------------
    fast_ema = c.ewm(span=config.ema_fast, adjust=False).mean()
    slow_ema = c.ewm(span=config.ema_slow, adjust=False).mean()

    gap      = (fast_ema - slow_ema).abs()
    prev_gap = gap.shift(1)

    ema_tightening = (gap < prev_gap) & (fast_ema < slow_ema)

    # ------------------------------------------------------------------
    # 5. EMA cross down
    #    Fast EMA crosses below slow EMA on this bar (event signal).
    # ------------------------------------------------------------------
    ema_cross_down = (fast_ema.shift(1) >= slow_ema.shift(1)) & (fast_ema < slow_ema)

    return {
        "kde_upper_baseline":   baseline,
        "price_rsi_divergence": baseline & price_rsi_divergence,
        "shrinking_impulse":    baseline & shrinking_impulse,
        "bb_rounding":          baseline & bb_rounding,
        "ema_tightening":       baseline & ema_tightening,
        "ema_cross_down":       baseline & ema_cross_down,
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
    rs       = avg_gain / avg_loss.replace(0, np.nan)
    return 100.0 - (100.0 / (1.0 + rs))


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Ensure runner._process_pair() attaches all signals first."
        )
