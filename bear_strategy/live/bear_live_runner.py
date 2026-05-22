"""Bear Strategy — Live Runner Entrypoint.

Usage:
    python -m bear_strategy.live.bear_live_runner

Configuration is loaded from BEAR_* environment variables (or a .env file at
the project root).  Secrets are read from BYBIT_API_KEY and BYBIT_API_SECRET.

See bear_strategy/live/control/profiles/ for per-symbol profile .env files and
bear_strategy/live/control/runctl.sh for process management.
"""

from __future__ import annotations

import logging
import sys

from bear_strategy.live.bear_runner.config import build_config_from_env
from bear_strategy.live.bear_runner.live_runner import BearLiveRunner

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)


def main() -> None:
    cfg = build_config_from_env()
    runner = BearLiveRunner(cfg)
    runner.run_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Interrupted by user.")
        sys.exit(0)
