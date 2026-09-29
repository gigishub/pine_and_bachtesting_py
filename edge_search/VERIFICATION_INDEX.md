# Edge search — VERIFICATION_INDEX

## Current truths
- Engine sanity holds (buy-and-hold matches, peeking = huge edge, random = no edge) → [Phase A: Engine sanity](VERIFICATION_PHASE_A.md#engine-sanity-buy-and-hold-peeking-random-weights)
- Of 10 ideas, A (BTC trend), B (momentum), E (low-vol), H (long/short momentum) pass train; C, D, F, G, I, J fail → [Phase A: Train](VERIFICATION_PHASE_A.md#train-a-b-e-h-pass-all-gates-c-d-f-g-i-j-rejected)
- No idea passes validation; none meets 20%/20% or beats BTC buy-and-hold; test untouched → [Phase A: Validation](VERIFICATION_PHASE_A.md#validation-nothing-survives-b-loses-money-all-trail-buy-and-hold)
- Capture ratios: A, B, E keep ~53–72% of BTC upside and take ~22–27% of downside on train, but 116–144% of downside on validation (no crash there, slow filters whipsaw) → [Phase A: Capture ratios](VERIFICATION_PHASE_A.md#capture-ratios-trend-ideas-protect-in-real-bear-markets-but-validation-had-no-crash-to-protect-against)
- Round 2 (crowding overlays K–T on BTC trend): none passes train; every overlay is indistinguishable from a shifted one (`shift_p` 0.47–0.92); funding carry blended in (T) and an equal-weight basket (R) improve drawdown but not because of the overlay → [Phase B: Round 2 train](VERIFICATION_PHASE_B.md#round-2-train-no-crowding-overlay-passes-every-overlay-is-indistinguishable-from-a-shifted-one)
- Rounds 3–4b (long/short trend, EMA/ATR bands, stops; 114 cells on 1h/4h/1d, 22 perps, costs + funding): no system with a short leg makes money in train or validation (0 of 114; shorts lose in every cell); funding is a first-order cost for long perps; shift-test bug fixed → [Phase B: shift test fixed](VERIFICATION_PHASE_B.md#round-3-to-4b-shift-test-fixed-funding-nan-bug-verdicts-re-checked)
- Best long-only find: 1h band breakout with fixed stop makes +35% with -19% drawdown on validation but trails BTC (+79%, Sharpe 1.5) and fails the shift gate; test untouched → [Phase B: Round 4b validation](VERIFICATION_PHASE_B.md#round-4b-validation-the-long-only-plateau-makes-35-with--19-drawdown-but-is-not-better-than-btc-and-fails-the-shift-gate-shorts-lose-2528)

### From earlier arcs (links go to the original docs)
- Live bot works on BTC/SOL but not the median coin; drawdowns ~45–55% → [Swing Phase A](../swing_research/VERIFICATION_PHASE_A.md#live-bot-baseline-btc-sol-22-coins)
- BTC 20-day-return entry filter improves the live bot and is robust; vol sizing cuts drawdown → [Swing index](../swing_research/VERIFICATION_INDEX.md)
- Per-coin Donchian / time-series momentum: no edge in train → [Swing Phase A](../swing_research/VERIFICATION_PHASE_A.md#donchian-and-tsmom-per-coin-fail-in-train)
- Rotation on top-10 by 180d volume ≈ BTC with trend filter, worse drawdown (-78% vs -63%) → [Swing Phase B](../swing_research/VERIFICATION_PHASE_B.md#rotation-stable-universe-top-10-by-180d-volume)
- No long/short trend edge passes; shorts lose in validation and test → [Long/short Phase A](../long_short_research/VERIFICATION_PHASE_A.md#holdout-btc_ret20-longshort-on-validation-and-test)
- Mean reversion loses on the top 10 and no chop detector fixes it → [Long/short Phase B](../long_short_research/VERIFICATION_PHASE_B.md#chop-regime-layer-no-detector-makes-mean-reversion-work)
- Funding carry BTC/ETH positive after costs but ~5%/yr and falling → [Long/short Phase C](../long_short_research/VERIFICATION_PHASE_C.md#funding-carry-btc-eth-real-but-shrinking-about-5-a-year-and-falling)
- Funding-as-filter (M10): a short-side lift on train and validation, but shorts stay unprofitable (PF 0.91 / 0.97) and the test fails → [Phase B: M10](VERIFICATION_PHASE_B.md#m10-funding-as-a-filter-a-short-side-lift-that-never-turns-the-shorts-profitable)

## Phases
- [Phase B](VERIFICATION_PHASE_B.md) — funding and open-interest work on Bybit-era data
- [Phase A](VERIFICATION_PHASE_A.md) — ten pre-declared daily ideas on the point-in-time top-10
- Earlier arcs: [Swing](../swing_research/VERIFICATION_INDEX.md), [Long/short](../long_short_research/VERIFICATION_INDEX.md)
