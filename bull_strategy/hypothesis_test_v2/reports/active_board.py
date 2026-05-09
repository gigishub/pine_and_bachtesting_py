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
    [OK]  = pf_lift >= min_pf_lift AND wr_zscore >= min_wr_zscore AND coverage >= min_coverage
    [!-]  = fails any gate BUT at least one failing value is within 15% below its threshold
    [--]  = fails and no value is close to any threshold
    cov X%!  = coverage below min_coverage (inline warning)
    Thresholds are set in hypothesis_test_v2/config.py  SHARED dict.
"""

from __future__ import annotations

import math
from pathlib import Path
from datetime import date

import pandas as pd

def _wr_zscore(wr_lift: float, baseline_wr: float, smaller_n: int) -> float:
    """z-score for WR lift: signal / noise, where noise = sqrt(p*(1-p)/n)."""
    if smaller_n <= 0:
        return 0.0
    noise = math.sqrt(baseline_wr * (1.0 - baseline_wr) / smaller_n)
    return (wr_lift / noise) if noise > 0.0 else 0.0


def _pair_flag(pf_lift: float, wr_zscore: float, coverage: float, thresholds: dict) -> str:
    pf_ok  = pf_lift   >= thresholds["min_pf_lift"]
    z_ok   = wr_zscore >= thresholds["min_wr_zscore"]
    cov_ok = coverage  >= thresholds["min_coverage"]
    if pf_ok and z_ok and cov_ok:
        return "[OK]"
    # Near-miss: any failing criterion is within 15% below its threshold
    near      = 0.85
    pf_close  = (not pf_ok)  and pf_lift   >= thresholds["min_pf_lift"]  * near
    z_close   = (not z_ok)   and wr_zscore >= thresholds["min_wr_zscore"] * near
    cov_close = (not cov_ok) and coverage  >= thresholds["min_coverage"]  * near
    return "[!-]" if (pf_close or z_close or cov_close) else "[--]"


def _cov_str(coverage: float, thresholds: dict) -> str:
    pct = coverage * 100
    warn = "!" if coverage < thresholds["min_coverage"] else ""
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


def write_active_boards(
    csv_path: Path,
    results_dir: Path,
    phase: str,
    thresholds: dict,
) -> None:
    """
    Write one active-board MD per entry_tf found in *csv_path*.

    Files are placed in *results_dir* as:
        phase_{phase}_entry{tf}_active.md

    Parameters
    ----------
    csv_path:    Phase comparison CSV.
    results_dir: Directory where MD files are written.
    phase:       "regime", "setup", or "trigger".
    thresholds:  THRESHOLDS dict from the phase config.
    """
    if not csv_path.exists():
        return

    df = pd.read_csv(csv_path)
    active = df[df["decision"].isin(["PENDING", "PROMOTED"])].copy()
    if active.empty:
        return

    # Pre-compute WR z-score for every row so the verdict gate can use it.
    active["wr_zscore"] = active.apply(
        lambda r: _wr_zscore(
            float(r["wr_lift"]),
            float(r["baseline_wr"]),
            int(min(r["candidate_n"], r["baseline_n"])),
        ),
        axis=1,
    )

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
                (idea_df["pf_lift"] >= thresholds["min_pf_lift"]) &
                (idea_df["wr_zscore"] >= thresholds["min_wr_zscore"]) &
                (idea_df["candidate_coverage"] >= thresholds["min_coverage"])
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
                z        = row["wr_zscore"]
                flag     = _pair_flag(row["pf_lift"], z, row["candidate_coverage"], thresholds)
                cov      = _cov_str(row["candidate_coverage"], thresholds)
                n_fmt    = f"{int(row['candidate_n']):,}"
                lines.append(
                    f"  {row['symbol']:10s}  "
                    f"WR {row['candidate_wr']*100:.1f}%  "
                    f"PF {row['candidate_pf']:.3f}  "
                    f"lift {row['pf_lift']:+.3f} / req {thresholds['min_pf_lift']:.2f}  "
                    f"z={z:.1f} / req {thresholds['min_wr_zscore']:.1f}  "
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
