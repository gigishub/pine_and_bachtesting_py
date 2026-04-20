"""CLI entrypoint for the strategy robustness evaluator.

Usage
-----
python -m strategy_evaluation <results_dir> [--label AMS]
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.consistency import symbol_pass_rate, timeframe_pass_rate, toggle_frequency, compute_toggle_consensus
from strategy_evaluation.importance import compute_shap_importance, compute_toggle_importance
from strategy_evaluation.loader import load_data_period, load_run_dir
from strategy_evaluation.metrics import annotate_dataframe
from strategy_evaluation.report import format_report, save_report
from strategy_evaluation.scorer import aggregate_verdict
from strategy_evaluation.significance import compute_ols_significance


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate a backtest results directory for strategy robustness."
    )
    parser.add_argument("results_dir", help="Path to the VBT backtest results directory.")
    parser.add_argument("--label", default="strategy", help="Strategy label for the report filename.")
    args = parser.parse_args(argv)

    cfg = RobustnessConfig()

    df = load_run_dir(args.results_dir)
    df = annotate_dataframe(df, cfg)

    sym_rates = symbol_pass_rate(df, cfg)
    tf_rates = timeframe_pass_rate(df, cfg)
    tog_freq = toggle_frequency(df, cfg)

    result = aggregate_verdict(sym_rates, tf_rates, tog_freq, cfg)

    importance = compute_toggle_importance(df, cfg)
    shap_result = compute_shap_importance(df, cfg)
    ols = compute_ols_significance(df, cfg)
    toggle_consensus_df = compute_toggle_consensus(df, cfg, ols, shap_result)
    top_combos = df[df["_passes"]].copy() if "_passes" in df.columns else None

    _n_total      = len(df)
    _n_symbols    = df[cfg.col_symbol].nunique()
    _n_timeframes = df[cfg.col_timeframe].nunique()
    _n_param_sets = _n_total // (_n_symbols * _n_timeframes) if (_n_symbols * _n_timeframes) else 0
    _n_passing    = int(df["_passes"].sum()) if "_passes" in df.columns else 0

    data_period = load_data_period(args.results_dir)

    report_str = format_report(
        result,
        label=args.label,
        importance=importance,
        shap=shap_result,
        ols=ols,
        top_combos=top_combos,
        data_period=data_period,
        toggle_consensus=toggle_consensus_df,
        combo_summary={
            "n_total": _n_total,
            "n_passing": _n_passing,
            "n_symbols": _n_symbols,
            "n_timeframes": _n_timeframes,
            "n_param_sets": _n_param_sets,
        },
        df=df,
        cfg=cfg,
    )
    print(report_str)

    saved = save_report(report_str, label=args.label, output_dir=Path(args.results_dir))
    print(f"\nReport saved → {saved}")


if __name__ == "__main__":
    main(sys.argv[1:])

