# Bear Strategy — From Hypothesis Test to Backtest

## 1. What was validated in the hypothesis test

`hypothesis_test_v2/oss_test/` tested one **promoted strategy stack** on unseen data (2023-11-02 → 2026-04-22):

| Layer | Component | Implementation |
|---|---|---|
| **Regime** | RSI(14) EMA(9) bear zone (30–50) on **1d** bars | `regime/indicators/rsi/rsi_bear_zone` |
| **Regime guard** | Funding-rate EMA(3) > 0 on **1h** bars (longs paying = shorts carry-safe) | `regime/indicators/combinations/rsi_bear_and_funding_bull` |
| **Trigger** | Session VP — POC failed-reclaim **or** HVN cross-below on **1h** bars | `trigger/indicators/vp_session_poc_or_hvn_break` |
| **Risk baseline** | SL = 2× ATR(7), TP = 3× ATR(7) | `oss_test/config.py → OOS_SHARED` |
| **Universe** | 9 USDT-margined perps (ADAUSDT … XRPUSDT) | `oss_test/config.py → PAIRS` |

The test measures **Profit Factor lift, Win-Rate z-score, and coverage** over a random baseline.  
Passing means the signal captures asymmetric short opportunity that is not noise.

---

## 2. What the backtest adds (and why it is separate)

The hypothesis test measures **signal quality** (does this filter select better-than-random entries?).  
The backtest measures **system performance** under realistic execution:

| Hypothesis test | VBT backtest |
|---|---|
| Raw outcome engine — no compounding | Full equity curve with compounding |
| Fixed ATR-based exit, no sizing | Risk-based position sizing (`risk_pct / sl_pct`) |
| No fees | Taker fees on entry **and** exit |
| No minimum filter | Min-SL distance filter (skips fee-dominated trades) |
| Signal logic only | Signal → size array → `Portfolio.from_signals` |

Nothing in `strategy/` re-implements the indicators; it imports and combines them.

---

## 3. The translation map (code)

```
hypothesis_test_v2/oss_test/config.py
        │
        │  stop_atr_mult, target_atr_mult, atr_period, pairs, OOS dates
        ▼
backtest/vectorbt/configs/default.py  ← ★ THE ONLY FILE YOU EDIT
        │  VbtRunConfig.to_parameters()
        ▼
strategy/parameters.py                ← pure dataclass, no I/O
        │  passed into
        ▼
strategy/signals.py                   ← compute_signals(df_1h, df_1d, funding_df, params)
        │  returns entry_signal, sl_pct, size arrays
        ▼
backtest/vectorbt/signals.py          ← shifts arrays +1 bar (fill at next open)
        │
        ▼
backtest/vectorbt/runner.py           ← vbt.Portfolio.from_signals(...)
        │
        ▼
backtest/vectorbt/metrics.py          ← extract_stats(pf) → standardised pd.Series
```

**Key translation decisions:**

- `context_tf: "1d"` in the OSS config → daily regime signal is `shift(1)` before `merge_asof` to 1h bars (no lookahead). Same logic in `hypothesis_test_v2/engine/alignment.py`.
- `stop_atr_mult / target_atr_mult` become vbt `sl_stop` / `tp_stop` as fractions of fill price (not absolute levels).
- Entries fire at `close[N]`; VBT fills at `open[N+1]` — consistent with the hypothesis test outcome engine.

---

## 4. Configuration reference

```
backtest/vectorbt/configs/
    default.py   ← single-run config  (pairs, dates, SL×, TP×, fees, sizing)
    sweep.py     ← SL/TP grid config  (sl_mults[], tp_mults[], min_trades)
```

Both files are self-documenting.  Change values in `build_config()` / `build_sweep_config()`.

**Date windows (match the hypothesis test splits exactly):**

| Window | Start | End |
|---|---|---|
| In-sample (dev) | 2021-01-01 | 2023-11-01 |
| Out-of-sample | 2023-11-02 | 2026-04-22 |

---

## 5. Running the backtest

```bash
# Single run (all pairs, default config)
python -m bear_strategy.backtest.vectorbt.run

# Override from CLI
python -m bear_strategy.backtest.vectorbt.run \
    --pairs BTCUSDT ETHUSDT --start 2023-11-02 --end 2026-04-22 \
    --sl-mult 2.0 --tp-mult 3.0

# SL/TP grid sweep
python -m bear_strategy.backtest.vectorbt.sweep_run

# Interactive dashboard
streamlit run bear_strategy/backtest/vectorbt/dashboard.py
```

Results land in `backtest/vectorbt/results/<timestamp>/`.

---

## 6. How to analyse the results

### What to look for first

| Metric | Minimum bar | Strong edge |
|---|---|---|
| **SQN** | > 0 | > 1.5 |
| **Profit Factor** | > 1.0 | > 1.5 |
| **Expectancy %** | > 0 | > 1% |
| **Win Rate %** | — | context-dependent (check R:R) |
| **Max Drawdown %** | < 40% | < 20% |
| **Sharpe Ratio** | > 0.5 | > 1.0 |

A good R:R trade system can have WR < 50% and still be profitable — always read WR alongside Expectancy and R:R Ratio together.

### Sweep analysis workflow

1. Run `sweep_run.py` on the **in-sample** window → pick top combos by `Breadth Score`.
2. **Breadth Score** = `avg_score × (pairs_passing / N_pairs)`.  It rewards combos that work on many pairs, not just one.
3. Shortlist 2–3 combos. Lock them in, do **not** re-optimise.
4. Run `run.py` on the **OOS window** with those combos.  Any degradation of > 50% in SQN or PF is a red flag.
5. A combo that passes on ≥ 6 / 9 pairs in OOS is considered robust.

### What the scoring formula weights

| Factor | Weight | Rationale |
|---|---|---|
| SQN | 22% | Captures both edge size and consistency (trade count) |
| Profit Factor | 18% | Direct measure of gross edge |
| Expectancy | 15% | Per-trade average outcome |
| Sharpe | 12% | Risk-adjusted return over time |
| Sortino | 10% | Same but penalises only downside volatility |
| Max Drawdown | 10% | Practical survivability |
| Calmar | 5% | Return relative to worst drawdown |
| Omega | 4% | Probability-weighted win/loss ratio |
| R:R Ratio | 4% | avg_win / \|avg_loss\| — trade structure quality |

### Red flags

- SQN **positive in-sample, negative OOS** → overfit signal, not genuine edge.
- Profit Factor driven by 1–2 outlier trades → check Best Trade % vs Avg Win %.
- Very high WR (> 75%) with poor Expectancy → likely large loss trades are hiding.
- Passes on only 1–2 pairs → pair-specific, not structural bear market edge.
