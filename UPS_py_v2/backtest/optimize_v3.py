from __future__ import annotations

import argparse

try:
    from .robustness_v3 import (
        DEFAULT_OPTIMIZATION_CONFIG_V3,
        STEP_DATASET_RUNS,
        STEP_PARAMETER_GRID,
        OptimizationConfigV3,
        render_pipeline_report,
        run_robustness_pipeline,
    )
    from .robustness_v3.config import ParameterValue
    from ..strategy.strategy_parameters import StrategySettings
except ImportError:
    from UPS_py_v2.backtest.robustness_v3 import (
        DEFAULT_OPTIMIZATION_CONFIG_V3,
        STEP_DATASET_RUNS,
        STEP_PARAMETER_GRID,
        OptimizationConfigV3,
        render_pipeline_report,
        run_robustness_pipeline,
    )
    from UPS_py_v2.backtest.robustness_v3.config import ParameterValue
    from UPS_py_v2.strategy.strategy_parameters import StrategySettings

STEP_CHOICES = [STEP_PARAMETER_GRID, STEP_DATASET_RUNS]


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


def build_cli_config(args: argparse.Namespace) -> OptimizationConfigV3:
    config = OptimizationConfigV3(
        source=DEFAULT_OPTIMIZATION_CONFIG_V3.source,
        market_type=DEFAULT_OPTIMIZATION_CONFIG_V3.market_type,
        primary_symbol=DEFAULT_OPTIMIZATION_CONFIG_V3.primary_symbol,
        primary_timeframe=DEFAULT_OPTIMIZATION_CONFIG_V3.primary_timeframe,
        validation_symbols=list(DEFAULT_OPTIMIZATION_CONFIG_V3.validation_symbols),
        validation_timeframes=list(DEFAULT_OPTIMIZATION_CONFIG_V3.validation_timeframes),
        start_time=DEFAULT_OPTIMIZATION_CONFIG_V3.start_time,
        end_time=DEFAULT_OPTIMIZATION_CONFIG_V3.end_time,
        min_bars=DEFAULT_OPTIMIZATION_CONFIG_V3.min_bars,
        top_n=DEFAULT_OPTIMIZATION_CONFIG_V3.top_n,
        baseline_settings=StrategySettings(**vars(DEFAULT_OPTIMIZATION_CONFIG_V3.baseline_settings)),
        boolean_filter_ranges=dict(DEFAULT_OPTIMIZATION_CONFIG_V3.boolean_filter_ranges),
        risk_reward_range=DEFAULT_OPTIMIZATION_CONFIG_V3.risk_reward_range,
        optional_parameter_ranges=dict(DEFAULT_OPTIMIZATION_CONFIG_V3.optional_parameter_ranges),
        feature_dependencies=dict(DEFAULT_OPTIMIZATION_CONFIG_V3.feature_dependencies),
    )

    if args.primary_symbol:
        config.primary_symbol = args.primary_symbol
    if args.primary_timeframe:
        config.primary_timeframe = args.primary_timeframe
    if args.symbol:
        config.set_validation_symbols(*args.symbol)
    if args.timeframe:
        config.set_validation_timeframes(*args.timeframe)
    if args.start_time:
        config.start_time = args.start_time
    if args.end_time:
        config.end_time = args.end_time
    if args.top_n is not None:
        config.top_n = args.top_n
    if args.min_bars is not None:
        config.min_bars = args.min_bars
    if args.risk_reward:
        config.risk_reward_range = tuple(float(value) for value in args.risk_reward)

    for spec in args.drop_param or []:
        config.remove_parameter(spec)
    for spec in args.param or []:
        name, values = _parse_parameter_override(spec)
        if name in config.boolean_filter_ranges:
            config.set_boolean_filter_range(name, *(bool(value) for value in values))
            continue
        if name == "risk_reward_multiplier":
            config.risk_reward_range = tuple(float(value) for value in values)
            continue
        config.set_optional_parameter_range(name, *values)

    return config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the robustness v3 optimizer")
    parser.add_argument("--primary-symbol", default=None, help="Primary optimization symbol")
    parser.add_argument("--primary-timeframe", default=None, help="Primary optimization timeframe")
    parser.add_argument("--symbol", action="append", help="Validation matrix symbol")
    parser.add_argument("--timeframe", action="append", help="Validation matrix timeframe")
    parser.add_argument("--start-time", default=None)
    parser.add_argument("--end-time", default=None)
    parser.add_argument("--top-n", type=int, default=None)
    parser.add_argument("--min-bars", type=int, default=None)
    parser.add_argument(
        "--risk-reward",
        action="append",
        type=float,
        help="Replace the fixed four-value RR list with custom values",
    )
    parser.add_argument(
        "--param",
        action="append",
        help="Add optional parameter ranges, example: --param iq_lookback=10,20,30",
    )
    parser.add_argument(
        "--drop-param",
        action="append",
        help="Remove an optional parameter or Boolean filter from the optimization grid",
    )
    parser.add_argument(
        "--stop-after",
        choices=STEP_CHOICES,
        default=None,
        help="Stop after a specific v3 step",
    )
    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    config = build_cli_config(args)
    artifacts = run_robustness_pipeline(config, stop_after=args.stop_after)
    print(render_pipeline_report(artifacts, config))