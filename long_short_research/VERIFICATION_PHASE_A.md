# Phase A — Top-down edge check, point-in-time top 10, daily

Run: `python sanity.py`, then `python run_layers.py` (from `long_short_research/`, with `../.venv`).

## Engine sanity: random, peek, delisting
- Universe: top 10 Binance spot USDT pairs by 180-day median dollar volume, ≥ 180 days listed. 57 coins were ever
  in it (incl. delisted BCC, BCHABC, BTT, LUNA, FTM, MATIC and memecoins PEPE, BONK, WIF, TRUMP, NEIRO, 1000SATS).
- Known answer: BTC 20-day forward return matches a hand calculation. Delisted coins exit at their last close.
- Random 50% signal: lift 0.000 long / -0.001 short, p_shift ≈ 0.5 → fail (correct).
- Peeking signal (sign of the future return): lift huge, 22/22 and 25/25 coins, 5/5 years → pass (correct).
- **Drift baseline (train 2018–2022, 20-day hold, 0.2% round trip):** long PF 1.24 (mean +2.0%), short PF 0.77
  (mean -2.4%). A short signal must turn a losing population into a winning one.
- Bug fixed: PF with no losing samples returned NaN instead of infinity.

## Regime layer: BTC trend filters sort years, btc_ret20 only survivor
Run: `python run_layers.py regime` → `results/regime_L-all_S-all.csv`. Train, baseline = all universe days.
- 12 BTC/market regime ideas (BTC above EMA 50/100/200/240, BTC 20/60/120-day return, 20d ≥ -3%, EMA50/200 cross,
  live-bot filter, breadth above EMA 50/100), each tested as a long filter and as a short filter.
- Pooled lifts are large (long +0.14 … +0.73, short +0.09 … +0.49), but random time-shifts of the same signal
  often do as well (p_shift 0.03–0.43) and the lift holds in only 0–3 of 5 years.
- **Why:** per-year check (btc_above_ema100, btc_ret20, btc_bot_filter): inside a year the filtered days rarely
  beat that year's baseline. The pooled lift comes from being long in 2020–21 and short in 2018/2022, i.e. a few
  regime swings. Few independent observations → weak statistics.
- Only **btc_ret20** (long if BTC 20-day return > 0, short if < 0) passes, on both sides, at p_shift = 0.05. Promoted.

## Setup layer: coin trend adds nothing over btc_ret20
Run: `python run_layers.py setup --long-base btc_ret20 --short-base btc_ret20`. Train.
- 12 coin-level ideas (coin above EMA 20/50/100/200, coin return 20/60/120, Donchian 20/55 position, EMA20/100
  cross, return vs BTC 30/90). Best lifts: long coin_ret120 +0.40, short coin_above_ema50 +0.15.
- All fail: p_shift ≥ 0.145. Strength vs BTC (coin_rel_btc) is negative on the long side. No setup promoted.

## Holdout: btc_ret20 long/short on validation and test
Run: `python run_holdout.py` (validation and test run once). 20-day hold, 0.2% round trip, no funding.

| period | side | PF | base PF | lift | mean / 20d | base mean | p_shift | coins | verdict |
|---|---|---|---|---|---|---|---|---|---|
| validation 2023-01 → 2024-09 | long | 1.60 | 1.42 | +0.17 | +3.3% | +2.3% | 0.31 | 10/13 | fail (p) |
| validation | short | **0.80** | 0.66 | +0.14 | **-1.3%** | -2.7% | 0.27 | 8/12 | fail (loses money) |
| test 2024-10 → 2026-09 | long | 1.55 | 1.18 | +0.38 | +3.7% | +1.2% | 0.11 | 11/12 | fail (p) |
| test | short | 1.18 | 0.80 | +0.38 | +1.0% | -1.6% | 0.10 | 11/12 | fail (p) |

- Lift is positive in every period on both sides: the direction of the edge holds out of sample.
- It is not statistically strong in any holdout period (p 0.10–0.31), and the **short side loses money in
  validation** (bull market). The draft requires the short side alone to be positive in validation and test → fail.
- Benchmark, live-bot filter long side: validation lift -0.26, test +0.53. Neither rule dominates.
- Verdict: **no long/short trend edge that passes the fixed rules.** The short side works as a bear-market hedge
  (it loses less than random shorting) but is not a standalone money-maker. M5 (full backtest) skipped.
