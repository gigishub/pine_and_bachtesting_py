"""Population masks for the EMA Cross-Below Setup Edge Check.

─── What is an EMA Cross-Below? ────────────────────────────────────────────

An EMA cross-below fires on bar t when:

    close[t]   < EMA[t]      ← price is now below the EMA
    close[t-1] > EMA[t-1]    ← price was above the EMA on the previous bar

This is the first bar where price has fallen through the EMA line — a
momentum shift from "trading above fair value" to "trading below fair value".

─── The min_bars_above qualifier ───────────────────────────────────────────

A raw cross can happen after price was only above EMA for one bar — that is
often noise (e.g. a single wick that briefly closed above EMA).

The min_bars_above qualifier requires that price was CONTINUOUSLY above EMA
for at least N bars before the cross bar.  The idea: a longer stay above EMA
represents a more established bullish short-term structure, so when it breaks
it is a more meaningful signal.

Implementation using rolling min:

    Step 1: Mark which bars were above EMA.
        above[t] = 1  if  close[t] > EMA[t]
                   0  otherwise

    Step 2: For each bar t, check whether ALL of the N bars ending at t-1
            were above EMA.
        sustained[t] = rolling_min(above, window=N)[t-1]
                     = above.shift(1).rolling(min_bars_above).min()

        rolling_min over a 0/1 series equals 1 only if every bar in the
        window was 1.  This ensures all N bars immediately before bar t
        had close > EMA — no gaps allowed.

    Step 3: Combine with the cross condition.
        ema_cross_below_N[t] = crossed_below[t]  AND  sustained[t] == 1

Example with min_bars_above = 3:

    bar:  t-4  t-3  t-2  t-1   t
    above:  0    1    1    1    0   ← cross at t
                                     sustained: rolling_min([1,1,1]) = 1  ✅

    bar:  t-4  t-3  t-2  t-1   t
    above:  1    0    1    1    0   ← cross at t
                                     sustained: rolling_min([0,1,1]) = 0  ❌
                                     (had a gap at t-3 — not sustained)

    bar:  t-4  t-3  t-2  t-1   t
    above:  1    1    1    1    0   ← cross at t
                                     sustained: rolling_min([1,1,1]) = 1  ✅
                                     (4 bars above is more than enough)

─── No-lookahead guarantee ─────────────────────────────────────────────────

    EMA[t] uses close[0..t] only — causal by definition (EWM adjust=False).
    above[t] depends only on close[t] and EMA[t] — both known at bar t close.
    sustained[t] uses above.shift(1).rolling(N).min() — the window ends at
    bar t-1 and reaches back N bars.  No future data.
    The cross condition compares bar t with bar t-1 — no future data.

    All signals are evaluated at bar t close and entered at that same close.

─── Populations ─────────────────────────────────────────────────────────────

    regime_only         — EMA-50 bear regime + EMA + ATR warmed (baseline).
                          All eligible bars after indicator warmup.

    ema_cross_below     — regime + close crossed below EMA(ema_period) this bar.
                          Any cross, regardless of how long price was above.
                          Includes noisy single-bar whipsaws.

    ema_cross_below_N   — regime + crossed below EMA AND was continuously above
                          EMA for at least min_bars_above bars before the cross.
                          The sustained qualifier: filters for meaningful breaks
                          after an established hold above EMA.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_tests.setup_ema_cross_edge_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: Entry-TF DataFrame with regime signal and ATR column attached.
        config: TestConfig providing EMA and min_bars_above parameters.

    Returns:
        dict with keys: ``regime_only``, ``ema_cross_below``,
        ``ema_cross_below_N``.
        All values are boolean pd.Series aligned to df's index.
    """
    _require_columns(df, [config.regime_col, "Close", "atr"])

    close = df["Close"]
    regime = df[config.regime_col].astype(bool)

    ema = close.ewm(span=config.ema_period, adjust=False).mean()

    # Per-bar flag: 1 if close was above EMA, 0 otherwise.
    above = (close > ema).astype(float)

    # Cross-below: this bar closed below EMA, previous bar was above.
    crossed_below = (close < ema) & (close.shift(1) > ema.shift(1))

    # Sustained above: all min_bars_above bars immediately before this bar
    # had close > EMA.  rolling().min() == 1 only when every bar in the
    # window is 1.
    sustained_before = (
        above.shift(1).rolling(config.min_bars_above).min() == 1.0
    )

    # Eligibility: EMA and ATR fully warmed.
    # EMA needs ema_period bars; ATR needs atr_period bars.
    # crossed_below also needs one prior bar valid.
    eligible = regime & ema.notna() & df["atr"].notna() & close.shift(1).notna()

    return {
        "regime_only": eligible,
        "ema_cross_below": eligible & crossed_below,
        "ema_cross_below_N": eligible & crossed_below & sustained_before,
    }


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Run runner._process_pair() to attach regime signals and ATR before "
            "calling build_population_masks()."
        )
