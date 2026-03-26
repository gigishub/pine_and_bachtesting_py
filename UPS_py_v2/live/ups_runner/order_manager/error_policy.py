from __future__ import annotations


def bybit_ret_code(exc: RuntimeError) -> str | None:
    """Extract Bybit retCode from a RuntimeError message."""
    text = str(exc)
    marker = "Bybit error "
    idx = text.find(marker)
    if idx < 0:
        return None
    code_part = text[idx + len(marker):].split(":", 1)[0].strip()
    return code_part or None


def is_unchanged_stop_error(exc: RuntimeError) -> bool:
    """True when Bybit reports the requested TP/SL state is unchanged."""
    return bybit_ret_code(exc) == "34040"


def is_non_fatal_entry_error(exc: RuntimeError) -> bool:
    """Entry errors that should skip the bar instead of stopping the runner."""
    code = bybit_ret_code(exc)
    if code in {"110004", "110006", "110007", "110012"}:
        return True
    msg = str(exc).lower()
    return "not enough" in msg or "insufficient" in msg


def is_non_fatal_cancel_error(exc: RuntimeError) -> bool:
    """Cancel errors that indicate order is already gone or no longer open."""
    code = bybit_ret_code(exc)
    if code in {"110001"}:
        return True
    msg = str(exc).lower()
    return "not exists" in msg or "already" in msg


def is_non_fatal_stop_error(exc: RuntimeError) -> bool:
    """Stop update errors that should not crash the live loop."""
    code = bybit_ret_code(exc)
    return code in {"10001", "110007"}
