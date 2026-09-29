# Long/short trend — VERIFICATION_INDEX

## Current truths
- Edge-check engine passes sanity checks (random = no edge, peeking = edge, known answers, delisted exits) → [Phase A: Engine sanity](VERIFICATION_PHASE_A.md#engine-sanity-random-peek-delisting)
- Unconditional drift: large caps held 20 days in train have long PF 1.24 / short PF 0.77 → [Phase A: Engine sanity](VERIFICATION_PHASE_A.md#engine-sanity-random-peek-delisting)
- BTC regime filters' pooled edge comes from a few bull/bear swings, not within-year timing; only btc_ret20 passes train → [Phase A: Regime layer](VERIFICATION_PHASE_A.md#regime-layer-btc-trend-filters-sort-years-btc_ret20-only-survivor)
- Coin-level trend adds no significant lift over the BTC regime → [Phase A: Setup layer](VERIFICATION_PHASE_A.md#setup-layer-coin-trend-adds-nothing-over-btc_ret20)
- No long/short trend edge passes: btc_ret20 lift is positive in validation and test but not significant, and shorts lose money in validation → [Phase A: Holdout](VERIFICATION_PHASE_A.md#holdout-btc_ret20-longshort-on-validation-and-test)
- Traded until flip, btc_ret20 long+short is worse than long-only in every period; short leg loses in validation and test (whipsaw, 27–48 flips/yr) → [Phase A: Traded until flip](VERIFICATION_PHASE_A.md#btc_ret20-traded-until-the-regime-flips-short-leg-loses-longshort-worse-than-long-only)

## Phases
- [Phase A](VERIFICATION_PHASE_A.md) — top-down edge check (regime → setup) on the point-in-time top-10 universe, daily
- Phase B: mean reversion (5-day) loses on the top 10 on all days, and no chop detector fixes it in train → [Phase B: Chop regime layer](VERIFICATION_PHASE_B.md#chop-regime-layer-no-detector-makes-mean-reversion-work)
- Funding carry (long spot + short perp) on BTC/ETH is positive after costs in every period but shrinking: ~22–28% (2020–22) → ~10% (2023–24) → ~5% (since 2024-10); alts and a "smart" on/off filter are worse → [Phase C: Funding carry BTC ETH](VERIFICATION_PHASE_C.md#funding-carry-btc-eth-real-but-shrinking-about-5-a-year-and-falling)
