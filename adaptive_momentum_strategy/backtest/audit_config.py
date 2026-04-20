"""CLI tool: inspect the effective parameter configuration of any config file.

Usage
-----
    python -m adaptive_momentum_strategy.backtest.audit_config <config_name>
    python -m adaptive_momentum_strategy.backtest.audit_config phase2_free_sweep
    python -m adaptive_momentum_strategy.backtest.audit_config phase2_free_sweep --save

<config_name> must match a module in adaptive_momentum_strategy/backtest/configs/
that exports a build_config() function.

--save  Writes run_manifest.txt to config.output_dir (directory is created if needed).
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

from .config import MomentumGridConfig, AuditEntry


_STATUS_LABEL: dict[str, str] = {
    "swept":      "swept       ",
    "pinned_on":  "pinned ON   ",
    "pinned_off": "pinned OFF  ",
    "pinned":     "pinned      ",
    "implicit":   "⚠ IMPLICIT  ",
}


def _format_values(entry: AuditEntry) -> str:
    if entry.status == "swept":
        return " / ".join(str(v) for v in entry.values)
    return str(entry.values[0])


def build_manifest(config: MomentumGridConfig, config_name: str) -> str:
    """Return the full audit manifest as a formatted string."""
    lines: list[str] = []

    lines.append(f"Config:      {config_name}")
    lines.append(f"Symbols:     {', '.join(config.symbols)}")
    lines.append(f"Timeframes:  {', '.join(config.timeframes)}")
    lines.append(f"Period:      {config.start_time}  →  {config.end_time or 'latest'}")
    lines.append(f"Direction:   long={'ON' if config.enable_long else 'OFF'}  short={'ON' if config.enable_short else 'OFF'}")
    exclusive = [
        layer
        for layer, attr in [
            ("regime", "regime_exclusive"), ("setup", "setup_exclusive"),
            ("trigger", "trigger_exclusive"), ("exit", "exit_exclusive"),
        ]
        if getattr(config, attr, False)
    ]
    lines.append(f"Exclusive:   {', '.join(exclusive) if exclusive else 'none (combination mode)'}")
    lines.append("")

    entries = config.param_audit()
    bool_entries = [e for e in entries if e.status not in ("swept", "pinned") or "/" not in _format_values(e) or e.name.startswith("use_")]
    bool_entries = [e for e in entries if not any(e.name == n for n in ("adx_threshold", "chandelier_atr_mult", "cmf_threshold", "trail_atr_mult"))]
    num_entries  = [e for e in entries if e.name in ("adx_threshold", "chandelier_atr_mult", "cmf_threshold", "trail_atr_mult")]

    lines.append("Boolean Flags")
    lines.append("-" * 58)
    lines.append(f"  {'FLAG':<28} {'STATUS':<14} {'VALUE(S)'}")
    lines.append(f"  {'-'*27} {'-'*13} {'-'*12}")
    implicit_found = False
    for e in bool_entries:
        label = _STATUS_LABEL.get(e.status, e.status)
        val   = _format_values(e)
        lines.append(f"  {e.name:<28} {label} {val}")
        if e.status == "implicit":
            implicit_found = True

    if implicit_found:
        lines.append("")
        lines.append("  ⚠  Implicit flags inherit Parameters() defaults without being explicitly declared.")
        lines.append("     Add them to boolean_filter_ranges to silence this warning.")

    lines.append("")
    lines.append("Numeric Sweeps")
    lines.append("-" * 58)
    for e in num_entries:
        label = _STATUS_LABEL.get(e.status, e.status)
        val   = _format_values(e)
        lines.append(f"  {e.name:<28} {label} {val}")

    # Grid size hint
    swept_bool  = sum(1 for e in bool_entries if e.status == "swept")
    swept_num   = sum(len(e.values) for e in num_entries if e.status == "swept")
    n_combos    = 2 ** swept_bool * (swept_num if swept_num else 1)
    lines.append("")
    lines.append(f"Grid size (upper bound, before validity filtering):  {n_combos:,} combos")
    lines.append(f"Conditions: {len(config.symbols)} symbols × {len(config.timeframes)} TF = {len(config.symbols)*len(config.timeframes)}")

    return "\n".join(lines)


def print_audit(config: MomentumGridConfig, config_name: str) -> None:
    print()
    print("=" * 60)
    print(" Parameter Audit")
    print("=" * 60)
    print(build_manifest(config, config_name))
    print("=" * 60)
    print()


def _load_config(name: str) -> MomentumGridConfig:
    module_path = f"adaptive_momentum_strategy.backtest.configs.{name}"
    try:
        mod = importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        print(f"Error: cannot find config module '{module_path}'", file=sys.stderr)
        print(f"  {exc}", file=sys.stderr)
        sys.exit(1)
    if not hasattr(mod, "build_config"):
        print(f"Error: module '{module_path}' has no build_config() function.", file=sys.stderr)
        sys.exit(1)
    return mod.build_config()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Inspect the effective parameter configuration before a run.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("config", help="Config module name (e.g. phase2_free_sweep)")
    parser.add_argument(
        "--save", action="store_true",
        help="Write run_manifest.txt to config.output_dir",
    )
    args = parser.parse_args(argv)

    config = _load_config(args.config)

    # Validate — prints a useful error if incomplete
    try:
        config.validate_coverage()
    except ValueError as exc:
        print(f"\n⚠  Coverage error: {exc}\n", file=sys.stderr)
        # Still print what we have so the user can see what's missing
    print_audit(config, args.config)

    if args.save:
        out = Path(config.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        manifest_path = out / "run_manifest.txt"
        manifest_path.write_text(build_manifest(config, args.config), encoding="utf-8")
        print(f"Manifest saved → {manifest_path}")


if __name__ == "__main__":
    main()
