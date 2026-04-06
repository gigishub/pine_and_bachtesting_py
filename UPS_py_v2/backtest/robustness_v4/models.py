from __future__ import annotations

# Standardized column names shared across every V4 output file.
# Defined once here so pipeline, reporter, and Streamlit never drift out of sync.
# Add new metric keys here first, then handle them in pipeline._build_row().

# Columns that identify a single result row (who ran it, what setup, what rank).
IDENTITY_COLUMNS: tuple[str, ...] = (
    "Symbol",       # e.g. "BTCUSDT"
    "Timeframe",    # e.g. "1h"
    "Condition",    # file-safe label, e.g. "BTC_1H" — used for CSV filenames and Streamlit
    "Rank",         # 1 = best for this condition; assigned after sorting
    "Parameter Signature",  # pipe-separated key=value string; used as a cross-condition join key
)

# Performance metrics captured per backtest run.
# These are the columns aggregated into Mean/Std in the robustness summary.
METRIC_COLUMNS: tuple[str, ...] = (
    "Return [%]",       # total return over the test period
    "Expectancy [%]",   # average edge per trade — primary ranking signal
    "Profit Factor",    # gross profit / gross loss; NaN when no losing trades
    "Win Rate [%]",     # % of trades that were winners
    "Max Drawdown [%]", # worst peak-to-trough decline
    "# Trades",         # total trades taken; low count = statistically weak result
    "SQN",              # System Quality Number: >2 good, >3 excellent
)

# Extra columns added only in ROBUSTNESS_SUMMARY.csv (not in per-condition CSVs).
# Low Std = stable across conditions = less likely a lucky shot.
SUMMARY_EXTRA_COLUMNS: tuple[str, ...] = (
    "Consistency Score",    # count of conditions where this setup was in top N
    "Consistency [%]",      # consistency_score / total_conditions * 100
    "Expectancy Mean",      # mean expectancy across all conditions
    "Expectancy Std",       # std of expectancy — high = inconsistent
    "Return Mean",
    "Return Std",
    "Profit Factor Mean",
    "Max Drawdown Mean",
    "Conditions Appeared In",  # comma-separated list of top-N appearances
)
