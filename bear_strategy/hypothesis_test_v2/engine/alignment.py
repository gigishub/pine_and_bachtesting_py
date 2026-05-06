"""
HTF → LTF signal alignment with strict anti-lookahead guarantees.

Rules enforced:
  1. Higher-timeframe (HTF) signals are shifted by 1 bar on the HTF index before
     alignment so the currently-forming HTF bar is never seen at entry time.
  2. merge_asof(direction="backward") ensures each LTF bar only sees HTF signals
     from already-closed bars.
  3. validate_no_lookahead() verifies the contract after alignment.

Usage
-----
    htf_signal = compute_something_on_htf(htf_df)          # raw HTF Series
    aligned    = align_htf_to_ltf(htf_df, htf_signal, ltf_df)
    validate_no_lookahead(ltf_df, aligned, htf_df)
"""

from __future__ import annotations

import logging

import pandas as pd

log = logging.getLogger(__name__)


class LookaheadError(Exception):
    """Raised when the anti-lookahead validation fails."""


def align_htf_to_ltf(
    htf_df: pd.DataFrame,
    htf_signal: pd.Series,
    ltf_df: pd.DataFrame,
    shift: bool = True,
) -> pd.Series:
    """
    Align a HTF boolean signal to the LTF index without lookahead.

    Parameters
    ----------
    htf_df:     DataFrame whose index defines the HTF bar timestamps.
    htf_signal: Boolean Series on the HTF index.
    ltf_df:     DataFrame whose index is the LTF bar timestamps.
    shift:      If True (default), shift the HTF signal forward by 1 bar so the
                current partially-formed HTF bar is excluded.

    Returns
    -------
    Boolean Series on the LTF index.  True = HTF condition active.
    """
    sig = htf_signal.copy()
    if shift:
        sig = sig.shift(1)

    left = pd.DataFrame({"_ltf_ts": ltf_df.index}, index=ltf_df.index)
    right = pd.DataFrame({"_htf_sig": sig}, index=htf_df.index)

    merged = pd.merge_asof(
        left.reset_index(),
        right.reset_index(),
        left_on="_ltf_ts",
        right_on=htf_df.index.name or "index",
        direction="backward",
    ).set_index("timestamp" if "timestamp" in left.reset_index().columns else left.reset_index().columns[0])

    result = merged["_htf_sig"].fillna(False).astype(bool)
    result.index = ltf_df.index
    return result


def align_htf_series(
    htf_index: pd.DatetimeIndex,
    htf_signal: pd.Series,
    ltf_index: pd.DatetimeIndex,
    shift: bool = True,
) -> pd.Series:
    """
    Low-level alignment using raw index objects.

    Parameters
    ----------
    htf_index:  DatetimeIndex of the higher-timeframe data.
    htf_signal: Boolean Series (same length as htf_index).
    ltf_index:  DatetimeIndex of the lower-timeframe data we want to map onto.
    shift:      Shift by 1 HTF bar before alignment (default True).

    Returns
    -------
    Boolean Series indexed to ltf_index.
    """
    sig = htf_signal.copy()
    sig.index = htf_index
    if shift:
        sig = sig.shift(1)

    left  = pd.DataFrame({"ltf_ts": ltf_index}, index=ltf_index)
    right = sig.rename("htf_val").to_frame()
    right.index.name = "htf_ts"

    merged = pd.merge_asof(
        left.reset_index(drop=True),
        right.reset_index(),
        left_on="ltf_ts",
        right_on="htf_ts",
        direction="backward",
    )
    htf_val = merged["htf_val"]
    result = htf_val.where(htf_val.notna(), other=False).astype(bool)
    result.index = ltf_index
    return result


def validate_no_lookahead(
    ltf_df: pd.DataFrame,
    aligned_signal: pd.Series,
    htf_df: pd.DataFrame,
) -> None:
    """
    Assert that the first True value in *aligned_signal* appears at least one
    full HTF bar after the beginning of the data.

    Raises LookaheadError if the very first LTF bar already has the HTF signal
    set, which would indicate that the shift / backward-alignment is broken.

    Parameters
    ----------
    ltf_df:         Entry-timeframe DataFrame (used for date context in error).
    aligned_signal: Boolean Series on the LTF index.
    htf_df:         HTF DataFrame (used to determine one HTF bar's length).
    """
    if aligned_signal.empty or not aligned_signal.any():
        return  # no signal at all — nothing to validate

    first_true_ts = aligned_signal.index[aligned_signal][0]

    if len(htf_df) < 2:
        return  # not enough HTF bars to determine the bar length

    htf_bar_length = htf_df.index[1] - htf_df.index[0]
    data_start     = ltf_df.index[0]
    min_allowed_ts = data_start + htf_bar_length

    if first_true_ts < min_allowed_ts:
        raise LookaheadError(
            f"Lookahead detected: aligned signal is True at {first_true_ts} "
            f"but the earliest safe timestamp is {min_allowed_ts} "
            f"(data start {data_start} + 1 HTF bar {htf_bar_length}). "
            "Ensure shift(1) is applied on the HTF index before alignment."
        )
