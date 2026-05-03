# Multiframe Testing Methodology

**Purpose:** Define how to correctly test regimes across different timeframes

---

## Core Concept

**Regime** = A filter/gate computed on a HIGHER timeframe, applied to ENTRY timeframe entries.

### Two Timeframes

| **Timeframe** | **Purpose** | **Example** | **Notes** |
|---|---|---|---|
| **Context TF** | Where regime gate is computed | 4h | Slower, smoother; decides if market is in regime |
| **Entry TF** | Where trades happen | 15m | Faster, more precise; where orders are placed |

---

## Testing Flow

### Phase 1: Find Best Context Timeframe

**Goal:** Entries happen on FIXED Entry TF. Find which Context TF regime gives best performance.

```python
# Fixed across all Phase 1 tests
entry_tf = "15m"

# Vary this
for context_tf in ["15m", "1h", "4h", "1d"]:
    config.regime_tf = context_tf
    config.entry_tf = entry_tf
    results = run_backtest(config)
    # → Compare PF across context TF choices
    # → Pick best context TF
    # → Save to regime_registry.json
```

### Example Phase 1 Test Results

```
REGIME CONTEXT TF COMPARISON (Entry TF = 15m, Data = 2024-10-01 to 2025-10-31)

Context TF: 15m
├─ Coverage: 65% of bars (regime TRUE 65% of time)
├─ PF: 1.52
├─ Issue: TOO NOISY — regime flips every bar, no selectivity
└─ Verdict: REJECT (too much false signals)

Context TF: 1h
├─ Coverage: 50% of bars
├─ PF: 1.58
├─ Issue: Still too frequent
└─ Verdict: OK but not best

Context TF: 4h ✅ WINNER
├─ Coverage: 40% of bars (regime TRUE 40% of time)
├─ PF: 1.63 ← BEST PF
├─ Observation: Selective (40% bars), clean (long runs of regime=TRUE)
└─ Verdict: PROMOTE to regime_registry.json

Context TF: 1d
├─ Coverage: 35% of bars
├─ PF: 1.55
├─ Issue: TOO SLOW — miss too many opportunities, regime stays on too long
└─ Verdict: REJECT (too slow)

PROMOTION:
{
  "regime_tf": "4h",
  "entry_tf": "15m",
  "regime_params": {"ema_period": 50, "threshold": 50},
  "pf": 1.63,
  "coverage": 0.40,
  "notes": "4h regime gate gives best edge to 15m entries"
}
```

---

## How Regime Gates Work (Technical)

### 1. Compute Regime on Context TF

```python
# On 4h bars:
ema_4h = close.ewm(span=50).mean()
regime_4h = ema_4h < 50  # TRUE if in downtrend
# Returns: Series with index = 4h timestamps
```

### 2. Forward-Fill to Entry TF

```python
# Merge 4h regime to 15m timestamps
# Every 15m bar gets the CURRENT regime state from 4h

Example:
├─ 4h bar at 12:00 → regime = TRUE
├─ Forward to 15m bars: 12:15, 12:30, 12:45, 13:00 → all TRUE
├─ 4h bar at 16:00 → regime = FALSE
├─ Forward to 15m bars: 16:15, 16:30, 16:45, 17:00 → all FALSE
└─ 4h bar at 20:00 → regime = TRUE
   └─ Forward to 15m bars: 20:15, 20:30, 20:45, 21:00 → all TRUE
```

### 3. Gate Entries

```python
# Entries happen ONLY when regime is TRUE
entry_signal = regime_gate & kde_upper & rsi_ma_below_50
# All three conditions must be true SIMULTANEOUSLY on 15m bar
```

---

## Why This Matters: Common Mistakes

### ❌ MISTAKE 1: Testing regime on entry TF only
```python
# WRONG:
for tf in ["15m", "1h", "4h", "1d"]:
    config.regime_tf = tf
    config.entry_tf = tf  # ← SAME TF, defeats purpose
    # → This doesn't answer "which context TF is best"
    # → It answers "which TF is best at making entries"
    # → Different question!
```

### ❌ MISTAKE 2: Forgetting forward-fill
```python
# WRONG:
regime_4h = compute_regime(df_4h)
entries_15m = regime_4h & kde_upper_15m  # ← Timestamps don't match!
```

### ✅ CORRECT: Fixed entry TF, vary context TF
```python
# CORRECT:
entry_tf = "15m"
for context_tf in ["15m", "1h", "4h", "1d"]:
    regime_on_context = compute_regime(load_bars(context_tf))
    regime_on_entry = forward_fill(regime_on_context, target_tf=entry_tf)
    entries = regime_on_entry & kde_upper_entry & rsi_ma_entry
    # → Now can compare which context TF gives best results on 15m entries
```

---

## Phase 2: Setup Testing (Context TF Fixed)

Once Phase 1 chooses best context TF (e.g., 4h), Phase 2 FIXES it:

```python
config.regime_tf = "4h"  # ← FIXED from Phase 1
config.entry_tf = "15m"  # ← FIXED

# Now test setups:
# ├─ Setup 1: regime + kde_upper
# ├─ Setup 2: regime + kde_upper + rsi_ma
# ├─ Setup 3: regime + kde_upper + rsi_ma + volatility_filter
# └─ etc.

# All use same 4h context regime
```

---

## Phase 3: Trigger Testing (Both TF Fixed)

Once Phase 2 chooses best setup, Phase 3 FIXES both:

```python
config.regime_tf = "4h"   # ← FIXED from Phase 1
config.entry_tf = "15m"   # ← FIXED
config.setup = "kde_upper_rsi_ma"  # ← FIXED from Phase 2

# Now test triggers:
# ├─ Trigger 1: ema_cross_price
# ├─ Trigger 2: close_below_bb
# ├─ Trigger 3: atr_expansion
# └─ etc.

# All use same 4h context regime + same setup
```

---

## Decision Rubric: Choosing Context TF

| **Aspect** | **Ideal Range** | **Why** |
|---|---|---|
| **Coverage** | 30–50% | Selective gate, but not too exclusive |
| **PF Lift** | +0.05 to +0.15 | Significant edge, but not unrealistic |
| **Stability** | 4/5 pairs confirm | Robust across different markets |
| **Run Length** | Avg 2–8 bars regime=TRUE | Long enough to catch moves, not too sticky |

**Typical Outcome:**
- 15m context TF: TOO NOISY (60–70% coverage)
- 1h context TF: OK (50–55% coverage)
- 4h context TF: SWEET SPOT (35–45% coverage) ✅
- 1d context TF: TOO SLOW (20–30% coverage)

---

## Configuration Template

### Phase 1 Config (Vary Context TF)

```python
# config.py for regime_context_4h_entry15m test

# ────────────────────────────────────────
# Timeframes (Phase 1: vary regime_tf)
# ────────────────────────────────────────
regime_tf: str = "4h"      # ← CHANGE THIS in each Phase 1 test
entry_tf: str = "15m"      # ← FIXED

# ────────────────────────────────────────
# Data Split (Standard)
# ────────────────────────────────────────
train_start: str = "2021-01-01"
train_end: str = "2024-09-30"
test_start: str = "2024-10-01"
test_end: str = "2025-10-31"

# ────────────────────────────────────────
# Regime Parameters
# ────────────────────────────────────────
regime_params: dict = {
    "ema_period": 50,
    "slope_lookback": 1,
    "threshold": 50,
}
```

### Phase 2 Config (Context TF Fixed)

```python
# config.py for setup_1_kde_upper test

# ────────────────────────────────────────
# Timeframes (Phase 2: FIXED from Phase 1)
# ────────────────────────────────────────
regime_tf: str = "4h"      # ← FIXED from regime_registry.json
entry_tf: str = "15m"      # ← FIXED

# ────────────────────────────────────────
# Data Split (Same as Phase 1)
# ────────────────────────────────────────
train_start: str = "2021-01-01"
train_end: str = "2024-09-30"
test_start: str = "2024-10-01"
test_end: str = "2025-10-31"

# ────────────────────────────────────────
# Regime Parameters (Same as Phase 1 winner)
# ────────────────────────────────────────
regime_params: dict = {
    "ema_period": 50,
    "slope_lookback": 1,
    "threshold": 50,
}

# ────────────────────────────────────────
# Setup Parameters
# ────────────────────────────────────────
kde_tf: str = "4h"
kde_window: int = 200
kde_bandwidth_mult: float = 1.0
```

---

## File Naming Convention

### Phase 1 Files

```
regime_testing/
├─ regime_context_15m_entry15m/      (regime on 15m, entries on 15m)
├─ regime_context_1h_entry15m/       (regime on 1h, entries on 15m)
├─ regime_context_4h_entry15m/       (regime on 4h, entries on 15m)
├─ regime_context_1d_entry15m/       (regime on 1d, entries on 15m)
└─ results/
   ├─ regime_context_15m_entry15m.csv
   ├─ regime_context_1h_entry15m.csv
   ├─ regime_context_4h_entry15m.csv
   ├─ regime_context_1d_entry15m.csv
   └─ regime_registry.json  (PROMOTED: "4h_entry15m" with PF 1.63)
```

### Phase 2 Files

```
setup_testing/
├─ setup_1_kde_upper_regime4h_entry15m/
├─ setup_2_kde_upper_rsi_ma_regime4h_entry15m/
├─ setup_3_<idea>_regime4h_entry15m/
└─ results/
   ├─ setup_1_summary.csv
   ├─ setup_2_summary.csv
   └─ setup_registry.json  (PROMOTED: "kde_upper_rsi_ma")
```

### Phase 3 Files

```
trigger_testing/
├─ trigger_1_ema_cross_price/
├─ trigger_2_close_below_bb/
├─ trigger_3_<idea>/
└─ results/
   ├─ trigger_1_summary.csv
   ├─ trigger_2_summary.csv
   └─ trigger_registry.json  (PROMOTED: ["ema_cross_price", "close_below_bb"])
```

---

## Summary: Testing Order

```
Phase 1 (Vary Regime Context TF):
├─ Test 1: regime on 15m  → entry on 15m  → results
├─ Test 2: regime on 1h   → entry on 15m  → results
├─ Test 3: regime on 4h   → entry on 15m  → results ✅ BEST
├─ Test 4: regime on 1d   → entry on 15m  → results
└─ Promote: 4h regime

Phase 2 (Fix Regime Context, Vary Setup):
├─ Test 1: regime(4h) + kde_upper → entry on 15m → results
├─ Test 2: regime(4h) + kde_upper + rsi_ma → entry on 15m → results ✅ BEST
├─ Test 3: regime(4h) + kde_upper + rsi_ma + volatility → entry on 15m → results
└─ Promote: regime(4h) + kde_upper + rsi_ma

Phase 3 (Fix Regime & Setup, Vary Trigger):
├─ Test 1: regime(4h) + kde_upper + rsi_ma + ema_cross_price → 15m → results ✅ BEST
├─ Test 2: regime(4h) + kde_upper + rsi_ma + close_below_bb → 15m → results ✅ GOOD
├─ Test 3: regime(4h) + kde_upper + rsi_ma + atr_expansion → 15m → results
└─ Promote: regime(4h) + kde_upper + rsi_ma + [ema_cross_price OR close_below_bb]
```

---

**End of Multiframe Methodology**
