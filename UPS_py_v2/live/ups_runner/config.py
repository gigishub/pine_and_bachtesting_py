from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

'''
running execution:
python -m UPS_py_v2.live.ups_live_runner 
'''

@dataclass
class LiveConfig:
    api_key: str
    api_secret: str
    testnet: bool = False  # toggle testnet/live environment

    # Market selection
    category: str = "linear"  # derivative category: linear/inverse/spot
    symbol: str = "ATOMUSDT"  # trading pair

    # Data timing
    timeframe: str = "15m"  # kline timeframe
    warmup_bars: int = 400  # historical bars needed before live signal execution
    poll_ahead_ms: int = 200  # REST polling lead-in to avoid late bar effects

    # WebSocket config
    use_ws_kline: bool = True  # use WS realtime klines when available
    ws_queue_timeout_s: float = 120.0  # ws queue timeout in seconds
    pending_fill_check_interval_s: float = 2.0  # when entry order is pending, poll fills at this interval
    pending_stop_retry_interval_s: float = 2.0  # while stop update is pending, retry at this interval

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
    trail_stop: bool = False
    trail_stop_size: float = 1.0
    trail_source: str = "High/Low"
    lookback: int = 5
    atr_length: int = 14
    point_allowance: int = 0


    # Leverage controls
    force_no_leverage: bool = False  # force 1x and ignore exchange/manual leverage
    leverage: float = 0.0            # fixed leverage fallback when auto is off
    auto_leverage_by_stop: bool = True       # toggle auto leverage on/off
    auto_leverage_min: float = 1.0           # lower bound for auto leverage
    auto_leverage_max: float = 10           # upper bound for auto leverage
    auto_leverage_sl_buffer_pct: float = 5.0 # liquidation buffer in %
    leverage_fail_soft: bool = True          # continue if leverage update fails

    # Execution controls
    position_idx: int = 0  # position mode: 0=one-way, 1=hedge-long, 2=hedge-short (futures only)
    reduce_only_closes: bool = True  # enforce all close orders as reduce-only to prevent accidental re-entries
    order_type: str = "Limit"  # entry order type: "Limit" (patient fill) or "Market" (instant)
    tp_as_limit: bool = True  # use limit order for TP exit to target maker fees (via Bybit partial mode)
    tp_limit_offset_ticks: int = 0  # tick offset for TP limit price (0=exact TP, >0=more aggressive fill)
    sl_as_market: bool = True  # use market order for SL to guarantee fill on emergency stop
    cancel_unfilled_limit_entry: bool = True  # cancel limit entry order if not filled by bar close
    cancel_unfilled_limit_entry_after_bars: int = 1  # wait N bars before canceling stale limit entry
    dry_run: bool = False  # dry-run mode: compute signals and log orders without executing on exchange

    # Sizing controls
    risk_per_trade_pct: float = 0.5 # risk percent of wallet (only if fixed_order_qty==0)
    fixed_order_qty: float = 0.0    # override to fixed size when > 0
    min_notional_usdt: float = 5.0  # avoid orders below exchange minimum



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


def _normalize_order_type(raw: str | None) -> str:
    value = (raw or "Market").strip().lower()
    if value in {"market", "m"}:
        return "Market"
    if value in {"limit", "l"}:
        return "Limit"
    raise ValueError("UPS_ORDER_TYPE must be 'Market' or 'Limit'")


def _load_dotenv_if_present() -> None:
    dotenv_path = Path(__file__).resolve().parents[3] / ".env"
    if not dotenv_path.exists():
        return

    for raw in dotenv_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        # Keep already-exported env vars as higher priority than .env defaults.
        if not os.getenv(key):
            os.environ[key] = value


def build_config_from_env() -> LiveConfig:
    _load_dotenv_if_present()

    api_key = os.getenv("BYBIT_API_KEY", "")
    api_secret = os.getenv("BYBIT_API_SECRET", "") or os.getenv("BYBIT_SECTRET", "")
    if not api_key or not api_secret:
        raise RuntimeError("Set BYBIT_API_KEY and BYBIT_API_SECRET")

    # Keep strategy/execution settings in code config; only secrets come from env/.env.
    cfg = LiveConfig(api_key=api_key, api_secret=api_secret)
    cfg.order_type = _normalize_order_type(cfg.order_type)

    return cfg
