"""Shared utility: capture printed analysis output and save it as a markdown file.

Usage in each run.py::

    from bear_strategy.hypothesis_tests.report_writer import (
        capture_prints, save_report, run_stem,
    )

    stem = run_stem(config.entry_tf, config.stop_atr_mult, config.target_atr_mult, config.atr_period)
    params = {"entry_tf": config.entry_tf, "stop_atr_mult": config.stop_atr_mult, ...}

    with capture_prints() as cap:
        _print_summary(results, config)
        _save_results(results, config)
        _print_verdict(results, config)

    save_report(cap.text, config.results_dir / f"analysis_{stem}.md", "Title", config_params=params)

The context manager tees stdout so everything still appears on the terminal;
the captured text is also written to the markdown file.
"""

from __future__ import annotations

import io
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Generator


def _fmt_param(v: float) -> str:
    """Format a float, stripping trailing zeros (e.g. 2.0→"2", 1.5→"1.5")."""
    return f"{v:g}"


def _next_version_path(path: Path) -> Path:
    """Return *path* if it doesn't exist; otherwise find the first free _2, _3, … variant."""
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    n = 2
    while True:
        candidate = parent / f"{stem}_{n}{suffix}"
        if not candidate.exists():
            return candidate
        n += 1


class _TeeIO:
    """Writes to both the original stdout and an internal buffer."""

    def __init__(self, original: object) -> None:
        self._original = original
        self._buf = io.StringIO()

    def write(self, s: str) -> int:
        self._original.write(s)  # type: ignore[union-attr]
        self._buf.write(s)
        return len(s)

    def flush(self) -> None:
        self._original.flush()  # type: ignore[union-attr]
        self._buf.flush()

    # Delegate every other attribute to the real stdout so that any code
    # that probes encoding, fileno, isatty, etc. still works correctly.
    def __getattr__(self, name: str) -> object:
        return getattr(self._original, name)

    @property
    def text(self) -> str:
        return self._buf.getvalue()


@contextmanager
def capture_prints() -> Generator[_TeeIO, None, None]:
    """Context manager that tees sys.stdout to a buffer while printing normally."""
    tee = _TeeIO(sys.stdout)
    old_stdout = sys.stdout
    sys.stdout = tee  # type: ignore[assignment]
    try:
        yield tee
    finally:
        sys.stdout = old_stdout


def run_stem(
    entry_tf: str,
    stop_atr_mult: float,
    target_atr_mult: float,
    atr_period: int,
    *,
    context_tf: str | None = None,
    extra: str = "",
) -> str:
    """Build a deterministic filename stem that encodes all exit parameters.

    Args:
        entry_tf:        Candle resolution used for entries.
        stop_atr_mult:   ATR multiplier for the stop.
        target_atr_mult: ATR multiplier for the target.
        atr_period:      ATR lookback period.
        context_tf:      Optional higher-TF (multi-TF tests only).
        extra:           Optional test-specific tag already part of the stem
                         (e.g. ``"N10"`` or ``"bars5"``).

    Returns:
        Stem such as ``"entry1h_sl2.0_tp3.0_atr7"`` or
        ``"entry1h_ctx4h_N10_sl2.0_tp3.0_atr7"``.
    """
    parts = [f"entry{entry_tf}"]
    if context_tf:
        parts.append(f"ctx{context_tf}")
    if extra:
        parts.append(extra)
    parts.append(f"sl{stop_atr_mult:.1f}_tp{target_atr_mult:.1f}_atr{atr_period}")
    return "_".join(parts)


def save_report(
    text: str,
    path: Path,
    title: str,
    config_params: dict[str, object] | None = None,
) -> Path:
    """Write captured analysis text as a Markdown file.

    The output is placed in a fenced ``text`` code block so that all
    alignment, unicode symbols (✅ ❌), and box-drawing characters render
    verbatim in any Markdown viewer.

    If *path* already exists, a versioned suffix (_2, _3, …) is appended so
    prior results are never overwritten.

    Args:
        text:          Raw captured stdout text (from ``_TeeIO.text``).
        path:          Desired destination ``.md`` file path.
        title:         Heading shown at the top of the document.
        config_params: Optional mapping of parameter names to values,
                       rendered as a Markdown table before the result block
                       so the exact settings used are always visible in the file.

    Returns:
        The actual ``Path`` the file was written to (may differ from *path*
        when versioning kicks in).
    """
    path = _next_version_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    params_section = ""
    if config_params:
        rows = "\n".join(f"| `{k}` | `{v}` |" for k, v in config_params.items())
        params_section = (
            "\n\n## Test Parameters\n\n"
            "| Parameter | Value |\n"
            "|-----------|-------|\n"
            f"{rows}"
        )
    content = f"# {title}{params_section}\n\n```text\n{text.rstrip()}\n```\n"
    path.write_text(content, encoding="utf-8")
    return path
