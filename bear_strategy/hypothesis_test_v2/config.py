"""
Shared global configuration for all hypothesis-testing phases.

This file is the single source of truth for:
  - The date window (start / end)
  - Exit parameters (ATR stop/target multipliers, ATR period)
  - Data directory location

Pairs are intentionally NOT here — each phase defines its own PAIRS list
in its config.py so different stages can test different universes.

Every phase (regime, setup, trigger) imports SHARED and merges it with
phase-specific settings (including PAIRS) in its own run.py.
"""

SHARED: dict = {
    # ── Date window ──────────────────────────────────────────────────────
    # ISO-8601 date strings; both ends inclusive.
    "start": "2021-01-01",
    "end":   "2023-11-01",

    # ── ATR-based exit parameters ─────────────────────────────────────────
    # Shorts: stop is above entry, target is below entry.
    "stop_atr_mult":   2.0,
    "target_atr_mult": 3,
    "atr_period":      7,

    # ── File system ───────────────────────────────────────────────────────
    "data_dir": "crypto_data/data",
}
