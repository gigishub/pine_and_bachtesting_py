"""Population masks for Setup 2 – Trigger 1: zone-sequence signals.

Baseline: regime AND kde_upper (4h). All populations are strict subsets.

All trigger_1 through trigger_5 signals are stateful: they require a
"zone touch" event (entry-TF bar's high >= kde_peak_aligned) and then fire
on subsequent bars within a lookback window.

Zone touch state resets when:
  - The regime gate or kde_upper gate deactivates (gate_active goes False).
  - The aligned 4h kde_peak value changes (new 4h reference snapshot).

No-lookahead guarantee:
  The aligned 4h kde_peak originates from runner.py where the entire 4h KDE
  output is .shift(1) before merge_asof alignment — so every entry-TF bar
  carries only the most recently *completed* 4h bar's levels.

  Within the state machine, signals are computed using bar i's OHLCV against
  state recorded at a *prior* bar (touch_idx < i).  The short ATR passed in
  is evaluated at position i-1 (prior bar) for signal 1 to avoid
  self-reference on the expansion bar.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_2_trigger_1_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return one boolean mask per population.

    Args:
        df: Entry-TF DataFrame with regime, atr, atr_short, kde_upper (bool),
            kde_peak (price), and OHLCV columns.
        config: TestConfig instance.

    Returns:
        dict mapping population name -> boolean pd.Series on df's index.
    """
    _require_columns(
        df,
        [
            config.regime_col,
            "Open", "High", "Low", "Close",
            "atr", "atr_short", "kde_upper", "kde_peak",
        ],
    )

    regime = df[config.regime_col].astype(bool)
    kde_upper = df["kde_upper"].infer_objects(copy=False).fillna(False).astype(bool)
    kde_peak = df["kde_peak"]
    kde_ready = kde_peak.notna()
    atr = df["atr"]

    baseline = regime & kde_upper & atr.notna() & kde_ready

    # gate_active drives the state machine — zone touches only count when
    # the full regime + kde_upper baseline is active
    gate_active = baseline.to_numpy(dtype=bool)

    signals = _compute_zone_triggered_signals(
        high=df["High"].to_numpy(dtype=float),
        low=df["Low"].to_numpy(dtype=float),
        close=df["Close"].to_numpy(dtype=float),
        open_=df["Open"].to_numpy(dtype=float),
        kde_peak_arr=kde_peak.to_numpy(dtype=float),
        atr_arr=atr.to_numpy(dtype=float),
        atr_short_arr=df["atr_short"].to_numpy(dtype=float),
        gate_active=gate_active,
        lookback=config.zone_touch_lookback,
        low_lookback=config.zone_touch_low_lookback,
        retest_lookback=config.retest_lookback,
        retest_proximity_atr=config.retest_proximity_atr,
        atr_expansion_mult=config.atr_expansion_mult,
        consec_n=config.consec_bearish_n,
        index=df.index,
    )

    rsi = _compute_rsi(df["Close"], config.rsi_period)
    rsi_below = rsi < config.rsi_threshold

    return {
        "kde_upper_baseline":  baseline,
        "trigger_1_atr_exp":   baseline & signals["atr_expansion"],
        "trigger_2_consec":    baseline & signals["consec_bearish"],
        "trigger_3_lower_high": baseline & signals["lower_high"],
        "trigger_4_low_viol":  baseline & signals["touch_low_violation"],
        "trigger_5_retest":    baseline & signals["failed_retest"],
        "trigger_6_rsi_below": baseline & rsi_below,
    }


def _compute_zone_triggered_signals(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    open_: np.ndarray,
    kde_peak_arr: np.ndarray,
    atr_arr: np.ndarray,
    atr_short_arr: np.ndarray,
    gate_active: np.ndarray,
    lookback: int,
    low_lookback: int,
    retest_lookback: int,
    retest_proximity_atr: float,
    atr_expansion_mult: float,
    consec_n: int,
    index: pd.Index,
) -> dict[str, pd.Series]:
    """Single-pass state machine computing all zone-sequenced trigger signals.

    Returns dict of signal name -> pd.Series[bool].
    """
    n = len(close)

    atr_exp_sig   = np.zeros(n, dtype=bool)
    consec_sig    = np.zeros(n, dtype=bool)
    lower_h_sig   = np.zeros(n, dtype=bool)
    low_viol_sig  = np.zeros(n, dtype=bool)
    retest_sig    = np.zeros(n, dtype=bool)

    # Zone-touch state
    touch_idx: int = -1
    touch_high: float = np.nan
    touch_low: float = np.nan
    touch_range: float = np.nan

    # Running max high seen between the touch bar and the current bar
    # (updated with high[i-1] at bar i — only completed bars)
    max_inter_high: float = -np.inf
    max_inter_high_open: float = np.nan

    was_gate_active: bool = False

    for i in range(consec_n, n):  # need consec_n prior bars for signal 2
        curr_gate = gate_active[i]

        if not curr_gate:
            if was_gate_active:
                # Gate just deactivated — wipe zone-touch state
                touch_idx = -1
                touch_high = np.nan
                touch_low = np.nan
                touch_range = np.nan
                max_inter_high = -np.inf
                max_inter_high_open = np.nan
            was_gate_active = False
            continue

        peak = kde_peak_arr[i]
        if np.isnan(peak):
            was_gate_active = False
            continue

        # Reset on 4h level change (new KDE snapshot arrived)
        if (was_gate_active and touch_idx >= 0
                and not np.isnan(kde_peak_arr[i - 1])
                and peak != kde_peak_arr[i - 1]):
            touch_idx = -1
            touch_high = np.nan
            touch_low = np.nan
            touch_range = np.nan
            max_inter_high = -np.inf
            max_inter_high_open = np.nan

        was_gate_active = True

        # ---------------------------------------------------------------- #
        # Register zone touch: entry-TF high tags or exceeds 4h kde_peak   #
        # ---------------------------------------------------------------- #
        if high[i] >= peak:
            touch_idx = i
            touch_high = high[i]
            touch_low = low[i]
            touch_range = high[i] - low[i]
            max_inter_high = -np.inf
            max_inter_high_open = np.nan
            continue  # signals fire on bars AFTER the touch bar

        if touch_idx < 0:
            continue  # no zone touch yet in this gate window

        bars = i - touch_idx  # >= 1 (touch bar is excluded by continue above)

        # Update running max of highs seen between touch and current bar.
        # At bar i, bar i-1 is the last completed bar we haven't yet included.
        if i - 1 > touch_idx:
            prev_high = high[i - 1]
            if prev_high > max_inter_high:
                max_inter_high = prev_high
                max_inter_high_open = open_[i - 1]

        # ---------------------------------------------------------------- #
        # Signal 1: ATR expansion bearish turn                              #
        # bar_range > mult × atr_short(prior bar)  AND  close < open       #
        # AND  close < prev_close                                           #
        # ---------------------------------------------------------------- #
        if bars <= lookback:
            prior_atr_short = atr_short_arr[i - 1]
            if (not np.isnan(prior_atr_short) and prior_atr_short > 0
                    and (high[i] - low[i]) > atr_expansion_mult * prior_atr_short
                    and close[i] < open_[i]
                    and close[i] < close[i - 1]):
                atr_exp_sig[i] = True

        # ---------------------------------------------------------------- #
        # Signal 2: consecutive bearish closes                              #
        # Last consec_n bars each close strictly below the prior close.     #
        # At bar i: close[i] < close[i-1] < ... < close[i-consec_n+1]      #
        # ---------------------------------------------------------------- #
        if bars <= lookback:
            ok = True
            for k in range(consec_n):
                if not (close[i - k] < close[i - k - 1]):
                    ok = False
                    break
            if ok:
                consec_sig[i] = True

        # ---------------------------------------------------------------- #
        # Signal 3: lower high formation                                    #
        # Highest high since zone touch is strictly below touch_high AND   #
        # current bar closes bearishly AND below the lower-high bar's open. #
        # ---------------------------------------------------------------- #
        if bars >= 2 and bars <= lookback:
            if (max_inter_high < touch_high
                    and not np.isnan(max_inter_high_open)
                    and close[i] < open_[i]
                    and close[i] < max_inter_high_open):
                lower_h_sig[i] = True

        # ---------------------------------------------------------------- #
        # Signal 4: zone-touch bar low violation                            #
        # Close strictly below the touch bar's low.                         #
        # ---------------------------------------------------------------- #
        if bars <= low_lookback and not np.isnan(touch_low):
            if close[i] < touch_low:
                low_viol_sig[i] = True

        # ---------------------------------------------------------------- #
        # Signal 5: failed retest                                           #
        # After at least 1 bar of pullback, price returns to within         #
        # retest_proximity_atr ATRs of kde_peak (from below).               #
        # Retest bar: close < midpoint, close < prev_close, range < touch_range. #
        # ---------------------------------------------------------------- #
        if bars >= 2 and bars <= retest_lookback:
            curr_atr = atr_arr[i]
            if not np.isnan(curr_atr) and curr_atr > 0:
                # high[i] < peak is guaranteed (would have `continue`'d above)
                near_zone = high[i] >= (peak - retest_proximity_atr * curr_atr)
                if near_zone:
                    bar_mid = (high[i] + low[i]) / 2.0
                    if (close[i] < bar_mid
                            and close[i] < close[i - 1]
                            and (high[i] - low[i]) < touch_range):
                        retest_sig[i] = True

    return {
        "atr_expansion":      pd.Series(atr_exp_sig,  index=index),
        "consec_bearish":     pd.Series(consec_sig,   index=index),
        "lower_high":         pd.Series(lower_h_sig,  index=index),
        "touch_low_violation": pd.Series(low_viol_sig, index=index),
        "failed_retest":      pd.Series(retest_sig,   index=index),
    }


def _compute_rsi(close: pd.Series, period: int) -> pd.Series:
    """Wilder RSI using exponential smoothing (standard definition)."""
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)
    avg_gain = gain.ewm(com=period - 1, adjust=False).mean()
    avg_loss = loss.ewm(com=period - 1, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, float("nan"))
    return 100 - (100 / (1 + rs))


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Ensure runner._process_pair() attaches all signals first."
        )
