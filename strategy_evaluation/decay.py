"""Short-period vs long-period performance decay detection."""

from __future__ import annotations

import pandas as pd

from strategy_evaluation.config import RobustnessConfig


def compare_runs(
    short_df: pd.DataFrame,
    long_df: pd.DataFrame,
    cfg: RobustnessConfig,
) -> pd.DataFrame:
    """Compare the top-ranked combo per (symbol, timeframe) across two runs.

    For each (Symbol, Timeframe) pair present in both DataFrames, finds the
    rank-1 combo (matching by Parameter Signature where possible) and computes
    the metric deltas between the long-period and short-period runs.

    Positive delta = improvement over the longer period.
    Negative delta = decay.

    Returns
    -------
    pd.DataFrame with columns:
        Symbol, Timeframe, Parameter Signature,
        SQN_short, SQN_long, SQN_delta, SQN_decay_flag,
        Return_short, Return_long, Return_delta, Return_decay_flag,
        decayed  ← True if either SQN or Return decayed beyond threshold
    """
    key = [cfg.col_symbol, cfg.col_timeframe]

    def top1(df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.sort_values(cfg.col_rank)
            .groupby(key, as_index=False)
            .first()
        )

    short_top = top1(short_df)
    long_top = top1(long_df)

    merged = pd.merge(
        short_top[key + [cfg.col_param_sig, cfg.col_sqn, cfg.col_return]].rename(
            columns={cfg.col_sqn: "SQN_short", cfg.col_return: "Return_short"}
        ),
        long_top[key + [cfg.col_param_sig, cfg.col_sqn, cfg.col_return]].rename(
            columns={
                cfg.col_param_sig: f"{cfg.col_param_sig}_long",
                cfg.col_sqn: "SQN_long",
                cfg.col_return: "Return_long",
            }
        ),
        on=key,
        how="inner",
    )

    merged["SQN_delta"] = merged["SQN_long"] - merged["SQN_short"]
    merged["Return_delta"] = merged["Return_long"] - merged["Return_short"]

    # Decay flag: performance drops by more than decay_threshold fraction
    def _decay(short_val: float, long_val: float, threshold: float) -> bool:
        if pd.isna(short_val) or pd.isna(long_val) or short_val == 0:
            return False
        drop = (short_val - long_val) / abs(short_val)
        return drop > threshold

    merged["SQN_decay_flag"] = [
        _decay(s, l, cfg.decay_threshold)
        for s, l in zip(merged["SQN_short"], merged["SQN_long"])
    ]
    merged["Return_decay_flag"] = [
        _decay(s, l, cfg.decay_threshold)
        for s, l in zip(merged["Return_short"], merged["Return_long"])
    ]
    merged["decayed"] = merged["SQN_decay_flag"] | merged["Return_decay_flag"]

    return merged.sort_values([cfg.col_symbol, cfg.col_timeframe]).reset_index(drop=True)
