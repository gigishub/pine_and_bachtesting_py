from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

"""
Running execution:
    python -m bear_strategy.live.bear_live_runner
"""


@dataclass
class BearLiveConfig:
    api_key: str
    api_secret: str
    testnet: bool = False
    profile: str = "default"

    # Market selection
    category: str = "linear"
    symbol: str = "NEARUSDT"

    # Data timing — 1h entry timeframe fixed for bear strategy
    timeframe: str = "1h"
    warmup_bars: int = 300  # 1h bars for VP + ATR + RSI warmup
    warmup_bars_1d: int = 100  # 1d bars for RSI regime
    warmup_bars_funding: int = 50  # 8h funding settlement periods
    poll_ahead_ms: int = 200

    # WebSocket
    use_ws_kline: bool = True
    ws_queue_timeout_s: float = 120.0
    pending_fill_check_interval_s: float = 2.0
    pending_stop_retry_interval_s: float = 2.0

    # ── OOS strategy parameters (oos_sl3_tp6) ────────────────────────────────
    stop_atr_mult: float = 3.0
    target_atr_mult: float = 6.0
    atr_period: int = 7
    vp_price_bins: int = 50
    entry_regime_offset: int = 2

    # RSI bear zone
    rsi_period: int = 14
    rsi_ma_period: int = 9   # Parameters default — not swept in OOS config
    rsi_lower: float = 30.0
    rsi_upper: float = 50.0

    # Funding guard
    funding_threshold: float = 0.0
    funding_ma_period: int = 3

    # EMA regime — disabled in OOS config
    use_ema_200_regime: bool = False

    # Min SL filter
    min_sl_pct: float = 0.005

    # ── Leverage controls ─────────────────────────────────────────────────────
    force_no_leverage: bool = False
    leverage: float = 0.0
    auto_leverage_by_stop: bool = True
    auto_leverage_min: float = 1.0
    auto_leverage_max: float = 20.0
    auto_leverage_sl_buffer_pct: float = 5.0
    leverage_fail_soft: bool = True

    # ── Execution controls ────────────────────────────────────────────────────
    position_idx: int = 0
    reduce_only_closes: bool = True
    order_type: str = "Limit"
    tp_as_limit: bool = True
    tp_limit_offset_ticks: int = 0
    sl_as_market: bool = True
    cancel_unfilled_limit_entry: bool = True
    cancel_unfilled_limit_entry_after_bars: int = 1
    dry_run: bool = False

    # Bear strategy is always short-only — no trail stop needed
    trail_stop: bool = False

    # ── Sizing controls ───────────────────────────────────────────────────────
    risk_per_trade_pct: float = 0.1
    fixed_order_qty: float = 0.0
    min_notional_usdt: float = 1.0


# ── Interval helpers (shared with UPS) ────────────────────────────────────────

_INTERVAL_TO_MS: dict[str, int] = {
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


def interval_to_ms(interval: str) -> int:
    return _INTERVAL_TO_MS[interval]


# ── Env-var helpers ────────────────────────────────────────────────────────────

def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def _env_str(name: str, default: str) -> str:
    raw = os.getenv(name)
    if raw is None:
        return default
    value = raw.strip()
    return value if value else default


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return float(raw.strip())
    except ValueError:
        return default


def _normalize_order_type(raw: str | None) -> str:
    value = (raw or "Limit").strip().lower()
    if value in {"market", "m"}:
        return "Market"
    if value in {"limit", "l"}:
        return "Limit"
    raise ValueError("BEAR_ORDER_TYPE must be 'Market' or 'Limit'")


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
        if not os.getenv(key):
            os.environ[key] = value


def build_config_from_env() -> BearLiveConfig:
    """Load BearLiveConfig from BEAR_* env vars with .env fallback."""
    _load_dotenv_if_present()

    api_key = os.getenv("BYBIT_API_KEY", "")
    api_secret = os.getenv("BYBIT_API_SECRET", "") or os.getenv("BYBIT_SECTRET", "")
    if not api_key or not api_secret:
        raise RuntimeError("Set BYBIT_API_KEY and BYBIT_API_SECRET")

    cfg = BearLiveConfig(api_key=api_key, api_secret=api_secret)
    cfg.profile = _env_str("BEAR_PROFILE", cfg.profile)
    cfg.category = _env_str("BEAR_CATEGORY", cfg.category)
    cfg.symbol = _env_str("BEAR_SYMBOL", cfg.symbol).upper()
    cfg.testnet = _env_bool("BEAR_TESTNET", cfg.testnet)
    cfg.use_ws_kline = _env_bool("BEAR_USE_WS_KLINE", cfg.use_ws_kline)
    cfg.dry_run = _env_bool("BEAR_DRY_RUN", cfg.dry_run)
    cfg.order_type = _normalize_order_type(os.getenv("BEAR_ORDER_TYPE"))
    cfg.risk_per_trade_pct = _env_float("BEAR_RISK_PCT", cfg.risk_per_trade_pct)
    cfg.leverage = _env_float("BEAR_LEVERAGE", cfg.leverage)
    cfg.auto_leverage_by_stop = _env_bool("BEAR_AUTO_LEVERAGE", cfg.auto_leverage_by_stop)
    return cfg
