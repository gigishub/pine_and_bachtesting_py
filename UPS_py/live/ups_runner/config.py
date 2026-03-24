from __future__ import annotations

import os
from dataclasses import dataclass


_INTERVAL_TO_MS = {
    "1": 60_000,
    "3": 180_000,
    "5": 300_000,
    "15": 900_000,
    "30": 1_800_000,
    "60": 3_600_000,
    "120": 7_200_000,
    "240": 14_400_000,
    "360": 21_600_000,
    "720": 43_200_000,
    "D": 86_400_000,
    "W": 604_800_000,
}

_TIMEFRAME_MAP = {
    "1m": "1",
    "3m": "3",
    "5m": "5",
    "15m": "15",
    "30m": "30",
    "1h": "60",
    "2h": "120",
    "4h": "240",
    "6h": "360",
    "12h": "720",
    "1d": "D",
    "1w": "W",
}


@dataclass
class LiveConfig:
    api_key: str
    api_secret: str
    testnet: bool = False
    category: str = "linear"
    symbol: str = "BTCUSDT"
    timeframe: str = "1m"
    warmup_bars: int = 400
    poll_ahead_ms: int = 200
    use_ws_kline: bool = True
    ws_queue_timeout_s: float = 120.0

    # Strategy settings (same defaults as backtest).
    ma_length: int = 50
    max_candles_beyond_ma: int = 1
    ma_consolidation_lookback: int = 10
    ma_consolidation_count: int = 4
    ma_breach_lookback: int = 5
    use_iq_filter: bool = True
    iq_lookback: int = 20
    iq_min_score: float = 0.55
    iq_slope_atr_scale: float = 1.5
    iq_er_weight: float = 0.5
    iq_slope_weight: float = 0.3
    iq_bias_weight: float = 0.2
    use_sq_boost: bool = True
    sq_boost_weight: float = 0.3
    sq_vol_lookback: int = 20
    long_trades: bool = True
    short_trades: bool = True
    enable_ec: bool = True
    enable_bullish_engulfing: bool = True
    enable_shooting_star: bool = True
    ec_wick: bool = False
    enable_hammer: bool = True
    atr_max_size: float = 2.5
    rejection_wick_max_size: float = 0.0
    hammer_fib: float = 0.3
    hammer_size: float = 0.1
    stop_multiplier: float = 1.0
    risk_reward_multiplier: float = 1.0
    minimum_rr: float = 0.0
    pb_reference: str = "Close"
    sl_reference: str = "High/Low"
    trail_stop: bool = True
    trail_stop_size: float = 1.0
    trail_source: str = "High/Low"
    lookback: int = 5
    atr_length: int = 14
    point_allowance: int = 0

    # Execution settings.
    position_idx: int = 0
    reduce_only_closes: bool = True
    risk_per_trade_usdt: float = 100.0
    fixed_order_qty: float = 0.0
    min_notional_usdt: float = 5.0
    dry_run: bool = False


def normalize_interval(timeframe: str) -> str:
    interval = _TIMEFRAME_MAP.get(timeframe.lower(), timeframe)
    if interval not in _INTERVAL_TO_MS:
        raise ValueError(f"Unsupported timeframe: {timeframe}")
    return interval


def interval_to_ms(interval: str) -> int:
    return _INTERVAL_TO_MS[interval]


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def build_config_from_env() -> LiveConfig:
    api_key = os.getenv("BYBIT_API_KEY", "")
    api_secret = os.getenv("BYBIT_API_SECRET", "")
    if not api_key or not api_secret:
        raise RuntimeError("Set BYBIT_API_KEY and BYBIT_API_SECRET")

    return LiveConfig(
        api_key=api_key,
        api_secret=api_secret,
        testnet=_env_bool("BYBIT_TESTNET", False),
        category=os.getenv("BYBIT_CATEGORY", "linear"),
        symbol=os.getenv("BYBIT_SYMBOL", "BTCUSDT"),
        timeframe=os.getenv("BYBIT_TIMEFRAME", "1m"),
        warmup_bars=int(os.getenv("UPS_WARMUP_BARS", "400")),
        use_ws_kline=_env_bool("UPS_USE_WS_KLINE", True),
        ws_queue_timeout_s=float(os.getenv("UPS_WS_QUEUE_TIMEOUT_S", "120")),
        dry_run=_env_bool("UPS_DRY_RUN", False),
        fixed_order_qty=float(os.getenv("UPS_FIXED_QTY", "0")),
        risk_per_trade_usdt=float(os.getenv("UPS_RISK_USDT", "100")),
        trail_stop=_env_bool("UPS_TRAIL_STOP", True),
    )
