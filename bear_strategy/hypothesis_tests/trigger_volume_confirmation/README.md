# Step 3 — Trigger Volume Confirmation

**Question:** Within a confirmed bear regime, does entering a short on a bar with *above-average volume* produce a better risk-adjusted edge than entering on normal/low volume?

---

## What this test does

Within every bar that passes the Step 1 regime filter (`ema_below_50`), we split candles into two populations based on volume relative to a rolling historical average:

| Population | Condition |
|---|---|
| `volume_triggered` | `volume > volume_mult × rolling_avg(volume_window)` |
| `not_triggered` | `volume ≤ volume_mult × rolling_avg(volume_window)` |

Each bar gets a simulated short: entry at bar close, stop = entry + 2×ATR, target = entry − 3×ATR. Outcome is determined by forward-scanning subsequent bars for whichever is hit first.

The verdict compares `volume_triggered` vs `not_triggered`. If `volume_triggered` clears the statistical thresholds on ≥ 3 of 4 pairs, the volume trigger is confirmed as an edge filter.

---

## Timeframe selection for bear shorts

`entry_tf` controls the candle resolution for entries, stops, targets, ATR sizing, and the volume rolling average.

| entry_tf | Trade style | Typical hold |
|---|---|---|
| `"15m"` | Intraday scalp | 15 min – 4 h |
| `"1h"` | Swing short ← **default** | 1–48 hours |
| `"4h"` | Position short | Days–weeks |

**Why 1h by default:**  
Volume spikes on 1h bars capture institutional participation without the extreme noise of sub-hour activity. On 4h bars the sample size drops significantly; on 15m bars the volume signal becomes very noisy and prone to false spikes from algorithmic activity.

**To change timeframe:**  
Edit `entry_tf` in `config.py`. Ensure matching parquet files exist at:  
`crypto_data/data/{PAIR}/{PAIR}_{entry_tf}_*.parquet`

No `context_tf` setting is needed for Step 3 — all calculations run on a single timeframe.

---

## How to run

```bash
source .venv/bin/activate
python -m bear_strategy.hypothesis_tests.trigger_volume_confirmation.run
```

---

## Output

Results are saved to:
```
bear_strategy/backtest/hypothesis_tests_raw/results/step3_trigger_check/
    step3_results_entry1h.csv   (filename reflects active entry_tf setting)
```

### CSV columns

| Column | Description |
|---|---|
| `pair` | Trading pair (e.g. BTCUSDT) |
| `population` | One of: `volume_triggered`, `not_triggered`, `all_regime` |
| `win_rate` | Fraction of trades that hit target before stop |
| `profit_factor` | Total gross profit / total gross loss |
| `avg_duration` | Mean bars from entry to exit |
| `n_trades` | Number of simulated trades |

---

## Pass/fail interpretation

**Verdict baseline:** `not_triggered`

A population **passes a pair** when all three hold:
1. `wr_lift > 2.5 × sqrt(p × (1-p) / n)` — WR gain is statistically significant
2. `pf_lift > noise_floor(n)` — PF gain exceeds sample-size-dependent floor (0.02/0.05/0.10)
3. `n_trades > 1000`

**Overall PASS:** ≥ 3 of 4 pairs (BTC, ETH, SOL, BNB) clear all thresholds.

If `volume_triggered` does not pass:
- Try adjusting `volume_window` (e.g., 10 or 50 bars)
- Try `volume_mult > 1.0` (e.g., 1.5×) for a stricter high-volume threshold
- Check if a different `entry_tf` changes the picture

---

## Look-ahead prevention

Volume look-ahead is prevented in `runner.py`:

- **Rolling average is shifted by 1 bar:** `rolling(window).mean().shift(1)` — at bar `t`, the average is computed over `[t−window, t−1]` only. pandas `.rolling().mean()` naturally includes bar `t` itself, so the `shift(1)` is mandatory.
- **NaN warmup guard:** bars where the rolling average is NaN (first `volume_window` bars) are excluded from both populations. This prevents warmup-period bars from artificially inflating one population.
- **Regime mask:** the daily signal is shifted by 1 before forward-fill onto the entry TF index (same pattern as Steps 1 and 2).
