# Bear Strategy — Indicator Hypothesis & Testing Framework

---

## Round 1 — Indicators to Test First

These are the strongest indicators in the system. Each has a clean, directly testable hypothesis, a concrete mechanism that holds in crypto specifically, and no meaningful logical gaps. Test only these before adding anything else. Every combination test in Round 1 uses only indicators from this list.

| Layer | Indicator | Why it goes first |
|---|---|---|
| Regime | **EMA 200 Daily** | Self-fulfilling at scale, crypto participants watch it explicitly, most powerful single filter in the system |
| Regime | **VATS (slope/ATR)** | Mathematically grounded, normalises trend by volatility, directly tests trend-to-noise ratio — may replace ADX entirely |
| Setup | **VPVR — High Volume Nodes** | Behavioural mechanism is specific and testable — trapped buyers at known price levels create predictable supply walls |
| Setup | **Anchored VWAP from Swing High** | Best single addition — identifies exact average cost of trapped buyers, self-fulfilling as institutional desks use it explicitly |
| Trigger | **Volume Spike vs 20-bar average** | Directly distinguishes committed selling from passive drift — translates cleanly across all liquid crypto pairs |
| Exit | **ATR stop at swing high + 1× ATR buffer** | Structurally sound invalidation logic — swing high reclaimed = thesis dead, ATR buffer handles wick noise |
| Exit | **Volatility-Scaled ATR Target** | Fat-tailed crypto returns require dynamic targets — fixed R:R systematically cuts large moves and keeps marginal ones equally |

**Indicators held for Round 2** (added one at a time to the best Round 1 combination only): RSI 14, Chandelier Exit re-parameterised at 2× ATR / 14-period.

**Indicators held for Round 3** (only if Round 2 produces stable results): ADX 14, TTM Squeeze, OBV Divergence, Candle Efficiency. These are weaker or crypto-problematic — they get tested last and cut if they do not improve profit factor on the already-validated trade population.

---

## Layer Definitions

### 🔴 Layer 1 — Regime
*"Is this market even in a state where this strategy should be active?"*

| Indicator | Role |
|---|---|
| **EMA 200 (Daily)** | Primary bear market filter — price below = shorts only |
| **VATS — Volatility-Adjusted Trend State** | Confirms the trend has both strength and directional clarity relative to current volatility |

**VATS Construction:**
Compute a rolling 50-period linear regression slope of price, then divide by ATR(14). This normalises the trend signal by current volatility — a steep slope in a low-volatility environment is a much stronger regime signal than the same slope during a spike. If slope/ATR < −0.3, the regime is confirmed bearish *and* directional. This filters out choppy sideways bear markets where the strategy would get stopped out repeatedly.

---

### 🟠 Layer 2 — Setup
*"Where is the potential entry zone forming?"*

| Indicator | Role |
|---|---|
| **Volume Profile (VPVR — visible range)** | Identifies high-volume nodes above current price that act as resistance ceilings — shows exactly where the market found equilibrium last time and where sellers are likely to re-emerge |
| **Anchored VWAP from Last Swing High** | Dynamic resistance anchored to the most recent significant swing high — shows exactly where the average trapped buyer sits |

**Anchored VWAP note:** The resistance effect weakens as time passes from the swing high because trapped buyers either capitulate or average down. Test with a maximum lookback window — setups where the swing high is more than N candles old should be treated as weaker and potentially filtered.

---

### 🟡 Layer 3 — Trigger
*"What confirms the move is actually starting?"*

| Indicator | Role |
|---|---|
| **Volume vs. 20-bar average** | Entry candle volume must exceed the 20-bar average — sellers are committing, not drifting |
| **True CVD Divergence** | Built from intra-candle trade data — if price makes a higher local high on the bounce but CVD makes a lower high, sellers are absorbing the rally in real time |

**True CVD Construction from Lower Timeframe Data:**

The OHLCV approximation of CVD (using candle body/wick ratios to infer buy vs. sell volume) is unreliable in crypto because wicks are disproportionately large and distort the buy/sell inference. The correct approach uses intra-candle data from a lower timeframe to build genuine CVD.

Pull 1-minute or 5-minute OHLCV for each asset. For each sub-candle, classify volume as buy-initiated or sell-initiated using the tick rule approximation: if the sub-candle closed higher than it opened, classify the volume as buy volume; if lower, sell volume. Aggregate these sub-candle classifications across the bounce window to build CVD at 15-minute resolution.

```
For each 15min candle window:
  Sub-candles = all 1min candles within that 15min window
  Buy_volume  = sum of volume from sub-candles where close > open
  Sell_volume = sum of volume from sub-candles where close < open
  CVD_delta   = Buy_volume − Sell_volume
  CVD         = cumulative sum of CVD_delta over the bounce

Divergence confirmed when:
  Price makes higher high on bounce AND
  CVD makes lower high over same window
```

This eliminates the wick noise problem entirely because volume is classified at the sub-candle level where directional movement is unambiguous, then aggregated upward. The result is genuine volume flow data rather than a structural approximation.

**➕ Additional lower-timeframe signals for later exploration:**

**Candle Efficiency (from 5min sub-candles)**
For each 15min candle, compute the average efficiency of its five 5min sub-candles: Efficiency = (Close − Open) / (High − Low). If price is making higher highs on the bounce but average sub-candle efficiency is falling, the market is expending increasing effort for diminishing directional result. This is absorption measured through price structure rather than volume flow — a convergent signal to CVD divergence derivable from pure OHLCV at lower timeframe.

**OBV Divergence (from 5min data)**
Build OBV at 5-minute resolution across the bounce window. If price makes a higher high but 5-minute OBV makes a lower high, cumulative volume flow is not confirming the rally. Less sensitive to wick noise than OHLCV CVD approximation but less precise than true CVD. Useful as a cross-validation signal: if true CVD and OBV divergence both fire simultaneously, absorption confidence is materially higher than either alone.

---

### 🟢 Layer 4 — Exit
*"How does the trade end — both winners and losers?"*

| Indicator | Role |
|---|---|
| **ATR 14** | Sets initial stop distance — stop placed at swing high + 1× ATR_4H |
| **Volatility-Scaled Profit Target** | Dynamic target computed as entry price minus N × ATR(14), where N is calibrated to average sharp-drop magnitude in backtest |

**Initial stop:** Placed at swing high + 1× ATR_4H. This is structural — swing high reclaimed invalidates the short thesis. ATR buffer handles the reality that price wicks above levels before rejecting.

**Trailing stop:** Once the trade moves into profit, trail using an ATR-based ratchet. Parameters determined in exit testing — start at Chandelier defaults of 22-period / 3× ATR and test 14-period / 2× and 2.5× variants. The version that keeps you in the largest moves without giving back excessive profit on the valid trade population wins.

---

## The Hypothesis Behind Each Layer

### 🔴 Layer 1 — Regime

**EMA 200 (Daily)**
> *"In crypto, the 200 EMA is a coordination point watched by a large enough cohort of sophisticated participants that it genuinely affects order flow. When price is below it, the dominant flow of capital is net-selling. Shorting in alignment with that flow produces better outcomes than fighting it. The mechanism is self-fulfilling — it works because enough people act on it that their collective behaviour makes it real."*

**VATS (slope/ATR)**
> *"A steep negative slope relative to current volatility means the trend is large compared to the noise. When the trend-to-noise ratio is high, momentum strategies have room to breathe before a reversal hits your stop. When the ratio is low — same direction but high volatility — the trend is not dominating price movement and stop hunts are frequent. VATS distinguishes these two regimes where the 200 EMA alone cannot."*

---

### 🟠 Layer 2 — Setup

**Volume Profile / VPVR**
> *"High volume nodes represent price levels where a large amount of supply and demand previously exchanged hands. Trapped buyers from those nodes will sell to break even when price returns there, creating a predictable supply wall. This is not a lagging indicator — it is a map of where human pain and obligation sit in price space. The mechanism is behavioural and does not decay over time the way a moving average signal does."*

**Anchored VWAP from Swing High**
> *"The average buyer since the last swing high is underwater. When price rallies back to that average cost, those participants face a break-even decision and many will exit — creating a predictable resistance cluster. Unlike a rolling average, anchored VWAP does not move as time passes, which means the resistance level is stable and the behaviour it predicts is stable. The effect weakens as the swing high ages because trapped buyers either capitulate or average down, reducing the concentration of break-even sellers at that specific level."*

---

### 🟡 Layer 3 — Trigger

**Volume spike on entry candle**
> *"A drop on above-average volume means large participants are actively selling, not that price is drifting down passively. High volume drops are more likely to continue because they represent conviction — a real seller is committing size. Low volume drops often reverse because there is no genuine seller behind the move, just a vacuum. Relative volume normalises this comparison across assets with very different base volumes."*

**True CVD Divergence**
> *"If price makes a higher high on the bounce but the net volume flow — measured from sub-candle data — is making a lower high, sellers are absorbing the rally in real time. The price surface looks bullish but the underlying flow is bearish. This represents a measurable information asymmetry: buyers are pushing price up but sellers are matching or exceeding that buying with sell pressure that does not show on the 15-minute candle close. When the last buyers are exhausted the absorbed selling pressure is already in place and the drop resumes sharply."*

**Candle Efficiency (later exploration)**
> *"If successive candles on the bounce are making higher highs but converting a shrinking fraction of their total range into directional movement, the market is expending increasing effort for diminishing result. This is the mechanical signature of absorption — sellers resisting each push without yet overwhelming buyers. The efficiency collapse precedes the price reversal because it reflects the build-up of opposing pressure before it dominates."*

**OBV Divergence (later exploration)**
> *"If price makes a higher high on the bounce but OBV makes a lower high, the net cumulative flow of volume is not supporting the price move. This is a coarser version of CVD divergence that makes no intra-candle assumptions. Its value is as a cross-validation signal: when OBV divergence and true CVD divergence fire together, the absorption signal has two independent confirmations and confidence is materially higher than either alone."*

---

### 🟢 Layer 4 — Exit

**ATR-based stop at swing high**
> *"The swing high is the level that, if reclaimed, structurally invalidates the short thesis. A price closing above the swing high means buyers have overwhelmed sellers at the key reference point — the trade is wrong, not just temporarily adverse. The ATR buffer exists because price in crypto frequently wicks above a level by a small amount before rejecting — without it, valid trades get stopped by noise rather than by genuine thesis invalidation."*

**Volatility-Scaled ATR Target**
> *"Fixed R:R targets are contextually blind — they cut you out of 5R moves and keep you in 1R moves equally, treating all trades as identical. ATR expands when a real sharp drop is happening, which means a target scaled to N × ATR automatically stretches when the opportunity is large and tightens when volatility is low and the move is marginal. This keeps you in genuine momentum moves without specifying in advance how far they will go. The N multiplier is calibrated from the actual distribution of sharp-drop magnitudes in your backtest — it is not assumed."*

---

## The Testing Approach — Proving Yourself Wrong at Each Stage

The goal at every stage is **falsification, not confirmation.** Every test is designed to kill the hypothesis if it is wrong. The indicators that survive being attacked are the ones worth trading. A hypothesis you cannot attack is not a hypothesis — it is a belief.

All testing uses the full 30-pair universe. Data minimum: 3 years of 15-minute OHLCV covering the 2021 bull, 2022 bear, and 2023–2024 mixed regime. Regime and setup indicators precomputed on daily and 4H data and mapped onto the 15-minute timeline as static arrays before any backtest loop runs. All results reported with and without fees.

---

### Step 1 — Prove the Regime Filter Creates Directional Skew

**What you are testing:** Does EMA 200 + VATS < −0.3 create a measurable downward bias in outcomes independent of any setup or trigger?

**How to run it:** Enter shorts at random 15-minute candles across all 30 pairs. Apply a fixed 2× ATR stop and fixed 3× ATR target. Run twice — once restricted to confirmed regime candles, once across all candles. Record win rate, profit factor, and average trade duration for both populations.

**How to prove yourself wrong:** If win rate and profit factor in the regime population are not meaningfully higher than the unrestricted population, the regime filter is not creating directional skew. Do not proceed to Step 2 — rewrite Layer 1 first. Use data-scaled thresholds rather than fixed bars. For each pair, set the minimum meaningful win-rate lift to `2.5 × sqrt(p × (1−p) / n)`, where `p` is the baseline all-candle win rate and `n` is the smaller trade count between the two populations being compared. For profit factor, require PF lift above a trade-count-adjusted noise floor: `0.02` when `n > 50k`, `0.05` when `10k ≤ n ≤ 50k`, `0.10` when `n < 10k`. Keep the minimum trade-count gate in place.

**Secondary attack — isolate each regime indicator:** Test EMA 200 alone vs. VATS alone vs. combined. If the combined filter does not outperform either component alone, VATS is not adding to EMA 200 and gets cut. The stronger individual indicator carries forward.

---

### Step 2 — Prove the Setup Levels Are Not Random Resistance

**What you are testing:** Within confirmed bear regime only, do random shorts near VPVR HVNs or Anchored VWAP outperform random shorts at arbitrary regime-period locations?

**How to run it:** Classify every regime-confirmed 15-minute candle as near-setup (within 0.5× ATR_4H of a VPVR HVN or Anchored VWAP) or away-from-setup. Enter random shorts in both populations with fixed stops and targets. Compare win rate and profit factor.

**How to prove yourself wrong:** If near-setup win rate and profit factor do not beat away-from-setup by more than the same data-scaled thresholds, the levels are not providing meaningful resistance prediction and Layer 2 is decorative. For each pair, compute `min_pp = 2.5 × sqrt(p × (1−p) / n)` using the away-from-setup baseline win rate and the smaller trade count between the two populations. Require observed win-rate lift to exceed `min_pp`, require PF lift above the same trade-count-adjusted noise floor (`0.02` above 50k trades, `0.05` at 10k–50k, `0.10` below 10k), and keep the minimum trade-count gate. Test VPVR alone vs. Anchored VWAP alone — if one is doing all the work, the other gets cut and one indicator carries forward, not two.

**Secondary attack — test Anchored VWAP age decay:** Sort Anchored VWAP setups by the age of the swing high anchor point in ATR-normalised units. If win rate at Anchored VWAP does not decline as the anchor ages, the trapped-buyer hypothesis is wrong — the level is working for a different reason and the hypothesis needs revision.

---

### Step 3 — Prove the Volume Trigger Adds Information Beyond the Setup

**What you are testing:** From the valid setup population only, does requiring above-average volume on the trigger candle improve outcomes vs. entering on any candle in that population?

**How to run it:** Take every candle in the valid setup population. Split into triggered (volume > 20-bar average) and untriggered (volume ≤ 20-bar average). Enter shorts at the close of each and compare outcomes with fixed exits.

**How to prove yourself wrong:** If the triggered population does not beat the untriggered population by more than the same data-scaled win-rate and PF thresholds, the volume spike is reducing trade count without improving quality. Compute the minimum meaningful win-rate lift from the untriggered baseline using `2.5 × sqrt(p × (1−p) / n)`, use the smaller of the two trade counts as `n`, require PF lift above the same trade-count-adjusted noise floor, and keep the minimum trade-count gate. If it cannot clear those bars, cut it or replace it.

**CVD divergence test:** From the triggered population, further split into CVD-divergent and non-divergent. If CVD divergence does not improve outcomes on top of the volume trigger, the absorption hypothesis — despite being the strongest conceptually — is not detectable in your data at this resolution. Record the result explicitly and do not carry a signal that does not improve outcomes regardless of how sound the theory is.

**Convergence test:** Check whether trades where both volume spike and CVD divergence fire simultaneously outperform trades where only one fires. If the convergence premium is meaningful, require both as a combined trigger. If not, use volume alone and keep the system simple.

---

### Step 4 — Prove the Exits Are Not Arbitrary

**What you are testing:** On the validated trade population from Steps 1–3, which exit configuration produces the best risk-adjusted return across the fat-tailed crypto return distribution?

**ATR stop buffer:**
```
  1× ATR_4H buffer vs. 1.5× ATR_4H buffer
  Measure: how many valid trades does each stop out before target?
  Measure: does the wider buffer reduce valid-trade stop-outs without
           meaningfully increasing invalid-trade stop-outs?
```

**Trailing stop parameters:**
```
  Chandelier 22-period / 3× ATR  (baseline)
  Chandelier 14-period / 2.5× ATR
  Chandelier 14-period / 2× ATR  (most reactive)
  Measure: average profit captured on winning trades per variant
  Measure: profit given back before trailing stop fires
```

**ATR target multiplier:**
```
  Calibrate N from the actual distribution of sharp-drop magnitudes
  in the validated trade population.
  Test N at 25th, 50th, and 75th percentile of that distribution.
  Measure: which N produces the best profit factor without
           cutting large moves short?
```

**How to prove yourself wrong:** If the ATR-scaled target does not outperform a fixed 2R target on profit factor, the volatility-scaling hypothesis is wrong for your specific trade population. Use the fixed target. Theoretical elegance is not a reason to use an indicator that does not improve outcomes.

---

### Step 5 — Robustness Attacks on the Full System

These tests run after Steps 1–4 produce a complete system. Each one is designed to break the system, not validate it.

**Walk-forward test:** Divide data into 6-month blocks. Optimise on block 1, test blind on block 2. Re-optimise on blocks 1–2, test blind on block 3. Continue forward. If out-of-sample blocks show profit factor below 1.1 consistently, the system is overfit to a specific regime and not robust.

**Regime removal test:** Remove 2022 entirely. Test on 2021 and 2023–2024 only. If the system only works in a crash, it is not a strategy — it is a position on market structure that may not repeat.

**Asset tier split:** Run the full system separately on the top 10 pairs by liquidity and the bottom 20. If performance holds only on the top 10, effective sample size is 10, not 30. Size expectations and live deployment accordingly.

**Fee stress test:** Run the full system at 1.5× assumed fees — simulating slippage, wider spreads, and taker-only execution. If profit factor drops below 1.1 under stress, the edge is too thin to survive real execution conditions.

**Monte Carlo validation:** Take the actual sequence of trade returns from the validated system. Reshuffle randomly 10,000 times. For each shuffle compute profit factor and maximum drawdown. If the observed profit factor sits above the 95th percentile of the shuffled distribution, the result is statistically significant. Below the 90th percentile — the result is not distinguishable from a lucky sequence and the system needs more trades or a higher profit factor before live deployment.

---

## Execution Architecture — Where Each Layer Lives

Each layer operates on a different timeframe. The timeframe used to **read** a signal and the timeframe used to **act** on it are separate decisions and must not be conflated.

```
Daily      → Regime check
             200 EMA and VATS computed on daily candles.
             Checked once per day. Binary: confirmed or not.

4H         → Setup identification
             VPVR high-volume nodes and Anchored VWAP from last
             swing high identified on 4H chart.
             Price reaching and stalling at these levels on 4H
             confirms a setup exists. No entry here.

1min/5min  → Signal detection (liquid pairs only)
             True CVD divergence, OBV divergence, candle efficiency
             read at sub-candle resolution to catch absorption as it
             forms. Purely observational — no orders placed here.

15min      → Entry and stop execution
             Trigger confirmed on 15min candle close.
             Entry on next 15min candle open.
             Stop at 4H swing high + 1× ATR_4H.
             Trailing stop managed at 15min resolution.
```

**Full decision flow:**

```
For each 15min candle:
  1. Daily     → Regime confirmed? (EMA 200 + VATS < −0.3)
  2. 4H        → Price within 0.5× ATR of VPVR HVN or
                 Anchored VWAP from last swing high?
  3. 1min/5min → Absorption forming? (CVD divergence, OBV
                 divergence, candle efficiency declining)
  4. 15min     → Volume spike confirmed on candle close?
                 → Pass fee filter? (stop > minimum viable)
                 → If all yes: enter on next 15min open
                 → Stop at 4H swing high + 1× ATR_4H
                 → Trail with ATR ratchet at 15min resolution
```

**Optimal signal timeframe by asset tier:**

| Asset Tier | Signal Detection | Entry + Stop |
|---|---|---|
| BTC, ETH, top 5 by liquidity | 1min / 5min | 15min |
| Mid-tier pairs 6–15 | 5min / 15min | 15min |
| Altcoins 16–30 | 15min | 15min, higher min stop threshold |

---

## Fee Protection and Entry Edge Validation

### The Fee Drag Problem

Fee drag ratio is determined entirely by stop distance and fee rate. Position size cancels out completely — scaling down position size on compressed setups does not fix fee drag. The proportional destruction of edge is identical regardless of how much capital is risked.

```
Fee drag ratio = (Fee rate × 2) / Stop distance
```

A stop 0.2% from entry with 0.08% per side fee = 80% of risk consumed by fees before the market moves. This ratio is the same at 1% risk or 0.1% risk.

### ATR-Based Minimum Stop Filter

Every setup must pass this filter before entry. No position sizing adjustment replaces it.

**Minimum viable stop by asset tier:**

```
Minimum viable stop = (Fee rate × 2) / Max acceptable fee drag

Fee rates:
  Top 10 pairs, maker order:   0.02–0.04% per side
  Top 10 pairs, taker order:   0.05–0.08% per side
  Pairs ranked 11–30:          add 0.02–0.03% for spread

Max acceptable fee drag: 15% of risk

Example — top 10 pair, taker execution:
  (0.08% × 2) / 0.15 = 1.07% minimum stop distance
```

**ATR noise floor applied on top of fee threshold:**

```
Minimum stop = max(
    swing high + 1× ATR_4H distance from entry,
    1.5× ATR_15min
)
```

A stop inside 1.5× ATR_15min is inside the noise band of the entry timeframe and will be hit by random movement regardless of signal quality. If the structural stop fails either threshold, the setup is skipped entirely.

### Entry Edge Calculation Across Timeframes

**Record all entry prices simultaneously for every valid setup:**

```
4H_entry    = close of 4H candle confirming resistance
15min_entry = close of 15min trigger candle
5min_entry  = close of 5min trigger candle
1min_entry  = close of 1min trigger candle (theoretical ceiling)
```

**Normalise by 4H ATR for cross-asset comparability:**

```
Edge_15min = (4H_entry − 15min_entry) / ATR_4H
Edge_5min  = (4H_entry − 5min_entry)  / ATR_4H
Edge_1min  = (4H_entry − 1min_entry)  / ATR_4H
```

Edge should increase as timeframe decreases. If this relationship does not hold consistently, the lower timeframe is adding noise not precision — move back up.

**Net benefit — incremental edge must exceed incremental cost:**

```
Incremental edge  = Edge_5min − Edge_15min
Incremental cost  = trades filtered by fee threshold at 5min
                    vs 15min (tighter stops filter more trades)
Net benefit       = (incremental edge × surviving trades)
                    − (edge lost from additional filtered trades)
```

If net benefit is negative for an asset tier, use 15min signal detection for that tier.

### Required Backtest Output Per Trade

```
stop_distance_pct     → must exceed minimum viable stop
fee_drag_pct          → fees / risk — must be below 15%
entry_edge_vs_4H      → price improvement in ATR units
gross_pnl             → before fees
net_pnl               → after fees
signal_timeframe      → which timeframe triggered the entry
```

Run the full backtest twice — once with fees, once without. The delta between the two equity curves is the precise cost of the execution approach. If the fee-adjusted curve remains positive with profit factor above 1.3, the edge survives real costs. If it turns marginal, average stop distance must widen, trade frequency must fall, or maker order discipline must improve before live deployment.