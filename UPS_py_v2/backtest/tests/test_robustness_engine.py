from __future__ import annotations

import pandas as pd

from UPS_py_v2.backtest.robustness import (
    DEFAULT_MATRIX_CONFIG,
    build_parameter_grid,
    build_parameter_signature,
    filter_consistent_winners,
    find_intersection_winners,
)


def test_build_parameter_grid_deduplicates_dependent_flags() -> None:
    baseline_params = {
        "use_iq_filter": True,
        "use_sq_boost": True,
        "enable_ec": True,
        "enable_bullish_engulfing": True,
        "enable_shooting_star": True,
        "enable_hammer": True,
        "risk_reward_multiplier": 1.0,
    }

    grid = build_parameter_grid(baseline_params, DEFAULT_MATRIX_CONFIG)
    signatures = {
        build_parameter_signature(params, DEFAULT_MATRIX_CONFIG.filter_names)
        for params in grid
    }

    assert len(grid) == len(signatures)
    assert len(grid) == 192


def test_find_intersection_winners_requires_majority_hits() -> None:
    rows = []
    for dataset_index in range(1, 6):
        rows.append(
            {
                "Dataset": f"BTCUSDT tf{dataset_index}",
                "Rank": 1,
                "Parameter Signature": "sig-majority",
                "Expectancy [%]": 2.0,
                "Return [%]": 4.0,
                "risk_reward_multiplier": 2.0,
                "use_iq_filter": True,
                "use_sq_boost": True,
                "enable_ec": True,
                "enable_bullish_engulfing": False,
                "enable_shooting_star": True,
                "enable_hammer": True,
            }
        )
    rows.append(
        {
            "Dataset": "ETHUSDT tf1",
            "Rank": 1,
            "Parameter Signature": "sig-minority",
            "Expectancy [%]": 6.0,
            "Return [%]": 8.0,
            "risk_reward_multiplier": 5.0,
            "use_iq_filter": False,
            "use_sq_boost": False,
            "enable_ec": False,
            "enable_bullish_engulfing": True,
            "enable_shooting_star": False,
            "enable_hammer": False,
        }
    )

    winners = find_intersection_winners(
        pd.DataFrame(rows),
        total_datasets=9,
        filter_names=DEFAULT_MATRIX_CONFIG.filter_names,
    )

    assert list(winners["Parameter Signature"]) == ["sig-majority"]
    assert int(winners.iloc[0]["Top 10 Hits"]) == 5


def test_filter_consistent_winners_requires_positive_expectancy_everywhere() -> None:
    results = pd.DataFrame(
        [
            {
                "Dataset": "BTCUSDT 1h",
                "Parameter Signature": "sig-keep",
                "Expectancy [%]": 1.2,
                "Return [%]": 3.0,
                "Profit Factor": 1.5,
                "# Trades": 12,
                "risk_reward_multiplier": 2.0,
                "use_iq_filter": True,
                "use_sq_boost": True,
                "enable_ec": True,
                "enable_bullish_engulfing": True,
                "enable_shooting_star": False,
                "enable_hammer": True,
            },
            {
                "Dataset": "ETHUSDT 1h",
                "Parameter Signature": "sig-keep",
                "Expectancy [%]": 0.8,
                "Return [%]": 2.0,
                "Profit Factor": 1.2,
                "# Trades": 9,
                "risk_reward_multiplier": 2.0,
                "use_iq_filter": True,
                "use_sq_boost": True,
                "enable_ec": True,
                "enable_bullish_engulfing": True,
                "enable_shooting_star": False,
                "enable_hammer": True,
            },
            {
                "Dataset": "BTCUSDT 1h",
                "Parameter Signature": "sig-drop",
                "Expectancy [%]": 1.8,
                "Return [%]": 4.0,
                "Profit Factor": 1.6,
                "# Trades": 11,
                "risk_reward_multiplier": 3.0,
                "use_iq_filter": False,
                "use_sq_boost": False,
                "enable_ec": True,
                "enable_bullish_engulfing": False,
                "enable_shooting_star": True,
                "enable_hammer": True,
            },
            {
                "Dataset": "ETHUSDT 1h",
                "Parameter Signature": "sig-drop",
                "Expectancy [%]": -0.3,
                "Return [%]": 1.0,
                "Profit Factor": 0.9,
                "# Trades": 8,
                "risk_reward_multiplier": 3.0,
                "use_iq_filter": False,
                "use_sq_boost": False,
                "enable_ec": True,
                "enable_bullish_engulfing": False,
                "enable_shooting_star": True,
                "enable_hammer": True,
            },
        ]
    )

    consistent = filter_consistent_winners(
        results,
        {"sig-keep", "sig-drop"},
        total_datasets=2,
        filter_names=DEFAULT_MATRIX_CONFIG.filter_names,
    )

    assert list(consistent["Parameter Signature"]) == ["sig-keep"]