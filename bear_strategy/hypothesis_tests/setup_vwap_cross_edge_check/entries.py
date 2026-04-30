"""Population masks for the VWAP Cross-Below Setup Edge Check.

─── Logic: identical to EMA cross, using VWAP as the level ─────────────────

See setup_ema_cross_edge_check/entries.py for the full explanation of the
rolling-min "sustained above" technique.  The only difference here is that
the reference level is the session-anchored VWAP instead of a fixed EMA.

─── Why VWAP instead of EMA? ───────────────────────────────────────────────

EMA is a price-only average that smooths historical closes.
VWAP is the volume-weighted average price for the current session — it tells
you where the average participant entered, weighted by how much they traded.

Crossing below VWAP means price has moved below the session's fair value as
judged by actual transaction volume.  In a bear regime, this is a session-
level confirmation that sellers are back in control.

The VWAP resets each anchor period (daily / weekly / monthly), so the
"sustained above VWAP" qualifier measures: for how many bars within THIS
session was price above the session average before it broke down.

─── Anchored VWAP ──────────────────────────────────────────────────────────

    typical_price[t] = (High + Low + Close) / 3
    vwap[t] = cumsum(typical × volume)[anchor_start..t]
              ──────────────────────────────────────────
              cumsum(volume)[anchor_start..t]

The anchor resets at:
    "daily"   → UTC midnight each day
    "weekly"  → Monday 00:00 UTC
    "monthly" → 1st of each month

groupby(anchor_period).cumsum() is strictly backward — no lookahead.

─── The min_bars_above qualifier ───────────────────────────────────────────

    above[t] = 1  if  close[t] > vwap[t],  else 0

    sustained[t] = above.shift(1).rolling(min_bars_above).min() == 1

    rolling_min over a 0/1 series equals 1 only when EVERY bar in the
    window was 1, so all N bars immediately before bar t had close > VWAP.

Example — daily VWAP, min_bars_above=3, session opens bullishly then fades:

    bar:   09:00  10:00  11:00  12:00  13:00
    above:   1      1      1      0      0
    cross:   —      —      —    ✅cross  no (not a cross)
    sust.:   —      —      —    rolling_min([1,1,1])=1  ✅

─── Populations ─────────────────────────────────────────────────────────────

    regime_only          — EMA-50 bear regime + ATR warmed (baseline).

    vwap_cross_below     — regime + close[t] < VWAP[t] AND close[t-1] > VWAP[t-1].
                           Any VWAP cross, including 1-bar whipsaws.

    vwap_cross_below_N   — regime + cross AND ≥ min_bars_above consecutive
                           bars above VWAP before the cross.
                           Sustained session control before the breakdown.

─── No-lookahead guarantee ─────────────────────────────────────────────────

    VWAP[t] uses only bars [anchor_start..t] — no future data.
    above[t] depends on close[t] and VWAP[t] — both at bar t close.
    sustained[t] uses above.shift(1).rolling(N).min() — window ends at t-1.
    Cross uses close[t] vs close[t-1] — no future data.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_tests.setup_vwap_cross_edge_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: Entry-TF DataFrame with regime signal and ATR column attached.
            Index must be a DatetimeIndex (UTC).
        config: TestConfig providing VWAP anchor and min_bars_above parameters.

    Returns:
        dict with keys: ``regime_only``, ``vwap_cross_below``,
        ``vwap_cross_below_N``.
        All values are boolean pd.Series aligned to df's index.
    """
    _require_columns(df, [config.regime_col, "High", "Low", "Close", "Volume", "atr"])

    close = df["Close"]
    regime = df[config.regime_col].astype(bool)

    vwap = _anchored_vwap(df, config.vwap_anchor)

    # Per-bar flag: 1 if close was above VWAP on that bar.
    above = (close > vwap).astype(float)

    # Cross-below: this bar closed below VWAP, previous bar was above VWAP.
    crossed_below = (close < vwap) & (close.shift(1) > vwap.shift(1))

    # Sustained above: all min_bars_above bars immediately before this bar
    # had close > VWAP.
    sustained_before = (
        above.shift(1).rolling(config.min_bars_above).min() == 1.0
    )

    eligible = regime & vwap.notna() & df["atr"].notna() & close.shift(1).notna()

    return {
        "regime_only": eligible,
        "vwap_cross_below": eligible & crossed_below,
        "vwap_cross_below_N": eligible & crossed_below & sustained_before,
    }


# ---------------------------------------------------------------------------
# VWAP helper
# ---------------------------------------------------------------------------


def _anchored_vwap(df: pd.DataFrame, anchor: str) -> pd.Series:
    """Compute anchored VWAP resetting at the given anchor period."""
    _anchor_freq = {"daily": "D", "weekly": "W", "monthly": "ME"}
    freq = _anchor_freq.get(anchor)
    if freq is None:
        raise ValueError(
            f"Invalid vwap_anchor '{anchor}'. Choose 'daily', 'weekly', or 'monthly'."
        )

    typical = (df["High"] + df["Low"] + df["Close"]) / 3.0
    tp_vol = typical * df["Volume"]

    anchor_key = df.index.to_period(freq)
    cum_tp_vol = tp_vol.groupby(anchor_key).cumsum()
    cum_vol = df["Volume"].groupby(anchor_key).cumsum()

    return cum_tp_vol / cum_vol


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Run runner._process_pair() to attach regime signals and ATR before "
            "calling build_population_masks()."
        )
