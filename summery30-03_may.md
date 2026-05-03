# Bear Strategy Hypothesis Testing: Development Summary & Workflow

**Created:** 2026-05-03  
**Status:** Transitioning from ad-hoc testing to structured workflow  
**Last Result:** Trigger Search 2 confirmed 2 event triggers (ema_cross_price, close_below_bb)

---

## Current State: What Was Accomplished

### Three-Phase Development (Apr 30 — May 3)

#### Phase 1: Regime & Setup Testing (Checkpoints 001–004)
- **Regime Testing:** Found `ema_below_50_regime` on 1h TF works with KDE signals
- **Setup 1:** `kde_upper` on 4h TF + regime confirmed (avg PF 1.551 across 5 pairs)
- **Setup 2 Variants:** Tested 4 different signal combinations on 15m TF (all failed; signals were too correlated with baseline)

#### Phase 2: Held-State Filter Testing (Checkpoints 005–007)
- **Trigger 1–7:** Built 7 iterations testing held-state momentum/volatility filters
  - All tested momentum conditions (RSI, MFI, MACD, BB) as "positional" filters (TRUE when condition met, held for many bars)
  - Key finding: Positional filters work OK on bare baseline but saturate when baseline is strengthened
- **Trigger 4 CONFIRMED:** `rsi_ma_baseline` (EMA-smoothed RSI < 50) added +0.181 PF lift on top of kde_upper_baseline
  - This became the new two-layer baseline: `regime AND kde_upper AND rsi_ma<50` → 1.732 avg PF

#### Phase 3: Event Trigger Testing (Checkpoint 008–009)
- **Trigger 8 Discovery:** When rsi_ma_below_50 is baseline, adding other positional filters (rsi<50, ema_order, mfi<50) adds ZERO lift
  - Reason: 80–97% correlated with baseline — redundant signals
  - **Critical insight:** Need EVENT triggers (fire on ONE bar) not HELD-STATE filters
- **Trigger Search 1:** Built 7 event-trigger variants; found two confirmed:
  - `bearish_engulfing` (body engulfs prior bar) — FAILED (43% coverage, no lift)
  - `break_prior_low` (close < prev_low) — FAILED (26% coverage, negative lift)
  - `atr_expansion` (range > 1.5×ATR, bearish close) — FAILED (7% coverage)
  - `macd_cross` (MACD crosses signal) — FAILED (3% coverage)
  - `rsi_cross_50` (RSI crosses below 50) — **CONFIRMED** (avg PF 1.975, 3/5 pairs, 4% sparse)
  - `ema_cross` (EMA 9 crosses below EMA 20) — FAILED (6% coverage, negative lift)
  - `close_below_bb` (close < lower BB) — **CONFIRMED** (avg PF 1.885, 4/5 pairs, 15% coverage)

- **Trigger Search 2:** Refined with 3 triggers:
  - `close_below_bb` (BASE, confirmed) — 1.885 PF, 4/5 pairs
  - `bearish_candle_size` (range 0.7–1.2×ATR, bearish close) — FAILED (27% coverage, -0.031 PF lift)
  - `ema_cross_price` (price crosses below EMA 10) — **CONFIRMED** (avg PF 1.967, 3/5 pairs, 6% sparse)

---

## Current Architecture Issues & Mess

### Problems with Current Approach

1. **No clear data/train/test split**
   - All tests use same data (2021-01-01 → 2025-11-01)
   - No 12–18 month holdout for final validation
   - Results may be overfitted or data-snooped

2. **File/Directory Explosion**
   - Every new idea = new dir: `setup_2_trigger_1_check`, `setup_2_trigger_2_check`, ... `trigger_search_1`, `trigger_search_2`
   - 8+ hypothesis test directories, no clear naming scheme
   - Hard to navigate, unclear which is "current best"

3. **Config Parameters Scattered**
   - Each module has its own config.py with overlapping params
   - No master registry of "what worked"
   - Hard to reproduce or compare setups side-by-side

4. **Date/Period Handling Broken**
   - `config.start_date` and `config.end_date` are hardcoded strings in each module
   - No systematic way to adjust train/test split
   - Can't easily run same strategy on different data periods

5. **Workflow Unclear**
   - "Which test should I run next?" — no documented decision process
   - "Is this result good?" — no scoring rubric or comparison baseline

   
   - "Which signals should go into Setup 3?" — no way to merge results from multiple tests

6. **No Promotion/Rollup**
   - Confirmed signals live in individual test modules
   - No way to "promote" a confirmed signal and re-test combined with others
   - Manual copy-paste of params between modules

---

## Proposed Structured Workflow

### Three-Stage Testing Pipeline

```
PHASE 1: REGIME CONTEXT TESTING (Multiframe Structure)
  ├─ Entry TF: 15m (fixed — where entries happen)
  ├─ Goal: Find best CONTEXT TF for regime filter (15m, 1h, 4h, 1d, etc.)
  │         → Test which context TF's regime gives edge to 15m entries
  ├─ Structure:
  │   ├─ Regime computed on CONTEXT TF (e.g., 4h EMA below 50)
  │   ├─ Forward-filled to ENTRY TF (15m)
  │   ├─ Entries happen ONLY on 15m when BOTH regime AND kde_upper AND rsi_ma active
  │   └─ Verdict: Does this context TF regime improve 15m entry PF?
  ├─ Train: 2021-01-01 → 2024-09-30 (3.75 years)
  ├─ Test: 2024-10-01 → 2025-10-31 (13 months unseen)
  ├─ Outputs: regime_testing/results/
  │   ├─ regime_context_15m_results.csv (regime on 15m)
  │   ├─ regime_context_1h_results.csv (regime on 1h, entries on 15m)
  │   ├─ regime_context_4h_results.csv (regime on 4h, entries on 15m)
  │   ├─ regime_context_1d_results.csv (regime on 1d, entries on 15m)
  │   └─ ... (one per context TF tested)
  └─ Promotion: Pick best context TF + regime params → regime_registry.json
  
  EXAMPLE:
  ├─ You tested: regime = "1d EMA50", entry_tf = "15m" → PF 1.55 ✅
  ├─ Then tested: regime = "4h EMA50", entry_tf = "15m" → PF 1.63 ✅ (BETTER)
  └─ Promote: 4h regime + 15m entries (because 4h regime gave higher PF on 15m)

PHASE 2: SETUP TESTING
  ├─ Goal: Combine filters on top of confirmed regime
  ├─ Input: regime_registry.json (promoted regime from Phase 1)
  ├─ Train: Same as Phase 1
  ├─ Test: Same as Phase 1
  ├─ Test Multiple Setups:
  │   ├─ setup_testing/setup_1/ (kde_upper on 4h)
  │   ├─ setup_testing/setup_2/ (kde_upper + rsi_ma on 1h)
  │   ├─ setup_testing/setup_3/ (kde_upper + rsi_ma + volatility_filter)
  │   └─ setup_testing/setup_N/ (user-defined combinations)
  ├─ Outputs: setup_testing/results/
  │   ├─ setup_1_summary.csv (all pairs)
  │   ├─ setup_2_summary.csv
  │   └─ setup_registry.json (confirmed setups only)
  └─ Promotion: Pick best setup → trigger_search input

PHASE 3: TRIGGER TESTING
  ├─ Goal: Find entry timing on top of confirmed setup
  ├─ Input: setup_registry.json (promoted setup from Phase 2)
  ├─ Train/Test: Same split as Phases 1–2
  ├─ Test Multiple Triggers:
  │   ├─ trigger_testing/trigger_1/ (bearish_engulfing)
  │   ├─ trigger_testing/trigger_2/ (atr_expansion)
  │   ├─ trigger_testing/trigger_3/ (ema_cross_price)
  │   └─ trigger_testing/trigger_N/ (user-defined combinations)
  ├─ Outputs: trigger_testing/results/
  │   ├─ trigger_1_summary.csv
  │   ├─ trigger_2_summary.csv
  │   └─ trigger_registry.json (confirmed triggers only)
  └─ Final: Merge best setup + best trigger(s) → Strategy 3 (ready for live test)
```

### Directory Structure (Proposed)

```
bear_strategy/
├─ hypothesis_tests/
│  ├─ PHASE_1_REGIME_TESTING/
│  │  ├─ regime_5m_check/
│  │  ├─ regime_15m_check/
│  │  ├─ regime_1h_check/
│  │  ├─ results/
│  │  │  ├─ regime_5m_results.csv
│  │  │  ├─ regime_15m_results.csv
│  │  │  └─ regime_registry.json (PROMOTED REGIME)
│  │  └─ README.md (methodology)
│  │
│  ├─ PHASE_2_SETUP_TESTING/
│  │  ├─ setup_1_kde_upper/
│  │  ├─ setup_2_kde_upper_rsi_ma/
│  │  ├─ setup_3_<user_idea>/
│  │  ├─ results/
│  │  │  ├─ setup_1_summary.csv
│  │  │  ├─ setup_2_summary.csv
│  │  │  └─ setup_registry.json (PROMOTED SETUP)
│  │  └─ README.md (methodology)
│  │
│  ├─ PHASE_3_TRIGGER_TESTING/
│  │  ├─ trigger_1_bearish_engulfing/
│  │  ├─ trigger_2_atr_expansion/
│  │  ├─ trigger_3_ema_cross_price/
│  │  ├─ results/
│  │  │  ├─ trigger_1_summary.csv
│  │  │  ├─ trigger_2_summary.csv
│  │  │  └─ trigger_registry.json (PROMOTED TRIGGERS)
│  │  └─ README.md (methodology)
│  │
│  └─ OUTPUTS/
│     ├─ strategy_3_final.json (setup + triggers combined)
│     ├─ backtesting_notebook.ipynb (run live tests here)
│     └─ performance_comparison.md

# At workspace root (session folder):
└─ summary.md (this file)
└─ methodology.md (detailed process: how to run each phase, decision rubrics)
└─ CURRENT_STATUS.md (quick ref: where we are, what's next)
```

---

## ⚠️ **CRITICAL CLARIFICATION: Multiframe Structure**

### The Problem You Found

You were testing regimes on DIFFERENT timeframes but applying them to entries on DIFFERENT timeframes:
```
Example (CONFUSING):
├─ Tested: 1d regime on 1d entries → 1.55 PF
├─ Then tested: 4h regime on 15m entries → 1.63 PF
├─ Then tested: 1h regime on 1h entries → 1.52 PF
├─ Then jumped to: 4h regime on 4h entries → 1.58 PF (wrong comparison!)
└─ PROBLEM: Can't tell if 4h regime is good or just works better on 4h entries than 1h entries does on 1h
```

### The Solution: Fix Entry TF, Vary Context TF

**PHASE 1 Rule:** Entry TF is FIXED. Regime TF (context) VARIES.

```
Phase 1 (CORRECT):
├─ Entry TF: 15m (FIXED across all tests)
├─ Test 1: regime on 15m, entries on 15m → PF 1.52
├─ Test 2: regime on 1h, entries on 15m → PF 1.58
├─ Test 3: regime on 4h, entries on 15m → PF 1.63 ✅ (BEST)
├─ Test 4: regime on 1d, entries on 15m → PF 1.55
└─ Promotion: Use 4h regime + 15m entries (because 4h gave best PF on 15m)
```

**Why This Matters:**
- Regime is a **GATE/FILTER** (gate stays open or closed based on context TF)
- Entries happen on ENTRY TF (always 15m in this example)
- Question: "Which context TF gate works best for 15m entries?"
  - 15m gate = too noisy, flips every bar
  - 1d gate = too slow, stays on for too long
  - 4h gate = sweet spot
  
**Multiframe Stack:**
```
Higher TF (4h) ← regime gate computed here
    ↓ (forward-fill)
Entry TF (15m) ← entries happen here, ONLY when regime is TRUE
    ↓ (sub-bars)
Sub-bars (also 15m) ← KDE signals, triggers computed at entry TF
```

---

### Standard Split for All Tests

```python
# In each module's config.py:

train_start: str = "2021-01-01"
train_end: str = "2024-09-30"      # 3.75 years of training data
test_start: str = "2024-10-01"     # Exact start: day after train_end
test_end: str = "2025-10-31"       # 13 months unseen data

# The "date section" works like this:
# ├─ TRAIN PERIOD (used to tune params, see patterns)
# ├─ TEST PERIOD (used to measure PF, WR, coverage — the verdict)
# └─ FUTURE HOLDOUT (reserved for live paper trading — NOT used in any test)
```

**Why this matters:**
- 13 months of unseen data is enough to validate robustness
- 3.75 years of training data is enough to find patterns without overfitting to recent market
- When Phase 3 is done, have 5 months (2025-11-01 → 2026-04-01+) for paper trading validation before deployment

---

## Execution Process: Each Phase

### Phase 1: Regime Context Testing (Find Best Timeframe for Gate)

**Key Concept:** Regime is a FILTER (gate) computed on one timeframe, applied to entries on another.

```
Entry TF: 15m (FIXED)
Context TF: TEST MULTIPLE (15m, 1h, 4h, 1d)
  ├─ For each context TF:
  │   ├─ Compute regime on that TF (e.g., "ema_below_50_regime on 4h")
  │   ├─ Forward-fill to 15m (so every 15m bar has regime TRUE/FALSE)
  │   ├─ Run entries on 15m, ONLY when regime is TRUE
  │   ├─ Measure: avg PF, WR, coverage on unseen test data (2024-10-01 → 2025-10-31)
  └─ Decision: Which context TF regime gives best PF on 15m entries?

EXAMPLE (What You Actually Did):
├─ Test 1: regime = "1d EMA50", entry = "15m" → PF 1.55, 50% coverage
├─ Test 2: regime = "4h EMA50", entry = "15m" → PF 1.63, 40% coverage ✅ BETTER
├─ Promotion: Use 4h regime + 15m entries (higher PF, less noisy)
└─ Never promoted "1d regime" because you didn't reach it in tests

Why it matters:
├─ 1d regime = TOO SLOW, too much coverage, regime stays on for too long
├─ 15m regime = TOO FAST, too noisy, regime flips every bar
└─ 4h regime = SWEET SPOT, selective enough, smooth enough for 15m entries
```

**Phase 1 Tests to Run:**
```python
for context_tf in ["15m", "1h", "4h", "1d"]:
    config.regime_tf = context_tf    # Compute regime on this TF
    config.entry_tf = "15m"          # Entries always on 15m
    run_test(config)
    # → Compare PF, WR, coverage across all context TFs
    # → Promote best to regime_registry.json
```

**Phase 1 Output File Naming:**
```
regime_testing/results/
├─ regime_context_15m_entry15m.csv    (regime on 15m, entries on 15m)
├─ regime_context_1h_entry15m.csv     (regime on 1h, entries on 15m) 
├─ regime_context_4h_entry15m.csv     (regime on 4h, entries on 15m)
├─ regime_context_1d_entry15m.csv     (regime on 1d, entries on 15m)
└─ regime_registry.json               (PROMOTED: best context TF + params)
```

### Phase 2: Setup Testing (Combine Confirmed Regimes with Filters)
```
1. Read regime_registry.json (which regimes confirmed?)
2. For each confirmed regime TF, create setup variants:
   - setup_1: regime + kde_upper
   - setup_2: regime + kde_upper + rsi_ma
   - setup_3: regime + kde_upper + rsi_ma + volatility (bb, mom, etc.)
   - setup_N: your idea here
3. For each setup:
   - Create: setup_testing/setup_N_<name>/
   - Config: train/test dates, all params
   - Run: python -m setup_testing.setup_N_<name>.run
   - Log result in results/ CSV
4. Criteria for promotion:
   - avg PF > baseline + 0.10 ?
   - 4/5 pairs passing ?
   - Coverage > 5% ? (if too sparse, risk survivor bias)
5. Promote best setup → setup_registry.json
```

### Phase 3: Trigger Testing (Find Entry Timing)
```
1. Read setup_registry.json (which setup to use?)
2. Load confirmed setup's baseline as the new reference
3. Test trigger variants:
   - trigger_1: event_signal_1 on top of setup baseline
   - trigger_2: event_signal_2 on top of setup baseline
   - trigger_N: your idea
4. For each trigger:
   - Create: trigger_testing/trigger_N_<name>/
   - Config: inherit setup params, add trigger params
   - Run: python -m trigger_testing.trigger_N_<name>.run
5. Criteria for promotion (STRICT):
   - avg PF > setup baseline + 0.15 ?  (high bar, triggers must add real edge)
   - 3/5 pairs passing ?
   - Coverage 3–20% (sparse events, not held-state filters)
6. Promote best 1–2 triggers → trigger_registry.json
7. Merge setup + triggers → Strategy 3
```

---

## Key Decisions & Rubrics

### Promotion Threshold by Phase

| Phase | Metric | Min Threshold | Notes |
|-------|--------|---------------|-------|
| 1 (Regime) | PF vs baseline | +0.05 | Low bar; regime is foundational |
| 1 (Regime) | Pairs passing | 3/5 | Some TFs may be weaker |
| 2 (Setup) | PF vs regime | +0.10 | Setup adds filters, expect good lift |
| 2 (Setup) | Pairs passing | 4/5 | Setup is core; should be robust |
| 3 (Trigger) | PF vs setup | +0.15 | Triggers are sparse; must justify overhead |
| 3 (Trigger) | Pairs passing | 3/5 | Triggers are event-based; OK to be selective |
| 3 (Trigger) | Coverage | 3–20% | Sparse fires = healthy; <3% risks data snooping |

### When to FAIL & Move On

- Regime: avg PF < baseline OR coverage < 5% → skip this TF
- Setup: avg PF < regime + 0.05 → reject this setup variant
- Trigger: avg PF < setup + 0.05 OR WR worse on >3 pairs → reject this trigger

---

## Known Issues to Fix

### Issue 1: Date/Period Handling (BROKEN)
**Problem:** Config has hardcoded dates; no train/test split logic.  
**Solution:** Add to `config.py` of each module:
```python
from datetime import datetime

train_start: str = "2021-01-01"
train_end: str = "2024-09-30"
test_start: str = "2024-10-01"
test_end: str = "2025-10-31"

# Auto-convert to datetime in runner.py
train_dates = (datetime.fromisoformat(config.train_start), datetime.fromisoformat(config.train_end))
test_dates = (datetime.fromisoformat(config.test_start), datetime.fromisoformat(config.test_end))

# Filter data:
df_train = df[(df.index >= train_dates[0]) & (df.index < train_dates[1])]
df_test = df[(df.index >= test_dates[0]) & (df.index <= test_dates[1])]
```

### Issue 2: No Registry System (NO WAY TO TRACK WINS)
**Problem:** Confirmed signals live in individual module configs; no master list.  
**Solution:** Create `setup_registry.json` and `trigger_registry.json`:
```json
// setup_registry.json
{
  "regime": {
    "name": "ema_below_50",
    "tf": "1h",
    "params": {"ema_period": 50, "threshold": 50},
    "baseline_pf": 1.732,
    "pairs_passing": 5
  },
  "setup": {
    "name": "kde_upper_rsi_ma",
    "params": {"kde_window": 200, "rsi_ma_period": 5, "rsi_ma_type": "ema", "rsi_ma_threshold": 50},
    "pf": 1.732,
    "pairs_passing": 5
  }
}
```

### Issue 3: File Explosion (HARD TO NAVIGATE)
**Problem:** 8+ test directories with unclear naming.  
**Solution:** Adopt naming scheme:
- `regime_testing/regime_<TF>_check/` (e.g., `regime_1h_check`)
- `setup_testing/setup_<N>_<name>/` (e.g., `setup_2_kde_upper_rsi_ma`)
- `trigger_testing/trigger_<N>_<name>/` (e.g., `trigger_3_ema_cross_price`)
- Each has clear phase, number (for ordering), and descriptive name

---

## Current Test Inventory (To Be Reorganized)

### Existing Tests (Will Move to Phase Dirs)

**Phase 1 Tests:**
- ✅ regime_1h (implicit in old tests) — confirmed

**Phase 2 Tests:**
- ✅ setup_2_trigger_4_check (kde_upper + rsi_ma) — CONFIRMED BEST SETUP
- ❌ setup_2_trigger_1–3_check (other variants) — failed

**Phase 3 Tests:**
- ✅ trigger_search_1 (7 events) — found rsi_cross_50, close_below_bb confirmed
- ✅ trigger_search_2 (3 refined) — confirmed ema_cross_price, close_below_bb

### What to Do with Old Tests

1. Archive to `archive_old_tests/` (keep for reference, not in main workflow)
2. Extract confirmed params → `regime_registry.json`, `setup_registry.json`, `trigger_registry.json`
3. Reorganize 5–10 best-performing tests into Phase directories
4. Document decision for each in results CSV (why did this pass/fail?)

---

## Next Immediate Steps

### Week 1: Reorganize & Fix

- [ ] Create Phase 1, 2, 3 directories
- [ ] Copy best-performing tests into Phase dirs; rename using scheme
- [ ] Fix date handling in config (add train/test split logic)
- [ ] Create `regime_registry.json`, `setup_registry.json`, `trigger_registry.json`
- [ ] Write README.md in each Phase dir (methodology + decision rubric)

### Week 2: Re-Run & Validate

- [ ] Re-run Phase 1 tests with new date split (2021-01-01 → 2024-09-30 train, 2024-10-01 → 2025-10-31 test)
- [ ] Compare results to old runs (should be close, different date split)
- [ ] Promote confirmed signals → registries
- [ ] Re-run Phase 2 tests with promoted regime
- [ ] Re-run Phase 3 tests with promoted setup

### Week 3: Merge & Deploy

- [ ] Combine best setup + best trigger(s) → Strategy 3
- [ ] Run final backtest (train + test periods)
- [ ] Reserve data from 2025-11-01 onward for paper trading

---

## Summary of Current Findings (Snapshot)

### Confirmed Two-Layer Baseline
```
regime: ema_below_50 on 1h
kde_upper: 4h, window=200, bandwidth=1
rsi_ma: ema, period=5, threshold=50

Result: avg PF 1.732 across 5 pairs (vs 1.551 baseline)
Lift: +0.181 (significant, >3 standard errors above baseline)
Pairs: 5/5 confirmed
```

### Confirmed Event Triggers (Top 2)
```
trigger_1: ema_cross_price (price crosses below EMA 10)
  - avg PF 1.967, lift +0.236 vs baseline
  - pairs: 3/5 confirmed
  - coverage: 6.9% (very sparse, high quality)

trigger_2: close_below_bb (close < lower BB 20, 2.0std)
  - avg PF 1.885, lift +0.153 vs baseline
  - pairs: 4/5 confirmed
  - coverage: 15.8% (moderate, consistent)
```

### What DIDN'T Work
- Held-state positional filters (RSI<50, MFI<50, EMA order) — saturate baseline, no added edge
- Crossover combos (fast/slow EMA cross) — too sparseand inconsistent
- Price action (engulfing, break_prior_low) — low quality, no consistent lift
- Medium-sized candles (0.7–1.2 ATR range) — actually hurts performance

---

## File References & Commands

### Quick Commands for Next Work

```bash
# Re-organize tests
mkdir -p bear_strategy/hypothesis_tests/{PHASE_1_REGIME_TESTING,PHASE_2_SETUP_TESTING,PHASE_3_TRIGGER_TESTING}/results

# Run Phase 1 example
source .venv/bin/activate && python -m bear_strategy.hypothesis_tests.PHASE_1_REGIME_TESTING.regime_1h_check.run

# Run Phase 2 example
python -m bear_strategy.hypothesis_tests.PHASE_2_SETUP_TESTING.setup_2_kde_upper_rsi_ma.run

# Run Phase 3 example
python -m bear_strategy.hypothesis_tests.PHASE_3_TRIGGER_TESTING.trigger_1_ema_cross_price.run
```

### Config Template for New Tests

Each new test module should have:
1. `config.py`: Inherit from base config, add train/test dates, override params
2. `entries.py`: Build population masks (signals, filters, triggers)
3. `runner.py`: Same outcome engine for all (ATR stop/target)
4. `run.py`: Same verdict logic (PF lift, pairs passing, coverage thresholds)
5. `test_results/`: Will populate with CSV results automatically

---

**End of Summary**

Next action: Review this workflow, approve structure, then begin Phase 1 re-organization.
