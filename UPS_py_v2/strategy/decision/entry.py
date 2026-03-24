"""Long/short entry gates for the UPS strategy.

Pure functions: receive precomputed bar-snapshot booleans, return bool.
No side effects, no order placement.
"""

from __future__ import annotations


def should_open_long(
    position_size: float,
    is_flat: bool,
    price_above_ma: bool,
    long_conditions_met: bool,
    bearish_pb: bool,
    long_entry_pattern: bool,
) -> bool:
    """Return True when all long entry conditions are satisfied.

    Mirrors Pine:
        validLongEntry = zen.isFlat() and priceAboveMA
                         and longConditionsMet and bearishPB
                         and longEntryPattern
    """
    if position_size != 0 or not is_flat:
        return False
    return bool(price_above_ma and long_conditions_met and bearish_pb and long_entry_pattern)


def should_open_short(
    position_size: float,
    is_flat: bool,
    price_above_ma: bool,
    short_conditions_met: bool,
    bullish_pb: bool,
    short_entry_pattern: bool,
) -> bool:
    """Return True when all short entry conditions are satisfied.

    Mirrors Pine:
        validShortEntry = zen.isFlat() and not priceAboveMA
                          and shortConditionsMet and bullishPB
                          and shortEntryPattern
    """
    if position_size != 0 or not is_flat:
        return False
    return bool((not price_above_ma) and short_conditions_met and bullish_pb and short_entry_pattern)
