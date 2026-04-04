from __future__ import annotations

import pandas as pd

from UPS_py_v2.backtest.robustness_v3 import (
    STEP_DATASET_RUNS,
    STEP_PARAMETER_GRID,
    OptimizationConfigV3,
    build_simple_config,
    build_parameter_grid,
    build_parameter_signature,
    run_robustness_pipeline,
)


def _sample_ohlcv(rows: int = 60) -> pd.DataFrame:
    index = pd.date_range("2025-01-01", periods=rows, freq="h")
    values = list(range(rows))
    return pd.DataFrame(
        {
            "Open": [100 + value for value in values],
            "High": [101 + value for value in values],
            "Low": [99 + value for value in values],
            "Close": [100.5 + value for value in values],
            "Volume": [10_000 + value for value in values],
        },
        index=index,
    )


def test_v3_defaults_to_boolean_filters_and_four_rr_values() -> None:
    config = OptimizationConfigV3()

    assert tuple(config.boolean_filter_ranges.keys()) == (
        "use_iq_filter",
        "use_sq_boost",
        "enable_ec",
        "enable_bullish_engulfing",
        "enable_shooting_star",
        "enable_hammer",
    )
    assert config.risk_reward_range == (1.5, 2.0, 3.0, 5.0)
    assert config.optional_parameter_ranges == {}


def test_simple_config_keeps_file_based_defaults() -> None:
    config = build_simple_config()

    assert config.primary_symbol == "BTCUSDT"
    assert config.primary_timeframe == "1day"
    assert config.validation_timeframes == ["1day"]
    assert config.risk_reward_range == (1.5, 2.0, 3.0, 5.0)
    assert config.optional_parameter_ranges == {}


def test_v3_parameter_grid_uses_baseline_defaults_for_inactive_optional_params() -> None:
    config = OptimizationConfigV3(
        boolean_filter_ranges={
            "use_iq_filter": (False, True),
        },
        risk_reward_range=(1.5, 3.0),
        optional_parameter_ranges={
            "iq_lookback": (10, 20),
        },
    )
    baseline = config.build_baseline_params()

    grid = build_parameter_grid(baseline, config)
    signatures = {
        build_parameter_signature(params, config.parameter_names)
        for params in grid
    }

    assert len(grid) == len(signatures)
    assert len(grid) == 6
    inactive_rows = [params for params in grid if not params["use_iq_filter"]]
    assert {row["iq_lookback"] for row in inactive_rows} == {baseline["iq_lookback"]}


def test_v3_pipeline_can_stop_after_parameter_grid() -> None:
    config = OptimizationConfigV3(
        validation_symbols=["BTCUSDT", "ETHUSDT"],
        validation_timeframes=["1h", "4h", "1day"],
        min_bars=20,
        top_n=3,
    )

    def fake_loader(_dataset):
        return _sample_ohlcv()

    def fake_runner(_df, params):
        score = 0.0
        if params["use_iq_filter"]:
            score += 1.0
        if params["enable_ec"]:
            score += 0.5
        score += float(params["risk_reward_multiplier"])
        return pd.Series(
            {
                "Return [%]": score * 10,
                "Expectancy [%]": score,
                "Profit Factor": 1.0 + score,
                "Win Rate [%]": 40.0 + score,
                "Max. Drawdown [%]": -5.0,
                "# Trades": 5,
                "SQN": 1.0 + score,
            }
        )

    artifacts = run_robustness_pipeline(
        config,
        stop_after=STEP_PARAMETER_GRID,
        data_loader=fake_loader,
        backtest_runner=fake_runner,
    )

    assert artifacts.completed_step == STEP_PARAMETER_GRID
    assert artifacts.parameter_grid_size > 0
    assert artifacts.dataset_results.empty


def test_v3_pipeline_runs_two_steps_and_returns_dataset_results_only() -> None:
    config = OptimizationConfigV3(
        boolean_filter_ranges={
            "use_iq_filter": (False, True),
            "enable_ec": (False, True),
        },
        risk_reward_range=(1.5, 2.0),
        validation_symbols=["BTCUSDT", "ETHUSDT"],
        validation_timeframes=["1h", "4h", "1day"],
        min_bars=20,
        top_n=2,
    )

    def fake_loader(_dataset):
        return _sample_ohlcv()

    def fake_runner(_df, params):
        score = 0.2
        if params["use_iq_filter"]:
            score += 1.0
        if params["enable_ec"]:
            score += 0.6
        score += float(params["risk_reward_multiplier"])
        return pd.Series(
            {
                "Return [%]": score * 8,
                "Expectancy [%]": score,
                "Profit Factor": 1.0 + score,
                "Win Rate [%]": 35.0 + score,
                "Max. Drawdown [%]": -4.0,
                "# Trades": 7,
                "SQN": 1.0 + score,
            }
        )

    artifacts = run_robustness_pipeline(
        config,
        stop_after=STEP_DATASET_RUNS,
        data_loader=fake_loader,
        backtest_runner=fake_runner,
    )

    assert artifacts.completed_step == STEP_DATASET_RUNS
    assert artifacts.parameter_grid_size == 8
    assert len(artifacts.dataset_results) == 48
    assert set(artifacts.dataset_results["Dataset"].unique()) == {
        "BTCUSDT 1h",
        "BTCUSDT 4h",
        "BTCUSDT 1day",
        "ETHUSDT 1h",
        "ETHUSDT 4h",
        "ETHUSDT 1day",
    }