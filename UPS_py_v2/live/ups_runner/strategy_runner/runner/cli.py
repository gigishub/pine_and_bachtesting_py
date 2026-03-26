from __future__ import annotations

import argparse

from ....analysis.paths import ensure_analysis_dirs
from .live_runner import LiveRunner
from ...config import build_config_from_env


def main() -> None:
    parser = argparse.ArgumentParser(description="Run UPS strategy live on Bybit V5")
    parser.add_argument("--dry-run", action="store_true", help="Compute signals but do not place orders")
    args = parser.parse_args()

    cfg = build_config_from_env()
    if args.dry_run:
        cfg.dry_run = True

    ensure_analysis_dirs(cfg)

    LiveRunner(cfg).run_forever()
