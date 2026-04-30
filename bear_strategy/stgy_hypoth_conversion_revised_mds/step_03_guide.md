# Step 3 — Trigger Volume Confirmation Check

---

## Overview

**What this test does:** Checks whether requiring above-average volume on the entry candle improves short outcomes within the confirmed bear regime — or whether volume adds no information and only reduces trade count.

**How it works:** Within regime-confirmed candles only (the `all_regime` population from Step 1), split into volume-triggered vs not-triggered. Enter shorts at close of each. Measure win rate and profit factor in both populations. Volume-triggered must beat not-triggered by more than the data-scaled noise floor.

**Why Layer 2 is gone:** Step 2 falsified setup-level proximity entirely. Near-setup underperformed away-from-setup on all 4 pairs and all 3 populations. Layer 2 is removed from the system. Step 3 operates directly on the regime population — no setup gate applied before the trigger test.

**Three things to implement:**
1. Classify every regime-confirmed candle as `volume_triggered` (volume > 20-bar rolling average) or `not_triggered` (volume ≤ 20-bar rolling average)
2. Enter shorts at close of each population with fixed 2× ATR stop / 3× ATR target; record outcomes
3. Run the verdict logic — win-rate lift, PF lift, and trade count all must clear thresholds on ≥3 of 4 pairs

**Three secondary attacks after the primary:**
- CVD divergence sub-test — from the triggered population, split CVD-divergent vs non-divergent (requires 1m/5m data; absence does not block the primary verdict)
- Convergence test — check whether both volume spike and CVD firing together outperform either alone
- Volume multiple sweep (1.2×, 1.5×, 2.0× average) — find optimal threshold without overfitting

**Pass criterion:** `volume_triggered` clears all three thresholds on ≥3 of 4 pairs → Layer 3 volume signal confirmed, proceed to Step 4.  
**Fail criterion:** Does not clear → reject volume trigger, revise the hypothesis.

---

## Purpose

Step 1 proved the regime filter creates directional skew. Step 2 was run and rejected — setup-level proximity does not add edge. Step 3 now attacks Layer 3 directly against the regime population.

**Question:** Within confirmed bear regime candles, does entering only when volume exceeds the rolling 20-bar average produce better outcomes than entering on any regime-confirmed candle?

**Attack design:** Classify every regime-confirmed 15-minute candle as triggered or not. Compare short outcomes with fixed stops and targets. The triggered population must beat the not-triggered baseline by more than the data-scaled noise floor. If it cannot, the volume spike is filtering out candles without improving quality — it makes the system smaller without making it better, and it gets cut.

---

## Victory Conditions

The volume trigger passes if it meets **all three** of the following on **at least 3 of 4 test pairs** (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT):

1. **Win-rate lift exceeds the data-scaled minimum** — compute `min_pp = 2.5 × sqrt(p × (1−p) / n)`, where `p` is the `not_triggered` baseline win rate and `n` is the smaller trade count between the two populations
2. **PF lift exceeds the sample-size noise floor** — require PF lift above `0.02` when `n > 50k`, `0.05` when `10k ≤ n ≤ 50k`, and `0.10` when `n < 10k`
3. **Trade count ≥ 1000 per pair** — minimum sample size gate stays fixed

**Secondary attacks:**

- **CVD divergence sub-test:** From the triggered population, further split into CVD-divergent and non-divergent. Requires sub-candle (1m or 5m) data. If not available for all pairs, record that CVD was untested rather than blocking the primary verdict.
- **Convergence test:** If both volume spike and CVD divergence are available, test whether trades where both fire simultaneously outperform trades where only volume spike fires. If convergence premium clears the same thresholds, require both as a combined trigger. If not, use volume alone.
- **Volume multiple sweep:** Test volume thresholds at 1.2×, 1.5×, and 2.0× the 20-bar rolling average. Identify whether a tighter or looser threshold improves signal quality. Record the optimal value but do not tune to overfit — if improvement is marginal, keep the default 1.0× (i.e., > rolling average).

**Failure criterion:** If the triggered population does not clear those thresholds on at least 3 pairs, Layer 3 volume trigger is rejected. Return to the hypothesis document and redefine the trigger, or proceed directly to Step 4 and test exits on the raw regime population.

---

## Test Architecture

### Directory Structure

```
bear_strategy/
└── hypothesis_tests/
    └── trigger_volume_confirmation/      # Named after the question
        ├── __init__.py
        ├── config.py                     # Volume threshold, data range, thresholds
        ├── entries.py                    # Classify triggered vs not_triggered
        ├── runner.py                     # Outcome engine specific to this test
        └── run.py                        # Entry point: python -m bear_strategy.hypothesis_tests.trigger_volume_confirmation.run
```

### Config Structure

```python
@dataclass
class TestConfig:
    # ---- Exit parameters (same as Steps 1 and 2) ----
    stop_atr_mult: float = 2.0              # Stop at entry + 2× ATR
    target_atr_mult: float = 3.0            # Target at entry - 3× ATR
    atr_period: int = 14                    # ATR(14) on 15-min bars

    # ---- Volume trigger threshold ----
    volume_window: int = 20                 # Rolling window for average volume
    volume_mult: float = 1.0               # Trigger when volume > volume_mult × rolling_avg

    # ---- Victory thresholds ----
    significance_zscore: float = 2.5        # Statistical guardrail for win-rate lift
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
            "bear_strategy/backtest/hypothesis_tests_raw/results/step3_trigger_check"
        )
    )
```

---

## Look-Ahead Guardrails

This test operates entirely on 15-minute OHLCV data. There is no multi-timeframe mapping required for the primary test. The look-ahead risk is substantially lower than Step 2, but two rules still apply.

**Rule 1: volume rolling average must use only completed prior bars.** The rolling average must be computed with `min_periods=volume_window` and the comparison made at bar close. Do not include the current bar's volume in its own average.

```python
rolling_avg_vol = df_15m['volume'].rolling(window=config.volume_window, min_periods=config.volume_window).mean()
volume_triggered = df_15m['volume'] > (config.volume_mult * rolling_avg_vol)
```

The rolling mean at bar `t` automatically uses bars `t - window` through `t - 1` when operating on a completed series. No explicit shift is needed here because the current bar's volume is measured at its own close and the rolling window is computed over prior bars. Confirm this holds in your implementation before running.

**Rule 2: regime mask must come from Step 1 output.** Do not recompute the regime in this harness. Load the regime mask from the Step 1 results (or recompute with the exact same logic using `.shift(1)` on daily signals mapped to 15-minute bars). The regime confirmed at bar `t` must be based on daily data through the close of the day ending before bar `t`.

```python
# Regime signal is already computed and aligned correctly if loaded from Step 1 output.
# If recomputing: shift the daily EMA and VATS flags by 1 before ffill onto 15m index.
regime_daily_shifted = df_daily['regime_confirmed'].shift(1)
regime_15m = regime_daily_shifted.reindex(df_15m.index, method='ffill').fillna(False)
```

No ATR timeframe alignment issues exist here — ATR is computed directly on the 15-minute series and used at the same resolution as the entry.

---

## Entry Classification Logic

Within regime-confirmed candles, classify each as `volume_triggered` or `not_triggered`:

```python
def classify_trigger_population(
    df_15m: pd.DataFrame,
    regime_mask: pd.Series,
    config: TestConfig,
) -> tuple[pd.Series, pd.Series]:
    """
    Classify regime-confirmed 15-min candles by volume trigger.

    volume_triggered: regime confirmed AND volume > volume_mult × rolling_avg
    not_triggered:    regime confirmed AND volume <= volume_mult × rolling_avg

    Returns:
        (volume_triggered_mask, not_triggered_mask) — boolean Series on df_15m index
    """
    rolling_avg = df_15m['volume'].rolling(
        window=config.volume_window,
        min_periods=config.volume_window,
    ).mean()

    vol_spike = df_15m['volume'] > (config.volume_mult * rolling_avg)

    volume_triggered = regime_mask & vol_spike
    not_triggered = regime_mask & ~vol_spike

    return volume_triggered, not_triggered
```

**Key detail:** Both populations are subsets of the same `all_regime` population from Step 1. The `not_triggered` population is the baseline — the question is whether `volume_triggered` outperforms it. There is no notion of setup proximity here; the split is purely on volume.

**No exclusion for NaN rolling windows:** Bars within the first `volume_window` candles of the dataset will have a NaN rolling average. These are automatically excluded from both populations because the comparison `volume > NaN` evaluates to False and `~False` with a NaN is not cleanly handled. Use `rolling_avg.notna()` as an additional guard in the regime mask to be explicit.

```python
valid_window = rolling_avg.notna()
volume_triggered = regime_mask & valid_window & vol_spike
not_triggered = regime_mask & valid_window & ~vol_spike
```

---

## Outcome Computation

For each population, enter shorts at close of every candle in that population. Fixed 2× ATR stop, 3× ATR target. Scan forward until resolution.

```python
def compute_outcomes(
    df_15m: pd.DataFrame,
    entry_mask: pd.Series,
    config: TestConfig,
) -> dict:
    """
    Vectorized outcome computation for trigger confirmation test.

    Inputs:
        df_15m     — 15-min OHLCV with precomputed 'atr_14' column
        entry_mask — boolean Series of entry candles (already regime-filtered)
        config     — TestConfig

    Returns:
        {
            'win_rate': float,
            'profit_factor': float,
            'avg_duration': float,
            'n_trades': int,
        }
    """
    entry_prices = df_15m.loc[entry_mask, 'close']
    atrs = df_15m.loc[entry_mask, 'atr_14']

    stop_levels = entry_prices + config.stop_atr_mult * atrs
    target_levels = entry_prices - config.target_atr_mult * atrs

    # Vectorized forward-scan: for each entry, step forward through df_15m
    # until close >= stop (loss) or close <= target (win) — same engine as Step 1.

    return {
        'win_rate': wins / (wins + losses),
        'profit_factor': sum(wins) / sum(losses),
        'avg_duration': mean(durations),
        'n_trades': len(durations),
    }
```

The forward-scan engine is identical to the one used in Steps 1 and 2. Reuse it directly rather than reimplementing it — copy the outcome engine from `setup_level_edge_check/runner.py` if it has not already been moved to a shared location.

---

## Per-Pair and Aggregated Results

**CSV Output Format:**

```
pair    , population        , win_rate , profit_factor , avg_duration , n_trades
BTCUSDT , all_regime        , 0.413    , 1.065         , 20.2         , 73819
BTCUSDT , volume_triggered  , 0.428    , 1.102         , 19.8         , 38245
BTCUSDT , not_triggered     , 0.398    , 1.027         , 20.6         , 35574
ETHUSDT , all_regime        , ...
...
```

**Populations to output:**

- `all_regime` — baseline carried from Step 1, all regime-confirmed candles
- `volume_triggered` — regime confirmed AND volume > rolling average
- `not_triggered` — regime confirmed AND volume ≤ rolling average

**Secondary attack populations (only if sub-candle data is available):**

- `vol_and_cvd` — volume triggered AND CVD divergence confirmed
- `vol_only` — volume triggered AND no CVD divergence
- `cvd_only` — CVD divergence confirmed AND no volume trigger (diagnostic, not a pass candidate)

---

## Verdict Logic

Compare `volume_triggered` against the `not_triggered` baseline. Use the smaller trade count for the significance threshold.

```python
def evaluate_verdict(results: pd.DataFrame, config: TestConfig) -> None:
    """
    Falsification verdict for trigger volume confirmation test.
    """
    df = results.reset_index()
    baseline = (
        df[df['population'] == 'not_triggered']
        .set_index('pair')[['win_rate', 'profit_factor', 'n_trades']]
        .rename(
            columns={
                'win_rate': 'wr_base',
                'profit_factor': 'pf_base',
                'n_trades': 'n_base',
            }
        )
    )

    print("── Trigger Volume Confirmation Verdict ──\n")

    passing = []

    for pop in ['volume_triggered', 'vol_and_cvd', 'vol_only']:
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
            f"  {pop:<22}  WR {wr*100:.1f}% (lift {wr_lift_pp:+.1f}pp)  "
            f"PF {pf:.3f}  pairs passing: {passing_pairs}/4  {status}"
        )

        if passing_pairs >= 3:
            passing.append((pop, pf))

    if passing:
        best_pop, best_pf = max(passing, key=lambda x: x[1])
        print(f"\n  ✅  VOLUME TRIGGER CONFIRMED — {best_pop} adds information beyond regime.")
        print(f"      Best performer: {best_pop} (avg PF {best_pf:.3f})")
        print("      Proceed to Step 4 (exit calibration) using the triggered population.")
    else:
        print(f"\n  ❌  VOLUME TRIGGER NOT CONFIRMED — no trigger population passes all thresholds.")
        print("      Layer 3 needs revision. Consider:")
        print("      • Adjusting the volume multiple threshold (1.2×, 1.5×, 2.0×)")
        print("      • Testing a different volume normalisation window (10, 20, 50 bars)")
        print("      • Proceeding to Step 4 on the raw all_regime population without a trigger gate")
```

---

## Secondary Attacks — Implementation

### Attack 1: CVD Divergence Sub-test

This attack requires sub-candle data (1-minute or 5-minute OHLCV) to compute true CVD. If that data is not available for all 4 pairs across the full date range, **skip this attack and record it as untested** in the results output. Do not fabricate a proxy from 15-minute data — that is not CVD divergence.

If data is available:

```python
def compute_cvd_divergence_mask(df_1m: pd.DataFrame, df_15m: pd.DataFrame) -> pd.Series:
    """
    Identify 15-min bars where price makes a local higher high on the bounce
    but net cumulative delta (buy volume - sell volume) makes a lower high.

    True CVD requires bid/ask volume split from sub-candle data.
    Approximation: use (close > open) * volume as buy volume proxy,
    but record that this is an approximation, not true CVD.
    """
    ...
```

From the `volume_triggered` population, split into `vol_and_cvd` (both fire) vs `vol_only` (volume only). Apply the same verdict thresholds. If `vol_and_cvd` outperforms `vol_only` by more than the noise floor, require both as a combined trigger. If not, use volume alone and note that CVD divergence was tested but did not improve on volume spike.

### Attack 2: Convergence Test

After both primary and CVD sub-tests are complete, run the convergence check:

- `vol_and_cvd` vs `volume_triggered`: Is there a meaningful convergence premium?
- Use the same z-score and PF lift thresholds as the primary verdict.
- If the premium is confirmed on ≥3 pairs, the combined trigger is the carry-forward signal.
- If not confirmed, use volume spike alone. Simplicity wins when evidence is ambiguous.

### Attack 3: Volume Multiple Sweep

Re-run the classification using three alternative thresholds:

```python
for mult in [1.2, 1.5, 2.0]:
    config.volume_mult = mult
    # re-run and record outcomes
```

Compare the volume-triggered populations at each threshold:

- If a higher multiple improves PF and win rate while keeping n_trades above the 1000-per-pair floor, record the optimal multiple explicitly.
- If improvement is marginal (PF lift < 0.01 across pairs), keep the default 1.0× and note that threshold tuning adds no value.
- Do not select the threshold that maximises per-pair performance — that is curve fitting. Use the threshold that shows consistent improvement across all 4 pairs.

---

## Promotion and Cleanup

### If Step 3 Passes

1. The volume trigger logic in `entries.py` becomes a permanent indicator. Move the computation to `bear_strategy/strategy/indicators/trigger/volume_spike.py`.
2. The function signature must follow the permanent code convention — zero I/O, pure input/output, no side effects.
3. Write a unit test in `bear_strategy/tests/test_indicators.py` covering the volume trigger classification with known inputs.
4. Update `bear_strategy/strategy/decision/entry.py` to include the volume trigger gate alongside the regime check.

### If Step 3 Fails

1. Delete the entire `bear_strategy/hypothesis_tests/trigger_volume_confirmation/` directory. It is a throwaway harness.
2. Record the failure verdict and root cause in `bear_strategy_rundown_+_hypothesis.md` under Layer 3.
3. Decide: proceed to Step 4 using the raw `all_regime` population, or revise Layer 3 and re-test with a different trigger definition before advancing.

### What Goes Where

```
bear_strategy/hypothesis_tests/trigger_volume_confirmation/   ← temporary harness, DELETE after verdict
bear_strategy/backtest/hypothesis_tests_raw/results/step3_trigger_check/   ← permanent results, KEEP
bear_strategy/strategy/indicators/trigger/volume_spike.py     ← permanent logic (only if passed)
bear_strategy/tests/test_indicators.py                        ← permanent test (only if passed)
```

The results CSV stays permanently — it is the falsification record. The harness code is throwaway the moment the verdict is in.

---

## Known Limitation: CVD on OHLCV Data

True CVD divergence requires knowing which volume traded at the bid versus at the ask on each sub-candle tick. Standard OHLCV data does not provide this. The primary test in Step 3 therefore uses only volume spike (available from 15-minute OHLCV). The CVD attack is a secondary check run only when 1-minute OHLCV is available.

If you approximate CVD using candle direction (e.g., `(close > open) * volume` as buy proxy), record that explicitly in the output. An approximation can be tested, but it must be labelled as an approximation and its result interpreted with that caveat. An untested CVD divergence does not block the primary verdict. Volume spike alone is a complete, self-contained test for Step 3.
