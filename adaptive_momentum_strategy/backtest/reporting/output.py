"""Run directory management for backtest output.

Handles timestamped output directories and checkpoint-resume support.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


_HERE = Path(__file__).parent
_RESULTS_ROOT = _HERE.parent / "results"


def build_output_dir(label: str = "AMS", suffix: str = "") -> Path:
    """Create (or resume) a timestamped run directory.

    Format: YYYY-MM-DD_HHMM_LABEL[_SUFFIX]
    Example: 2026-04-06_1210_AMS  or  2026-04-06_1530_AMS_adx_sweep

    On first run: creates the folder and writes a .current_run marker so
    checkpoint-resume works across restarts.
    On restart:   reads the marker and resumes the same folder — the
    CSV-exists check in the sequencer skips already-finished conditions.

    To force a brand-new run, delete the .current_run marker file or change
    the label / suffix argument.
    """
    engine_dir = _RESULTS_ROOT / "results_vbt"
    engine_dir.mkdir(parents=True, exist_ok=True)

    marker = engine_dir / ".current_run"
    if marker.exists():
        existing = marker.read_text().strip()
        candidate = engine_dir / existing
        if candidate.exists():
            return candidate
        # Marker points to a deleted folder — start fresh.

    now = datetime.now()
    folder_name = now.strftime("%Y-%m-%d_%H%M") + f"_{label}"
    if suffix:
        folder_name += f"_{suffix}"
    output_dir = engine_dir / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    marker.write_text(folder_name)
    return output_dir
