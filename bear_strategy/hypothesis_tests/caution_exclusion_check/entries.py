"""Population masks for Step 2b — Caution Exclusion Filter.

Two caution conditions identify bars where the short edge degrades:

    is_caution = (close > EMA(close, 20))           ← local momentum weakening
                 OR (range7 > ATR(7) × 1.5)          ← choppy, not trending

    range7 = current High − min(Low, last range_period bars)
             This measures the recent swing from local lows to current bar.

Populations (regime_only is the eligible baseline post-warmup):
    regime_only  — EMA-50 bear + warmup guard (eligible baseline)
    ema20_filter — regime + close ≤ EMA(20)   (removes reclaim bars only)
    range_filter — regime + range7 ≤ ATR×1.5  (removes chop bars only)
    no_caution   — regime + both conditions   (full exclusion)

Subset relationships (used in tests):
    no_caution ⊆ ema20_filter ⊆ regime_only
    no_caution ⊆ range_filter ⊆ regime_only

No-lookahead:
    EMA(20) at bar t uses ewm up to and including bar t's close.
    Entering and signalling occur simultaneously at bar close — no shift needed.
    range7 at bar t uses current High and rolling min of Low over last range_period
    bars (including bar t) — all values known at close.
    ATR at bar t uses EWM over TR; TR uses current H/L and previous close.
    Warmup gate: range7.notna() (requires range_period bars) and atr.notna().

    Known limitation: compute_regime_signals() maps daily signals backward onto
    intraday bars using merge_asof. Same-day intraday bars can see the current
    day's regime before the daily close. This pre-exists in strategy/signals.py
    and is consistent across all hypothesis steps.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_tests.caution_exclusion_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: Entry-TF DataFrame with regime signal, ATR, and OHLCV columns.
        config: TestConfig with filter parameters.

    Returns:
        Dict with keys ``regime_only``, ``ema20_filter``, ``range_filter``,
        ``no_caution``. All are boolean pd.Series aligned to df's index.
    """
    _require_columns(df, [config.regime_col, "Close", "High", "Low", "atr"])

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    atr = df["atr"]
    regime = df[config.regime_col].astype(bool)

    # Caution condition 1: local momentum weakening
    ema20 = close.ewm(span=config.ema20_period, adjust=False).mean()
    above_ema20 = close > ema20

    # Caution condition 2: choppy, not trending
    # range7 = current high minus the rolling minimum low over range_period bars
    range7 = high - low.rolling(config.range_period).min()
    wide_range = range7 > (atr * config.range_atr_mult)

    # Warmup: range7 requires range_period bars before producing a valid value;
    # ATR requires at least 1 bar (first bar has no prev_close → TR is NaN).
    # ema20 is non-NaN from bar 0 but meaningful only after several bars;
    # guarded by range7 anyway since range_period > 1.
    range_ready = range7.notna()
    atr_ready = atr.notna()
    ema20_ready = ema20.notna()
    eligible = regime & range_ready & atr_ready & ema20_ready

    return {
        # Eligible regime baseline — comparison anchor for the verdict.
        "regime_only": eligible,
        # Removes bars where price is reclaiming the local EMA — momentum weakening.
        "ema20_filter": eligible & ~above_ema20,
        # Removes bars where the recent swing is too wide — choppy noise.
        "range_filter": eligible & ~wide_range,
        # Full exclusion: removes bars that fail either condition.
        "no_caution": eligible & ~above_ema20 & ~wide_range,
    }


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Run runner._process_pair() to attach regime signals and ATR before "
            "calling build_population_masks()."
        )
