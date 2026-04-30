"""Population masks for the BB Range Setup Edge Check.

All signals are computed on entry_tf bars at bar close.  No higher-TF
alignment is needed — this is a single-timeframe test.

No-lookahead:
    BB_basis = rolling SMA(bb_period) on close.  At bar t this includes bar
               t's close — correct because we signal and enter at close.
    BB_std   = rolling StdDev(bb_period) on close.  Same argument.
    ATR warmup bars are excluded by requiring both bb_ready and atr_ready.

Populations (regime_only is the eligible baseline post-warmup):
    regime_only    — EMA-50 bear regime + BB/ATR warm (eligible baseline).
    price_in_bands — regime_only AND BB_lower ≤ close ≤ BB_upper.
                     Price has not yet broken below the lower band — still
                     has room to fall before becoming statistically extended.
    below_upper    — regime_only AND close ≤ BB_upper, WITHOUT lower guard.
                     Superset of price_in_bands — tests whether the lower-
                     band floor (≥ BB_lower) adds value beyond just being
                     below the upper band.
    above_lower    — regime_only AND close ≥ BB_lower, WITHOUT upper cap.
                     Superset of price_in_bands — tests whether capping at
                     BB_upper adds value beyond just being above the lower band.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_tests.setup_bb_range_edge_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: Entry-TF DataFrame with regime signal and ATR column attached.
        config: TestConfig providing ``regime_col``, ``bb_period``,
            ``bb_std_mult``.

    Returns:
        dict with keys: ``regime_only``, ``price_in_bands``,
        ``below_upper``, ``above_lower``.
        All values are boolean pd.Series aligned to df's index.
    """
    _require_columns(df, [config.regime_col, "Close", "atr"])

    close = df["Close"]
    regime = df[config.regime_col].astype(bool)

    bb_basis = close.rolling(config.bb_period).mean()
    bb_std = close.rolling(config.bb_period).std(ddof=1)
    bb_upper = bb_basis + config.bb_std_mult * bb_std
    bb_lower = bb_basis - config.bb_std_mult * bb_std

    # Both BB bands and ATR must be warmed up before any bar is eligible.
    bb_ready = bb_basis.notna() & bb_std.notna()
    atr_ready = df["atr"].notna()
    eligible = regime & bb_ready & atr_ready

    at_or_below_upper = close <= bb_upper
    at_or_above_lower = close >= bb_lower

    return {
        "regime_only": eligible,
        # Primary: price inside the full band envelope.
        "price_in_bands": eligible & at_or_above_lower & at_or_below_upper,
        # Decomposition: only upper cap — does the lower floor add value?
        "below_upper": eligible & at_or_below_upper,
        # Decomposition: only lower floor — does the upper cap add value?
        "above_lower": eligible & at_or_above_lower,
    }


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Run runner._process_pair() to attach regime signals and ATR before "
            "calling build_population_masks()."
        )
