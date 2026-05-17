"""Bear Strategy — default BearGridConfig.

The baseline for all named configs. Represents the validated OOS setup.
Named configs (exit_isolation, exit_value_sweep, etc.) import and override this.

Run:
    python -m bear_strategy.backtest.vectorbt.run_grid --config default
"""

from __future__ import annotations

from pathlib import Path

from bear_strategy.backtest.vectorbt.bear_grid_config import BearGridConfig


def build_config() -> BearGridConfig:
    return BearGridConfig(
        symbols=[
            "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT",
            "BNBUSDT", "ADAUSDT", "DOTUSDT", "LTCUSDT", "XLMUSDT",
        ],
        start_date="2021-01-01",
        end_date="2023-11-01",
        data_dir="crypto_data/data",
        boolean_filter_ranges={
            "use_vp_trigger":        (True,),
            "use_fixed_tp":          (True,),
            "use_rsi_exit":          (False,),
            "use_macd_exit":         (False,),
            "use_rsi_oversold_exit": (False,),
            "use_ema_reclaim_exit":  (False,),
            "use_funding_exit":      (False,),
            "use_vbt_sl":            (False,),
            "use_vbt_sl_trail":      (False,),
        },
        fees=0.0011,
        output_dir=Path("bear_strategy/backtest/vectorbt/results/default"),
    )
