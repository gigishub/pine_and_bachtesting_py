"""Population masks for the EMA Cross-Below Setup Edge Check.

─── What is an EMA Cross-Below? ────────────────────────────────────────────

An EMA cross-below is the specific bar where price transitions from above
the EMA to below it:

    bar t-1:  close[t-1] > EMA[t-1]   (was above)
    bar t:    close[t]   < EMA[t]     (now below)

This is very different from simply being below the EMA.  In a bear regime,
most bars are already below the EMA — the cross captures the precise moment
a rally ends and the downtrend resumes.

─── Why require N bars above first? ────────────────────────────────────────

A raw cross can fire after just one bar above the EMA — a single noise bar
that briefly poked above and came straight back.  That is not a meaningful
rally.

By requiring min_bars_above consecutive bars above EMA before the cross, we
ensure the signal describes a real counter-trend bounce that has now failed:

    price was above EMA for ≥ N bars  →  a genuine pullback or rally
    then close < EMA on this bar      →  the rally failed; downtrend resumes

─── Implementation ─────────────────────────────────────────────────────────

    ema[t]       = EWM(close, span=ema_period, adjust=False).mean()
    above_ema[t] = close[t] > ema[t]            ← True if above EMA

    Any cross (ema_cross_below):
        cross[t] = (close[t] < ema[t])           ← below now
                   AND above_ema[t-1]             ← was above 1 bar ago

    Sustained cross (ema_cross_below_sustained):
        # Were the last min_bars_above bars ALL above EMA?
        # above_ema shifted by 1 so the window covers bars [t-1, t-2, ..., t-N].
        sustained[t] = rolling_min(above_ema.shift(1), window=min_bars_above)[t] == True

        sustained_cross[t] = (close[t] < ema[t])  AND  sustained[t]

The rolling_min trick:
    rolling(N).min() over a boolean (0/1) series equals 1 only if ALL N
    values in the window are 1.  So sustained[t] is True iff every one of
    bars t-1, t-2, ..., t-N was above the EMA.

    Crucially: after the shift(1), the window never includes bar t itself —
    only prior bars.  No lookahead.

Timeline example (min_bars_above = 3):

    bar  | close > ema | cross_below | sustained_cross
    -----|-------------|-------------|----------------
    t-4  |    True     |      -      |       -
    t-3  |    True     |      -      |       -
    t-2  |    True     |      -      |       -
    t-1  |    True     |      -      |       -      ← 4 bars above
    t    |    False    |    True     |     True     ← cross fires

─── Populations ─────────────────────────────────────────────────────────────

    regime_only              — EMA-50 bear regime + EMA + ATR warmed (baseline).

    ema_cross_below          — regime + any downward EMA cross.
                               Tests whether the cross moment itself (even
                               after just 1 bar above) has predictive value.

    ema_cross_below_sustained — regime + cross after ≥ min_bars_above bars above.
                               Tests whether requiring a genuine rally before
                               the breakdown improves signal quality.

─── No-lookahead guarantee ─────────────────────────────────────────────────

    ema[t]         uses close[0..t] only — EWM is causal.
    above_ema[t-1] uses the previous bar — no current bar data.
    rolling_min on shift(1) uses bars [t-N..t-1] — purely historical.
    Signal at bar t uses only information available at bar t's close.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_tests.setup_ema_cross_below_edge_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: Entry-TF DataFrame with regime signal and ATR column attached.
        config: TestConfig providing EMA period and min_bars_above.

    Returns:
        dict with keys: ``regime_only``, ``ema_cross_below``,
        ``ema_cross_below_sustained``.
        All values are boolean pd.Series aligned to df's index.
    """
    _require_columns(df, [config.regime_col, "Close", "atr"])

    close = df["Close"]
    regime = df[config.regime_col].astype(bool)

    ema = close.ewm(span=config.ema_period, adjust=False).mean()
    above_ema = close > ema

    # Any cross: below now, above on the previous bar.
    any_cross = (close < ema) & above_ema.shift(1).fillna(False)

    # Sustained cross: below now AND all of the last min_bars_above bars were above.
    # shift(1) moves the window to bars [t-1, t-2, ..., t-N] — no current bar.
    sustained_above = (
        above_ema.shift(1)
        .rolling(config.min_bars_above)
        .min()
        .fillna(0)
        .astype(bool)
    )
    sustained_cross = (close < ema) & sustained_above

    # Eligibility: EMA and ATR warmed.
    eligible = regime & ema.notna() & df["atr"].notna()

    return {
        "regime_only": eligible,
        "ema_cross_below": eligible & any_cross,
        "ema_cross_below_sustained": eligible & sustained_cross,
    }


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Run runner._process_pair() to attach regime signals and ATR before "
            "calling build_population_masks()."
        )
