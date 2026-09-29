# Funding carry — PLAN3

## Start
- PLAN.md (trend long/short) and PLAN2.md (chop + mean reversion, M7–M8 unfinished) found no directional edge on
  daily top-10 coins. Carry earns a risk premium instead of predicting direction.

## Goal
Know whether long spot + short perp on Bybit earns enough after costs, on data it was not tuned on.

## Done when
- Carry measured per period (train / validation / test) net of costs, on BTC, ETH and alts, with a verdict.

## Milestones
- [x] M9 — Funding download + carry test (BTC, ETH, alts, smart filter). Result: positive but ~5%/yr and falling.
- [x] M10 — Funding as a filter for directional bots (avoid longs when funding is extreme), only if worth it.
  - **Handoff:** funding for 134 Bybit perps is downloaded (`../crypto_data/data_funding/` plus the 22 coins in
    `../crypto_data/data/`). `funding_filter.py` (top-40 point-in-time universe, funding signal uses only
    settlements before the daily close) was run to completion (all three periods) but its output was not read or written up. Results land in
    `results/funding_filter_{train,validation,test}.csv`; re-run `python funding_filter.py` if they are missing.
    Verdict (no edge) logged in `../edge_search/VERIFICATION_PHASE_B.md`. Caveat: 39% of universe coin-days have no funding (delisted coins have no
    Bybit perp), so the sample leans toward survivors.

## Open / deferred
- Basis risk, margin/liquidation, and Bybit spot fees for real numbers.
