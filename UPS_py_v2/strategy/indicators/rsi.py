"""RSI (Relative Strength Index) filter for the UPS strategy.

Uses Wilder smoothing (RMA) to match Pine Script's ta.rsi exactly.
Pure pandas functions — no side effects.
"""

from __future__ import annotations

import pandas as pd

from .atr import ind_rma


def compute_rsi(close: pd.Series, period: int) -> pd.Series:
    """Pine-compatible RSI using Wilder/RMA smoothing.

    Returns values in [0, 100]; NaN for the first `period` bars.
    """
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = (-delta.clip(upper=0.0))
    avg_gain = ind_rma(gain, period)
    avg_loss = ind_rma(loss, period)
    rs = avg_gain / avg_loss.replace(0.0, float("nan"))
    return (100.0 - (100.0 / (1.0 + rs))).rename("rsi")


def compute_rsi_filter(
    close: pd.Series,
    use_rsi_filter: bool,
    rsi_period: int,
    rsi_overbought: float,
) -> dict[str, pd.Series]:
    """RSI trend-extension filter for the pullback strategy.

    Prevents entering a pullback when price is already in an extended
    overbought/oversold zone — a common cause of failed pullback setups.

    Logic (both derived from one threshold):
        rsi_long_filter:  RSI < rsi_overbought  (don't buy into overbought)
        rsi_short_filter: RSI > (100 - rsi_overbought)  (don't sell into oversold)

    When use_rsi_filter=False returns all-True filters so no trades are blocked.

    Args:
        close:          Close price series.
        use_rsi_filter: Master on/off switch; wired into the robustness grid.
        rsi_period:     Lookback period for RSI (default 14).
        rsi_overbought: Upper RSI threshold for longs, e.g. 70.
                        Short threshold = 100 - rsi_overbought.
    """
    true_s = pd.Series(True, index=close.index, dtype=bool)

    if not use_rsi_filter:
        return {
            "rsi_value": pd.Series(50.0, index=close.index, dtype=float),
            "rsi_long_filter": true_s.copy(),
            "rsi_short_filter": true_s.copy(),
        }

    rsi = compute_rsi(close, rsi_period)
    rsi_oversold = 100.0 - rsi_overbought

    return {
        "rsi_value": rsi,
        "rsi_long_filter": (rsi < rsi_overbought).fillna(True),
        "rsi_short_filter": (rsi > rsi_oversold).fillna(True),
    }
