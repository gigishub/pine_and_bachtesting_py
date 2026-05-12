"""VBT signal adapter for the Bear Strategy.

ARCHITECTURE
------------
                 ┌──────────────────────────────────────┐
                 │  strategy/signals.py                 │
                 │  compute_entry_signal()              │  ← shared with backtesting.py
                 └──────────────┬───────────────────────┘
                                │
                                ▼
                 ┌──────────────────────────────────────┐
                 │  vectorbt/signals.py  ← YOU ARE HERE │
                 │  build_vbt_arrays()                  │  converts to VBT format
                 └──────────────┬───────────────────────┘
                                │
                                ▼
                 ┌──────────────────────────────────────┐
                 │  vectorbt/runner.py                  │
                 │  run() → vbt.Portfolio               │
                 └──────────────────────────────────────┘

FILL MODEL
----------
entry_signal fires at bar N (computed from close[N]).
fill_at_next_open=True shifts arrays +1 so VBT fills at open[N+1].
sl_stop / tp_stop are also shifted so the ATR from signal bar N
governs the exit levels (consistent with the backtesting.py engine).

EXIT MODEL
----------
VBT sl_stop / tp_stop are fractions relative to the actual fill price:
  sl_stop[i] = stop_atr_mult  × ATR[i] / close[i]   → SHORT exits when price RISES by this fraction
  tp_stop[i] = target_atr_mult × ATR[i] / close[i]  → SHORT exits when price FALLS by this fraction

MIN SL DISTANCE FILTER
-----------------------
Signals where sl_pct < params.min_sl_pct are masked out before shifting.
This prevents entries where round-trip taker fees dominate the risk premium.
Example: at 0.08% round-trip and min_sl_pct=0.5%, fees are at most 16% of R.

SIZING
------
  size_frac = risk_pct / sl_pct     (both dimensionless fractions)
Clipped to [0, 0.9999] so the position never exceeds available equity.
size_type="percent" in from_signals() interprets this as a fraction of cash.

LOOKAHEAD AUDIT (all exits)
----------------------------
All indicator exits fire at bar N using data known by the END of bar N.
fill_at_next_open=True then shifts every signal array +1, so execution
always happens at open[N+1] — the earliest fill with no future knowledge.

  exit_mode                data source          cross detection at bar N     execute
  ──────────────────────── ──────────────────── ──────────────────────────── ───────
  fixed_tp                 ATR at signal bar    VBT internal stop            open[N+1]
  rsi_cross_up             daily RSI close[N]  align_htf shift=True +       open[N+1]
                                                fill_at_next_open shift
  fixed_tp_or_rsi_cross_up same as above        same                         open[N+1]
  macd_hist_cross_zero     1h close[N]          hist.shift(1)<0 & hist>=0    open[N+1]
  rsi_oversold             1h close[N]          rsi.shift(1)>=L & rsi<L      open[N+1]
  ema_reclaim              1h close[N]          close.shift(1)<ema.shift(1)  open[N+1]
                                                & close>=ema
  funding_regime_shift     8h settlements       settled.shift(1)>thr &       open[N+1]
                           ffill→EMA smoothed   settled<=thr
                           settled=smoothed.    (settled = smoothed.shift(1)
                           shift(1)             matches the entry guard —
                                                uses smoothed[N-2],
                                                smoothed[N-1] only)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_test_v2.engine.alignment import align_htf_to_ltf
from bear_strategy.strategy.parameters import Parameters
from bear_strategy.strategy.signals import compute_atr, compute_entry_signal


# ─────────────────────────────────────────────────────────────────────────────
# Indicator helpers — pure functions, no I/O, no lookahead
# ─────────────────────────────────────────────────────────────────────────────

def _compute_rsi(close: pd.Series, period: int) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def _compute_macd_histogram(
    close: pd.Series, fast: int, slow: int, signal: int
) -> pd.Series:
    """MACD histogram = (fast EMA − slow EMA) − signal EMA of that difference.

    All EMAs use only close[0..N] at bar N — no lookahead.
    """
    ema_fast    = close.ewm(span=fast,   adjust=False).mean()
    ema_slow    = close.ewm(span=slow,   adjust=False).mean()
    macd_line   = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line - signal_line


def _compute_ema(close: pd.Series, period: int) -> pd.Series:
    return close.ewm(span=period, adjust=False).mean()


def _smoothed_funding(
    funding_df: pd.DataFrame,
    target_index: pd.DatetimeIndex,
    ma_period: int,
) -> pd.Series:
    """Align 8h funding settlements to *target_index* and apply EMA smoothing.

    Returns the smoothed series WITHOUT any shift — identical to the internal
    series inside ``compute_funding_bull_guard`` before its ``shift(1)`` call.
    The caller is responsible for applying the correct shift for their use case.
    """
    rate = funding_df["fundingrate"].copy()
    fund_idx = pd.to_datetime(rate.index)
    fund_idx = (
        fund_idx.tz_localize("UTC") if fund_idx.tz is None else fund_idx.tz_convert("UTC")
    )
    rate.index = fund_idx

    tgt_utc = (
        target_index.tz_localize("UTC")
        if target_index.tz is None
        else target_index.tz_convert("UTC")
    )
    combined = rate.reindex(rate.index.union(tgt_utc)).ffill()
    result = combined.reindex(tgt_utc)
    result.index = target_index

    if ma_period > 1:
        result = result.ewm(span=ma_period, adjust=False).mean()
    return result


def _apply_entry_throttle(signal: pd.Series, every_n: int, phase: int) -> pd.Series:
    if every_n <= 1:
        return signal.fillna(False).astype(bool)
    if phase < 1 or phase > every_n:
        phase = 1

    sig = signal.fillna(False).astype(bool)
    hit_count = sig.cumsum()
    keep = sig & (((hit_count - phase) % every_n) == 0)
    return keep.astype(bool)


# ─────────────────────────────────────────────────────────────────────────────
# Main signal builder
# ─────────────────────────────────────────────────────────────────────────────

def build_vbt_arrays(
    df_1h: pd.DataFrame,
    df_1d: pd.DataFrame,
    funding_df: pd.DataFrame,
    params: Parameters,
    fill_at_next_open: bool = True,
) -> dict[str, pd.Series]:
    """Compute all arrays needed for vbt.Portfolio.from_signals().

    Args:
        df_1h:             1h OHLCV DataFrame (entry timeframe), lowercase columns.
        df_1d:             1d OHLCV DataFrame (regime timeframe), lowercase columns.
        funding_df:        Funding rate DataFrame with 'fundingrate' column.
        params:            Strategy parameters.
        fill_at_next_open: When True (default) shift arrays +1 bar so VBT fills
                           at the open of the bar after the signal.

    Returns:
        Dict with keys:
          short_entries — bool Series (entry bars)
          short_exits   — bool Series (indicator-based exits)
          sl_stop       — float Series (SL fraction relative to fill price)
          tp_stop       — float Series (TP fraction relative to fill price)
          short_size    — float Series (position size fraction of equity)
    """
    idx   = df_1h.index
    close = df_1h["close"].astype(float)

    entry_signal = compute_entry_signal(df_1h, df_1d, funding_df, params)
    atr          = compute_atr(df_1h, params.atr_period)

    # SL / TP as fractions of current close price
    safe_close = close.where(close > 0, np.nan)
    sl_pct = (params.stop_atr_mult  * atr / safe_close).fillna(0.0)
    tp_pct = (params.target_atr_mult * atr / safe_close).fillna(0.0)

    # Min-SL filter: skip when stop distance is too small vs price
    # (prevents trades dominated by taker fees)
    min_sl_mask = sl_pct >= params.min_sl_pct
    warmup_mask = atr.notna()

    short_entries = (entry_signal & warmup_mask & min_sl_mask).astype(bool)
    short_entries = _apply_entry_throttle(
        short_entries,
        every_n=max(int(params.entry_every_n), 1),
        phase=max(int(params.entry_phase), 1),
    )

    exit_mode = str(params.exit_mode).strip().lower()

    # ── Daily RSI cross-up (computed once, reused by two modes) ──────────────
    # All lookahead prevention happens inside align_htf_to_ltf(shift=True):
    #   1. cross fires on daily bar N using daily close[N] (known at day close)
    #   2. shift=True maps it to the 1h bar AFTER the daily bar closes
    #   3. fill_at_next_open adds another +1 → execute at open of the bar after that
    exit_rsi_1d = _compute_rsi(
        df_1d["close"].astype(float), max(int(params.exit_rsi_period), 2)
    )
    rsi_cross_up_1d = (
        (exit_rsi_1d.shift(1) <= float(params.exit_rsi_level))
        & (exit_rsi_1d > float(params.exit_rsi_level))
    )
    rsi_cross_up = align_htf_to_ltf(
        df_1d, rsi_cross_up_1d.fillna(False), df_1h, shift=True
    )

    # ── Exit routing ──────────────────────────────────────────────────────────
    if exit_mode in ("rsi_cross_up",):
        # Indicator-only exit: disable fixed TP so the SL is the only hard stop
        short_exits = rsi_cross_up.fillna(False)
        tp_pct      = pd.Series(0.0, index=idx, dtype=float)

    elif exit_mode == "fixed_tp_or_rsi_cross_up":
        # Whichever fires first: VBT TP stop OR the RSI cross signal
        short_exits = rsi_cross_up.fillna(False)

    elif exit_mode == "macd_hist_cross_zero":
        # Exit when 1h MACD histogram crosses from negative to ≥ 0.
        # Bearish momentum fading → close the short early.
        #
        # Lookahead check:
        #   hist[N]   = f(close[0..N])  — known at end of bar N ✓
        #   cross uses hist.shift(1) (bar N-1) and hist (bar N) ✓
        hist = _compute_macd_histogram(
            close,
            fast=int(params.macd_fast_period),
            slow=int(params.macd_slow_period),
            signal=int(params.macd_signal_period),
        )
        short_exits = (hist.shift(1) < 0) & (hist >= 0)
        short_exits = short_exits.fillna(False)
        tp_pct      = pd.Series(0.0, index=idx, dtype=float)

    elif exit_mode == "rsi_oversold":
        # Exit when 1h RSI drops below rsi_oversold_level.
        # Move exhausted on the short side → take profit before bounce.
        #
        # Lookahead check:
        #   rsi_1h[N] = f(close[0..N]) — known at end of bar N ✓
        #   cross uses rsi.shift(1) and rsi — both past/current bar ✓
        rsi_1h = _compute_rsi(close, max(int(params.exit_rsi_period), 2))
        oversold = float(params.rsi_oversold_level)
        short_exits = (rsi_1h.shift(1) >= oversold) & (rsi_1h < oversold)
        short_exits = short_exits.fillna(False)
        tp_pct      = pd.Series(0.0, index=idx, dtype=float)

    elif exit_mode == "ema_reclaim":
        # Exit when 1h close crosses back above EMA(exit_ema_period).
        # Bearish price structure broken → exit now.
        #
        # Lookahead check:
        #   ema[N]   = f(close[0..N]) — known at end of bar N ✓
        #   cross uses close.shift(1), ema.shift(1) and close, ema — all current/past ✓
        ema = _compute_ema(close, int(params.exit_ema_period))
        short_exits = (close.shift(1) < ema.shift(1)) & (close >= ema)
        short_exits = short_exits.fillna(False)
        tp_pct      = pd.Series(0.0, index=idx, dtype=float)

    elif exit_mode == "funding_regime_shift":
        # Exit when the EMA-smoothed funding rate drops at or below
        # funding_threshold — the same regime flip that would invalidate entry.
        #
        # Lookahead check (critical — funding is external data):
        #   raw[N]      = most recently *settled* 8h rate at or before ts_N (ffill).
        #                 This is always a past settlement — no lookahead ✓
        #   smoothed[N] = EMA(raw[0..N])  — uses only past/current raw values ✓
        #   settled[N]  = smoothed[N-1]   — the entry guard convention (shift(1)) ✓
        #
        #   Transition detected at bar N:
        #     settled[N-1] = smoothed[N-2] > threshold  (guard was True one bar ago)
        #     settled[N]   = smoothed[N-1] <= threshold (guard just turned False)
        #   → uses smoothed[N-2] and smoothed[N-1] only — both strictly past ✓
        #
        #   fill_at_next_open then shifts +1 → execute at open[N+1] ✓
        smoothed = _smoothed_funding(funding_df, idx, int(params.funding_ma_period))
        # Replicate the entry guard's shift(1) exactly
        settled     = smoothed.shift(1)
        thr         = float(params.funding_threshold)
        short_exits = (settled.shift(1) > thr) & (settled <= thr)
        short_exits = short_exits.fillna(False)
        # Keep fixed TP active as a safety net — funding exits can be slow
        # (do NOT zero out tp_pct here)

    else:
        # fixed_tp — VBT's internal tp_stop handles exit; no signal needed
        short_exits = pd.Series(False, index=idx, dtype=bool)

    # ── Risk-based sizing: fraction of equity = risk_pct / sl_pct ─────────────
    raw_size = (
        params.risk_pct / sl_pct.replace(0.0, np.nan)
    ).clip(lower=0.0, upper=0.9999).fillna(0.0)

    # ── Shift everything +1 bar so VBT fills at the next open ─────────────────
    if fill_at_next_open:
        short_entries = short_entries.shift(1, fill_value=False)
        short_exits   = short_exits.shift(1, fill_value=False)
        sl_pct        = sl_pct.shift(1).fillna(0.0)
        tp_pct        = tp_pct.shift(1).fillna(0.0)
        raw_size      = raw_size.shift(1).fillna(0.0)

    return {
        "short_entries": pd.Series(short_entries.values, index=idx, dtype=bool),
        "short_exits":   pd.Series(short_exits.values,   index=idx, dtype=bool),
        "sl_stop":       pd.Series(sl_pct.values,        index=idx, dtype=float),
        "tp_stop":       pd.Series(tp_pct.values,        index=idx, dtype=float),
        "short_size":    pd.Series(raw_size.values,      index=idx, dtype=float),
    }
