# Step 2 — Setup Level Edge Check

**Question:** Does entering a short *near* a known supply zone (VPVR HVN or Anchored VWAP) produce a better risk-adjusted edge than entering away from those levels — within a confirmed bear regime?

---

## What this test does

Within every bar that passes the Step 1 regime filter (`ema_below_50`), we split candles into populations based on proximity to two supply-zone indicators:

| Population | Condition |
|---|---|
| `all_regime` | Any bar inside the bear regime |
| `near_setup` | Within `setup_distance_atr × ATR_context` of the nearest VPVR HVN **or** Anchored VWAP |
| `away_from_setup` | Regime-confirmed but outside the proximity threshold |
| `vpvr_only` | Near VPVR HVN only (not AVWAP) |
| `vwap_only` | Near Anchored VWAP only (not VPVR) |

Each bar gets a simulated short: entry at bar close, stop = entry + 2×ATR, target = entry − 3×ATR. Outcome is determined by forward-scanning subsequent bars for whichever is hit first.

The verdict compares `near_setup` vs `away_from_setup` (and the individual components). If `near_setup` clears the statistical thresholds on ≥ 3 of 4 pairs, the setup edge is confirmed and the strategy proceeds to Step 3.

---

## Timeframe selection for bear shorts

`entry_tf` controls the candle resolution for entries, stops, targets, and ATR sizing.  
`context_tf` controls the resolution for VPVR, Anchored VWAP, and ATR proximity signals.

| entry_tf | context_tf | Trade style | Typical hold |
|---|---|---|---|
| `"15m"` | `"4h"` | Intraday scalp | 1–8 hours |
| `"1h"` | `"4h"` | Swing short ← **default** | 4–48 hours |
| `"4h"` | `"1d"` | Position short | Days–weeks |

**Why 1h + 4h by default:**  
Swing shorts benefit from a context window wide enough to identify meaningful supply zones (4h HVNs and AVWAP anchors) while keeping entries precise enough to avoid excessive slippage (1h bars). Smaller entry TFs increase noise in the setup classification and require extremely tight stops. Larger entry TFs reduce sample size significantly.

**To change timeframe:**  
Edit `entry_tf` and `context_tf` in `config.py`. Ensure matching parquet files exist at:  
`crypto_data/data/{PAIR}/{PAIR}_{tf}_*.parquet`

---

## How to run

```bash
source .venv/bin/activate
python -m bear_strategy.hypothesis_tests.setup_level_edge_check.run
```

---

## Output

Results are saved to:
```
bear_strategy/backtest/hypothesis_tests_raw/results/step2_setup_check/
    step2_results_entry1h_context4h.csv   (filename reflects active TF settings)
```

### CSV columns

| Column | Description |
|---|---|
| `pair` | Trading pair (e.g. BTCUSDT) |
| `population` | One of: `all_regime`, `near_setup`, `away_from_setup`, `vpvr_only`, `vwap_only` |
| `win_rate` | Fraction of trades that hit target before stop |
| `profit_factor` | Total gross profit / total gross loss |
| `avg_duration` | Mean bars from entry to exit |
| `n_trades` | Number of simulated trades |

---

## Pass/fail interpretation

**Verdict baseline:** `away_from_setup`

A population **passes a pair** when all three hold:
1. `wr_lift > 2.5 × sqrt(p × (1-p) / n)` — WR gain is statistically significant
2. `pf_lift > noise_floor(n)` — PF gain exceeds sample-size-dependent floor (0.02/0.05/0.10)
3. `n_trades > 1000`

**Overall PASS:** ≥ 3 of 4 pairs (BTC, ETH, SOL, BNB) clear all thresholds.

**Component decision guide:**
- Both `vpvr_only` and `vwap_only` pass → keep both
- Only one passes → cut the other; do not stack components that don't independently contribute
- Only `near_setup` (combined) passes → both required together; neither is sufficient alone

---

## Look-ahead prevention

All look-ahead protection is applied in `runner.py` at a single point (`_align_4h_to_1h`):

- **4H signals are shifted by 1 bar** before being forward-filled onto the entry TF index. At any 1h bar during 4H bar T, only the signal from T−1 is visible.
- **VPVR** uses a trailing window `[t−window, t−1]` — the current bar is never included in its own profile.
- **Anchored VWAP** anchors only to *confirmed* swing highs (requires `swing_confirmation_bars` subsequent bars to confirm), preventing hindsight anchoring.
- **ATR (entry TF)** is computed with standard EWM; no shift needed because it uses past closes only.
