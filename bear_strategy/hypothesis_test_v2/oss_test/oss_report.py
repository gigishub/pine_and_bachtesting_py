"""
OOS report writer.

Produces one Markdown file per entry_tf:
    results/oss_report_entry{tf}.md

Format:
  - Header with OOS window and purpose statement
  - Summary table (strategy × avg PF, lift, pairs OK, verdict)
  - Per-strategy detail (one line per pair with flag, same style as active_board)
  - Population comparison table per pair
"""

from __future__ import annotations

import math
from datetime import date
from pathlib import Path

import pandas as pd


def _wr_zscore(wr_lift: float, baseline_wr: float, smaller_n: int) -> float:
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
    near      = 0.85
    pf_close  = (not pf_ok)  and pf_lift   >= thresholds["min_pf_lift"]  * near
    z_close   = (not z_ok)   and wr_zscore >= thresholds["min_wr_zscore"] * near
    cov_close = (not cov_ok) and coverage  >= thresholds["min_coverage"]  * near
    return "[!-]" if (pf_close or z_close or cov_close) else "[--]"


def _cov_str(coverage: float, thresholds: dict) -> str:
    pct  = coverage * 100
    warn = "!" if coverage < thresholds["min_coverage"] else ""
    return f"cov {pct:.1f}%{warn}"


def write_oss_report(csv_path: Path, results_dir: Path, thresholds: dict) -> None:
    """
    Read *csv_path* and write one ``oss_report_entry{tf}.md`` per entry_tf.

    Parameters
    ----------
    csv_path:    Path to oss_comparison.csv produced by oss_runner.
    results_dir: Directory where report files are written.
    thresholds:  THRESHOLDS dict from oss_test/config.py.
    """
    if not csv_path.exists():
        return
    df = pd.read_csv(csv_path)
    if df.empty:
        return

    df["wr_zscore"] = df.apply(
        lambda r: _wr_zscore(
            float(r["wr_lift"]),
            float(r["baseline_wr"]),
            int(min(r["candidate_n"], r["baseline_n"])),
        ),
        axis=1,
    )

    start = df["start_date"].iloc[0]
    end   = df["end_date"].iloc[0]

    for entry_tf, tf_df in df.groupby("entry_tf"):
        pairs_total = tf_df["symbol"].nunique()

        lines: list[str] = [
            f"## OOS Test: BEAR STRATEGY  |  Entry TF: {entry_tf}",
            (
                f"_OOS window: {start} → {end}  |  "
                f"Baseline: random (all candles)  |  Updated: {date.today()}_"
            ),
            "",
            "> **Purpose**: verify that the promoted strategy (regime + setup + trigger)",
            "> generalises to completely unseen data.  The baseline is every warmed candle",
            f"> — a pure random entry.  PASS requires PF lift ≥ {thresholds['min_pf_lift']:.2f}"
            f" AND WR z-score ≥ {thresholds['min_wr_zscore']:.1f}.",
            "",
        ]

        # ── Summary table ─────────────────────────────────────────────────────
        summary_rows: list[dict] = []
        for strategy_name, s_df in tf_df.groupby("idea_name"):
            avg_pf   = s_df["candidate_pf"].mean()
            avg_lift = s_df["pf_lift"].mean()
            pairs_ok = int(
                (
                    (s_df["pf_lift"]              >= thresholds["min_pf_lift"]) &
                    (s_df["wr_zscore"]            >= thresholds["min_wr_zscore"]) &
                    (s_df["candidate_coverage"]   >= thresholds["min_coverage"])
                ).sum()
            )
            summary_rows.append({
                "name":     strategy_name,
                "avg_pf":   avg_pf,
                "avg_lift": avg_lift,
                "pairs_ok": pairs_ok,
                "verdict":  "PASS" if pairs_ok > 0 else "FAIL",
            })
        summary_rows.sort(key=lambda r: r["avg_lift"], reverse=True)

        lines += [
            "### Summary",
            "| strategy | avg PF | avg PF lift | pairs OK | verdict |",
            "|----------|--------|-------------|----------|---------|",
        ]
        for r in summary_rows:
            lines.append(
                f"| {r['name']} "
                f"| {r['avg_pf']:.3f} "
                f"| {r['avg_lift']:+.3f} "
                f"| {r['pairs_ok']}/{pairs_total} "
                f"| {r['verdict']} |"
            )
        lines.append("")

        # ── Per-strategy detail ───────────────────────────────────────────────
        lines.append("### Per-Strategy Detail")
        lines.append("")
        for r in summary_rows:
            name  = r["name"]
            s_df  = tf_df[tf_df["idea_name"] == name].sort_values("symbol")
            lines.append(
                f"**{name}**  "
                f"avg PF {r['avg_pf']:.3f}  "
                f"avg lift {r['avg_lift']:+.3f}  "
                f"{r['pairs_ok']}/{pairs_total} pairs  "
                f"{r['verdict']}"
            )
            for _, row in s_df.iterrows():
                z    = row["wr_zscore"]
                flag = _pair_flag(row["pf_lift"], z, row["candidate_coverage"], thresholds)
                cov  = _cov_str(row["candidate_coverage"], thresholds)
                n_fmt = f"{int(row['candidate_n']):,}"
                lines.append(
                    f"  {row['symbol']:10s}  "
                    f"WR {row['candidate_wr'] * 100:.1f}%  "
                    f"PF {row['candidate_pf']:.3f}  "
                    f"lift {row['pf_lift']:+.3f} / req {thresholds['min_pf_lift']:.2f}  "
                    f"z={z:.1f} / req {thresholds['min_wr_zscore']:.1f}  "
                    f"n={n_fmt}  "
                    f"{cov}  "
                    f"{flag}"
                )
            lines.append("")

        # ── Population comparison per pair ────────────────────────────────────
        lines.append("### Population Comparison")
        lines.append("")
        for symbol, sym_df in tf_df.groupby("symbol"):
            first = sym_df.iloc[0]
            lines += [
                f"#### {symbol}",
                "",
                "| population | wr_% | pf | n_trades |",
                "|------------|-----:|---:|---------:|",
                (
                    f"| random_all_candles "
                    f"| {first['baseline_wr'] * 100:.1f}% "
                    f"| {first['baseline_pf']:.3f} "
                    f"| {int(first['baseline_n']):,} |"
                ),
            ]
            for _, row in sym_df.sort_values("idea_name").iterrows():
                lines.append(
                    f"| {row['idea_name']} "
                    f"| {row['candidate_wr'] * 100:.1f}% "
                    f"| {row['candidate_pf']:.3f} "
                    f"| {int(row['candidate_n']):,} |"
                )
            lines.append("")

        out_path = results_dir / f"oss_report_entry{entry_tf}.md"
        out_path.write_text("\n".join(lines))
