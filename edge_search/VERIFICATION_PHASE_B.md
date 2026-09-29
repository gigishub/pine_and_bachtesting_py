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
