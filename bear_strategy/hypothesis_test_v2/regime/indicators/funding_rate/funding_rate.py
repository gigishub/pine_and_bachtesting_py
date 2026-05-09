"""
funding_rate — Regime indicator (BEAR version).

What it measures
----------------
True when the (optionally smoothed) funding rate is BELOW a threshold.

Financial interpretation
-------------------------
Perpetual funding rate < threshold means:
  - Near-zero or negative funding → the perpetual is at par or discount to spot.
  - Either bearish OI dominates (shorts pay longs, rate < 0), or funding has
    normalised after a bullish extreme — both reduce the tailwind for longs.

This is useful as a *bear regime gate*:
  - Sustained negative funding confirms the crowd is positioned short.
  - Funding below a small positive cap (e.g. 0.0001) rules out periods where
    excessive long OI creates adverse funding costs for new short positions.

Parameters
----------
threshold : float   — Maximum funding rate for signal to be True.
                      Default 0.0001 (1 basis point, the Bybit floor rate).
                      Use 0.0 to require strictly negative funding.
ma_period : int     — Number of funding observations for EMA smoothing.
                      1 = raw rate (no smoothing).  Default 1.
direction : str    — "bear" or "bull". Default "bear".
                      "bear" returns True when funding is below threshold.
                      "bull" returns True when funding is above threshold.

Lookahead note
--------------
Funding rate at timestamp T was *settled* at T — it is already known at T.
The series is shift(1)'d inside signal() so entries only see the previously
*completed* funding observation, never the one still accruing.

Signal contract
---------------
Returns a boolean Series on the same index as df.
True  = smoothed funding rate < threshold (bearish funding regime).
False = funding at or above threshold, or warm-up / missing data bars.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.engine.data_loader import load_funding


def _align_funding(funding_df: pd.DataFrame, target_index: pd.DatetimeIndex) -> pd.Series:
    """Forward-fill the 8-hour funding series onto *target_index*.

    Both indexes are normalised to tz-aware UTC before the union so that
    pandas produces a proper DatetimeIndex (not object dtype) and ffill
    propagates chronologically rather than by insertion order.
    """
    rate = funding_df["fundingrate"].copy()
    # Normalise funding index to tz-aware UTC.
    fund_idx = pd.to_datetime(rate.index)
    if fund_idx.tz is None:
        fund_idx = fund_idx.tz_localize("UTC")
    else:
        fund_idx = fund_idx.tz_convert("UTC")
    rate.index = fund_idx

    # Normalise target index to tz-aware UTC.
    if target_index.tz is None:
        tgt_utc = target_index.tz_localize("UTC")
    else:
        tgt_utc = target_index.tz_convert("UTC")

    combined = rate.reindex(rate.index.union(tgt_utc)).ffill()
    result = combined.reindex(tgt_utc)
    result.index = target_index  # restore caller's original index form
    return result


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    True when smoothed funding rate < threshold (bearish funding regime).

    Parameters
    ----------
    df:     OHLCV DataFrame — provides the timestamp index to align funding data.
    params: {
        "threshold": float  — default 0.0001
        "ma_period": int    — default 1 (raw)
        "_symbol":   str    — injected by batch_runner
        "_data_dir": str    — injected by batch_runner
        "_funding_df": pd.DataFrame — optional; injected by tests to skip disk I/O
    }
    """
    threshold: float = float(params.get("threshold", 0.0001))
    ma_period:  int  = int(params.get("ma_period", 1))

    # Allow tests to inject pre-built funding data to avoid disk I/O.
    funding_df: pd.DataFrame | None = params.get("_funding_df")
    if funding_df is None:
        symbol   = params["_symbol"]
        data_dir = params.get("_data_dir", "crypto_data/data")
        # Load full range and let alignment trim to df.index.
        funding_df = load_funding(symbol, str(df.index[0].date()), str(df.index[-1].date()), data_dir)

    rate = _align_funding(funding_df, df.index)

    if ma_period > 1:
        rate = rate.ewm(span=ma_period, adjust=False).mean()

    direction: str = str(params.get("direction", "bear")).lower()
    settled_rate = rate.shift(1)

    # shift(1): use the previously *settled* funding rate — no lookahead.
    if direction == "bull":
        return (settled_rate > threshold).fillna(False)

    return (settled_rate < threshold).fillna(False)
