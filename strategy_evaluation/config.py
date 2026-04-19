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
    min_trades: int = 30
    min_win_rate: float = 30.0   # percent
    min_sharpe: float = 0.5
    # Max drawdown gate — only applied when the column is present in the data.
    max_max_drawdown: float = 20.0   # percent
    # Fraction of combos per symbol/TF that must pass before the symbol/TF is
    # counted as "passing" in consistency analysis.  0.0 = any single combo
    # passing is enough (old behaviour); 1.0 = every combo must pass.
    min_combo_pass_rate: float = 0.20

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
    # win_rate and trades are pass/fail gates only — not in the composite score.
    weights: dict[str, float] = field(default_factory=lambda: {
        "sqn":            0.28,
        "profit_factor":  0.22,
        "expectancy":     0.18,
        "sharpe":         0.15,
        "max_drawdown":   0.12,  # inverted: lower DD scores higher
        "calmar":         0.05,
    })

    # ── Column name mapping (VBT schema) ───────────────────────────────────
    col_sqn: str = "SQN"
    col_pf: str = "Profit Factor"
    col_trades: str = "# Trades"
    col_win_rate: str = "Win Rate [%]"
    col_sharpe: str = "Sharpe Ratio"
    col_return: str = "Return [%]"
    col_max_drawdown: str = "Max Drawdown [%]"
    col_expectancy: str = "Expectancy"
    col_calmar: str = "Calmar Ratio"
    col_symbol: str = "Symbol"
    col_timeframe: str = "Timeframe"
    col_param_sig: str = "Parameter Signature"
    col_rank: str = "Rank"
