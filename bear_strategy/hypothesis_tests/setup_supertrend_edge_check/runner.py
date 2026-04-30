"""Vectorized outcome engine for the SuperTrend Setup Edge Check.

For every bar in a population, enters a short at the bar's close and scans
forward until stop or target is resolved.

Stop   = entry + stop_mult × ATR(entry_tf, atr_period)
Target = entry − target_mult × ATR(entry_tf, atr_period)

Populations per pair:
    regime_only        — eligible regime baseline (post ST/ATR warmup)
    st_bear            — regime + SuperTrend direction = −1
    st_near_resistance — regime + ST bearish + close within proximity_atr_mult×ATR of ST line
    st_extended        — regime + ST bearish + close > proximity_atr_mult×ATR below ST line

Look-ahead prevention:
    SuperTrend and ATR are computed by pandas_ta at bar t using only data
    ≤ t.  No shifting is required — bar t's signal uses only bar t and
    prior bars.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_supertrend_edge_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_supertrend_edge_check.entries import (
    build_population_masks,
    compute_supertrend,
)
from bear_strategy.strategy.parameters import Parameters
from bear_strategy.strategy.signals import compute_regime_signals

logger = logging.getLogger(__name__)

_POPULATION_ORDER = [
    "regime_only",
    "st_bear",
    "st_near_resistance",
    "st_extended",
]


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def run_test(config: TestConfig) -> pd.DataFrame:
    """Run the SuperTrend setup edge check across all configured pairs.

    Returns:
        DataFrame indexed by (pair, population) with columns:
        win_rate, profit_factor, avg_duration, n_trades.
    """
    params = Parameters(
        ema_slope_period=config.ema_slope_period,
        ema_slope_lookback=config.ema_slope_lookback,
        ema_below_periods=config.ema_below_periods,
    )

    records: list[dict] = []
    for pair in config.pairs:
        logger.info("Processing %s", pair)
        try:
            records.extend(_process_pair(pair, config, params))
        except FileNotFoundError as exc:
            logger.warning("Skipping %s — data not found: %s", pair, exc)
        except Exception as exc:
            logger.error("Error processing %s: %s", pair, exc, exc_info=True)
            raise

    if not records:
        return pd.DataFrame(
            columns=["pair", "population", "win_rate", "profit_factor", "avg_duration", "n_trades"]
        )

    return pd.DataFrame(records).set_index(["pair", "population"])


# ---------------------------------------------------------------------------
# Per-pair processing
# ---------------------------------------------------------------------------


def _process_pair(
    pair: str,
    config: TestConfig,
    params: Parameters,
) -> list[dict]:
    df = _load_parquet(config.data_dir, pair, config.entry_tf, config.start_date, config.end_date)
    df_daily = _load_parquet(config.data_dir, pair, "1d", config.start_date, config.end_date)

    df = _standardise_ohlcv(df)
    df_daily = _standardise_ohlcv(df_daily)

    # Regime signals mapped from daily onto entry_tf bars.
    regime = compute_regime_signals(df, df_daily, params)
    df = df.copy()
    for col, series in regime.items():
        df[col] = series.values

    # Entry-TF ATR for stop/target sizing and proximity threshold.
    df["atr"] = _atr(df, config.atr_period).values

    # SuperTrend via pandas_ta — all four columns attached at once.
    st_df = compute_supertrend(df, config)
    for col in st_df.columns:
        df[col] = st_df[col].values

    masks = build_population_masks(df, config)

    records = []
    for pop_name in _POPULATION_ORDER:
        mask = masks[pop_name]
        result = _compute_outcomes(df, mask, config)
        records.append({"pair": pair, "population": pop_name, **result})
        logger.debug(
            "%s | %-20s | trades=%d  win=%.1f%%  PF=%.2f  dur=%.1f bars",
            pair,
            pop_name,
            result["n_trades"],
            result["win_rate"] * 100 if not np.isnan(result["win_rate"]) else float("nan"),
            result["profit_factor"],
            result["avg_duration"],
        )

    return records


# ---------------------------------------------------------------------------
# Outcome engine (identical forward-scan logic used across all steps)
# ---------------------------------------------------------------------------


def _compute_outcomes(
    df: pd.DataFrame,
    entry_mask: pd.Series,
    config: TestConfig,
) -> dict:
    """Forward-scan every entry bar in the mask.

    Enters a short at each bar's close.  Scans forward bar by bar until
    the high ≥ stop (loss) or the low ≤ target (win).  Ties on the same
    bar are resolved as a loss (conservative).  Unresolved trades are
    excluded from statistics.

    Returns dict with win_rate, profit_factor, avg_duration, n_trades.
    """
    closes = df["Close"].to_numpy(dtype=float)
    highs = df["High"].to_numpy(dtype=float)
    lows = df["Low"].to_numpy(dtype=float)
    atrs = df["atr"].to_numpy(dtype=float)
    mask_arr = entry_mask.to_numpy(dtype=bool)

    entry_indices = np.where(mask_arr)[0]
    wins: list[float] = []
    losses: list[float] = []
    durations: list[int] = []

    for idx in entry_indices:
        if np.isnan(atrs[idx]) or atrs[idx] == 0:
            continue
        entry_price = closes[idx]
        stop = entry_price + config.stop_atr_mult * atrs[idx]
        target = entry_price - config.target_atr_mult * atrs[idx]

        resolved = False
        for fwd in range(1, len(closes) - idx):
            bar = idx + fwd
            if highs[bar] >= stop:
                losses.append(config.stop_atr_mult)
                durations.append(fwd)
                resolved = True
                break
            if lows[bar] <= target:
                wins.append(config.target_atr_mult)
                durations.append(fwd)
                resolved = True
                break

        if not resolved:
            continue

    n_wins = len(wins)
    n_losses = len(losses)
    n_trades = n_wins + n_losses

    if n_trades == 0:
        return {
            "win_rate": float("nan"),
            "profit_factor": float("nan"),
            "avg_duration": float("nan"),
            "n_trades": 0,
        }

    win_rate = n_wins / n_trades
    profit_factor = sum(wins) / sum(losses) if losses else float("inf")
    avg_duration = sum(durations) / len(durations)

    return {
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "avg_duration": avg_duration,
        "n_trades": n_trades,
    }


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------


def _load_parquet(
    data_dir: Path,
    symbol: str,
    timeframe: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    symbol_dir = data_dir / symbol
    if not symbol_dir.exists():
        raise FileNotFoundError(f"No data directory for {symbol}: {symbol_dir}")

    exact = symbol_dir / f"{symbol}_{timeframe}_start_{start_date}_end_{end_date}.parquet"
    if exact.exists():
        return pd.read_parquet(exact)

    candidates = sorted(symbol_dir.glob(f"{symbol}_{timeframe}_*.parquet"))
    if not candidates:
        raise FileNotFoundError(
            f"No parquet file for {symbol}/{timeframe} in {symbol_dir}."
        )

    path = candidates[0]
    logger.debug("Exact file not found; using %s", path.name)
    return pd.read_parquet(path)


def _standardise_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "open": "Open", "high": "High", "low": "Low",
        "close": "Close", "volume": "Volume",
        "Open time": "timestamp", "open_time": "timestamp",
    }
    df = df.rename(columns=rename_map)
    if not isinstance(df.index, pd.DatetimeIndex):
        for col in ("timestamp", "date", "Datetime"):
            if col in df.columns:
                df = df.set_index(pd.to_datetime(df[col])).drop(columns=[col], errors="ignore")
                break
    return df.sort_index()


def _atr(df: pd.DataFrame, period: int) -> pd.Series:
    """ATR using EWM smoothing (consistent with all other steps)."""
    high = df["High"]
    low = df["Low"]
    prev_close = df["Close"].shift(1)
    tr = pd.concat(
        [high - low, (high - prev_close).abs(), (low - prev_close).abs()],
        axis=1,
    ).max(axis=1)
    return tr.ewm(span=period, adjust=False).mean()
