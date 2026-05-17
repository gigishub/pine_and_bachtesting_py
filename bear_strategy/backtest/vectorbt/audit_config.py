"""Bear Strategy — parameter configuration auditor.

Provides build_manifest() and print_audit() for BearGridConfig.
Mirrors adaptive_momentum_strategy/backtest/audit_config.py adapted for the
bear strategy's trigger + exit flag structure (regime is always active).
"""

from __future__ import annotations

from .bear_grid_config import BearGridConfig, AuditEntry


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


def build_manifest(config: BearGridConfig, config_name: str) -> str:
    """Return the full audit manifest as a formatted string."""
    lines: list[str] = []

    lines.append(f"Config:      {config_name}")
    lines.append(f"Symbols:     {', '.join(config.symbols)}")
    lines.append(f"Period:      {config.start_date}  →  {config.end_date}")
    lines.append(f"Fees:        {config.fees * 100:.3f}%   Init cash: ${config.initial_cash:,.0f}")

    exclusive_parts: list[str] = []
    if config.trigger_exclusive:
        exclusive_parts.append("trigger")
    if config.exit_exclusive:
        exclusive_parts.append("exit")
    lines.append(f"Exclusive:   {', '.join(exclusive_parts) if exclusive_parts else 'none (combination mode)'}")
    lines.append("")

    entries     = config.param_audit()
    bool_names  = {
        "use_vp_trigger",
        "use_fixed_tp", "use_rsi_exit", "use_macd_exit",
        "use_rsi_oversold_exit", "use_ema_reclaim_exit", "use_funding_exit",
    }
    bool_entries = [e for e in entries if e.name in bool_names]
    num_entries  = [e for e in entries if e.name not in bool_names]

    # ── Regime section (always active — informational only) ───────────────────
    lines.append("Regime (always active)")
    lines.append("-" * 58)
    lines.append("  RSI bear zone (1d) + Funding bull guard (1h) are always ON.")
    lines.append("  Numeric regime params appear in the Numeric Sweeps section.")
    lines.append("")

    # ── Trigger flags ─────────────────────────────────────────────────────────
    lines.append("Trigger Flags")
    lines.append("-" * 58)
    lines.append(f"  {'FLAG':<30} {'STATUS':<14} {'VALUE(S)'}")
    lines.append(f"  {'-'*29} {'-'*13} {'-'*12}")
    trigger_entries = [e for e in bool_entries if e.name.startswith("use_vp")]
    for e in trigger_entries:
        label = _STATUS_LABEL.get(e.status, e.status)
        val   = _format_values(e)
        lines.append(f"  {e.name:<30} {label} {val}")
    lines.append("")

    # ── Exit flags ────────────────────────────────────────────────────────────
    lines.append("Exit Flags")
    lines.append("-" * 58)
    lines.append(f"  {'FLAG':<30} {'STATUS':<14} {'VALUE(S)'}")
    lines.append(f"  {'-'*29} {'-'*13} {'-'*12}")
    exit_entries  = [e for e in bool_entries if e not in trigger_entries]
    implicit_found = False
    for e in exit_entries:
        label = _STATUS_LABEL.get(e.status, e.status)
        val   = _format_values(e)
        lines.append(f"  {e.name:<30} {label} {val}")
        if e.status == "implicit":
            implicit_found = True

    if implicit_found:
        lines.append("")
        lines.append("  ⚠  Implicit flags inherit Parameters() defaults without being explicitly declared.")
        lines.append("     Add them to boolean_filter_ranges to silence this warning.")
    lines.append("")

    # ── Numeric sweeps ────────────────────────────────────────────────────────
    lines.append("Numeric Sweeps")
    lines.append("-" * 58)
    lines.append(f"  {'PARAM':<30} {'STATUS':<14} {'VALUE(S)'}")
    lines.append(f"  {'-'*29} {'-'*13} {'-'*12}")
    for e in num_entries:
        label = _STATUS_LABEL.get(e.status, e.status)
        val   = _format_values(e)
        lines.append(f"  {e.name:<30} {label} {val}")

    # ── Grid size estimate ────────────────────────────────────────────────────
    swept_bool_count = sum(1 for e in bool_entries if e.status == "swept")
    swept_num_combos = 1
    for e in num_entries:
        if e.status == "swept":
            swept_num_combos *= len(e.values)

    n_combos = (2 ** swept_bool_count) * swept_num_combos
    lines.append("")
    lines.append(f"Grid size (upper bound, before validity filtering):  {n_combos:,} combos")
    lines.append(f"Conditions: {len(config.symbols)} symbol(s)")

    return "\n".join(lines)


def print_audit(config: BearGridConfig, config_name: str) -> None:
    print()
    print("=" * 60)
    print(" Bear Strategy — Parameter Audit")
    print("=" * 60)
    print(build_manifest(config, config_name))
    print("=" * 60)
    print()
