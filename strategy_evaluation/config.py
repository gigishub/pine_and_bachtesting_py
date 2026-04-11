"""Robustness configuration — thresholds and scoring weights.

All thresholds are the *minimum acceptable* values for a combo to be counted
as "passing".  Override via a YAML file or directly in code.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RobustnessConfig:
    # ── Per-combo pass/fail thresholds ─────────────────────────────────────
    min_sqn: float = 1.0
    min_profit_factor: float = 1.5
    min_trades: int = 10
    min_win_rate: float = 30.0   # percent
    min_sharpe: float = 0.5

    # ── Decay detection ────────────────────────────────────────────────────
    # Flag a symbol/TF if SQN or Return drops by more than this fraction
    # when comparing the short-period run to the long-period run.
    decay_threshold: float = 0.30  # 30 %

    # ── Verdict thresholds ─────────────────────────────────────────────────
    robust_symbol_rate: float = 0.60   # ≥ 60 % of symbols must pass
    robust_tf_rate: float = 0.60       # ≥ 60 % of timeframes must pass
    robust_avg_sqn: float = 1.0

    weak_symbol_rate: float = 0.40     # < 40 % → WEAK
    weak_avg_sqn: float = 0.5

    # ── Scoring weights (must sum to 1.0) ──────────────────────────────────
    weights: dict[str, float] = field(default_factory=lambda: {
        "sqn": 0.30,
        "profit_factor": 0.25,
        "sharpe": 0.20,
        "win_rate": 0.15,
        "trades": 0.10,
    })

    # ── Column name mapping (VBT schema) ───────────────────────────────────
    col_sqn: str = "SQN"
    col_pf: str = "Profit Factor"
    col_trades: str = "# Trades"
    col_win_rate: str = "Win Rate [%]"
    col_sharpe: str = "Sharpe Ratio"
    col_return: str = "Return [%]"
    col_symbol: str = "Symbol"
    col_timeframe: str = "Timeframe"
    col_param_sig: str = "Parameter Signature"
    col_rank: str = "Rank"
