"""Population masks for the EMA20 / VWAP Setup Edge Check.

─── EMA 20 ─────────────────────────────────────────────────────────────────

    ema20[t] = EWM(close, span=20, adjust=False).mean() up to bar t

Pandas EWM is right-aligned and causal: the value at bar t only depends
on bars ≤ t.  No lookahead.

    signal: close[t] < ema20[t]   — price is below the 20-period EMA at close

─── Anchored VWAP ──────────────────────────────────────────────────────────

VWAP is a session-based indicator that resets at a configurable anchor point.

    typical_price[t] = (high[t] + low[t] + close[t]) / 3

    vwap[t] = sum(typical_price[anchor..t] × volume[anchor..t])
              ───────────────────────────────────────────────────
              sum(volume[anchor..t])

The anchor (reset point) is set via config.vwap_anchor:

    "daily"   → resets at UTC midnight (00:00) each day.
                Best for intraday TFs (15m, 5m, 1h).

    "weekly"  → resets at Monday 00:00 UTC each week.
                Best for 1h / 4h swing entries.

    "monthly" → resets at the 1st of each UTC month.
                Best for 4h / daily position-level entries.

Implementation using pandas groupby + cumsum:

    1. Compute an anchor_key series using df.index.to_period(freq)
       where freq = "D" / "W" / "ME" for daily / weekly / monthly.
    2. tp_vol  = typical_price × volume
    3. cum_tp_vol = tp_vol.groupby(anchor_key).cumsum()
    4. cum_vol    = volume.groupby(anchor_key).cumsum()
    5. vwap       = cum_tp_vol / cum_vol

groupby.cumsum() is row-order-preserving and backward-looking within each
group — it accumulates from the first bar of the anchor period to the
current bar.  No lookahead.

─── VWAP Standard Deviation Bands ─────────────────────────────────────────

Within each anchor window we also track the volume-weighted variance of the
typical price around the VWAP.  This gives a ±Nσ band:

    sq_dev[t]    = (typical_price[t] - vwap[t])² × volume[t]
    cum_sq_dev   = sq_dev.groupby(anchor_key).cumsum()
    vwap_std[t]  = sqrt(cum_sq_dev[t] / cum_vol[t])

    lower_band   = vwap[t] - vwap_std_mult × vwap_std[t]

When close[t] < lower_band, price is more than N standard deviations below
the session VWAP — a strong bearish-positioning signal.

The first bar of each anchor window always has vwap_std == 0 (only one
data point), so lower_band == vwap on that bar.  This is handled naturally
— the signal requires a meaningful deviation, so it does not fire on bar 1
of a new session unless vwap_std_mult == 0.

─── Populations ─────────────────────────────────────────────────────────────

    regime_only      — EMA-50 bear regime + EMA + ATR warmed (baseline).
                       All eligible bars after indicator warmup.

    below_ema20      — regime + close < EMA(ema_period).
                       Tests whether price below the EMA adds short edge.

    below_vwap       — regime + close < anchored VWAP.
                       Tests whether price below VWAP adds short edge.

    below_both       — regime + close < EMA AND close < VWAP.
                       Tests whether both conditions combined improve edge.

    below_vwap_1std  — regime + close < VWAP − vwap_std_mult × std.
                       Tests whether price deep below VWAP (lower band) adds
                       extra edge over simple below_vwap.

─── No-lookahead guarantee ─────────────────────────────────────────────────

    EMA[t]         uses close[0..t] only — causal by definition.
    VWAP[t]        uses bars [anchor_start..t] only — no future bars.
    lower_band[t]  derived from same backward window — no lookahead.
    All signals are evaluated at bar t close and entered at that same close.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_tests.setup_ema_vwap_edge_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: Entry-TF DataFrame with regime signal and ATR column attached.
            Index must be a DatetimeIndex (UTC).
        config: TestConfig providing EMA and VWAP parameters.

    Returns:
        dict with keys: ``regime_only``, ``below_ema20``,
        ``below_vwap``, ``below_both``.
        All values are boolean pd.Series aligned to df's index.
    """
    _require_columns(df, [config.regime_col, "Open", "High", "Low", "Close", "Volume", "atr"])

    close = df["Close"]
    regime = df[config.regime_col].astype(bool)

    ema = close.ewm(span=config.ema_period, adjust=False).mean()
    vwap, lower_band = _anchored_vwap(df, config.vwap_anchor, config.vwap_std_mult)

    below_ema = close < ema
    below_vwap_mask = close < vwap
    below_lower_band = close < lower_band

    # Eligibility: EMA and ATR warmed; at least one VWAP bar computed.
    eligible = regime & ema.notna() & vwap.notna() & df["atr"].notna()

    return {
        "regime_only": eligible,
        "below_ema20": eligible & below_ema,
        "below_vwap": eligible & below_vwap_mask,
        "below_both": eligible & below_ema & below_vwap_mask,
        "below_vwap_1std": eligible & below_lower_band,
    }


# ---------------------------------------------------------------------------
# VWAP helper
# ---------------------------------------------------------------------------


def _anchored_vwap(
    df: pd.DataFrame,
    anchor: str,
    std_mult: float,
) -> tuple[pd.Series, pd.Series]:
    """Compute anchored VWAP and its lower standard deviation band.

    Args:
        df:       Entry-TF DataFrame with High, Low, Close, Volume.
        anchor:   Reset period — "daily", "weekly", or "monthly".
        std_mult: Lower band = VWAP − std_mult × volume-weighted std.

    Returns:
        (vwap, lower_band) — both pd.Series aligned to df.index.
    """
    _anchor_freq = {"daily": "D", "weekly": "W", "monthly": "ME"}
    freq = _anchor_freq.get(anchor)
    if freq is None:
        raise ValueError(
            f"Invalid vwap_anchor '{anchor}'. Choose 'daily', 'weekly', or 'monthly'."
        )

    typical = (df["High"] + df["Low"] + df["Close"]) / 3.0
    tp_vol = typical * df["Volume"]

    # Group by anchor period and accumulate within each window.
    anchor_key = df.index.to_period(freq)
    cum_tp_vol = tp_vol.groupby(anchor_key).cumsum()
    cum_vol = df["Volume"].groupby(anchor_key).cumsum()

    vwap = cum_tp_vol / cum_vol

    # Volume-weighted standard deviation within the anchor window.
    sq_dev = (typical - vwap) ** 2 * df["Volume"]
    cum_sq_dev = sq_dev.groupby(anchor_key).cumsum()
    vwap_std = (cum_sq_dev / cum_vol).pow(0.5)

    lower_band = vwap - std_mult * vwap_std

    return vwap, lower_band


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Run runner._process_pair() to attach regime signals and ATR before "
            "calling build_population_masks()."
        )
