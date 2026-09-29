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
- [ ] M10 — Funding as a filter for directional bots (avoid longs when funding is extreme), only if worth it.

## Open / deferred
- Basis risk, margin/liquidation, and Bybit spot fees for real numbers.
