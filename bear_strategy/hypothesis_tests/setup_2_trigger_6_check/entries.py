"""Population masks for Setup 2 – Trigger 6: MACD-based momentum signals.

Baseline: regime AND kde_upper (4h). All populations are strict subsets.

Six MACD-based signals, all condition-based (not crossovers except where noted).

No-lookahead guarantee:
    The aligned 4h kde_upper gate originates from runner.py where the 4h KDE
    output is .shift(1) before merge_asof alignment.
    All conditions use direct comparisons or .shift(1) for prior values.

Signal definitions
──────────────────
zero_line_rejection     : MACD approaches 0 from below, turns lower without crossing
histogram_peak_roll     : Histogram[1] > Histogram while Histogram is still positive
rapid_separation        : (MACD - Signal) increasing (widening negative gap)
signal_line_wall        : Signal_Line < 0 AND MACD_Line < Signal_Line
histogram_twin_peaks    : Price HH but MACD Histogram LH (bearish divergence)
cross_velocity          : MACD crosses below Signal with steep slope
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_2_trigger_6_check.config import TestConfig


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

    c = df["Close"]
    h = df["High"]

    # Compute MACD
    ema_fast = c.ewm(span=config.macd_fast, adjust=False).mean()
    ema_slow = c.ewm(span=config.macd_slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=config.macd_signal, adjust=False).mean()
    histogram = macd_line - signal_line

    # ------------------------------------------------------------------
    # 1. Zero-line rejection: MACD touches 0 from below, turns lower
    # ------------------------------------------------------------------
    prev_macd = macd_line.shift(1)
    near_zero = macd_line.abs() < config.zero_line_margin
    was_below_zero = prev_macd < 0
    turning_lower = macd_line < prev_macd
    zero_line_rejection = near_zero & was_below_zero & turning_lower

    # ------------------------------------------------------------------
    # 2. Histogram peak roll: Histogram[1] > Histogram while Histogram > 0
    # ------------------------------------------------------------------
    prev_hist = histogram.shift(1)
    histogram_positive = histogram > 0
    hist_declining = prev_hist > histogram
    histogram_peak_roll = histogram_positive & hist_declining

    # ------------------------------------------------------------------
    # 3. Rapid separation: (MACD - Signal) increasing (gap widening)
    # ------------------------------------------------------------------
    gap = macd_line - signal_line
    prev_gap = gap.shift(1)
    gap_widening = gap < prev_gap  # more negative = wider gap below zero
    rapid_separation = gap_widening & (gap < 0)

    # ------------------------------------------------------------------
    # 4. Signal line wall: Signal < 0 AND MACD < Signal
    # ------------------------------------------------------------------
    signal_line_wall = (signal_line < 0) & (macd_line < signal_line)

    # ------------------------------------------------------------------
    # 5. Histogram twin peaks: Price HH but Histogram LH (bearish divergence)
    # ------------------------------------------------------------------
    lookback = config.histogram_lookback
    price_higher_high = h > h.shift(lookback)
    hist_lower_high = histogram < histogram.shift(lookback)
    histogram_twin_peaks = price_higher_high & hist_lower_high & (histogram > 0)

    # ------------------------------------------------------------------
    # 6. Cross velocity: MACD crosses below Signal with steep slope
    # ------------------------------------------------------------------
    prev_macd_above_signal = prev_macd > signal_line.shift(1)
    now_macd_below_signal = macd_line < signal_line
    is_crossing = prev_macd_above_signal & now_macd_below_signal
    slope = (macd_line - prev_macd).abs()
    steep_slope = slope > config.cross_velocity_slope_threshold
    cross_velocity = is_crossing & steep_slope

    return {
        "kde_upper_baseline": baseline,
        "zero_line_rejection": baseline & zero_line_rejection,
        "histogram_peak_roll": baseline & histogram_peak_roll,
        "rapid_separation": baseline & rapid_separation,
        "signal_line_wall": baseline & signal_line_wall,
        "histogram_twin_peaks": baseline & histogram_twin_peaks,
        "cross_velocity": baseline & cross_velocity,
    }


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Ensure runner._process_pair() attaches all signals first."
        )
