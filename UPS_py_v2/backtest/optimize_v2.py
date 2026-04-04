from __future__ import annotations

import argparse

from .robustness_v2 import (
    DEFAULT_OPTIMIZATION_CONFIG,
    STEP_CONSISTENCY,
    STEP_DATASETS,
    STEP_DATASET_SEARCH,
    STEP_INTERSECTION,
    STEP_MASTER_WINNERS,
    STEP_OUT_OF_SAMPLE,
    OptimizationConfig,
    render_pipeline_report,
    run_optimizer_pipeline,
)
from ..strategy.strategy_parameters import StrategySettings
from .robustness_v2.config import ParameterValue

STEP_CHOICES = [
    STEP_DATASETS,
    STEP_DATASET_SEARCH,
    STEP_MASTER_WINNERS,
    STEP_INTERSECTION,
    STEP_CONSISTENCY,
    STEP_OUT_OF_SAMPLE,
]


def _parse_value(raw: str) -> ParameterValue:
    lowered = raw.strip().lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    try:
        if any(char in raw for char in (".", "e", "E")):
            return float(raw)
        return int(raw)
    except ValueError:
        return raw.strip()


def _parse_parameter_override(spec: str) -> tuple[str, tuple[ParameterValue, ...]]:
    if "=" not in spec:
        raise ValueError(f"Invalid parameter override: {spec}")
    name, raw_values = spec.split("=", 1)
    values = tuple(_parse_value(value) for value in raw_values.split(",") if value.strip())
    if not values:
        raise ValueError(f"No values supplied for parameter override: {spec}")
    return name.strip(), values


def build_cli_config(args: argparse.Namespace) -> OptimizationConfig:
    config = OptimizationConfig(
        source=DEFAULT_OPTIMIZATION_CONFIG.source,
        market_type=DEFAULT_OPTIMIZATION_CONFIG.market_type,
        symbols=list(DEFAULT_OPTIMIZATION_CONFIG.symbols),
        timeframes=list(DEFAULT_OPTIMIZATION_CONFIG.timeframes),
        start_time=DEFAULT_OPTIMIZATION_CONFIG.start_time,
        end_time=DEFAULT_OPTIMIZATION_CONFIG.end_time,
        in_sample_ratio=DEFAULT_OPTIMIZATION_CONFIG.in_sample_ratio,
        min_bars=DEFAULT_OPTIMIZATION_CONFIG.min_bars,
        top_n=DEFAULT_OPTIMIZATION_CONFIG.top_n,
        baseline_settings=StrategySettings(**vars(DEFAULT_OPTIMIZATION_CONFIG.baseline_settings)),
        parameter_ranges=dict(DEFAULT_OPTIMIZATION_CONFIG.parameter_ranges),
        feature_dependencies=dict(DEFAULT_OPTIMIZATION_CONFIG.feature_dependencies),
    )

    if args.symbol:
        config.set_symbols(*args.symbol)
    if args.timeframe:
        config.set_timeframes(*args.timeframe)
    if args.start_time:
        config.start_time = args.start_time
    if args.end_time:
        config.end_time = args.end_time
    if args.top_n is not None:
        config.top_n = args.top_n
    if args.min_bars is not None:
        config.min_bars = args.min_bars
    if args.in_sample_ratio is not None:
        config.in_sample_ratio = args.in_sample_ratio

    for spec in args.drop_param or []:
        config.remove_parameter(spec)
    for spec in args.param or []:
        name, values = _parse_parameter_override(spec)
        config.set_parameter_range(name, *values)

    return config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the robustness v2 optimizer")
    parser.add_argument("--symbol", action="append", help="Add or replace symbols to optimize")
    parser.add_argument("--timeframe", action="append", help="Add or replace timeframes to optimize")
    parser.add_argument("--start-time", default=None)
    parser.add_argument("--end-time", default=None)
    parser.add_argument("--top-n", type=int, default=None)
    parser.add_argument("--min-bars", type=int, default=None)
    parser.add_argument("--in-sample-ratio", type=float, default=None)
    parser.add_argument(
        "--param",
        action="append",
        help="Override or add parameter ranges, example: --param ma_length=20,50,100",
    )
    parser.add_argument(
        "--drop-param",
        action="append",
        help="Remove a parameter from the optimization grid",
    )
    parser.add_argument(
        "--stop-after",
        choices=STEP_CHOICES,
        default=None,
        help="Stop after a specific pipeline step and print results up to that point",
    )
    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    config = build_cli_config(args)
    artifacts = run_optimizer_pipeline(config, stop_after=args.stop_after)
    print(render_pipeline_report(artifacts, config))
