# Step 2 — Setup Level Edge Check

---

## Overview

**What this test does:** Checks whether VPVR high-volume nodes and Anchored VWAP from the last swing high create genuine resistance within confirmed bear regimes — or whether they are decorative price labels with no edge.

**How it works:** Within regime-confirmed candles only, enter random shorts near setup levels vs. away from them. Measure win rate and profit factor in both populations. Near-setup must beat away-from-setup by more than a data-scaled noise floor.

**Regime rule for this step:** Keep the regime filter fixed to the winner from Step 1. Step 2 is testing whether setup adds edge on top of an already-validated regime, not whether a different regime definition works better. If you want to test different regime filters together with setup, run a separate interaction matrix after the base Step 2 verdict.

**Three things to implement:**
1. Classify every regime candle as near-setup or away-from-setup (within 0.5× ATR_4H of a VPVR HVN or Anchored VWAP above price)
2. Enter random shorts in both populations with fixed 2× ATR stop / 3× ATR target; record outcomes
3. Run the verdict logic — win-rate lift, PF lift, and trade count all must clear thresholds on ≥3 of 4 pairs

**Three secondary attacks after the primary:**
- VPVR alone vs. Anchored VWAP alone — cut the weaker one if combined doesn't outperform both
- Anchored VWAP age decay — win rate must fall as swing-high ages, or the trapped-buyer hypothesis is wrong
- Setup distance sweep (0.3×, 0.5×, 0.7× ATR) — find optimal threshold without overfitting

**Pass criterion:** At least one of `near_setup`, `vpvr_only`, or `vwap_only` clears all three thresholds on ≥3 pairs → Layer 2 confirmed, proceed to Step 3.  
**Fail criterion:** Nothing clears → reject Layer 2, revise the hypothesis.



---

## Purpose

Step 1 proved the regime filter creates directional skew. Step 2 attacks Layer 2 — the setup indicators.

**Question:** Do VPVR high-volume nodes and Anchored VWAP from the swing high create meaningful resistance within confirmed bear regimes? Or are they decorative price labels with no predictive power?

**Attack design:** Within regime-confirmed candles only, compare random short outcomes near setup levels (within 0.5× ATR_4H) versus away from setup levels. If the near-setup population does not beat the away-from-setup baseline by more than the data-scaled noise floor, Layer 2 is rejected and the hypothesis requires revision.

---

## Victory Conditions

A setup indicator passes if it meets **all three** of the following on **at least 3 of 4 test pairs** (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT):

1. **Win-rate lift exceeds the data-scaled minimum** — compute `min_pp = 2.5 × sqrt(p × (1−p) / n)`, where `p` is the away-from-setup baseline win rate and `n` is the smaller trade count between the two populations
2. **PF lift exceeds the sample-size noise floor** — require PF lift above `0.02` when `n > 50k`, `0.05` when `10k ≤ n ≤ 50k`, and `0.10` when `n < 10k`
3. **Trade count ≥ 1000 per pair** — minimum sample size gate stays fixed

**Secondary attacks:**

- **Individual vs. combined:** Test VPVR alone vs. Anchored VWAP alone vs. combined. If combined does not outperform the better individual component, the weaker one is cut.
- **Anchored VWAP age decay:** Stratify Anchored VWAP setups by swing-high age (in ATR-normalised units). If win rate does not decline as age increases, the trapped-buyer hypothesis is wrong.
- **Setup distance sweep:** Test different distance thresholds (0.3×, 0.5×, 0.7× ATR_4H) to find the optimal distance that maximises near-setup advantage without overfitting.

**Failure criterion:** If no setup indicator clears those thresholds on at least 3 pairs, Layer 2 is rejected. Return to the hypothesis document and redefine setup logic.

---

## Test Architecture

### Directory Structure

```
bear_strategy/
└── hypothesis_tests/
    └── setup_level_edge_check/              # Named after the question
        ├── __init__.py
        ├── config.py                        # Setup distance, thresholds, data range
        ├── entries.py                       # Logic to classify near-setup vs away
        ├── runner.py                        # Outcome engine specific to this test
        └── run.py                           # Entry point: python -m bear_strategy.hypothesis_tests.setup_level_edge_check.run
```

### Config Structure

```python
@dataclass
class TestConfig:
    # ---- Exit parameters (same as Step 1) ----
    stop_atr_mult: float = 2.0              # Stop at entry + 2× ATR
    target_atr_mult: float = 3.0            # Target at entry - 3× ATR
    atr_period: int = 14                    # ATR(14) on 15-min bars

    # ---- Setup distance threshold ----
    setup_distance_atr: float = 0.5         # 0.5× ATR_4H from VPVR/VWAP

    # ---- Victory thresholds ----
    significance_zscore: float = 2.5        # statistical guardrail for win-rate lift
    min_pf_diff_high_n: float = 0.02        # PF lift floor when smaller population > 50k
    min_pf_diff_mid_n: float = 0.05         # PF lift floor when smaller population is 10k-50k
    min_pf_diff_low_n: float = 0.10         # PF lift floor when smaller population < 10k
    min_trades_per_pair: int = 1000         # Minimum resolved trades

    # ---- Data ----
    data_dir: Path = Path("crypto_data/data")
    pairs: list[str] = field(default_factory=lambda: ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"])
    start_date: str = "2021-01-01"
    end_date: str = "2025-11-01"

    # ---- Output ----
    results_dir: Path = field(
        default_factory=lambda: Path(
            "bear_strategy/backtest/hypothesis_tests_raw/results/step2_setup_check"
        )
    )
```

---

## Look-Ahead Guardrails

This test uses 4H data to define setup context and 15-minute data to measure outcomes. That is fine, but only if every 15-minute bar sees information from completed 4H candles only.

**Rule 1: never use the currently forming 4H candle.** Any 4H ATR, VWAP anchor state, or VPVR state mapped onto the 15-minute grid must be shifted by one completed 4H bar before forward-fill.

```python
atr_4h_completed = df_4h['atr_14'].shift(1)
atr_4h_aligned = atr_4h_completed.reindex(df_15m.index, method='ffill')
```

Without that shift, every 15-minute candle inside the active 4H window would see information from an unfinished higher-timeframe bar.

**Rule 2: Anchored VWAP can only anchor from a confirmed swing high.** A swing high is not known in real time at the high itself. It becomes known only after subsequent 4H bars confirm that the high held. Use a confirmation rule such as `N` lower highs or closes after the candidate bar, then shift the swing-high signal forward so it becomes available only when confirmed.

```python
N = 3
candidate_is_highest = (
    df_4h['high']
    .rolling(N + 1)
    .apply(lambda window: window[0] == window.max(), raw=True)
)
confirmed_swing_high = candidate_is_highest.shift(N).fillna(False).astype(bool)
```

That means the anchored VWAP starts from the most recent confirmed swing high, not from a peak that is obvious only in hindsight.

**Rule 3: VPVR must be built from a trailing window only.** You do not need tick data for this. You do need to ensure the volume profile for each 15-minute decision point uses completed historical bars only and never future 4H or 15-minute candles.

If those three rules are followed, lack of tick data does not create look-ahead bias in Step 2. It only limits precision.

---

## Entry Classification Logic

Within regime-confirmed candles, classify each as **near-setup** or **away-from-setup** using:

```python
def classify_setup_population(
    df_15m: pd.DataFrame,
    df_4h: pd.DataFrame,
    setup_distance_atr: float,
) -> tuple[pd.Series, pd.Series]:
    """
    Classify 15-min candles as near-setup or away-from-setup.
    
    Near-setup: price within setup_distance_atr × ATR_4H of either:
      1. VPVR high-volume node above current price
      2. Anchored VWAP from last swing high
    
    Returns:
      (near_setup_mask, away_from_setup_mask)  — boolean Series on df_15m index
    """
        # Align the PREVIOUS completed 4H ATR to the 15m grid
        atr_4h_aligned = ...  # df_4h['atr'].shift(1).reindex(df_15m.index, method='ffill')
    
    # Compute distance from current price to VPVR HVN above
        dist_to_vpvr = ...  # For each 15min bar, nearest trailing-window HVN above current price
    
    # Compute distance from current price to Anchored VWAP
        dist_to_vwap = ...  # Distance to VWAP anchored from the latest CONFIRMED swing high
    
    # Near-setup if within threshold of EITHER level
    near_setup = (
        (dist_to_vpvr <= setup_distance_atr * atr_4h_aligned) |
        (dist_to_vwap <= setup_distance_atr * atr_4h_aligned)
    )
    
    away_from_setup = ~near_setup
    
    return near_setup, away_from_setup
```

**Key detail:** Distances are computed relative to current price. A level below current price is not "near setup" — we are looking for resistance above. Only resistance levels matter in a short setup.

**Second key detail:** `0.5 × ATR_4H` is not a prediction target. It is just the distance threshold that defines whether price is close enough to a resistance level to count as a setup candle. Example: if ATR_4H is 1000 and the nearest valid resistance is 400 above current price, that candle is near-setup. If resistance is 900 above, it is away-from-setup.

---

## Outcome Computation

For each population (near-setup, away-from-setup), enter shorts at close of every regime-confirmed candle in that population. Fixed 2× ATR stop, 3× ATR target. Scan forward until resolution.

```python
def compute_outcomes(
    df_15m: pd.DataFrame,
    entry_mask: pd.Series,      # near_setup or away_from_setup
    regime_mask: pd.Series,     # regime confirmed
    config: TestConfig,
) -> dict:
    """
    Vectorized outcome computation for setup-level test.
    
    Returns:
      {
          'win_rate': float,
          'profit_factor': float,
          'avg_duration': float,
          'n_trades': int,
      }
    """
    # Only enter on candles that are BOTH regime-confirmed AND in this setup population
    combined_mask = regime_mask & entry_mask
    
    # Vectorized forward-scan identical to Step 1
    # (same stop/target hit logic)
    
    return {
        'win_rate': wins / (wins + losses),
        'profit_factor': sum(wins) / sum(losses),
        'avg_duration': mean(durations),
        'n_trades': len(durations),
    }
```

---

## Per-Pair and Aggregated Results

**CSV Output Format:**

```
pair    , population       , win_rate , profit_factor , avg_duration , n_trades
BTCUSDT , all_regime       , 0.413    , 1.065         , 20.2         , 73819
BTCUSDT , near_setup       , 0.421    , 1.091         , 20.1         , 54320
BTCUSDT , away_from_setup  , 0.402    , 1.031         , 20.4         , 19499
BTCUSDT , vpvr_only        , 0.419    , 1.082         , 20.0         , 31245
BTCUSDT , vwap_only        , 0.423    , 1.101         , 20.3         , 23075
...
```

**Populations to test:**

- `all_regime` — baseline, all regime-confirmed candles (from Step 1 results)
- `near_setup` — within distance threshold of VPVR or VWAP
- `away_from_setup` — regime-confirmed but away from setup levels
- `vpvr_only` — near VPVR nodes only (secondary attack)
- `vwap_only` — near Anchored VWAP only (secondary attack)

---

## Verdict Logic

For each population, compute per-pair lifts against the `away_from_setup` baseline using the smaller trade count for the significance threshold:

```python
def evaluate_verdict(results: pd.DataFrame, config: TestConfig) -> None:
    """
    Falsification verdict against sample-size-aware thresholds.
    """
    df = results.reset_index()
    baseline = (
        df[df['population'] == 'away_from_setup']
        .set_index('pair')[['win_rate', 'profit_factor', 'n_trades']]
        .rename(
            columns={
                'win_rate': 'wr_base',
                'profit_factor': 'pf_base',
                'n_trades': 'n_base',
            }
        )
    )
    
    print("── Setup Level Edge Verdict ──\n")
    
    passing = []
    
    for pop in ['near_setup', 'vpvr_only', 'vwap_only']:
        pop_df = df[df['population'] == pop].set_index('pair')
        if pop_df.empty:
            continue
        joined = pop_df.join(baseline)
        joined['smaller_n'] = joined[['n_trades', 'n_base']].min(axis=1).astype(int)
        joined['wr_lift'] = joined['win_rate'] - joined['wr_base']
        joined['pf_lift'] = joined['profit_factor'] - joined['pf_base']
        joined['min_wr_lift'] = config.significance_zscore * np.sqrt(
            joined['wr_base'] * (1.0 - joined['wr_base']) / joined['smaller_n']
        )
        joined['min_pf_lift'] = np.select(
            [joined['smaller_n'] > 50_000, joined['smaller_n'] >= 10_000],
            [config.min_pf_diff_high_n, config.min_pf_diff_mid_n],
            default=config.min_pf_diff_low_n,
        )
        joined['pair_passes'] = (
            (joined['wr_lift'] > joined['min_wr_lift'])
            & (joined['pf_lift'] > joined['min_pf_lift'])
            & (joined['n_trades'] > config.min_trades_per_pair)
            & (joined['profit_factor'] > joined['pf_base'])
        )
        passing_pairs = int(joined['pair_passes'].sum())
        wr = joined['win_rate'].mean()
        pf = joined['profit_factor'].mean()
        wr_lift_pp = joined['wr_lift'].mean() * 100
        
        status = "✅" if passing_pairs >= 3 else "❌"
        
        print(
            f"  {pop:<20}  WR {wr*100:.1f}% (lift {wr_lift_pp:+.1f}pp)  "
            f"PF {pf:.3f}  pairs passing: {passing_pairs}/4  {status}"
        )
        
        if passing_pairs >= 3:
            passing.append((pop, pf))
    
    if passing:
        best_pop, best_pf = max(passing, key=lambda x: x[1])
        print(f"\n  ✅  SETUP EDGE CONFIRMED — {best_pop} creates predictive resistance.")
        print(f"      Best performer: {best_pop} (avg PF {best_pf:.3f})")
        print("      Proceed to Step 3 (trigger confirmation).")
    else:
        print(f"\n  ❌  SETUP EDGE NOT CONFIRMED — no setup level passes all thresholds.")
        print("      Layer 2 needs revision. Consider:")
        print("      • Adjusting setup distance threshold")
        print("      • Redefining resistance level computation")
        print("      • Increasing ATR buffer or target multiple to improve PF")
```

---

## Secondary Attacks — Implementation

Before running these attacks, keep the regime filter fixed. Do not swap EMA-only, VATS-only, or other regime variants inside the same Step 2 pass, because that confounds the question being tested. First answer: does setup add edge on top of the chosen regime? Only after that should you run a separate regime-by-setup interaction study.

### Attack 1: Individual vs. Combined

After primary populations pass, test VPVR alone vs. Anchored VWAP alone:

- If `vwap_only` PF > `near_setup` PF consistently, VPVR adds nothing — cut VPVR.
- If `vpvr_only` PF > `near_setup` PF consistently, Anchored VWAP adds nothing — cut VWAP.
- If `near_setup` combines both and outperforms both individual components, keep both.

Record the decision explicitly in the verdict output.

### Attack 2: Anchored VWAP Age Decay

Stratify results by swing-high age (measured in bars or ATR-normalised units):

```python
def test_vwap_age_decay(results_per_trade: pd.DataFrame) -> None:
    """
    Stratify VWAP setups by swing-high age.
    If win rate does NOT decline with age, trapped-buyer hypothesis is wrong.
    """
    vwap_trades = results_per_trade[results_per_trade['setup_type'] == 'vwap']
    
    # Age bins: 0–10 bars, 10–25 bars, 25–50 bars, 50+ bars
    vwap_trades['age_bin'] = pd.cut(
        vwap_trades['swing_high_age_bars'],
        bins=[0, 10, 25, 50, float('inf')],
        labels=['0-10', '10-25', '25-50', '50+']
    )
    
    age_results = vwap_trades.groupby('age_bin').agg({
        'win': 'mean',
        'pnl': 'mean',
    })
    
    print("  VWAP Win Rate by Anchor Age:\n")
    print(age_results.to_string())
    
    # Check if trend is downward as age increases
    if age_results['win'].iloc[-1] >= age_results['win'].iloc[0]:
        print("  ⚠️  Win rate does NOT decline with anchor age.")
        print("     Trapped-buyer hypothesis may be wrong; level works for different reason.")
    else:
        print("  ✅  Win rate declines with anchor age — trapped-buyer hypothesis holds.")
```

### Attack 3: Setup Distance Sweep

Test multiple distance thresholds to find optimal:

```python
def sweep_setup_distance(
    df_15m: pd.DataFrame,
    df_4h: pd.DataFrame,
    distances: list[float] = [0.3, 0.5, 0.7, 1.0],
) -> pd.DataFrame:
    """
    Sweep setup_distance_atr from 0.3× to 1.0× and measure outcomes.
    Tighter = fewer but higher-quality setups. Looser = more but lower-quality.
    """
    sweep_records = []
    
    for dist in distances:
        near_setup, away = classify_setup_population(df_15m, df_4h, dist)
        result_near = compute_outcomes(df_15m, near_setup, ...)
        result_away = compute_outcomes(df_15m, away, ...)
        
        sweep_records.append({
            'distance_atr': dist,
            'near_setup_pf': result_near['profit_factor'],
            'away_setup_pf': result_away['profit_factor'],
            'pf_lift': result_near['profit_factor'] - result_away['profit_factor'],
            'n_trades_near': result_near['n_trades'],
        })
    
    sweep_df = pd.DataFrame(sweep_records)
    print("\n── Setup Distance Sweep ──\n")
    print(sweep_df.to_string())
    
    # Find distance with best trade-off between PF and trade count
    best_idx = (sweep_df['pf_lift'] * sweep_df['n_trades_near']).idxmax()
    best_dist = sweep_df.loc[best_idx, 'distance_atr']
    
    print(f"\n  ✅  Optimal distance: {best_dist:.1f}× ATR")
    print(f"      Update config.setup_distance_atr to {best_dist:.1f}")
```

---

## Promotion to Permanent Code

If Step 2 passes:

1. **Extract** `classify_setup_population()` into `strategy/indicators/setup/` with proper indicator modules for VPVR and Anchored VWAP.
2. **Keep** the test harness in `hypothesis_tests/setup_level_edge_check/` until Step 3–5 pass. Then delete it.
3. **Do NOT** move the entire test runner to permanent code — only the indicator math gets promoted.

---

## Cleanup

Once verdict is final (pass or fail):

```bash
# If PASSED: Keep the temporary test for reference; proceed to Step 3
# If FAILED: Delete the test and revise Layer 2 in the hypothesis document
rm -rf bear_strategy/hypothesis_tests/setup_level_edge_check/
```

Update the hypothesis document with the verdict and decision (which indicator carried forward, which was cut).


