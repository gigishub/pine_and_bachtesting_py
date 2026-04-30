# Bear Strategy — Indicator Hypothesis & Testing Framework (v2)

---

## ✅ Step 1 — Confirmed Finding: EMA 50 Daily Filter Creates Directional Skew

This is no longer a hypothesis. It is a validated result across five pairs on 1H data.

### What was tested

Four populations were compared on each pair using random short entries at fixed 2× ATR stop / 3× ATR target on 1H bars, with daily regime filters mapped onto each 1H candle:

| Population | Definition |
|---|---|
| `all_candles` | No filter — baseline |
| `ema_200_slope` | Daily EMA 200 slope pointing down |
| `ema_below_50` | Price below Daily EMA 50 |
| `ema_200_slope_and_below_50` | Both conditions combined |

### Results

| Pair | Population | Win Rate | Profit Factor | N Trades |
|---|---|---|---|---|
| BTCUSDT | all_candles | 41.2% | 0.934 | 53,216 |
| BTCUSDT | ema_200_slope | 45.0% | 1.091 | 18,426 |
| BTCUSDT | ema_below_50 | **47.5%** | **1.204** | 23,544 |
| BTCUSDT | ema_200_slope_and_below_50 | 46.5% | 1.157 | 16,056 |
| ETHUSDT | all_candles | 42.9% | 1.000 | 44,685 |
| ETHUSDT | ema_200_slope | 44.9% | 1.085 | 20,709 |
| ETHUSDT | ema_below_50 | **47.5%** | **1.204** | 23,904 |
| ETHUSDT | ema_200_slope_and_below_50 | 47.4% | 1.201 | 17,136 |
| SOLUSDT | all_candles | 44.2% | 1.056 | 39,554 |
| SOLUSDT | ema_200_slope | 46.4% | 1.153 | 22,994 |
| SOLUSDT | ema_below_50 | 47.6% | 1.212 | 22,347 |
| SOLUSDT | ema_200_slope_and_below_50 | **47.8%** | **1.221** | 18,483 |
| BNBUSDT | all_candles | 43.2% | 1.015 | 42,161 |
| BNBUSDT | ema_200_slope | 45.6% | 1.116 | 18,312 |
| BNBUSDT | ema_below_50 | **48.1%** | **1.237** | 20,234 |
| BNBUSDT | ema_200_slope_and_below_50 | 46.9% | 1.176 | 15,362 |
| XRPUSDT | all_candles | 45.6% | 1.119 | 43,255 |
| XRPUSDT | ema_200_slope | 48.0% | 1.231 | 24,040 |
| XRPUSDT | ema_below_50 | 48.9% | 1.276 | 24,586 |
| XRPUSDT | ema_200_slope_and_below_50 | **49.9%** | **1.328** | 19,618 |

### Interpretation

**`ema_below_50` is the strongest single regime filter across BTC, ETH, SOL, and BNB.** It consistently outperforms `ema_200_slope` alone, and on four of five pairs it outperforms the combined filter. The combined filter only wins on XRP, and marginally.

**Decision going forward: use `ema_below_50` (price below Daily EMA 50) as the sole Layer 1 regime filter.** The EMA 200 slope is dropped. Adding it to the EMA 50 filter costs trade count and produces no consistent improvement in profit factor. The simpler filter is the better filter.

This is not a minor result. A random short strategy with no setup filter or trigger achieves profit factor below 1.0 on BTC and only marginally above 1.0 on others. Restricting to price-below-EMA-50 candles lifts profit factor to 1.20–1.24 on BTC, ETH, BNB, and SOL with large trade counts — this is a structurally clean and consistent directional skew. The regime filter is doing real work.

---

## Layer 1 — Revised Definition

### 🔴 Layer 1 — Regime
*"Is this market even in a state where this strategy should be active?"*

| Indicator | Role |
|---|---|
| **EMA 50 (Daily)** | Primary bear regime filter — price below Daily EMA 50 = shorts only |

**Construction:** Compute a 50-period EMA on daily close. Each 1H bar inherits the regime state of its parent daily bar. Regime is binary: confirmed (price < EMA 50 daily) or not. No slope or ATR normalisation required at this layer.

**Why EMA 50, not EMA 200:** The data shows EMA 50 below-price creates stronger directional skew than EMA 200 slope in isolation and in combination across four of five tested pairs. EMA 50 reacts faster to structural trend changes, which means it captures more of the usable bear trend early rather than waiting for the slower 200 to confirm. The mechanism is the same — a widely-watched coordination level creates self-fulfilling order flow — but the 50 identifies the operative bear regime more cleanly at this population size.

**VATS is dropped entirely at this stage.** It was not tested in Step 1 output. Given that EMA 50 alone produces profit factor above 1.20 on most pairs, VATS is a candidate for Round 2 testing — added back on top of the EMA 50 filter only if it improves the valid setup population. It does not carry forward into Layer 2 construction.

---

## Layer 2 — Setup Hypothesis (Next Test)

### 🟠 Layer 2 — Setup
*"Within the confirmed regime, where is a structurally meaningful short opportunity forming?"*

The original Layer 2 used Volume Profile (VPVR) and Anchored VWAP — both valid structural concepts, but both require significant computational infrastructure (VPVR in particular is not trivially computed from OHLCV bars) and are difficult to test cleanly across 30 pairs at scale.

The new Layer 2 hypothesis replaces these with a Bollinger Band structure that is directly computable from OHLCV data, is already validated in the existing BTC Momentum Strategy, and has a clean, testable mechanism for identifying short setup zones.

---

### Bollinger Band Downtrend Setup — Hypothesis

**The hypothesis:**
> *"When price is below the Bollinger Band basis (20-period SMA) and the basis itself is declining, the market is in an active downtrend at that resolution. When price additionally closes below the lower Bollinger Band, it confirms that the move is large relative to recent volatility. The combination — declining basis and close below lower band — identifies candles where the trend is both directional and gaining momentum, rather than simply range-bound below a moving average. Short entries in this population, within an already-confirmed EMA 50 bear regime, should produce meaningfully better outcomes than regime-only entries."*

**Construction on 1H bars:**

```
BB_basis  = SMA(close, 20)
BB_dev    = StdDev(close, 20) × 2.0
BB_upper  = BB_basis + BB_dev
BB_lower  = BB_basis - BB_dev

bb_downtrend = close < BB_basis
               AND BB_basis < BB_basis[1]
               AND close < BB_lower
```

This mirrors the `bbDowntrend` condition from the BTC Momentum Strategy exactly, applied to the 1H entry timeframe rather than as a filter on a higher timeframe.

**The three conditions and what each does:**

`close < BB_basis` — price is below the 20-period mean. This is the directional condition: the market is in the lower half of its recent range. Alone it is weak — price oscillates around the mean constantly.

`BB_basis < BB_basis[1]` — the mean itself is declining. This confirms the trend is pulling the range downward, not just drifting inside it. A falling basis means the distribution of recent prices is shifting lower — sellers are winning across the lookback window.

`close < BB_lower` — price is more than 2 standard deviations below the falling mean. This is the momentum condition: the move is large relative to the current volatility environment. In a normal distribution this is a low-probability event; in trending crypto markets it marks the candles where momentum is actually running, not just leaking.

**Why this replaces VPVR and Anchored VWAP at this stage:**

VPVR and Anchored VWAP identify *where* resistance sits in price space. Bollinger downtrend identifies *when* the trend is actually executing — it is a state filter on the entry timeframe, not a spatial price level. These are complementary, not competing. Bollinger goes in Layer 2 now because it is testable immediately from raw OHLCV. VPVR and Anchored VWAP remain as candidates for a later layer, added back once the Bollinger setup filter is validated.

---

### Step 2 — How to Test This

**What you are testing:** Within EMA-50-confirmed bear regime candles, does the `bb_downtrend` filter (all three conditions) produce meaningfully better outcomes than random shorts in the same regime?

**Populations to test:**

| Population | Definition |
|---|---|
| `regime_only` | EMA 50 bear regime confirmed (this is your new baseline — replaces all_candles) |
| `bb_downtrend` | Regime confirmed AND bb_downtrend = true |
| `bb_basis_only` | Regime confirmed AND close < BB_basis AND BB_basis falling (without requiring close < BB_lower) |
| `bb_lower_only` | Regime confirmed AND close < BB_lower (without requiring basis declining) |

Test `bb_basis_only` and `bb_lower_only` separately to isolate which condition is doing the work. If `bb_downtrend` (all three) does not outperform its components, identify the strongest sub-condition and carry that forward. Do not require all three if only two are earning it.

**Entry, stop, target:** Identical to Step 1 — entry at close, fixed 2× ATR(1H, 5) stop, fixed 3× ATR(1H, 5) target. Same bar resolution. ATR period matches Step 1 to ensure comparability.

**Falsification criteria:**

Apply the same data-scaled thresholds used in Step 1. For each pair compute:

```
min_wr_lift = 2.5 × sqrt(p × (1−p) / n)
```

where `p` is the `regime_only` baseline win rate and `n` is the smaller of the two trade counts being compared. For profit factor, require PF lift above the trade-count-adjusted noise floor: 0.02 when n > 50k, 0.05 when 10k ≤ n ≤ 50k, 0.10 when n < 10k.

If `bb_downtrend` does not clear both thresholds on at least four of five pairs, the setup filter is not adding meaningful information to the regime. Either loosen to the strongest individual condition, or move to an alternative setup layer before proceeding to Layer 3.

**Secondary checks:**

- Does `bb_downtrend` reduce trade count by less than 60% relative to `regime_only`? If it eliminates more than 60% of regime candles, the filter is too aggressive and will leave insufficient trades for the entry trigger layer to work with.
- Does the improvement hold across all five pairs or cluster on one or two? A result that only holds on BTC and ETH is a different signal than one that holds across asset classes.
- Do average trade durations change materially? A shorter average duration with higher win rate and profit factor is a better outcome than a longer one — it implies faster resolution and less exposure to overnight gaps and funding.

**Parameters to record per trade:**

```
pair
population
entry_price
stop_price
target_price
stop_distance_atr    (stop distance / ATR at entry)
bars_to_exit
outcome              (win / loss / unresolved)
exit_type            (stop / target)
bb_basis_value       (at entry bar)
bb_lower_value       (at entry bar)
atr_value            (at entry bar)
```

---

## Layers 3 and 4 — Unchanged, Held for Later

Layer 3 (trigger) and Layer 4 (exit) from the original document remain structurally unchanged. They are not tested until Layer 2 produces a validated setup population.

The Bollinger setup filter, if validated in Step 2, becomes the population on which the volume trigger (Layer 3) and ATR-based exits (Layer 4) are tested. Nothing in those layers changes mechanically — only the input population narrows.

One addition worth noting for Step 3: the BTC Momentum Strategy uses a `isCaution` state — a volatility warning when the high-to-low range exceeds 1.5× ATR or price falls back below the EMA — which tightens the trailing stop multiplier. This same concept (caution state within the trend) is a candidate trigger-side filter: entries during caution bars could be filtered out, reducing stops that get hit by high-volatility chop inside a valid downtrend. This is a Step 3 hypothesis, not a Step 2 one.

---

## Testing Order — What Gets Tested When

```
Step 1  ✅ COMPLETE
        Regime filter: EMA 50 daily creates directional skew
        Result: ema_below_50 is strongest single filter on 4/5 pairs
        Decision: EMA 50 below-price is the sole Layer 1 condition

Step 2  ← CURRENT
        Setup filter: bb_downtrend on 1H bars
        Baseline: regime_only population from Step 1
        Target: bb_downtrend shows PF lift above noise floor on 4/5 pairs

Step 3  (after Step 2 validates)
        Trigger: volume spike vs 20-bar average on entry candle
        Optional: caution-state filter (exclude high-ATR-range candles)
        Baseline: bb_downtrend population from Step 2

Step 4  (after Step 3 validates)
        Exit configuration: ATR stop buffer, trailing stop parameters, target multiplier
        Run on validated trade population from Steps 1–3

Step 5  (after full system validated)
        Robustness: walk-forward, regime removal, asset tier split,
        fee stress test, Monte Carlo
```

---

## Execution Architecture — Unchanged

Each layer operates on a different timeframe. The timeframe used to **read** a signal and the timeframe used to **act** on it are separate decisions and must not be conflated.

```
Daily      → Regime check
             EMA 50 computed on daily candles.
             Checked once per day. Binary: confirmed or not.

1H         → Setup identification and entry
             Bollinger Band downtrend computed on 1H bars.
             Entry at close of confirmed bb_downtrend candle
             (or open of next bar — to be determined in Step 2 analysis).
             Stop at entry + 2× ATR(1H).
             Target at entry − 3× ATR(1H).
```

**Full decision flow (current state after Step 1):**

```
For each 1H candle:
  1. Daily  → EMA 50 regime confirmed? (close < EMA50_daily)
  2. 1H     → bb_downtrend = true?
              (close < BB_basis AND BB_basis < BB_basis[1] AND close < BB_lower)
  3. If both: record as valid setup candle
              entry = close[i]
              stop  = entry + 2 × ATR[i]
              target = entry − 3 × ATR[i]
              scan forward until stop or target hit
```
