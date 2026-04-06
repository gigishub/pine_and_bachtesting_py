from __future__ import annotations

try:
    from .robustness_v4.simple_config import build_simple_config
    from .robustness_v4.sequencer import run_sequential
    from .robustness_v4.reporter import build_robustness_summary
except ImportError:
    from UPS_py_v2.backtest.robustness_v4.simple_config import build_simple_config
    from UPS_py_v2.backtest.robustness_v4.sequencer import run_sequential
    from UPS_py_v2.backtest.robustness_v4.reporter import build_robustness_summary

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

if __name__ == "__main__":
    config = build_simple_config()

    print(f"\nV4 Robustness Run")
    print(f"  Symbols:    {', '.join(config.symbols)}")
    print(f"  Timeframes: {', '.join(config.timeframes)}")
    print(f"  Conditions: {len(config.build_datasets())}")
    print(f"  Output dir: {config.output_dir}\n")

    saved = run_sequential(config)

    print(f"\nAll conditions complete. Building robustness summary...")
    summary = build_robustness_summary(config.output_dir, consistency_top_n=config.consistency_top_n)

    print(f"\nTop 10 most robust setups:")
    if not summary.empty:
        cols = [c for c in ["Robustness Rank", "Consistency Score", "Consistency [%]",
                             "Expectancy [%] Mean", "Return [%] Mean", "Parameter Signature"]
                if c in summary.columns]
        print(summary[cols].head(10).to_string(index=False))

    print(f"\nFull summary saved to: {config.output_dir}/ROBUSTNESS_SUMMARY.csv")
    print(f"Launch viewer: streamlit run UPS_py_v2/backtest/robustness_v4/streamlit_viewer.py")
