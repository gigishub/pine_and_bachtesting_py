"""Population masks for the BB Widening Setup Edge Check.

All BB signals are computed on entry_tf bars at bar close.  No higher-TF
alignment is needed — this test is single-timeframe.

No-lookahead:
    BB_width  = BB_upper − BB_lower = 2 × bb_std_mult × std(close, bb_period).
                At bar t this includes bar t's close — correct because we
                signal and enter at close.
    bb_widening = BB_width > BB_width.shift(1) — uses only the previous
                bar's width, no future data.
    ATR warmup bars are excluded by requiring both bb_ready and atr_ready.

Populations (regime_only is the eligible baseline post-warmup):
    regime_only          — EMA-50 bear regime + BB/ATR warm (eligible baseline).

    bb_widening          — regime_only AND BB bands are expanding
                           (BB_width > BB_width[1]).
                           Captures bars where volatility is picking up —
                           in a bear regime this often precedes an
                           accelerating downward move.

    bb_widening_bearish  — bb_widening AND close < BB_basis.
                           Bands widening AND price already in the lower half
                           of the channel — directional confirmation on top
                           of the volatility signal.

    bb_widening_breakout — bb_widening AND close < BB_lower.
                           Bands widening AND price has broken below the lower
                           band — extreme momentum during a volatility expansion.

Note: bb_widening_bearish ⊃ bb_widening_breakout (breakout implies below-basis).
Comparing all three against regime_only isolates how much value each layer of
price-position filtering adds on top of the widening signal alone.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_tests.setup_bb_edge_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: Entry-TF DataFrame enriched with regime signal and ATR column.
        config: TestConfig providing ``regime_col``, ``bb_period``,
            ``bb_std_mult``.

    Returns:
        dict with keys: ``regime_only``, ``bb_widening``,
        ``bb_widening_bearish``, ``bb_widening_breakout``.
        All values are boolean pd.Series aligned to df's index.
    """
    _require_columns(df, [config.regime_col, "Close", "atr"])

    close = df["Close"]
    regime = df[config.regime_col].astype(bool)

    bb_std = close.rolling(config.bb_period).std(ddof=1)
    bb_basis = close.rolling(config.bb_period).mean()
    bb_upper = bb_basis + config.bb_std_mult * bb_std
    bb_lower = bb_basis - config.bb_std_mult * bb_std
    bb_width = bb_upper - bb_lower   # = 2 × bb_std_mult × std

    # Expanding bands: width is larger than the previous bar's width.
    widening = bb_width > bb_width.shift(1)
    below_basis = close < bb_basis
    below_lower = close < bb_lower

    # Eligibility: both BB and ATR must be warmed for a fair comparison.
    bb_ready = bb_basis.notna() & bb_std.notna() & bb_width.shift(1).notna()
    atr_ready = df["atr"].notna()
    eligible = regime & bb_ready & atr_ready

    return {
        # Eligible regime baseline — comparison anchor in the verdict.
        "regime_only": eligible,
        # Primary: volatility picking up (bands expanding).
        "bb_widening": eligible & widening,
        # Widening + price in lower half of the channel (directional bias).
        "bb_widening_bearish": eligible & widening & below_basis,
        # Widening + price broken below the lower band (extreme momentum).
        "bb_widening_breakout": eligible & widening & below_lower,
    }


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Run runner._process_pair() to attach regime signals and ATR before "
            "calling build_population_masks()."
        )
