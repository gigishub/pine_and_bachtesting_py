# Multiframe Testing Methodology

**Purpose:** Define how to correctly test regimes across different timeframes

---

## Core Concept

**Regime** = A filter/gate computed on a timeframe, applied to ENTRY timeframe entries.

### Two Timeframes

| **Timeframe** | **Purpose** | **Example** | **Notes** |
|---|---|---|---|
| **Context TF** | Where regime gate is computed | 4h | Slower, smoother; decides if market is in regime |
| **Entry TF** | Where trades happen | 15m | Faster, more precise; where orders are placed |

---

## Testing Flow

### Phase 1: Find Promising Regime x Entry TF Pairs

**Goal:** Treat the regime timeframe and the entry timeframe as two separate variables. Start with one regime idea, such as `short only when price is below the daily EMA`, then test that same regime across multiple entry TFs and compare the edge against the unrestricted entry baseline on each entry TF.

```python
# Regime idea under test
regime_tf = "1d"
regime_rule = "close_below_ema_50"

# Test the same regime against multiple entry TFs
for entry_tf in ["15m", "1h", "4h", "1d"]:
    config.regime_tf = regime_tf
    config.entry_tf = entry_tf
    results = run_backtest(config)
    # → Compare regime-filtered entries vs all-bars baseline on this entry_tf
    # → Keep entry TFs that show real edge
    # → Save promoted regime_tf x entry_tf pairs to the registry
```

> Note: do not fix the entry TF when testing a regime idea. Fix the regime idea, then test that regime against multiple entry TFs and promote the entry TFs that show promise.

### Example Phase 1 Test Results

```
REGIME IDEA TEST: daily close below EMA 50
Data = 2024-10-01 to 2025-10-31

Regime TF: 1d
Regime rule: short only when price is below daily EMA 50

Entry TF: 15m
├─ Coverage: 62% of entry bars
├─ PF: 1.61
├─ Baseline: all 15m bars
└─ Verdict: PROMOTE

Entry TF: 1h
├─ Coverage: 61% of entry bars
├─ PF: 1.58
├─ Baseline: all 1h bars
└─ Verdict: PROMOTE

Entry TF: 4h
├─ Coverage: 60% of entry bars
├─ PF: 1.44
├─ Baseline: all 4h bars
└─ Verdict: REJECT

Entry TF: 1d
├─ Coverage: 59% of entry bars
├─ PF: 1.31
├─ Baseline: all 1d bars
└─ Verdict: REJECT

PROMOTION:
{
    "regime_tf": "1d",
    "regime_rule": "close_below_ema_50",
    "promoted_entry_tfs": ["15m", "1h"],
    "notes": "Daily EMA regime shows edge on 15m and 1h, but not on 4h or 1d."
}
```

> If more than one entry TF shows a good edge under the same regime idea, promote all of those entry TFs into Phase 2 and let later setup and trigger tests decide which one survives.
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

> Note: the regime TF and the entry TF are different variables. A daily regime can be tested against 15m, 1h, 4h, or even 1d entries. Promote the entry TFs that show edge under that regime, and demote them later if they fail in the next stages.


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

### ✅ CORRECT: Fix the Regime Idea, Test Multiple Entry TFs
```python
# CORRECT:
regime_tf = "1d"
regime_on_context = compute_regime(load_bars(regime_tf))

for entry_tf in ["15m", "1h", "4h", "1d"]:
    regime_on_entry = forward_fill(regime_on_context, target_tf=entry_tf)
    entries = regime_on_entry
    # → Compare regime-filtered entries vs all-bars baseline on each entry_tf
    # → Promote the entry TFs that show real edge
```

---

## Phase 2: Setup Testing (Regime Fixed, Entry TF Candidate Range)

Once Phase 1 chooses a winning regime idea, Phase 2 fixes that regime. Entry TF may still be a candidate range if multiple entry TFs were promoted in Phase 1:

```python
config.regime_tf = "1d"  # ← FIXED from Phase 1 winner
config.regime_rule = "close_below_ema_50"  # ← FIXED from Phase 1 winner
config.entry_tfs = ["15m", "1h"]  # ← candidate range if both entry TFs were promoted

# Now test setups i.e.:
# ├─ Setup 1: regime + bb set up
# ├─ Setup 2: regime + kde_upper & rsi_ma
# ├─ Setup 3: regime + kde_setup(multple option how to read kde) or rsi_ma or volatility_filter
# └─ etc.

# All use same promoted regime
```

If only one entry TF remains viable, use the surviving TF instead of the range.

---

## Phase 3: Trigger Testing (Regime + Setup Fixed, Entry TF Candidate Range)

Once Phase 2 chooses best setup, Phase 3 fixes the regime and setup, but may still test a range of entry TFs if multiple entry candidates survived earlier promotion:

```python
config.regime_tf = "1d"   # ← FIXED from Phase 1 winner
config.regime_rule = "close_below_ema_50"  # ← FIXED from Phase 1 winner
config.setup = "kde_upper_rsi_ma"  # ← FIXED from Phase 2
config.entry_tfs = ["15m", "1h"]   # ← candidate range if both TFs showed edge


# Now test triggers on the surviving entry TFs:
# ├─ Trigger 1: ema_cross_price
# ├─ Trigger 2: close_below_bb
# ├─ Trigger 3: atr_expansion
# └─ etc.

# All use same promoted regime + same setup
```

If one entry TF later fails, demote that TF and continue with the remaining candidate.

---

## Decision Rubric: Choosing Regime x Entry TF Pairs

| **Aspect** | **Ideal Range** | **Why** |
|---|---|---|
| **Coverage** | 30–70% | Selective gate, but not too exclusive |
| **PF Lift** | is the signal 2.5x bigger than the luck? = z = signal / noise |
| **Stability** | high percentage of tested pairs| Robust across different markets |



## Configuration Template

### Phase 1 Config (Test One Regime Idea Across Entry TFs)

```python
# config.py for regime_daily_ema50 test

# ────────────────────────────────────────
# Timeframes (Phase 1: fixed regime_tf, vary entry_tf)
# ────────────────────────────────────────
regime_tf: str = "1d"      # ← timeframe where the regime is computed
entry_tfs: list[str] = ["15m", "1h", "4h", "1d"]      # ← test all candidate entry TFs

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

# Example regime rule:
# short only when price is below the daily EMA 50
```

### Phase 2 Config (Regime Fixed)

```python
# config.py for setup_1_kde_upper test

# ────────────────────────────────────────
# Timeframes (Phase 2: FIXED from Phase 1)
# ────────────────────────────────────────
regime_tf: str = "1d"      # ← FIXED from regime_registry.json
entry_tfs: list[str] = ["15m", "1h"]      # ← candidate range if both entry TFs were promoted

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

regime_rule: str = "close_below_ema_50"

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
├─ regime_daily_ema50_entry15m/
├─ regime_daily_ema50_entry1h/
├─ regime_daily_ema50_entry4h/
├─ regime_daily_ema50_entry1d/
└─ results/
    ├─ regime_daily_ema50_entry15m.csv
    ├─ regime_daily_ema50_entry1h.csv
    ├─ regime_daily_ema50_entry4h.csv
    ├─ regime_daily_ema50_entry1d.csv
    └─ regime_registry.json  (PROMOTED: daily_ema50 with entry_tfs ["15m", "1h"])
```

### Phase 2 Files

```
setup_testing/
├─ setup_1_kde_upper_regimeDailyEma50_entry15m/
├─ setup_1_kde_upper_regimeDailyEma50_entry1h/
├─ setup_2_kde_upper_rsi_ma_regimeDailyEma50_entry15m/
├─ setup_2_kde_upper_rsi_ma_regimeDailyEma50_entry1h/
├─ setup_3_<idea>_regimeDailyEma50_entry15m/
├─ setup_3_<idea>_regimeDailyEma50_entry1h/
└─ results/
    ├─ setup_1_summary.csv
    ├─ setup_2_summary.csv
    └─ setup_registry.json  (PROMOTED: regime daily_ema50 + setup kde_upper_rsi_ma + entry_tfs ["15m", "1h"])
```

### Phase 3 Files

```
trigger_testing/
├─ trigger_1_ema_cross_price_entry15m/
├─ trigger_1_ema_cross_price_entry1h/
├─ trigger_2_close_below_bb_entry15m/
├─ trigger_2_close_below_bb_entry1h/
├─ trigger_3_<idea>_entry15m/
├─ trigger_3_<idea>_entry1h/
└─ results/
   ├─ trigger_1_summary.csv
   ├─ trigger_2_summary.csv
    └─ trigger_registry.json  (PROMOTED: trigger winners by surviving entry_tfs)
```

---

## Summary: Testing Order

```
Phase 1 (Fix Regime Idea, Vary Entry TF):
├─ Test 1: daily EMA regime → entry on 15m → results ✅ PROMOTE
├─ Test 2: daily EMA regime → entry on 1h  → results ✅ PROMOTE
├─ Test 3: daily EMA regime → entry on 4h  → results
├─ Test 4: daily EMA regime → entry on 1d  → results
└─ Promote: daily EMA regime with entry TF candidates [15m, 1h]

Phase 2 (Fix Regime, Vary Setup):
├─ Test 1: daily EMA regime + kde_upper → entry on 15m and 1h → results
├─ Test 2: daily EMA regime + kde_upper + rsi_ma → entry on 15m and 1h → results ✅ BEST
├─ Test 3: daily EMA regime + kde_upper + rsi_ma + volatility → entry on 15m and 1h → results
└─ Promote: daily EMA regime + kde_upper + rsi_ma with entry TF candidates [15m, 1h]

Phase 3 (Fix Regime & Setup, Vary Trigger):
├─ Test 1: daily EMA regime + kde_upper + rsi_ma + ema_cross_price → 15m and 1h → results ✅ BEST
├─ Test 2: daily EMA regime + kde_upper + rsi_ma + close_below_bb → 15m and 1h → results ✅ GOOD
├─ Test 3: daily EMA regime + kde_upper + rsi_ma + atr_expansion → 15m and 1h → results
└─ Promote: daily EMA regime + kde_upper + rsi_ma + trigger winner on the surviving entry TFs
```

---

**End of Multiframe Methodology**
