"""Entry-point for the vectorbt robustness run.

Usage:
  source .venv/bin/activate && python -m UPS_py_v2.backtest.vectorbt.run

Edit backtest/config/simple_config.py to change symbols, timeframes
and parameter grid — the same config drives both engines.

Results are saved to a timestamped subdirectory inside:
  UPS_py_v2/backtest/results/results_vbt/

The robustness summary CSV is built by the shared reporter module after all
conditions are complete.  Both engines write the same column format so you can
compare their outputs side-by-side.
"""

from __future__ import annotations

import logging
from pathlib import Path

from ..config.simple_config import build_simple_config, build_output_dir
from ..reporting.reporter import build_robustness_summary
from .sequencer import run_sequential

if __name__ == "__main__":
    output_dir = build_output_dir("vbt", "UPS")
    config = build_simple_config(output_dir=output_dir)

    log_path = Path(config.output_dir) / "run_vbt.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_path, mode="a"),
        ],
    )

    print(f"\nVectorBT Robustness Run")
    print(f"  Symbols:    {', '.join(config.symbols)}")
    print(f"  Timeframes: {', '.join(config.timeframes)}")
    print(f"  Conditions: {len(config.build_datasets())}")
    print(f"  Output dir: {config.output_dir}")
    print(f"  Log file:   {log_path}\n")

    saved = run_sequential(config)

    print(f"\nAll conditions complete. Building robustness summary...")
    summary = build_robustness_summary(config.output_dir, consistency_top_n=config.consistency_top_n)

    print(f"\nTop 10 most robust setups:")
    if not summary.empty:
        cols = [
            c for c in [
                "Robustness Rank", "Consistency Score", "Consistency [%]",
                "Expectancy [%] Mean", "Return [%] Mean", "Parameter Signature",
            ]
            if c in summary.columns
        ]
        print(summary[cols].head(10).to_string(index=False))

    print(f"\nFull summary saved to: {config.output_dir}/ROBUSTNESS_SUMMARY.csv")
    print(f"Launch viewer: streamlit run UPS_py_v2/backtest/reporting/streamlit_viewer.py")
