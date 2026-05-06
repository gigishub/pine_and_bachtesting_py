"""
Rejected archive Markdown writer — one file per phase × entry_tf.

Naming:  phase_{phase}_entry{tf}_rejected.md

Format (per rejected idea):
    ### {idea_name}
    Description: {short_description or params}
    Params: key=val ...
    Rejected at: {date}  |  Reason: {decision_reason}

      avg PF: 1.41  avg PF lift: -0.15  pairs OK: 1/3
      BTCUSDT   WR 48.2%  PF 1.395  lift +0.024 / req 0.05  n=249    cov 3.0%!  [--]
      ETHUSDT   WR 52.3%  PF 1.643  lift -0.102 / req 0.05  n=241    cov 3.0%!  [--]
"""

from __future__ import annotations

from pathlib import Path
from datetime import date

import pandas as pd

MIN_LIFT_THRESHOLD     = 0.05
MIN_COVERAGE_THRESHOLD = 0.10


def _pair_flag(pf_lift: float, coverage: float) -> str:
    return "[OK]" if (pf_lift >= MIN_LIFT_THRESHOLD and coverage >= MIN_COVERAGE_THRESHOLD) else "[--]"


def _cov_str(coverage: float) -> str:
    pct = coverage * 100
    warn = "!" if coverage < MIN_COVERAGE_THRESHOLD else ""
    return f"cov {pct:.1f}%{warn}"


def append_rejected_by_tf(
    csv_path: Path,
    results_dir: Path,
    phase: str,
) -> None:
    """
    For each entry_tf in *csv_path*, append newly REJECTED ideas to
    ``phase_{phase}_entry{tf}_rejected.md`` inside *results_dir*.

    Already-archived entries are de-duplicated by (idea_name, symbol, entry_tf).

    Parameters
    ----------
    csv_path:    Phase comparison CSV.
    results_dir: Directory where rejected archive MD files live.
    phase:       "regime", "setup", or "trigger".
    """
    if not csv_path.exists():
        return

    df      = pd.read_csv(csv_path)
    rejects = df[df["decision"] == "REJECTED"]
    if rejects.empty:
        return

    results_dir.mkdir(parents=True, exist_ok=True)
    pairs_total = df["symbol"].nunique()

    for entry_tf, tf_df in rejects.groupby("entry_tf"):
        out_path     = results_dir / f"phase_{phase}_entry{entry_tf}_rejected.md"
        existing_txt = out_path.read_text() if out_path.exists() else ""

        new_sections: list[str] = []

        for idea_name, idea_df in tf_df.groupby("idea_name"):
            # De-duplicate: skip if this idea is already in the archive.
            if f"### {idea_name}" in existing_txt:
                continue

            idea_df   = idea_df.sort_values("symbol")
            avg_pf    = idea_df["candidate_pf"].mean()
            avg_lift  = idea_df["pf_lift"].mean()
            pairs_ok  = (
                (idea_df["pf_lift"] >= MIN_LIFT_THRESHOLD) &
                (idea_df["candidate_coverage"] >= MIN_COVERAGE_THRESHOLD)
            ).sum()

            params_str = ""  # filled if a decision_reason col exists
            reason     = idea_df.get("decision_reason", pd.Series([""])).iloc[0] or "—"

            section: list[str] = [
                f"### {idea_name}",
                f"Rejected at: {date.today()}  |  Reason: {reason}",
                "",
                f"  avg PF: {avg_pf:.3f}  avg PF lift: {avg_lift:+.3f}  "
                f"pairs OK: {int(pairs_ok)}/{pairs_total}",
            ]

            for _, row in idea_df.iterrows():
                flag  = _pair_flag(row["pf_lift"], row["candidate_coverage"])
                cov   = _cov_str(row["candidate_coverage"])
                n_fmt = f"{int(row['candidate_n']):,}"
                section.append(
                    f"  {row['symbol']:10s}  "
                    f"WR {row['candidate_wr']*100:.1f}%  "
                    f"PF {row['candidate_pf']:.3f}  "
                    f"lift {row['pf_lift']:+.3f} / req {MIN_LIFT_THRESHOLD:.2f}  "
                    f"n={n_fmt}  "
                    f"{cov}  "
                    f"{flag}"
                )
            section.append("---")
            new_sections.append("\n".join(section))

        if not new_sections:
            continue

        header = (
            f"## Phase: {phase.upper()}  |  Entry TF: {entry_tf}  |  Rejected Archive\n\n"
            if not existing_txt
            else ""
        )
        with open(out_path, "a") as f:
            f.write(header + "\n\n".join(new_sections) + "\n")
