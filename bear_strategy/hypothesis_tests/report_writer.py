"""Shared utility: capture printed analysis output and save it as a markdown file.

Usage in each run.py::

    from bear_strategy.hypothesis_tests.report_writer import capture_prints, save_report

    with capture_prints() as cap:
        _print_summary(results, config)
        _save_results(results, config)
        _print_verdict(results, config)

    save_report(cap.text, config.results_dir / "analysis.md", "Step X Analysis Title")

The context manager tees stdout so everything still appears on the terminal;
the captured text is also written to the markdown file.
"""

from __future__ import annotations

import io
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Generator


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


def save_report(text: str, path: Path, title: str) -> None:
    """Write captured analysis text as a Markdown file.

    The output is placed in a fenced ``text`` code block so that all
    alignment, unicode symbols (✅ ❌), and box-drawing characters render
    verbatim in any Markdown viewer.

    Args:
        text:  Raw captured stdout text (from ``_TeeIO.text``).
        path:  Destination ``.md`` file path.
        title: Heading shown at the top of the document.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"# {title}\n\n```text\n{text.rstrip()}\n```\n"
    path.write_text(content, encoding="utf-8")
