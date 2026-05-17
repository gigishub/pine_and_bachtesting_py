"""Bear Strategy — grid-search CLI entry point.

Usage
-----
    python -m bear_strategy.backtest.vectorbt.run_grid --config <name> [OPTIONS]

Named configs (bear_strategy/backtest/vectorbt/configs/)
---------------------------------------------------------
  default             Single baseline run (fixed TP, all indicators off)
  exit_isolation      One exit at a time  (exit_exclusive mode)
  exit_value_sweep    All exits × numeric param sweeps
  regime_value_sweep  RSI/funding threshold sweeps
  full_combo          Full Cartesian: all exits × SL/TP/level sweeps

Options
-------
  --config  NAME          Named config to load (required)
  --symbols SYM [SYM ...] Override symbols from config
  --start   DATE          Override start date  (YYYY-MM-DD)
  --end     DATE          Override end date    (YYYY-MM-DD)
  --output  DIR           Override output directory
  --dry-run               Print audit and grid size, then exit
  --stop-after COND_KEY   Stop after this condition key (e.g. BTCUSDT_1H)
"""

from __future__ import annotations

import argparse
import dataclasses
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bear Strategy — AMS-style vectorbt grid runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--config",
        required=True,
        metavar="NAME",
        help="Named grid config (filename stem under configs/)",
    )
    parser.add_argument(
        "--symbols",
        nargs="+",
        metavar="SYM",
        help="Override symbols (e.g. --symbols BTCUSDT ETHUSDT)",
    )
    parser.add_argument("--start",   metavar="DATE", help="Override start date (YYYY-MM-DD)")
    parser.add_argument("--end",     metavar="DATE", help="Override end date   (YYYY-MM-DD)")
    parser.add_argument("--output",  metavar="DIR",  help="Override output directory")
    parser.add_argument("--stop-after", metavar="COND", help="Stop after condition key")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print audit manifest and grid size, then exit without running",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)

    # ── Load named config ─────────────────────────────────────────────────────
    from bear_strategy.backtest.vectorbt.configs import load_config
    try:
        config = load_config(args.config)
    except (ValueError, AttributeError, TypeError) as exc:
        logger.error("%s", exc)
        sys.exit(1)

    # ── Apply CLI overrides ───────────────────────────────────────────────────
    overrides: dict = {}
    if args.symbols:
        overrides["symbols"] = args.symbols
    if args.start:
        overrides["start_date"] = args.start
    if args.end:
        overrides["end_date"] = args.end
    if args.output:
        overrides["output_dir"] = Path(args.output)
    if overrides:
        config = dataclasses.replace(config, **overrides)

    # ── Validate + audit ──────────────────────────────────────────────────────
    try:
        config.validate_coverage()
    except ValueError as exc:
        logger.error("Config validation failed:\n%s", exc)
        sys.exit(1)

    from bear_strategy.backtest.vectorbt.audit_config import print_audit
    from bear_strategy.backtest.vectorbt.pipeline import build_parameter_grid
    print_audit(config, args.config)

    baseline = config.build_baseline_params()
    grid     = build_parameter_grid(baseline, config)
    total    = len(grid) * len(config.symbols)
    print(
        f"Grid: {len(grid)} unique combo(s) × {len(config.symbols)} symbol(s)"
        f" = {total} backtest run(s)\n"
    )

    if args.dry_run:
        print("Dry run — exiting without running backtests.")
        return

    # ── Run ───────────────────────────────────────────────────────────────────
    from bear_strategy.backtest.vectorbt.sequencer import run_sequential
    saved = run_sequential(
        config,
        stop_after=args.stop_after,
    )
    print(f"\n✓ Done. {len(saved)} CSV(s) written.")


if __name__ == "__main__":
    main()
