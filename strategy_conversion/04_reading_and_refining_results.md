# Phase 4 / 5 — Reading Results and Refining Toward a Tradable System

This guide answers the question: **"I have a robustness report and a folder of CSVs —
what do I do with them?"**

It covers:
1. What every output file is and what it contains
2. How to read each section of the robustness report
3. How to combine the four analytical lenses into a single decision
4. A decision flowchart: toggle changes vs. parameter sweep vs. move on
5. Worked example using the latest AMS results

---

## 1  The output files

After a VBT grid-search run you have:

```
backtest/results/results_vbt/<timestamp>/
├── BTCUSDT_4H.csv       ← one per symbol/timeframe pair
├── ETHUSDT_4H.csv
├── ...
├── run_vbt.log          ← timing, errors, combo counts
└── trades/              ← optional per-trade logs
```

After running `strategy_evaluation` you get:

```
<timestamp>_<label>_robustness.md
```

### The per-symbol CSV

Each row is one parameter combination.  Key columns:

| Column | What it measures |
|--------|-----------------|
| `Parameter Signature` | The exact flag/value combination for this row |
| `# Trades` | Total trades fired — below 20–30 is statistically meaningless |
| `SQN` | System Quality Number — the most important single metric |
| `Profit Factor` | Gross profit ÷ gross loss. Must be > 1.0 to make money |
| `Win Rate [%]` | % of trades that close in profit |
| `Expectancy [%]` | Average $ made per dollar risked. Must be positive |
| `Sharpe Ratio` | Return per unit of volatility |
| `Max Drawdown [%]` | Worst peak-to-trough loss — your pain threshold |
| `Return [%]` | Absolute return over the test period |
| `Rank` | Pre-computed rank (1 = best) within this symbol/TF |

**SQN reference scale** (Van Tharp):

| SQN | Verdict |
|-----|---------|
| < 0 | Losing system |
| 0–1 | Below par |
| 1–2 | Acceptable |
| 2–3 | Good |
| 3–5 | Excellent |
| > 5 | Superb (and suspicious — check for look-ahead) |

The raw CSV you should use for manual exploration or feeding back into analysis.
Do not use the top-N rows alone — read the distribution across the whole sheet.

---

## 2  The robustness report — section by section

### 2.1  Verdict (first thing to read)

| Verdict | Meaning | What to do |
|---------|---------|-----------|
| ✅ ROBUST | Meets all thresholds | Move to parameter sweep (Section 4) |
| ⚠️ MARGINAL | One target missed | Fix the one failing dimension first |
| ❌ WEAK | Two or more targets missed | Back to toggle redesign |

The verdict tells you *which phase you are in*, not how good the strategy is.
MARGINAL is not a failure — it means one specific thing needs fixing.

### 2.2  Pass rates

Two counts that must both reach ≥ 60 % for ROBUST:

- **Symbol pass rate** → is the strategy general across assets?
- **Timeframe pass rate** → is it general across time resolutions?

If one is low:

| Low dimension | Likely cause | First action |
|---------------|-------------|-------------|
| Symbol rate | Strategy is fitted to one asset's behaviour | Read which symbols fail; compare toggle frequency for failing vs. passing symbols |
| Timeframe rate | Indicator periods are wrong at the failing TF | Drop or re-parameterise indicators tuned to a specific period |

### 2.3  Avg SQN (long run)

This is the mean SQN of the top-1 combo per symbol/TF in the **long** dataset.
Target: ≥ 1.0 for viable, ≥ 1.5 for good.

A large gap between short-run SQN and long-run SQN suggests the strategy needs
more data to find its edge — 1–2 years of data is usually too little for daily/1h.

### 2.4  Decay table

Format: `symbol | TF | SQN short | SQN long | Δ SQN | Decayed`

Reading rules:
- **Δ SQN is positive** → strategy performs *better* on longer data → good, edge is improving with more data
- **Δ SQN is negative and absolute gap > 30 %** → performance decayed → the combo that worked in the development window does not hold up historically
- One or two decay flags are normal. More than 25 % flagged → the strategy has a regime-fitting problem.

### 2.5  Toggle Frequency

This is a naive count: *how often does each toggle appear in the top-5 combos
across all symbol/TF pairs?*

It is useful for a first-pass view but **misleading on its own** because:
- A toggle that always appears may be helping *or* it may simply be that very
  few valid combos can exclude it (structural selection bias).
- The frequency table does not tell you the *direction* of the effect.

Use this as a starting filter only.  Always cross-check with SHAP and OLS.

### 2.6  Toggle Importance (RandomForest)

The forest is trained to predict SQN from the toggle values.
Higher importance = that toggle explains more of the SQN variance across all combos.

This tells you **which toggles matter most**, but not whether turning them on helps
or hurts.  The OOB R² (out-of-bag R²) calibrates how much to trust the result:

| OOB R² | Trust level |
|--------|------------|
| > 0.3 | High — use these importances confidently |
| 0.1–0.3 | Medium — directionally useful |
| < 0.1 | Low — variance not well explained; flag combinations may be too correlated |

A negative OOB R² means the model is no better than guessing the mean — the importances
are unreliable for that run.

### 2.7  Toggle Impact (SHAP)

SHAP gives you both **magnitude** (how much does this toggle move SQN) and
**direction** (does enabling it raise or lower SQN).

**Correct interpretation:**
- **Positive Mean SHAP** → enabling this toggle pushes predicted SQN *above* the
  dataset average → enabling it **helps**
- **Negative Mean SHAP** → enabling this toggle pushes predicted SQN *below* the
  dataset average → enabling it **hurts**

> Note: the direction label in older report versions may be printed incorrectly.
> Always use the sign of the number: positive = helps, negative = hurts.

### 2.8  Toggle Significance (OLS)

OLS regression identifies whether a toggle's effect is statistically real or noise.

| Column | What it tells you |
|--------|-----------------|
| `Coefficient` | Average change in SQN when this toggle is switched ON |
| `p-value` | Probability the effect is random. < 0.05 = significant |
| `Significant ✅` | Effect is real with 95 % confidence |
| `Significant ⚠️` | Possible noise — do not rely on it for decisions |

OLS R² quantifies how well toggle choices (alone) explain the SQN variation.
Values of 0.05–0.20 are normal — SQN is noisy and many factors interact.

---

## 3  Combining the four lenses: the decision matrix

Read all four lenses together before making any change.
The table below maps every common signal pattern to a concrete action.

| Frequency | SHAP | OLS sig. | OLS coeff. | Interpretation | Action |
|-----------|------|----------|------------|----------------|--------|
| High | Positive | ✅ | Positive | Core edge — this toggle reliably improves results | **Pin to True** in `simple_config.py`; remove from grid |
| High | Negative | ✅ | Negative | Structural selection bias — combos that include this pass threshold even though it hurts at margin | **Pin to False** or reformulate the indicator |
| Low | Positive | ✅ | Positive | Occasionally useful when active, rarely selected | Keep in grid; add a parameter sweep version |
| Low | Negative | ✅ | Negative | This toggle is harmful and rarely selected | **Remove from grid** |
| Any | Any | ⚠️ | Any | Effect cannot be distinguished from noise | Leave unchanged; do not act on it until R² improves or you have more data |
| High RF importance, non-significant OLS | — | ⚠️ | — | The toggle interacts strongly with others but has no independent effect | Investigate interaction — try fixing the correlated toggle first |

**Worked example from AMS latest run:**

| Toggle | Freq rank | SHAP | OLS coeff | OLS sig | Decision |
|--------|-----------|------|-----------|---------|----------|
| `use_donchian` | Low (5/40) | −0.37 | −0.87 | ✅ | Strongest drag. Pin to False or replace the indicator |
| `use_adx` | High (40/40) | −0.01 | −0.36 | ✅ | High frequency but slight drag. Keep — removes bad trades even though marginal cost exists |
| `use_ema_ribbon` | Medium (12/40) | −0.09 | −0.22 | ✅ | Modest drag. Candidate for parameter tuning (period) before dropping |
| `use_volume_profile` | High (35/40) | +0.05 | +0.19 | ✅ | Both signal agree: this helps. **Pin to True** |
| `use_trailing_stop` | Medium (30/40) | −0.01 | −0.03 | ⚠️ | Not statistically significant. Leave in grid; do not act |
| `use_chandelier` | Medium (16/40) | −0.01 | −0.08 | ⚠️ | Not statistically significant. Leave in grid |
| `chandelier_atr_mult` | — | — | +0.39 | ✅ | Numerical parameter — higher multiplier improves SQN. Sweep a wider range |
| `cmf_threshold` | — | — | −4.10 | ✅ | Large negative coefficient — check if this is the CMF threshold being too tight. Try lower values |

---

## 4  The refinement decision flowchart

```
Run grid search (Phase 3)
        │
        ▼
Generate robustness report (Phase 4)
        │
        ▼
┌───────────────────────────────────────────┐
│ What is the verdict?                       │
└───────────────────────────────────────────┘
        │                   │               │
       WEAK              MARGINAL         ROBUST
        │                   │               │
 Fix symbol or     Fix the one               │
 timeframe pass    failing metric        ┌───▼────────────────────────────┐
 rate (see 4.1)    (see 4.2)             │ Read four-lens decision matrix  │
                                         │ (Section 3)                     │
                                         └───┬────────────────────────────┘
                                             │
               ┌─────────────────────────────┼──────────────────────────┐
               │                             │                          │
    Strong toggle signal        No strong toggle signal      Strategy already stable
    (significant SHAP + OLS)    but OLS R² < 0.10           (toggles decided, R² OK)
               │                             │                          │
         Apply toggle                 Increase data                Parameter sweep
         change (4.3)                 range and re-run             (Section 5)
               │
               ▼
         Re-run grid search
         Re-run robustness
         Compare to previous report
```

### 4.1  Fixing symbol pass rate

1. Group the failing symbols and look at what they have in common (volatility regime, correlation, token age).
2. Open the CSV for a failing symbol and compare the top-5 rows against a passing symbol. Are the toggle signatures similar or completely different?
3. If the toggle signatures are completely different → the strategy is too context-specific. Consider removing one regime filter.
4. If they are similar → the indicator periods may be wrong for that asset. Try a parameter sweep (Section 5).

### 4.2  Fixing timeframe pass rate

1h is almost always harder than 4H because noise dominates at shorter timeframes.

| Low-TF fix | How |
|------------|-----|
| Reduce fast indicators | EMA ribbon periods too short for 1h? Multiply all periods by 3 for a 1h test |
| Require more confirmations | Pin a second trigger flag to True on the smaller TF |
| Accept the TF is out of scope | Remove 1h from your test set and document the applicable range |

### 4.3  Making a toggle change and validating it

1. Open `strategy/<strategy>/backtest/simple_config.py`.
2. Make exactly **one** change at a time (pin one toggle, change one default).
3. Re-run the grid search.
4. Compare the new robustness report to the previous one.

**Signs you have improved:**
- avg SQN rises or holds steady
- The changed toggle no longer appears in the OLS significant-negative list
- Passing combo count increases

**Signs you have over-fitted:**
- One metric improves dramatically but others drop
- Decay count increases

---

## 5  When to switch from toggle tuning to parameter sweep

Move to numerical parameter sweep when:
- The robustness verdict is ✅ ROBUST
- Toggle frequency is stable across two consecutive runs (same flags in top combos)
- OLS shows one or more numerical parameters with significant positive coefficients

**How to run a parameter sweep**

In `simple_config.py`, replace the single default value with a list for the target parameter.
Example for `chandelier_atr_mult` which has a positive OLS coefficient (+0.39):

```python
# Before (single value)
chandelier_atr_mult: float = 3.0

# After (sweep)
chandelier_atr_mult: list[float] = [2.5, 3.0, 3.5, 4.0, 4.5]
```

Re-run the grid. The new results will show whether a higher multiplier consistently
produces higher SQN across symbols/timeframes or only helps on the development asset.

**What to look for in a parameter sweep result:**
1. Plot (or sort) SQN vs. parameter value. Is there a clear peak, or a flat plateau?
   - Peak → optimised value, pick the peak
   - Plateau → the parameter is not sensitive; use the middle of the plateau
   - Monotone → you have not swept wide enough; extend the range
2. Is the best value the same (or close) across multiple symbols?
   - Yes → it reflects a real market property; use it
   - No → it is over-fitted; revert to a neutral midpoint

Do **not** sweep all numerical parameters at once. Do them one at a time in order
of OLS coefficient magnitude (biggest effect first).

---

## 6  Knowing when to stop refining

Stop the iteration loop and move to Phase 6 (live deployment) when:

| Criterion | Target |
|-----------|--------|
| Robustness verdict | ✅ ROBUST on two consecutive data windows |
| Toggle decisions | Same 3–5 flags appear in top combos for 2+ consecutive runs |
| Numerical parameters | Sweeps show a stable, non-extreme optimum |
| Decay flags | < 25 % of symbol/TF pairs flagged |
| Avg SQN (long run) | ≥ 1.5 |
| Min # Trades per top combo | ≥ 30 across the validation window |

You do not need a perfect report. You need a *consistent* report — one that gives
the same answer across different data windows and different assets.

If you have been iterating for more than 4–5 cycles without consistent improvement,
the most likely causes are:
1. The core indicator (e.g. Donchian band for setup) does not have an edge on this asset
2. The test period contains a regime change (bull → bear) that breaks the setup logic
3. The exit layer is too tight — most trades stop out before they can express

---

## 7  Quick-reference: what to bring to an AI analysis session

When you want to analyse a report and get a next-step recommendation, paste:

1. The **Verdict** line and **Key Metrics** block
2. The **Toggle Significance (OLS)** table (the most signal-dense table)
3. The **Toggle Impact (SHAP)** table
4. The **Toggle Frequency** count
5. A one-line description of what you changed since the last run

With those four tables and the change note, the analysis can immediately cross-reference
all four lenses and produce a prioritised action list instead of generic advice.
