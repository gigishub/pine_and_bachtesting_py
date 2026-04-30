"""Population masks for the ROC Exhaustion Setup Edge Check.

Translates the "ROC Exhaustion Zones" Pine Script indicator into Python.
All signals are computed on entry_tf bars at bar close — single-timeframe,
no higher-TF alignment needed.

─── Pine Script → Python translation ───────────────────────────────────────

ROC:
    roc = ta.roc(close, rocLen)   →   close.pct_change(roc_len) * 100

ta.rising(roc, driftBars):
    True if roc[0] > roc[1] AND roc[1] > roc[2] AND ... for driftBars bars.
    Implemented by checking roc.shift(k) > roc.shift(k+1) for k in range(driftBars).

isBullTrend  = ta.rising(roc, driftBars) AND roc > accelThresh
isBearTrend  = ta.falling(roc, driftBars) AND roc < -accelThresh

Exhaustion states (stateful `var bool` in Pine Script — require a bar loop):
    bullExhaustionActive:
        if isBullTrend            → False  (active trend; not yet exhausted)
        elif isBullTrend[1] or bullExhaustionActive[1]  → True   (trend just ended or already in zone)
        else                      → keep previous value
        # reset: if isBearTrend   → False  (new bear trend kills the post-bull zone)

    bearExhaustionActive:
        if isBearTrend            → False
        elif isBearTrend[1] or bearExhaustionActive[1]  → True
        else                      → keep previous value
        # reset: if isBullTrend   → False

─── No-lookahead guarantee ─────────────────────────────────────────────────

    ROC at bar t uses close[t] / close[t - roc_len] - 1.  Both are known at
    bar t's close — correct for signal-and-enter-at-close.
    The exhaustion loop only reads the previous bar's state and the current
    and previous isBullTrend / isBearTrend, which depend only on bars ≤ t.

─── Populations ─────────────────────────────────────────────────────────────

    regime_only    — EMA-50 bear regime + ROC/ATR warmed (eligible baseline).

    roc_post_bull  — regime + bullExhaustionActive = True.
                     Red zone: ROC just finished rising; potential overbought
                     exhaustion in a bear regime.

    roc_bear_trend — regime + isBearTrend = True.
                     Bear prediction: ROC actively falling and momentum
                     confirmed below -accelThresh.

    roc_post_bear  — regime + bearExhaustionActive = True.
                     Green zone: local bear ROC trend ended; testing whether
                     a failing local bounce within a larger bear regime still
                     offers short edge.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_roc_exhaustion_edge_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: Entry-TF DataFrame with regime signal and ATR column attached.
        config: TestConfig providing ROC and drift parameters.

    Returns:
        dict with keys: ``regime_only``, ``roc_post_bull``,
        ``roc_bear_trend``, ``roc_post_bear``.
        All values are boolean pd.Series aligned to df's index.
    """
    _require_columns(df, [config.regime_col, "Close", "atr"])

    close = df["Close"]
    regime = df[config.regime_col].astype(bool)

    roc = close.pct_change(config.roc_len) * 100.0

    is_bull_trend = _is_rising(roc, config.drift_bars) & (roc > config.accel_thresh)
    is_bear_trend = _is_falling(roc, config.drift_bars) & (roc < -config.accel_thresh)

    bull_ex, bear_ex = _compute_exhaustion_states(is_bull_trend, is_bear_trend)

    # Eligibility: ROC and ATR both fully warmed.
    # ROC needs roc_len + drift_bars bars; ATR needs atr_period bars.
    roc_ready = roc.notna() & is_bull_trend.notna() & is_bear_trend.notna()
    atr_ready = df["atr"].notna()
    eligible = regime & roc_ready & atr_ready

    bull_ex_series = pd.Series(bull_ex, index=df.index)
    bear_ex_series = pd.Series(bear_ex, index=df.index)
    bear_trend_series = pd.Series(is_bear_trend.to_numpy(dtype=bool), index=df.index)

    return {
        "regime_only": eligible,
        "roc_post_bull": eligible & bull_ex_series,
        "roc_bear_trend": eligible & bear_trend_series,
        "roc_post_bear": eligible & bear_ex_series,
    }


# ---------------------------------------------------------------------------
# ROC trend helpers
# ---------------------------------------------------------------------------


def _is_rising(series: pd.Series, length: int) -> pd.Series:
    """True if series has been strictly rising for `length` consecutive bars.

    Mirrors Pine Script's ta.rising(series, length):
    series[0] > series[1] AND series[1] > series[2] AND ... for length bars.
    """
    result = pd.Series(True, index=series.index)
    for lag in range(length):
        result = result & (series.shift(lag) > series.shift(lag + 1))
    return result


def _is_falling(series: pd.Series, length: int) -> pd.Series:
    """True if series has been strictly falling for `length` consecutive bars.

    Mirrors Pine Script's ta.falling(series, length).
    """
    result = pd.Series(True, index=series.index)
    for lag in range(length):
        result = result & (series.shift(lag) < series.shift(lag + 1))
    return result


# ---------------------------------------------------------------------------
# Stateful exhaustion state machine
# ---------------------------------------------------------------------------


def _compute_exhaustion_states(
    is_bull: pd.Series,
    is_bear: pd.Series,
) -> tuple[np.ndarray, np.ndarray]:
    """Replicate the Pine Script `var bool` exhaustion state machine.

    The states are sticky: once activated they remain True until a new
    trend of the opposite type begins, exactly matching the Pine Script
    `var bool` persistence semantics.

    Args:
        is_bull: Boolean series — True when isBullTrend is active.
        is_bear: Boolean series — True when isBearTrend is active.

    Returns:
        (bull_exhaustion, bear_exhaustion) — two boolean numpy arrays
        aligned to the input series index.
    """
    bull_arr = is_bull.fillna(False).to_numpy(dtype=bool)
    bear_arr = is_bear.fillna(False).to_numpy(dtype=bool)
    n = len(bull_arr)

    bull_ex = np.zeros(n, dtype=bool)
    bear_ex = np.zeros(n, dtype=bool)

    for i in range(1, n):
        # Previous bar values used as [1] references in Pine Script.
        bull_ex_prev = bull_ex[i - 1]
        bear_ex_prev = bear_ex[i - 1]
        is_bull_prev = bull_arr[i - 1]
        is_bear_prev = bear_arr[i - 1]

        # Update bullExhaustionActive for bar i.
        if bull_arr[i]:
            # Active bull trend → not exhausted.
            bull_current = False
        elif is_bull_prev or bull_ex_prev:
            # Bull trend just ended, or already in exhaustion zone.
            bull_current = True
        else:
            # Neither condition met → keep previous value (var bool semantics).
            bull_current = bull_ex_prev

        # Update bearExhaustionActive for bar i.
        if bear_arr[i]:
            bear_current = False
        elif is_bear_prev or bear_ex_prev:
            bear_current = True
        else:
            bear_current = bear_ex_prev

        # Reset: a new opposite trend kills the exhaustion zone.
        if bear_arr[i]:
            bull_current = False
        if bull_arr[i]:
            bear_current = False

        bull_ex[i] = bull_current
        bear_ex[i] = bear_current

    return bull_ex, bear_ex


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Run runner._process_pair() to attach regime signals and ATR before "
            "calling build_population_masks()."
        )
