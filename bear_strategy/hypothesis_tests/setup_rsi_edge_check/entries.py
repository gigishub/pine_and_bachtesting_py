"""Population masks for the RSI Setup Edge Check.

All RSI signals are computed on entry_tf bars at bar close.  No higher-TF
alignment is needed — this is a single-timeframe test.

No-lookahead:
    RSI uses Wilder EWM (alpha = 1/period, adjust=False) on close.  At bar t
    the value includes bar t's close — correct because we signal and enter
    at close.
    ATR warmup bars are excluded by requiring both rsi_ready and atr_ready.

Populations (regime_only is the eligible baseline post-warmup):
    regime_only  — EMA-50 bear regime + RSI/ATR warm (eligible baseline).
    rsi_30_50    — regime_only AND RSI > rsi_lower AND RSI < rsi_upper.
                   Bearish zone: momentum is heading down but not yet
                   oversold, leaving room to fall further.
    rsi_below_50 — regime_only AND RSI < rsi_upper, WITHOUT the lower guard.
                   Superset of rsi_30_50 — tests whether excluding oversold
                   bars (RSI < 30) adds value on top of the upper cap.
    rsi_above_30 — regime_only AND RSI > rsi_lower, WITHOUT the upper cap.
                   Superset of rsi_30_50 — tests whether capping at 50 adds
                   value on top of the oversold exclusion.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_tests.setup_rsi_edge_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: Entry-TF DataFrame with regime signal and ATR column attached.
        config: TestConfig providing ``regime_col``, ``rsi_period``,
            ``rsi_lower``, ``rsi_upper``.

    Returns:
        dict with keys: ``regime_only``, ``rsi_30_50``,
        ``rsi_below_50``, ``rsi_above_30``.
        All values are boolean pd.Series aligned to df's index.
    """
    _require_columns(df, [config.regime_col, "Close", "atr"])

    close = df["Close"]
    regime = df[config.regime_col].astype(bool)

    rsi = _compute_rsi(close, config.rsi_period)

    # Both RSI and ATR must be warmed up for a fair comparison baseline.
    rsi_ready = rsi.notna()
    atr_ready = df["atr"].notna()
    eligible = regime & rsi_ready & atr_ready

    in_lower = rsi > config.rsi_lower   # exclude oversold
    in_upper = rsi < config.rsi_upper   # exclude neutral/overbought

    return {
        "regime_only": eligible,
        # Primary: both boundaries active — bearish zone only.
        "rsi_30_50": eligible & in_lower & in_upper,
        # Decomposition: upper cap only — is the RSI > 30 guard adding value?
        "rsi_below_50": eligible & in_upper,
        # Decomposition: lower guard only — does capping at RSI < 50 add value?
        "rsi_above_30": eligible & in_lower,
    }


def _compute_rsi(close: pd.Series, period: int) -> pd.Series:
    """Wilder RSI using EWM smoothing (alpha = 1/period, no lookahead)."""
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False).mean()
    # Replace zero avg_loss to avoid divide-by-zero on flat sequences.
    rs = avg_gain / avg_loss.replace(0.0, float("nan"))
    return 100.0 - (100.0 / (1.0 + rs))


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Run runner._process_pair() to attach regime signals and ATR before "
            "calling build_population_masks()."
        )
