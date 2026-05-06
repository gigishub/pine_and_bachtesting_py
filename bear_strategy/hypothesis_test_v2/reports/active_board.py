"""
Active-board Markdown writer.

Produces one Markdown file per entry_tf, matching the methodology format:

    phase_{phase}_entry{tf}_active.md

Format per file:
    ## Phase: REGIME  |  Entry TF: 15m

    ### Batch Summary
    | idea | avg PF | avg PF lift | pairs OK | decision |
    ...

    ### Per-Idea Detail
    **close_below_ema_50**  avg PF 1.064  avg lift +0.071  3/3 pairs
      BTCUSDT  WR 40.4%  PF 1.018  lift +0.053 / req 0.05  n=75,063  cov 48.2%  [OK]
      ...

    ### Population Comparison
    #### BTCUSDT - Population Comparison
    | population          | wr_%  | pf    | dur   | n_trades |
    ...

Guard rails:
    [OK]  = pf_lift >= MIN_LIFT_THRESHOLD AND coverage >= MIN_COVERAGE_THRESHOLD
    [--]  = fails either guard
    cov X%!  = coverage below MIN_COVERAGE_THRESHOLD (inline warning)
"""

from __future__ import annotations

from pathlib import Path
from datetime import date

import pandas as pd

# Guardrail thresholds — adjust if needed.
MIN_LIFT_THRESHOLD     = 0.05   # minimum PF lift to pass
MIN_COVERAGE_THRESHOLD = 0.10   # minimum coverage fraction (10%)


def _pair_flag(pf_lift: float, coverage: float) -> str:
    return "[OK]" if (pf_lift >= MIN_LIFT_THRESHOLD and coverage >= MIN_COVERAGE_THRESHOLD) else "[--]"


def _cov_str(coverage: float) -> str:
    pct = coverage * 100
    warn = "!" if coverage < MIN_COVERAGE_THRESHOLD else ""
    return f"cov {pct:.1f}%{warn}"


def _population_table(symbol: str, symbol_df: pd.DataFrame, baseline_label: str) -> list[str]:
    """Build a per-pair population comparison table (baseline row + one row per idea)."""
    # All rows for this symbol share the same baseline stats — take from first row.
    first = symbol_df.iloc[0]
    has_dur = "baseline_avg_dur" in symbol_df.columns

    lines = [
        f"#### {symbol} - Population Comparison",
        "",
        "| population | wr_% | pf | dur | n_trades |",
        "|------------|-----:|---:|----:|---------:|",
    ]

    # Baseline row
    b_dur = f"{first['baseline_avg_dur']:.1f}" if has_dur else "-"
    lines.append(
        f"| {baseline_label} "
        f"| {first['baseline_wr']*100:.2f} "
        f"| {first['baseline_pf']:.3f} "
        f"| {b_dur} "
        f"| {int(first['baseline_n']):,} |"
    )

    # One row per idea, sorted by pf_lift descending
    for _, row in symbol_df.sort_values("pf_lift", ascending=False).iterrows():
        c_dur = f"{row['candidate_avg_dur']:.1f}" if has_dur else "-"
        lines.append(
            f"| {row['idea_name']} "
            f"| {row['candidate_wr']*100:.2f} "
            f"| {row['candidate_pf']:.3f} "
            f"| {c_dur} "
            f"| {int(row['candidate_n']):,} |"
        )

    lines.append("")
    return lines


def write_active_boards(csv_path: Path, results_dir: Path, phase: str) -> None:
    """
    Write one active-board MD per entry_tf found in *csv_path*.

    Files are placed in *results_dir* as:
        phase_{phase}_entry{tf}_active.md

    Parameters
    ----------
    csv_path:    Phase comparison CSV.
    results_dir: Directory where MD files are written.
    phase:       "regime", "setup", or "trigger".
    """
    if not csv_path.exists():
        return

    df = pd.read_csv(csv_path)
    active = df[df["decision"].isin(["PENDING", "PROMOTED"])].copy()
    if active.empty:
        return

    results_dir.mkdir(parents=True, exist_ok=True)
    baseline_label = active["baseline_label"].iloc[0]

    for entry_tf, tf_df in active.groupby("entry_tf"):
        lines: list[str] = [
            f"## Phase: {phase.upper()}  |  Entry TF: {entry_tf}",
            f"_Baseline: {baseline_label}  |  Updated: {date.today()}_",
            "",
        ]

        # ── Batch Summary ─────────────────────────────────────────────────
        pairs_total = tf_df["symbol"].nunique()
        summary_rows: list[dict] = []
        for idea_name, idea_df in tf_df.groupby("idea_name"):
            avg_pf   = idea_df["candidate_pf"].mean()
            avg_lift = idea_df["pf_lift"].mean()
            pairs_ok = (
                (idea_df["pf_lift"] >= MIN_LIFT_THRESHOLD) &
                (idea_df["candidate_coverage"] >= MIN_COVERAGE_THRESHOLD)
            ).sum()
            decision = idea_df["decision"].iloc[0]
            summary_rows.append({
                "idea": idea_name,
                "avg_pf":   avg_pf,
                "avg_lift": avg_lift,
                "pairs_ok": pairs_ok,
                "decision": decision,
            })

        summary_rows.sort(key=lambda r: r["avg_lift"], reverse=True)

        lines += [
            "### Batch Summary",
            f"| idea | avg PF | avg PF lift | pairs OK | decision |",
            f"|------|--------|-------------|----------|----------|",
        ]
        for r in summary_rows:
            lines.append(
                f"| {r['idea']} "
                f"| {r['avg_pf']:.3f} "
                f"| {r['avg_lift']:+.3f} "
                f"| {int(r['pairs_ok'])}/{pairs_total} "
                f"| {r['decision']} |"
            )

        lines.append("")

        # ── Per-Idea Detail ───────────────────────────────────────────────
        lines.append("### Per-Idea Detail")
        lines.append("")

        for r in summary_rows:
            idea_name = r["idea"]
            idea_df   = tf_df[tf_df["idea_name"] == idea_name].sort_values("symbol")
            avg_pf    = r["avg_pf"]
            avg_lift  = r["avg_lift"]
            pairs_ok  = r["pairs_ok"]
            decision  = r["decision"]

            lines.append(
                f"**{idea_name}**  "
                f"avg PF {avg_pf:.3f}  "
                f"avg lift {avg_lift:+.3f}  "
                f"{int(pairs_ok)}/{pairs_total} pairs  "
                f"{decision}"
            )

            for _, row in idea_df.iterrows():
                flag     = _pair_flag(row["pf_lift"], row["candidate_coverage"])
                cov      = _cov_str(row["candidate_coverage"])
                n_fmt    = f"{int(row['candidate_n']):,}"
                lines.append(
                    f"  {row['symbol']:10s}  "
                    f"WR {row['candidate_wr']*100:.1f}%  "
                    f"PF {row['candidate_pf']:.3f}  "
                    f"lift {row['pf_lift']:+.3f} / req {MIN_LIFT_THRESHOLD:.2f}  "
                    f"n={n_fmt}  "
                    f"{cov}  "
                    f"{flag}"
                )
            lines.append("")

        # ── Population Comparison (per pair) ─────────────────────────────
        lines.append("### Population Comparison")
        lines.append("")
        for symbol, symbol_df in tf_df.groupby("symbol"):
            lines += _population_table(str(symbol), symbol_df, baseline_label)

        out_path = results_dir / f"phase_{phase}_entry{entry_tf}_active.md"
        out_path.write_text("\n".join(lines))
