"""
Regime phase configuration.

IDEAS are split by indicator family — edit the relevant file:
  indicators/rsi/config.py          ← RSI-based regime ideas
  indicators/ema/config.py          ← EMA slope / price-vs-EMA ideas
  indicators/funding_rate/config.py ← Funding rate ideas
  indicators/supertrend/config.py   ← Supertrend ideas
  indicators/misc/config.py         ← Bollinger Bands, SAR

How to promote to setup phase
------------------------------
1. Change "decision" to "PROMOTED" in the winning idea (in its indicator config).
2. Copy the indicator_module + params + context_tf (if any) to setup/config.py BASELINE.
3. The setup phase will compare new ideas against regime-filtered bars.
"""

from bear_strategy.hypothesis_test_v2.config import SHARED  # noqa: F401
from bear_strategy.hypothesis_test_v2.regime.indicators.ema.config import IDEAS as _EMA_IDEAS
from bear_strategy.hypothesis_test_v2.regime.indicators.funding_rate.config import IDEAS as _FUNDING_IDEAS
from bear_strategy.hypothesis_test_v2.regime.indicators.misc.config import IDEAS as _MISC_IDEAS
from bear_strategy.hypothesis_test_v2.regime.indicators.rsi.config import IDEAS as _RSI_IDEAS
from bear_strategy.hypothesis_test_v2.regime.indicators.supertrend.config import IDEAS as _SUPERTREND_IDEAS
from bear_strategy.hypothesis_test_v2.regime.indicators.combinations.config import IDEAS as _COMBINATIONS_IDEAS

# ── Verdict thresholds for this phase ────────────────────────────────────────
# ── Pairs under test for this phase ─────────────────────────────────────────
# Edit this list to narrow or expand the universe for the regime phase.
PAIRS: list[str] = [
    "AAVEUSDT",
    "ADAUSDT",
    "ALGOUSDT",
    "ATOMUSDT",
    "AVAXUSDT",
    "BATUSDT",
    "BCHUSDT",
    "BNBUSDT",
    "BTCUSDT",
    "DOGEUSDT",
    "DOTUSDT",
    "ETHUSDT",
    "HYPEUSDT",
    "LINKUSDT",
    "LTCUSDT",
    "NEARUSDT",
    "SOLUSDT",
    "TONUSDT",
    "TRXUSDT",
    "UNIUSDT",
    "XLMUSDT",
    "XMRUSDT",
    "XRPUSDT",
    "ZECUSDT",
]

# ── Verdict thresholds for this phase ────────────────────────────────────────
# A pair is [OK] only when ALL three gates are cleared.
# Hard floor on absolute PF > 1.0 is enforced separately inside the engine.
THRESHOLDS: dict = {
    "min_pf_lift":   0.05,   # absolute PF lift required
    "min_wr_zscore": 2.5,    # WR z-score (> 2.5 → 99 % confidence)
    "min_coverage":  0.10,   # min fraction of baseline bars that match
    "min_candidate_pf": 1.0, # absolute PF floor — filter must not lose money
}

# ── Entry timeframes for trade entries ───────────────────────────────────────
# These are the timeframes where trades are entered.
# The signal can be computed on a different (context) TF — see context_tf below.
ENTRY_TIMEFRAMES: list[str] = ["1h","4h","1d"]

# ── Baseline: all bars (unrestricted random-entry population) ─────────────────
BASELINE: dict = {
    "type":  "all_candles",
    "label": "all_candles",
}

# ── Ideas — assembled from per-indicator configs ──────────────────────────────
# To add/enable/disable ideas for a specific indicator family, edit its config:
#   indicators/rsi/config.py
#   indicators/ema/config.py
#   indicators/funding_rate/config.py
#   indicators/supertrend/config.py
#   indicators/misc/config.py
IDEAS: list[dict] = [
    # *_RSI_IDEAS,
    *_COMBINATIONS_IDEAS,
    # *_EMA_IDEAS,
    # *_FUNDING_IDEAS,
    # *_SUPERTREND_IDEAS,
    # *_MISC_IDEAS,
    # {
    #     "name":             "funding_bear_positive_raw",
    #     "enabled":          True,
    #     "decision":         "PENDING",
    #     "indicator_module": "bear_strategy.hypothesis_test_v2.regime.indicators.funding_rate",
    #     "params":           {"threshold": 0.0, "ma_period": 1},
    # },
]
