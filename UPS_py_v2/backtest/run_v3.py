from __future__ import annotations

try:
    from .robustness_v3 import render_pipeline_report, run_robustness_pipeline
    from .robustness_v3.simple_config import build_simple_config
except ImportError:
    from UPS_py_v2.backtest.robustness_v3 import render_pipeline_report, run_robustness_pipeline
    from UPS_py_v2.backtest.robustness_v3.simple_config import build_simple_config


if __name__ == "__main__":
    config = build_simple_config()
    artifacts = run_robustness_pipeline(config)
    print(render_pipeline_report(artifacts, config))