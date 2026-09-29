# Edge search — VERIFICATION_PHASE_B

Funding and open-interest work on the shorter Bybit-era data.

## M10 funding as a filter: a short-side lift that never turns the shorts profitable
Run by `../long_short_research/funding_filter.py` (top-40 point-in-time universe, signal uses only settlements
before the daily close, 40 fixed variants per split, results in `../long_short_research/results/funding_filter_*.csv`).
- Train (2021 → 2022): 1 of 40 passes: in BTC-bull days, dropping short days with very negative funding
  ("no cold", abs 3d funding > 0.03% / < 0). Short PF 1.47 vs base 1.35, lift +0.12, `p_shift` 0.04, 30 of 38 coins.
- Validation: the same variant passes again (lift +0.13, `p_shift` 0.00) plus one z-score variant, but the short PF is
  **0.91** (base 0.78): the filter improves a losing leg, it does not make it profitable.
- Test: same variant lift +0.03, `p_shift` 0.085, short PF **0.97** → fail.
- Every "avoid longs when funding is hot" variant fails on train. Hot funding as a short signal fails.
- Verdict: no funding-filter edge. Funding is not a usable entry or short signal on the daily top coins.
- Caveats: about 39% of universe coin-days have no funding (delisted coins have no Bybit perp), so the sample leans to
  survivors. All 40 variants were also run on the test window, so that window is no longer untouched for
  funding-filter ideas of this kind. Forward-return PF metric, not the portfolio engine.

## Round 2 train: no crowding overlay passes, every overlay is indistinguishable from a shifted one
Ideas K–T (declared in `PLAN.md`, "Round 2"), run once with `run_round2.py train` (train 2020-11-15 → 2023-06-30, daily
funding and OI, results in `results/round2_train.csv`). Baseline A on this window: CAGR 28.2%, maxDD -49.3%, Calmar 0.57
(BTC buy-and-hold 27.6% / -76.6%).
- Sanity first: a peeking overlay (cash before down days) gives CAGR 483% with `shift_p` 0.00; a shuffled overlay gives
  `shift_p` 0.44 → the runner detects edge when there is one and not when there isn't.
- Gate 2 (overlay beats ≥ 95% of shifted overlays) fails for all ten: `shift_p` 0.47 to 0.92. Nothing beats the timing of a random overlay.
- Cutting on funding (K, L, O), OI stall (M), OI z-score (N), or market-wide funding (Q) all lower or keep CAGR while
  drawdown falls only when the overlay sits in cash a lot (L: 17% of days, CAGR 8%, maxDD -34%; Q: 26% of days, CAGR 0.3%).
  That is de-risking by being out of the market, not a crash signal.
- K, M, N cut only 3% of days and change little (M: 27.4% / -48.4% vs A 28.2% / -49.3%).
- R (equal-weight funding coins, K overlay) and T (50% L + 50% BTC funding carry) beat A on Calmar and drawdown (R 0.76,
  maxDD -37.8%; T 1.09, maxDD -14.6%, CAGR 15.9%) but fail gate 2 — the gain is the basket (R) and the carry sleeve (T), not the overlay.
  S (vol-targeted, cut on funding or OI stall) loses money (-1.3%).
- Verdict: none of K–T passes train; validation and test untouched by this round. Crowding overlays on a BTC trend baseline
  add nothing that timing luck doesn't.
- Caveat: BTC-only overlays; OI lagged one day; train is 2.6 years with 15 non-overlapping 30-day BTC-down blocks.

## Round 3 train: no long/short trend system on 1h, 4h or 1d makes money after costs and funding
36 cells (Donchian stop-and-reverse, SMA cross, chandelier reversal, time-series momentum × horizons 5/20/60 days × 1h/4h/1d),
22 Bybit perps (11 have 1h), 0.10% per side plus real funding, train 2021-01-01 → 2023-06-30 (`swing_trend.py train`,
`results/round3_train.csv`). BTC buy-and-hold on the window 2.1%/yr, maxDD -77%; equal-weight 22 coins -6.6%/yr, maxDD -83%.
- Both legs: **0 of 36** cells have positive CAGR; 0 of 36 pass the shift gate (`shift_p` ≈ 1.0: real timing is no better than shifted timing).
- Long-only: 3 of 36 positive (4h F1/20 +3.2%, 4h F2/20 +3.2%, 1d F2/20 +0.7%); short-only: **0 of 36**.
- Lower timeframes are worse, not better: 1h chandelier (F3) loses 64–77%/yr (about 50+ trades a year per coin at 0.10% + whipsaw).
- Hindsight ceiling, daily BTC train: a zigzag riding every ≥20% swing both ways would make ~1,700%/yr (19 swings). The moves are real
  and visible on a chart, but no real-time rule here captures them: the rules enter after the move and exit after the reversal.
- Funding is a first-order cost, not a detail: always-long BTC perp = -14.8%/yr vs +2.1% spot buy-and-hold on this window (longs paid
  ~18%/yr on average). BTC F1/20 is -6.1% net and +10.6% without funding. Long-biased perp systems start ~15 points behind.
- Engine checks: peeking (knows next bar) → absurd return; always-long = buy-and-hold minus funding. Signal inversion does not rescue
  it (inverted also loses on ETH and the 22-coin average) → whipsaw and volatility drag, not a sign error.
- Single-coin exceptions, not evidence: BTC time-series momentum 60d makes +20.7% net (its inverse -51.8%), but ETH and the coin average do not.
- Verdict: none of the 36 cells passes train; validation and test untouched.
- Caveat: fixed grid of 3 horizons per family; the plan did not tune stops, filters or coin selection. Train includes the 2021 alt
  blow-off and the 2022 bear, both hard for trend systems with 5–20 day horizons.
