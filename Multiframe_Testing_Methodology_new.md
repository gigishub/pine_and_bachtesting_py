# Multiframe Testing Methodology

**Purpose:** Define a streamlined, auditable workflow for regime, setup, and trigger testing.

---

## What This Fixes

Current pain points:
- Too many one-off folders and markdown files.
- Hard to add or remove an idea quickly.
- Promotion decisions live in memory, not in a system.
- Results are hard to compare across layers.

This document defines one simple operating model:
1. Keep one phase config as the source of truth.
2. Toggle ideas on/off inside that config.
3. Run a batch for the phase.
4. Save every idea result to one phase comparison file.
5. Flag ideas automatically, then manually approve promotion.

---

## Core Concept

**Regime** is still a gate computed on a context timeframe and applied to entry timeframe bars.

| **Timeframe** | **Purpose** | **Example** | **Notes** |
|---|---|---|---|
| **Context TF** | Where regime gate is computed | 4h | Slower, smoother; determines allowed market context |
| **Entry TF** | Where trades happen | 15m | Faster; where setup and trigger are evaluated |

---

## New Workflow (Single-Control Pattern)

For each phase, maintain one control config with:
- shared settings (pairs, dates, risk, baseline)
- candidate ideas list
- per-idea enabled flag
- per-idea params

### Example Phase Control Shape

```python
PHASE = "setup"

BASELINE = {
    "regime_tf": "1d",
    "regime_rule": "close_below_ema_50",
    "entry_tfs": ["15m", "1h"],
    "start": "2021-01-01",
    "end": "2025-11-01",
}

IDEAS = [
    {
        "idea_id":           "setup_kde_upper",
        "enabled":           True,
        "indicator_module":  "bear_strategy.hypothesis_tests.indicators.setup.kde_upper",
        "short_description": "Price in upper KDE population (4h)",
        "params":            {"kde_tf": "4h", "kde_window": 200, "kde_bandwidth_mult": 1.0},
        "decision":          "testing",   # testing | promoted | rejected
        "decision_reason":   "",
        "last_test_batch":   "batch_2025_01",
        "last_tested_at":    "2025-01-15",
    },
    {
        "idea_id":           "setup_kde_upper_rsi_ma",
        "enabled":           True,
        "indicator_module":  "bear_strategy.hypothesis_tests.indicators.setup.kde_rsi_ma",
        "short_description": "KDE upper AND RSI-MA held below 50",
        "params":            {"kde_tf": "4h", "kde_window": 200, "rsi_ma_period": 5, "rsi_ma_threshold": 50},
        "decision":          "testing",
        "decision_reason":   "",
        "last_test_batch":   "batch_2025_01",
        "last_tested_at":    "2025-01-15",
    },
    {
        "idea_id":           "setup_rvol_breakdown",
        "enabled":           False,
        "indicator_module":  "bear_strategy.hypothesis_tests.indicators.setup.rvol_breakdown",
        "short_description": "Relative volume spike on breakdown bar",
        "params":            {"rvol_period": 20, "rvol_threshold": 1.5},
        "decision":          "rejected",
        "decision_reason":   "coverage 3% — too sparse to measure edge",
        "last_test_batch":   "batch_2024_12",
        "last_tested_at":    "2024-12-10",
    },
]
```

**Decision field — three states only:**

| `decision`  | Meaning |
|-------------|----------|
| `testing`   | Active candidate; results pending review |
| `promoted`  | Passed review; carried forward to next phase |
| `rejected`  | Failed; archived with reason — do not re-enable without new hypothesis |

### Add or Remove an Idea

- Add: append one idea block to the list.
- Remove temporarily: set `enabled=False`.
- Remove permanently: delete the idea block.
- Re-run only a subset: keep enabled only for ideas you want this batch.

No new folder is required for each small idea change.

---

## Tracking System (No More Memory-Based Promotion)

Use four artifacts per phase.

### 1) Phase Comparison CSV

One row per idea × entry_tf × pair, plus aggregated rows.

Suggested file:
- `bear_strategy/hypothesis_tests/results/phase_setup_comparison.csv`

Minimum columns:
- `phase`, `batch_id`, `idea_id`, `entry_tf`, `pair`
- `population`, `baseline_pf`, `candidate_pf`, `pf_lift`
- `baseline_wr_pct`, `candidate_wr_pct`, `win_rate_lift_pp`
- `baseline_avg_duration_bars`, `candidate_avg_duration_bars`, `duration_delta_bars`
- `coverage`, `n_trades`, `decision`, `decision_reason`, `tested_at`

Notes:
- `population` lets you keep baseline and candidate populations in one table for the same pair.
- Duration is tracked as bars on the entry timeframe. Example: on `1h`, `avg_duration_bars=21` means average hold time is 21 hours.

### 2) Active Board Markdown — one per stage × entry_tf

Lists every idea currently at `decision=testing` for this stage and entry TF.
Updated after each batch run.

Naming:
```
phase_setup_entry1h_active.md
phase_setup_entry15m_active.md
phase_regime_entry1h_active.md
```

Format:
```
## Phase: Setup  |  Entry TF: 1h  |  Batch: batch_2025_01

### Batch Summary
| idea_id              | description              | avg PF | PF lift | pairs OK | decision |
|----------------------|--------------------------|--------|---------|----------|----------|
| setup_kde_upper      | KDE upper population 4h  | 1.969  | +0.233  | 4/5      | PROMOTED |
| setup_kde_upper_rsi  | KDE upper + RSI-MA < 50  | 1.783  | +0.097  | 3/5      | TESTING  |

### Per-Idea Detail
[setup_kde_upper]  avg PF 1.969  PF lift +0.233  4/5 pairs
  BTCUSDT   WR 49.9%  PF 1.495  lift +0.124 / req 0.10  n=2,416  cov 46%  [OK]
  ETHUSDT   WR 59.5%  PF 2.208  lift +0.462 / req 0.10  n=2,393  cov 46%  [OK]
  SOLUSDT   WR 47.3%  PF 1.344  lift -0.092 / req 0.10  n=1,831  cov 35%  [--]
  BNBUSDT   WR 55.2%  PF 1.998  lift +0.252 / req 0.10  n=1,944  cov 37%  [OK]
  XRPUSDT   WR 57.1%  PF 2.101  lift +0.355 / req 0.10  n=1,712  cov 33%  [OK]
```

**Coverage flag rule:** append `!` to `cov X%` if coverage is below the minimum threshold (default 10%).  
Example: `cov 9%!` means the idea covers fewer than 10% of baseline bars — low confidence.  
Do not add separate lines below pairs for coverage warnings. Inline only.

**Result flag rule:** `[OK]` = passes all guardrails, `[--]` = fails one or more.  
No other tags. No GOOD/BAD/BORDERLINE in the pair lines.

### Per-Pair Population Drilldown 

Purpose:
- Show robustness of prior filters on each pair.
- Make it obvious what works and what does not, per pair.
- Track average trade duration, which is often where hidden fragility appears.

Format example (inside active board or as linked section from active board):
```
#### ETHUSDT - Population Comparison

| population            | wr_%  | pf    | dur | n_trades |
|-----------------------|------:|------:|----:|---------:|
| kde_upper_baseline    | 53.79 | 1.746 | 21.0|     5256 |
| price_rsi_divergence  | 49.02 | 1.442 | 16.1|      816 |
| shrinking_impulse     | 44.44 | 1.200 | 18.4|      117 |
| bb_rounding           | 54.97 | 1.831 | 14.0|      875 |
| ema_tightening        | 59.45 | 2.199 | 20.8|     1058 |
| ema_cross_down        | 55.70 | 1.886 | 19.9|      158 |
```

Interpretation guideline:
- Compare each candidate row against `kde_upper_baseline` for the same pair.
- Prefer candidates that improve PF without collapsing coverage or n_trades.
- Treat very short or very long duration shifts as a warning to inspect trade behavior before promotion.

### 3) Rejected Archive Markdown — one per stage × entry_tf

Naming:
```
phase_setup_entry1h_rejected.md
phase_setup_entry15m_rejected.md
```

Purpose: look up what was already tried, why it failed, and whether it is worth retesting.

Format:
```
## Phase: Setup  |  Entry TF: 1h  |  Rejected Archive

### setup_rvol_breakdown
Description: Relative volume spike on breakdown bar
Params: rvol_period=20, rvol_threshold=1.5
Rejected batch: batch_2024_12  |  Reject reason: coverage 3% — too sparse to measure edge
Retest condition: only if RVOL logic changes or minimum coverage can be demonstrated

  avg PF: 1.41  PF lift: -0.15  pairs OK: 1/5
  BTCUSDT   WR 48.2%  PF 1.395  lift +0.024 / req 0.10  n=249   cov 3%!  [--]
  ETHUSDT   WR 52.3%  PF 1.643  lift -0.102 / req 0.10  n=241   cov 3%!  [--]
  SOLUSDT   WR 44.1%  PF 1.102  lift -0.435 / req 0.10  n=198   cov 3%!  [--]
  BNBUSDT   WR 55.8%  PF 1.921  lift +0.185 / req 0.10  n=211   cov 3%!  [OK]
  XRPUSDT   WR 46.9%  PF 1.288  lift -0.249 / req 0.10  n=188   cov 3%!  [--]
---
```

### 4) Promotion Registry JSON

Machine-readable source for the next phase.  
Rule: only manually approved ideas enter these registries.

Suggested files:
```
bear_strategy/hypothesis_tests/results/regime_registry.json
bear_strategy/hypothesis_tests/results/setup_registry.json
bear_strategy/hypothesis_tests/results/trigger_registry.json
```


## Phase Rules

### Phase 1: Regime Idea x Entry TF Matrix

Goal:
- Fix one regime idea.
- Test it against multiple entry timeframes.
- Promote all entry timeframes with real edge.

```python
regime_tf = "1d"
regime_rule = "close_below_ema_50"

for entry_tf in ["15m", "1h", "4h", "1d"]:
    # compare regime-filtered entries vs unrestricted baseline on this entry_tf
    pass
```

Output:
- comparison CSV rows for each entry_tf
- decision markdown for this batch
- `regime_registry.json` with promoted entry_tfs

### Phase 2: Setup Sweep

Goal:
- Fix promoted regime.
- Test setup ideas from one setup phase config.
- Keep entry_tfs that survived Phase 1 unless demoted by data.

Output:
- `phase_setup_comparison.csv`
- `phase_setup_decisions.md`
- `setup_registry.json`

### Phase 3: Trigger Sweep

Goal:
- Fix promoted regime + setup.
- Test trigger ideas from one trigger phase config.
- Promote 1-2 strongest triggers by your rules.

Output:
- `phase_trigger_comparison.csv`
- `phase_trigger_decisions.md`
- `trigger_registry.json`

---

## Decision Rubric

| **Phase** | **Metric** | **Threshold** |
|---|---|---|
| **Regime** | PF lift vs unrestricted baseline |is the signal 2.5x bigger than the luck?  (z = signal / noise) |
| **Regime** | Pairs passing | >~ 70% |
| **Setup** | PF lift vs regime baseline | is the signal 2.5x bigger than the luck?  (z = signal / noise) ||
| **Setup** | Pairs passing | >~ 70%|
| **Trigger** | PF lift vs setup baseline | is the signal 2.5x bigger than the luck?  (z = signal / noise) ||
| **Trigger** | Pairs passing | >~ 70% |

at least 50 trades per year tested 

---

## Baseline Precomputation

The baseline (unrestricted random entries on a fixed regime) is the same for every candidate idea within a phase + entry_tf combination.  
When the date range matches the previous run, skip recomputation.

**Rule:**
```
baseline_file = results_dir / f"baseline_{entry_tf}_{regime_col}_{start_date}_{end_date}.csv"

if baseline_file.exists():
    df_baseline = pd.read_csv(baseline_file)
else:
    df_baseline = compute_baseline(...)
    df_baseline.to_csv(baseline_file, index=False)
```

The file name encodes all relevant parameters. Any change to entry_tf, regime rule, or date range produces a new filename and forces recomputation. Same date range → always reuses the cached file.

---

## Indicator Module Contract

Each idea is backed by one Python module. The module exposes a single function:

```python
def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    df      : OHLCV frame aligned to the entry timeframe index
    params  : idea-specific params from the IDEAS config
    returns : boolean pd.Series on the same index
                True  = condition met, include in candidate population
                False = condition not met
    """
```

Module location convention:
```
bear_strategy/hypothesis_tests/indicators/regime/
bear_strategy/hypothesis_tests/indicators/setup/
bear_strategy/hypothesis_tests/indicators/trigger/
```

Multi-timeframe indicators receive a pre-aligned frame — alignment (shift + merge_asof backward) is the runner's responsibility, not the indicator's.

---

## Minimal Operating Loop

For any phase:
1. Open the phase control config.
2. Toggle ideas in `IDEAS` with `enabled=True/False`.
3. Run the phase batch — baseline is loaded from cache if date range matches.
4. Review batch summary in the active board MD, sorted by `pf_lift` and `pairs_passing`.
5. For each idea: set `decision` to `promoted` or `rejected` in the config; add `decision_reason`.
6. Copy promoted ideas to next-phase registry JSON.
7. Move rejected ideas' pair detail to the rejected archive MD (same entry_tf file).

This gives you:
- easy add/remove testing
- one place to compare candidates
- explicit promotion history
- per-TF rejected archive — something that worked on 1h may not work on 15m and vice versa
- cross-layer continuity through registries

---

## Implementation Notes for Current Codebase

You can adopt this without deleting old test modules immediately:
- Keep existing per-test folders as engines.
- Add phase control configs that point to those engines.
- Write all outputs into shared phase result files under one results root.
- Archive old standalone result files once reflected in phase comparison CSV.

This is an incremental migration, not a forced rewrite.

---

## Final Principle

Do not create a new directory because you have a new idea.
Create a new directory only when you have a new engine type.

For normal hypothesis work, add or remove ideas in the phase control config and track decisions in phase-level comparison + registry files.

---

**End of Multiframe Methodology**
