"""Regime entry gate.

A simple predicate that returns True when the regime is confirmed.
The caller decides which regime signal(s) to pass in.
"""

from __future__ import annotations


def regime_confirmed(ema_ok: bool, vats_ok: bool, use_ema: bool, use_vats: bool) -> bool:
    """Return True when all enabled regime filters agree.

    Args:
        ema_ok:   True when price is below EMA 200 (daily).
        vats_ok:  True when VATS < threshold (daily).
        use_ema:  Whether the EMA filter is active.
        use_vats: Whether the VATS filter is active.

    Returns:
        True only if every enabled filter is confirmed.  If no filter is
        enabled the function returns False to prevent unconstrained entries.
    """
    if not use_ema and not use_vats:
        return False

    result = True
    if use_ema:
        result = result and ema_ok
    if use_vats:
        result = result and vats_ok
    return result
