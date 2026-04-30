"""Shared experiment configuration for hypothesis Steps 1-3.

**Edit this file to run all three steps with the same TF and exit settings.**

Each step's run.py reads this config and passes the relevant fields into
its own TestConfig.  Step-specific settings (VPVR window, volume window,
regime EMA periods, etc.) remain in each step's config.py.

──────────────────────────────────────────────────────────────────────
Timeframe combinations for bear shorts
──────────────────────────────────────────────────────────────────────

  entry_tf  context_tf  Trade style    Typical hold    Notes
  ─────── ──────────── ────────────── ─────────────── ─────────────────────
  "15m"   "4h"         Intraday scalp  15 min – 4 h   High noise; large n
  "1h"    "4h"         Swing short     4 h  – 2 days  ← recommended start
  "4h"    "1d"         Position short  2 days – 2 wk  Low n, slow feedback

• regime_tf is always "1d" — the regime filter reads daily closes.
  Do not change it.

• context_tf must be coarser than entry_tf.
  Only used by Step 2 (VPVR / Anchored VWAP / context ATR).

• Changing entry_tf changes bar count, ATR magnitude, and trade count.
  Smaller TF → more trades, smaller ATR per bar, shorter average hold.
  Larger TF → fewer trades, larger ATR per bar, longer average hold.

──────────────────────────────────────────────────────────────────────
Stop / target sizing
──────────────────────────────────────────────────────────────────────

  stop    = entry_price + stop_atr_mult  × ATR(entry_tf)
  target  = entry_price − target_atr_mult × ATR(entry_tf)

  Default 2× stop / 3× target gives a 1.5 R:R ratio.
  For intraday scalps consider 1.5× stop / 2× target.
  For position trades consider 2.5× stop / 4× target.

──────────────────────────────────────────────────────────────────────
Required parquet files
──────────────────────────────────────────────────────────────────────
  crypto_data/data/{PAIR}/{PAIR}_{entry_tf}_*.parquet   (Steps 1-3)
  crypto_data/data/{PAIR}/{PAIR}_{context_tf}_*.parquet (Step 2 only)
  crypto_data/data/{PAIR}/{PAIR}_{regime_tf}_*.parquet  (all steps)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExperimentConfig:
    # ------------------------------------------------------------------
    # ⬇  Edit these fields to sweep timeframes and exit sizing
    # ------------------------------------------------------------------

    # Candle resolution for entries, ATR, stops, and targets (Steps 1-3)
    entry_tf: str = "1h"

    # Higher-TF for VPVR, Anchored VWAP, and context ATR (Step 2 only)
    # Must be coarser than entry_tf.
    #   entry_tf "15m" or "1h"  →  context_tf "4h"
    #   entry_tf "4h"           →  context_tf "1d"
    context_tf: str = "4h"

    # Stop distance: entry + stop_atr_mult × ATR(entry_tf)
    stop_atr_mult: float = 2.0

    # Target distance: entry − target_atr_mult × ATR(entry_tf)
    target_atr_mult: float = 3.0

    # ATR lookback period (applied on entry_tf bars)
    atr_period: int = 7

    # ------------------------------------------------------------------
    # ⬇  Do not change — regime is always computed on daily closes
    # ------------------------------------------------------------------
    regime_tf: str = "1d"
