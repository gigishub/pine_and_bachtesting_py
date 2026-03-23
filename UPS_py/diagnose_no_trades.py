from __future__ import annotations

import sys

sys.path.insert(0, "/Users/andre/Documents/Python_local/pine_script/UPS_py")

from fetch_data.fetch_kucoin_candles import load_ohlcv_kucoin
from strategy_logic import build_strategy_series
from ups_backtest import Settings


def main() -> None:
    s = Settings()
    df = load_ohlcv_kucoin(
        symbol="XBTUSDTM",
        market_type="futures",
        timeframe="15min",
        start_time="2026-01-01 00:00:00",
        end_time="2026-01-31 23:59:59",
    )

    sig = build_strategy_series(
        df=df,
        ma_length=s.ma_length,
        max_candles_beyond_ma=s.max_candles_beyond_ma,
        ma_consolidation_lookback=s.ma_consolidation_lookback,
        ma_consolidation_count=s.ma_consolidation_count,
        ma_breach_lookback=s.ma_breach_lookback,
        use_iq_filter=s.use_iq_filter,
        iq_lookback=s.iq_lookback,
        iq_min_score=s.iq_min_score,
        iq_slope_atr_scale=s.iq_slope_atr_scale,
        iq_er_weight=s.iq_er_weight,
        iq_slope_weight=s.iq_slope_weight,
        iq_bias_weight=s.iq_bias_weight,
        use_sq_boost=s.use_sq_boost,
        sq_boost_weight=s.sq_boost_weight,
        sq_vol_lookback=s.sq_vol_lookback,
        long_trades=s.long_trades,
        short_trades=s.short_trades,
        enable_ec=s.enable_ec,
        enable_bullish_engulfing=s.enable_bullish_engulfing,
        enable_shooting_star=s.enable_shooting_star,
        ec_wick=s.ec_wick,
        enable_hammer=s.enable_hammer,
        atr_max_size=s.atr_max_size,
        rejection_wick_max_size=s.rejection_wick_max_size,
        hammer_fib=s.hammer_fib,
        hammer_size=s.hammer_size,
        stop_multiplier=s.stop_multiplier,
        risk_reward_multiplier=s.risk_reward_multiplier,
        minimum_rr=s.minimum_rr,
        pb_reference=s.pb_reference,
        sl_reference=s.sl_reference,
        trail_stop=s.trail_stop,
        trail_stop_size=s.trail_stop_size,
        trail_source=s.trail_source,
        lookback=s.lookback,
        atr_length=s.atr_length,
        point_allowance=s.point_allowance,
    )

    ready = sig["is_ready"].astype(bool)

    print("bars", len(df))
    print("ready", int(ready.sum()))
    for k in [
        "price_above_ma",
        "long_conditions_met",
        "bearish_pb",
        "long_entry_pattern",
        "valid_long_entry",
        "bullish_engulfing",
        "hammer_candle",
    ]:
        if k in sig:
            print(k, int((ready & sig[k].astype(bool)).sum()))

    print("diagnosis_done")


if __name__ == "__main__":
    main()
