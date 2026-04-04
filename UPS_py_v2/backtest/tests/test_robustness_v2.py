from __future__ import annotations

import pandas as pd

from UPS_py_v2.backtest.robustness_v2 import (
    STEP_INTERSECTION,
    OptimizationConfig,
    build_parameter_grid,
    build_parameter_signature,
    run_optimizer_pipeline,
)


def _sample_ohlcv(rows: int = 40) -> pd.DataFrame:
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


def test_config_supports_dataset_and_parameter_changes() -> None:
    config = OptimizationConfig()

    config.add_symbol("ETHUSDT")
    config.add_timeframe("4h")
    config.set_parameter_range("atr_length", 10, 14, 20)
    config.remove_parameter("enable_hammer")

    assert config.symbols == ["BTCUSDT", "ETHUSDT"]
    assert config.timeframes == ["1h", "4h"]
    assert config.parameter_ranges["atr_length"] == (10, 14, 20)
    assert "enable_hammer" not in config.parameter_ranges


def test_build_parameter_grid_is_generic_and_deduplicates_dependencies() -> None:
    config = OptimizationConfig(
        parameter_ranges={
            "use_iq_filter": (False, True),
            "use_sq_boost": (False, True),
            "risk_reward_multiplier": (1.5, 2.0),
        }
    )
    baseline = config.build_baseline_params()

    grid = build_parameter_grid(baseline, config)
    signatures = {
        build_parameter_signature(params, config.parameter_names)
        for params in grid
    }

    assert len(grid) == len(signatures)
    assert len(grid) == 6


def test_pipeline_can_stop_after_intersection_and_expose_step_outputs() -> None:
    config = OptimizationConfig(
        parameter_ranges={
            "ma_length": (20, 50),
            "risk_reward_multiplier": (1.0, 2.0),
            "use_iq_filter": (False, True),
        },
        min_bars=20,
        top_n=2,
    )

    def fake_loader(_dataset):
        return _sample_ohlcv()

    def fake_runner(_df, params):
        score = 0.5
        if params["ma_length"] == 50:
            score += 1.0
        if params["risk_reward_multiplier"] == 2.0:
            score += 1.0
        if params["use_iq_filter"]:
            score += 1.0
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

    artifacts = run_optimizer_pipeline(
        config,
        stop_after=STEP_INTERSECTION,
        data_loader=fake_loader,
        backtest_runner=fake_runner,
    )

    assert artifacts.completed_step == STEP_INTERSECTION
    assert artifacts.dataset_splits
    assert not artifacts.dataset_results.empty
    assert not artifacts.master_winners.empty
    assert not artifacts.intersection_winners.empty
    assert artifacts.consistent_winners.empty
    assert artifacts.out_of_sample_results.empty
