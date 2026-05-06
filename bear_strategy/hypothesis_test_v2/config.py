"""
Shared global configuration for all hypothesis-testing phases.

This file is the single source of truth for:
  - Which pairs to test
  - The date window (start / end)
  - Exit parameters (ATR stop/target multipliers, ATR period)
  - Data directory location

Every phase (regime, setup, trigger) imports SHARED and extends it
with phase-specific settings in its own config.py.
"""

SHARED: dict = {
    # ── Pairs ────────────────────────────────────────────────────────────
    "pairs": ["BTCUSDT", "ETHUSDT", "SOLUSDT","BNBUSDT","XRPUSDT"],

    # ── Date window ──────────────────────────────────────────────────────
    # ISO-8601 date strings; both ends inclusive.
    "start": "2021-01-01",
    "end":   "2025-11-01",

    # ── ATR-based exit parameters ─────────────────────────────────────────
    # Shorts: stop is above entry, target is below entry.
    "stop_atr_mult":   2.0,
    "target_atr_mult": 3.0,
    "atr_period":      7,

    # ── File system ───────────────────────────────────────────────────────
    "data_dir": "crypto_data/data",
}
