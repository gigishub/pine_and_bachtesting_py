"""Population masks for the VWAP Rejection Candle Setup Edge Check.

─── What is a VWAP Rejection Candle? ───────────────────────────────────────

A VWAP rejection candle is a bearish bar that crossed VWAP from above to
below within the same candle:

    open  > VWAP   — price started the bar above VWAP (buyers in control)
    close < VWAP   — sellers took over and drove it through VWAP

This is meaningful because VWAP is the fair-value benchmark for the session.
Institutions and algorithms often defend or sell at VWAP.  A bar that opens
above VWAP but closes below it signals that a test of VWAP was rejected —
sellers absorbed the move and pushed price back under fair value.

In a bear regime context, this is a continuation signal: VWAP is acting as
resistance rather than support.

─── Clean vs noisy rejection ───────────────────────────────────────────────

A raw VWAP rejection (open > VWAP, close < VWAP) can still have large wicks,
meaning the price probed far above the open (upper wick) or far below the
close (lower wick) within the bar.

For a bearish rejection candle:

    top_wick    = High  − Open    (price tested above the open — upper noise)
    bottom_wick = Close − Low     (price dipped below the close — lower noise)
    candle_range = High − Low

    top_wick_ratio    = top_wick    / candle_range
    bottom_wick_ratio = bottom_wick / candle_range

Diagram of a CLEAN rejection (small wicks, large body):

        ─── High
        |       ← top_wick  (small = sellers rejected any recovery immediately)
    ┌───────┐
    │ OPEN  │ ← open above VWAP
    │       │   ← body (close - open = the actual selling)
    │ CLOSE │ ← close below VWAP
    └───────┘
        |       ← bottom_wick  (small = no recovery from lows)
        ─── Low

A "clean" candle has:
    top_wick_ratio    ≤ max_wick_ratio   (e.g. ≤ 0.20 = top wick < 20% of range)
    bottom_wick_ratio ≤ max_wick_ratio   (e.g. ≤ 0.20 = bottom wick < 20% of range)

This means at least 60% of the candle range is solid body — a decisive move.

Doji candles (High == Low, zero range) are excluded from the clean filter
(wick ratios are undefined) and also from the rejection filter since they
cannot have open != close.

─── Anchored VWAP ──────────────────────────────────────────────────────────

VWAP resets at a configurable anchor (config.vwap_anchor):

    "daily"   → UTC midnight each day  (best for 15m / 1h)
    "weekly"  → Monday 00:00 UTC       (best for 1h / 4h)
    "monthly" → 1st of each month      (best for 4h / daily)

Computed as:
    typical_price[t] = (High + Low + Close) / 3
    vwap[t] = cumsum(typical × volume)[anchor..t] / cumsum(volume)[anchor..t]

groupby(anchor_period).cumsum() is strictly backward — no lookahead.

─── Populations ─────────────────────────────────────────────────────────────

    regime_only            — EMA-50 bear regime + ATR warmed (baseline).

    vwap_rejection         — regime + open > VWAP AND close < VWAP.
                             Any bearish VWAP cross bar, regardless of shape.

    vwap_rejection_clean   — regime + vwap_rejection + both wicks ≤ max_wick_ratio.
                             Clean body: sellers drove price decisively through
                             VWAP with minimal noise at either end.

─── No-lookahead guarantee ─────────────────────────────────────────────────

    VWAP[t] uses only bars within the current anchor window up to bar t.
    open[t], close[t], high[t], low[t] are all bar-t values — no future data.
    Signals are evaluated at bar t close and entered at that close.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_tests.setup_vwap_rejection_edge_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: Entry-TF DataFrame with regime signal and ATR column attached.
            Index must be a DatetimeIndex (UTC).
        config: TestConfig providing VWAP anchor and wick ratio parameters.

    Returns:
        dict with keys: ``regime_only``, ``vwap_rejection``,
        ``vwap_rejection_clean``.
        All values are boolean pd.Series aligned to df's index.
    """
    _require_columns(df, [config.regime_col, "Open", "High", "Low", "Close", "Volume", "atr"])

    open_ = df["Open"]
    high = df["High"]
    low = df["Low"]
    close = df["Close"]
    regime = df[config.regime_col].astype(bool)

    vwap = _anchored_vwap(df, config.vwap_anchor)

    # Core rejection: bearish VWAP cross within the bar.
    rejection = (open_ > vwap) & (close < vwap)

    # Wick ratios — only meaningful when the candle has non-zero range.
    candle_range = high - low
    has_range = candle_range > 0

    # For a bearish candle (open > close): top wick is above open, bottom below close.
    top_wick = (high - open_).clip(lower=0)
    bottom_wick = (close - low).clip(lower=0)

    top_wick_ratio = top_wick / candle_range.where(has_range)
    bottom_wick_ratio = bottom_wick / candle_range.where(has_range)

    clean = (
        has_range
        & (top_wick_ratio <= config.max_wick_ratio)
        & (bottom_wick_ratio <= config.max_wick_ratio)
    )

    eligible = regime & vwap.notna() & df["atr"].notna()

    return {
        "regime_only": eligible,
        "vwap_rejection": eligible & rejection,
        "vwap_rejection_clean": eligible & rejection & clean,
    }


# ---------------------------------------------------------------------------
# VWAP helper
# ---------------------------------------------------------------------------


def _anchored_vwap(df: pd.DataFrame, anchor: str) -> pd.Series:
    """Compute anchored VWAP resetting at the given anchor period.

    Args:
        df:     DataFrame with High, Low, Close, Volume and DatetimeIndex.
        anchor: "daily", "weekly", or "monthly".

    Returns:
        VWAP pd.Series aligned to df.index.
    """
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
