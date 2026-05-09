"""Entry point for downloading Bybit funding rate history.

Automatically detects which symbols already have OHLCV data and downloads
the corresponding funding rates for those same pairs.

Run from the project root with the virtual environment active:

    cd /Users/andre/Documents/Python_local/pine_script
    source .venv/bin/activate && python -m crypto_data.funding_main

Files are saved to:
    crypto_data/data/<SYMBOL>/<SYMBOL>_funding_start_<date>_end_<date>.parquet
"""
from __future__ import annotations

import logging
from pathlib import Path

from crypto_data.config import OUTPUT_DIR
from crypto_data.funding_downloader import download_funding_rates

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


def _detect_symbols(data_dir: Path) -> list[str]:
    """Return all symbols that have an existing OHLCV data subdirectory."""
    return sorted(
        d.name
        for d in data_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


# ── Configuration ─────────────────────────────────────────────────────────────

# None → auto-detect from existing OHLCV data directories
SYMBOLS: list[str] | None = None

START_TIME = "2019-01-01 00:00:00"
END_TIME = "2026-04-22 00:00:00"  # None → downloads up to now

CATEGORY = "linear"  # 'linear' for USDT perpetuals; 'inverse' for coin-margined

# Set to False to re-download files that already exist on disk
SKIP_EXISTING = True

# Override output directory if needed; defaults to crypto_data/data/
OUTPUT_DIR_OVERRIDE: Path | None = None

# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    output_dir = OUTPUT_DIR_OVERRIDE or OUTPUT_DIR

    symbols = SYMBOLS or _detect_symbols(output_dir)
    logger.info("Symbols to fetch funding rates for: %s", symbols)

    download_funding_rates(
        symbols=symbols,
        start_time=START_TIME,
        end_time=END_TIME,
        category=CATEGORY,
        output_dir=output_dir,
        skip_existing=SKIP_EXISTING,
    )
