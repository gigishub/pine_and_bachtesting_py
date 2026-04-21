

---

### The 4-Step Filter Architecture

```
Step 1 — Regime Filter
         Is the market in a state where trades should be taken at all?
         (ADX or EMA Ribbon)

Step 2 — Setup Filter  
         Is there a specific structure present that precedes good moves?
         (Donchian or Volume Profile)

Step 3 — Entry Trigger
         Is there a precise moment to enter?
         (CMF or Power Candle)

Step 4 — Exit / Risk Management
         How do you protect the trade and take profit?
         (BBands, Chandelier, PSAR, Trailing Stop)
```

Every combination is a clean AND chain through all 4 steps. No OR statements inside a single combination. OR means two separate combinations.

---

### Phase 1 — Combination Search (Done ✅)

**Goal:** Identify filter combinations that pass strict simultaneous quality thresholds across multiple coins and timeframes.

```
Run all combinations across multiple coins and timeframes
Apply strict quality thresholds simultaneously:
  SQN ≥ 1.0
  Profit Factor ≥ 1.5
  Min Trades ≥ 30
  Win Rate ≥ 30%
  Sharpe ≥ 0.5
  Max Drawdown ≤ 20%

Result: 80 combinations passed out of 3,600
        6 coins on 4H with overlapping filter sets
        CMF + Volume Profile constant across all passes
```

**Pass criteria:** At least one combination meets all thresholds consistently across several coins. Any filter that appears in every passing combination is a candidate for pinning in Phase 2.

**A low pass rate is ok — it means the thresholds are doing their job. The few combinations that survive are the only ones worth investigating further.**

---

### Phase 2 — Cross-Validation

**Goal:** Confirm that passing combinations are not accidents of a specific coin, timeframe, or market regime.

```
Check 1 — Cross-coin validation
          Same combination passes on multiple coins?
          ✅ You have this — 6 coins on 4H

Check 2 — Cross-timeframe validation
          Same combination passes on multiple TFs?
          ⚠️  Partial — strong on 4H, weak on 1H, silent on 1D
          This means 4H is the natural resolution of this edge
          Not a failure — a finding

Check 3 — Temporal validation  
          Do passing trades distribute across the full data history
          or cluster in one market regime?
          This is the next test to run
```

**Pass criteria:** The signature holds across several pairs and tfs and trades distribute across multiple market regimes, with no single regime dominating the results.

**Cross-validation separates real edges from lucky runs. If a combination only works on one coin or one market period, it is not an edge — it is a coincidence.**

---

### Phase 3 — Edge Characterization (Next)

**Goal:** Understand which filters are carrying the edge and whether the performance is robust to parameter changes or curve-fitted to specific values.

```
Filter isolation test
  → Turn off CMF alone — does performance collapse?
  → Turn off Volume Profile alone — does performance collapse?
  → This confirms which layer is carrying the edge

Regime dependency test
  → Do passes cluster in trending markets only?
  → Or do they survive in ranging and volatile periods too?

Parameter sensitivity test
  → Vary indicator parameters ±30%
  → Smooth performance surface = real edge
  → Sharp spike = curve fitted to specific parameter values
```

**Pass criteria:** At least one filter causes meaningful performance collapse when removed, confirming it is load-bearing; the parameter sensitivity surface is smooth across a range of values, not spiked at one specific setting.

**Only run this if Phase 2 passes. Characterising a fragile signature is wasted effort — you need to know the edge is real before you try to understand it.**

---

### Phase 4 — Falsification & Regime Stress Test (After Characterization)

**Goal:** Verify the edge is not accidental and will survive regime changes in live trading.

**What to do:**
- Formulate a falsifiable hypothesis explaining why the edge works (e.g., "CMF detects accumulation, Volume Profile confirms support")
- Design a stress test that would *only fail* if your hypothesis is wrong — not by removing indicators, but by testing conditions that violate the hypothesis logic
- Run Phase 3's best config on out-of-sample data (2025-09-01 → present) held from phases 1–3
- Compare in-sample vs. out-of-sample SQN, PF, win rate — expect 20–30% degradation as normal

**Pass criteria:** Out-of-sample performance degrades by a tolerable margin relative to in-sample (some degradation is expected and normal); the falsification test fails under the conditions that should break the hypothesis, confirming the explanation holds.

**This is the real validation. Only move to live trading if Phase 4 passes. An edge you can explain survives regime changes; one you cannot will disappear without warning.**

### The Rule Going Forward

```
A combination is valid if it passes ALL of:

  ✅ Quality thresholds (Phase 1)
  ✅ Works on 3+ coins (cross-coin)
  ✅ Trades distribute across full data history (temporal)
  ✅ Edge survives filter isolation (characterization)
  ✅ Parameter surface is smooth not spiky (not curve fitted)

Only then does it move to Phase 4 and live testing
```

