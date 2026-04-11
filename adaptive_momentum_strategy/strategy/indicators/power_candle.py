"""Power Candle execution trigger (Trigger Option C).

A high-volume candle that closes at or above the Donchian upper band
indicates strong buyer conviction and a low probability of a 'bull trap'.
Requiring the close to reclaim a structural high on elevated volume ensures
the breakout is backed by actual capital commitment rather than thin liquidity.

Mathematical condition:
    Close > High(lookback)  AND  Volume > vol_multiplier × SMA(Volume, vol_period)

Reference: Bulkowski, T. N. (2005). Encyclopedia of Chart Patterns.
"""

from __future__ import annotations

import pandas as pd


def compute_volume_sma(volume: pd.Series, period: int = 20) -> pd.Series:
    """Simple moving average of volume."""
    return volume.rolling(period).mean().astype(float)


def trigger_is_power_candle(
    close: pd.Series,
    high: pd.Series,
    volume: pd.Series,
    lookback: int = 15,
    vol_period: int = 20,
    vol_multiplier: float = 1.5,
) -> pd.Series:
    """True when close breaks the N-bar high on above-average volume.

    Args:
        close:          Bar close prices.
        high:           Bar high prices (used for the rolling maximum).
        volume:         Bar volume.
        lookback:       Bars for the rolling maximum (analogous to Donchian lookback).
        vol_period:     Bars for the volume SMA baseline.
        vol_multiplier: Volume must exceed this multiple of its SMA.
    """
    rolling_high = high.rolling(lookback).max()
    vol_sma = compute_volume_sma(volume, vol_period)

    breakout = close >= rolling_high
    high_volume = volume > (vol_sma * vol_multiplier)

    return (breakout & high_volume).fillna(False)


def trigger_is_bearish_power_candle(
    close: pd.Series,
    low: pd.Series,
    volume: pd.Series,
    lookback: int = 15,
    vol_period: int = 20,
    vol_multiplier: float = 1.5,
) -> pd.Series:
    """True when close breaks the N-bar low on above-average volume.

    Short-side mirror of trigger_is_power_candle().  A close at or below the
    N-bar low on elevated volume confirms aggressive selling and low probability
    of an immediate reversal.

    Args:
        close:          Bar close prices.
        low:            Bar low prices (used for the rolling minimum).
        volume:         Bar volume.
        lookback:       Bars for the rolling minimum.
        vol_period:     Bars for the volume SMA baseline.
        vol_multiplier: Volume must exceed this multiple of its SMA.
    """
    rolling_low = low.rolling(lookback).min()
    vol_sma = compute_volume_sma(volume, vol_period)

    breakdown = close <= rolling_low
    high_volume = volume > (vol_sma * vol_multiplier)

    return (breakdown & high_volume).fillna(False)
