"""Derive human-readable aliases from parameter signatures.

Rule (works for any number of parameters):
  Read the use_*=0/1 values left to right.
  Assign A, B, C, … (one letter per position, up to 26).
  Include the letter only if that position is 1.
  Append the full binary string after an underscore as a unique suffix.

Examples (5 params):
  use_adx=1|use_ema_ribbon=1|use_chandelier=1|use_psar=1|use_trailing_stop=0  →  ABCD_11110
  use_adx=0|use_ema_ribbon=1|use_chandelier=1|use_psar=0|use_trailing_stop=0  →  BC_01100
  use_adx=0|...(all zeros)...                                                  →  NONE_00000

Examples (3 params):
  use_adx=1|use_ema_ribbon=0|use_chandelier=1                                  →  AC_101

Examples (10 params, all on):
  use_a=1|use_b=1|...|use_j=1                                                  →  ABCDEFGHIJ_1111111111

The alias is deterministic and requires no lookup table — it is fully recoverable
from the binary suffix alone (the letter prefix is just a convenience for reading).
"""

from __future__ import annotations

import re
import string

_LETTERS: str = string.ascii_uppercase  # A-Z, supports up to 26 parameters


def sig_to_alias(sig: str) -> str:
    """Return a short alias derived from a parameter signature string.

    Parameters
    ----------
    sig:
        Pipe-separated ``key=value`` string produced by the AMS runner.
        Values are ``0``/``1`` or ``True``/``False`` (case-insensitive).
        Backslash-escaped pipes (``\\|``) are normalised before parsing.

    Returns
    -------
    str
        ``<letters>_<binary>`` alias, e.g. ``ABCD_11110``.
        Returns the original *sig* unchanged if parsing yields no bits
        (e.g. malformed or non-boolean values), so callers always get
        a displayable string.
    """
    # Normalise escaped pipes that appear in some serialisation formats
    normalised = sig.replace("\\|", "|")
    pairs = re.split(r"\|", normalised)

    bits: list[int] = []
    for pair in pairs:
        pair = pair.strip()
        if "=" not in pair:
            continue
        _, raw_val = pair.rsplit("=", 1)
        val = raw_val.strip().lower()
        if val in ("1", "true"):
            bits.append(1)
        elif val in ("0", "false"):
            bits.append(0)
        # Non-boolean token → skip (keeps bits shorter than expected,
        # but still produces a valid alias for the tokens we could parse)

    if not bits:
        return sig  # fallback: nothing usable parsed

    letters = "".join(
        _LETTERS[i]
        for i, b in enumerate(bits)
        if b == 1 and i < len(_LETTERS)
    )
    binary = "".join(str(b) for b in bits)
    return f"{letters or 'NONE'}_{binary}"
