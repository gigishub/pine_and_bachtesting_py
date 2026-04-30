"""Population masks for the RVOL Setup Edge Check.

─── What is Relative Volume (RVOL)? ────────────────────────────────────────

RVOL measures how current volume compares to its own recent average:

    RVOL[t] = Volume[t]  /  rolling_mean(Volume, vol_ma_len)[t]

Reading the value:

    RVOL = 1.0   → exactly average — nothing notable
    RVOL = 0.5   → half the normal volume — quiet, low conviction
    RVOL = 1.5   → 50% ABOVE average — the threshold used here
    RVOL = 2.0   → double average — strong participation
    RVOL = 3.0+  → exceptional spike — news, liquidation, momentum

The rolling mean is pandas .rolling(N).mean() which is right-aligned: at
bar t it uses bars [t-N+1 … t].  No lookahead.

─── The min_bars_active parameter ──────────────────────────────────────────

On HIGHER timeframes (4h, 1d) a single spike bar is meaningful because each
candle already represents a long window of real trading activity.

On LOWER timeframes (15m, 5m, 1m) a single spike bar can be noise — a brief
burst that reverses within the next bar.  Requiring N consecutive bars above
the threshold filters out these false signals.

How it works:

    spike_raw = (rvol >= threshold)          # per-bar boolean True/False

    If min_bars_active == 1:
        spike = spike_raw                    # single bar is enough

    If min_bars_active >= 2:
        spike = spike_raw.rolling(min_bars_active).min().astype(bool)

The key insight: rolling().min() over a 0/1 (False/True) series equals 1
only if EVERY bar in the rolling window was 1.  This means:

    spike[t] = True  iff  rvol[t-N+1] >= threshold
                      AND  rvol[t-N+2] >= threshold
                      ...
                      AND  rvol[t]     >= threshold

All N consecutive bars must be above the threshold.  Still no lookahead:
the rolling window only reaches backward from bar t.

Recommended settings by timeframe:

    1d / 4h  →  min_bars_active = 1   (single spike bar)
    1h       →  min_bars_active = 1–2
    15m      →  min_bars_active = 2–3
    5m       →  min_bars_active = 3

─── Populations ─────────────────────────────────────────────────────────────

    regime_only          — EMA-50 bear regime + vol_ma + ATR warmed (baseline).
                           All eligible regime bars after indicator warmup.

    rvol_spike           — regime + RVOL ≥ threshold (for min_bars_active bars).
                           Tests whether volume participation alone adds edge.

    rvol_spike_bearish   — rvol_spike + close < open (bearish candle body).
                           Tests whether high-volume bearish candles add edge.

    rvol_spike_down      — rvol_spike + close < close.shift(1) (price declined).
                           Tests whether a high-volume down-move confirms short.

─── No-lookahead guarantee ─────────────────────────────────────────────────

    vol_ma[t]    = mean of Volume[t-N+1 … t]       — backward window only
    rvol[t]      = Volume[t] / vol_ma[t]            — both known at bar t
    spike[t]     = rolling min over [t-N+1 … t]     — backward window only
    bearish[t]   = close[t] < open[t]               — same bar, no future data
    down[t]      = close[t] < close[t-1]            — same bar vs prior close
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_tests.setup_rvol_edge_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: Entry-TF DataFrame with regime signal and ATR column attached.
        config: TestConfig providing RVOL and threshold parameters.

    Returns:
        dict with keys: ``regime_only``, ``rvol_spike``,
        ``rvol_spike_bearish``, ``rvol_spike_down``.
        All values are boolean pd.Series aligned to df's index.
    """
    _require_columns(df, [config.regime_col, "Close", "Open", "Volume", "atr"])

    close = df["Close"]
    open_ = df["Open"]
    regime = df[config.regime_col].astype(bool)

    # Rolling average volume (right-aligned — no lookahead).
    vol_ma = df["Volume"].rolling(config.vol_ma_len).mean()
    rvol = df["Volume"] / vol_ma

    # Per-bar spike: volume is ≥ threshold × its rolling average.
    spike_raw = rvol >= config.rvol_threshold

    # Apply min_bars_active persistence: require N consecutive spike bars.
    if config.min_bars_active > 1:
        # rolling min over a bool-as-int: 1 only if ALL bars in window are True.
        spike = spike_raw.rolling(config.min_bars_active).min().astype(bool)
    else:
        spike = spike_raw

    # Direction filters (applied on top of the spike condition).
    bearish_candle = close < open_                  # close below open on this bar
    price_declined = close < close.shift(1)         # close below previous close

    # Eligibility: vol_ma and ATR fully warmed.
    eligible = regime & vol_ma.notna() & df["atr"].notna()

    return {
        "regime_only": eligible,
        "rvol_spike": eligible & spike,
        "rvol_spike_bearish": eligible & spike & bearish_candle,
        "rvol_spike_down": eligible & spike & price_declined,
    }


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Run runner._process_pair() to attach regime signals and ATR before "
            "calling build_population_masks()."
        )
