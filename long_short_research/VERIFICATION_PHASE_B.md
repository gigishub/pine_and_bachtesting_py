# Phase B — Chop regime + mean reversion, point-in-time top 10, daily

Run: `python run_chop.py regime` → `results/chop_regime.csv`. Train, 5-day hold, 0.2% round trip.

## Chop regime layer: no detector makes mean reversion work
- Baseline reversal probe (long after a 5-day drop, short after a 5-day rise) loses on all days in train:
  long PF 0.955 (mean -0.19%), short PF 0.79 (mean -1.06%). Big coins continue more than they revert over 5 days.
- 11 chop detectors (BTC / coin efficiency ratio 20/40, BTC flat 30/60 days, BTC trend flips 60/90 days, BTC near
  EMA100, coin flat 30 days): none passes. Best: btc_near_ema100<5% (long lift +0.11, p 0.32; short lift +0.26,
  p 0.12), still PF ≈ 1.05, i.e. about break-even after costs.
- Efficiency-ratio and "flat BTC" detectors make the long probe worse (lift down to -0.25).
- Verdict: no chop regime promoted. The setup layer and holdout (M7, M8) have not been run yet.
