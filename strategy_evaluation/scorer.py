"""Aggregate analysis results into a single robustness verdict."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from strategy_evaluation.config import RobustnessConfig

_log = logging.getLogger(__name__)


@dataclass
class RobustnessResult:
    verdict: str                          # "ROBUST" | "MARGINAL" | "WEAK"
    symbol_pass_rates: dict[str, float]   # symbol → 0.0 or 1.0
    tf_pass_rates: dict[str, float]       # timeframe → 0.0–1.0
    toggle_frequency: dict[str, int]      # toggle → count in top combos
    symbol_rate: float                    # fraction of symbols that pass
    tf_rate: float                        # fraction of TFs that pass
    notes: list[str] = field(default_factory=list)


def aggregate_verdict(
    symbol_rates: dict[str, float],
    tf_rates: dict[str, float],
    toggle_freq: dict[str, int],
    cfg: RobustnessConfig,
) -> RobustnessResult:
    """Combine symbol/TF pass rates into a RobustnessResult with a verdict."""
    symbol_rate = sum(symbol_rates.values()) / len(symbol_rates) if symbol_rates else 0.0
    tf_rate = sum(tf_rates.values()) / len(tf_rates) if tf_rates else 0.0

    notes: list[str] = []

    is_weak = symbol_rate < cfg.weak_symbol_rate
    is_robust = (
        symbol_rate >= cfg.robust_symbol_rate
        and tf_rate >= cfg.robust_tf_rate
    )

    if is_weak:
        verdict = "WEAK"
        notes.append(
            f"Symbol pass rate {symbol_rate:.0%} is below weak threshold ({cfg.weak_symbol_rate:.0%})."
        )
    elif is_robust:
        verdict = "ROBUST"
        notes.append("Strategy meets all robustness thresholds.")
    else:
        verdict = "MARGINAL"
        if symbol_rate < cfg.robust_symbol_rate:
            notes.append(
                f"Symbol pass rate {symbol_rate:.0%} below robust threshold ({cfg.robust_symbol_rate:.0%})."
            )
        if tf_rate < cfg.robust_tf_rate:
            notes.append(
                f"Timeframe pass rate {tf_rate:.0%} below robust threshold ({cfg.robust_tf_rate:.0%})."
            )

    return RobustnessResult(
        verdict=verdict,
        symbol_pass_rates=symbol_rates,
        tf_pass_rates=tf_rates,
        toggle_frequency=toggle_freq,
        symbol_rate=symbol_rate,
        tf_rate=tf_rate,
        notes=notes,
    )
