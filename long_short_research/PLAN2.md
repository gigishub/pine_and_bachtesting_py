# Chop regime + mean reversion — PLAN2

Follows PLAN.md (trend long/short failed: shorts get whipsawed in sideways markets). Idea: detect the chop and
trade it the other way.

## Start
- Edge-check engine, point-in-time top-10 universe and periods from PLAN.md (Phase A).
- Since 2023 the BTC 20-day trend flips 27–48 times a year: chop is common.

## Goal
Know whether a chop detector plus a mean-reversion entry (long dips, short rips) has an edge on the largest coins
that survives validation and test. A clear "no" is a valid result.

## Done when
- Every chop detector and mean-reversion signal has a train verdict, and the promoted stack ran once on
  validation and test.

## Rules (fixed before testing)
- Same universe, periods, costs (0.2% round trip), next-open entry and pass rule as PLAN.md.
- Primary hold 5 days (3 and 10 shown too).
- Regime layer: a chop detector passes if it improves a generic reversal probe (long if the coin's 5-day return
  < 0, short if > 0) over the same probe on all days.
- Setup layer: mean-reversion signals on top of the promoted chop regime, baseline = all chop days (each side).

## Milestones
- [x] M6 — Chop regime layer (detectors vs reversal probe), train
- [ ] M7 — Mean-reversion setup layer on the promoted chop regime, train
- [ ] M8 — Frozen stack on validation and test (once), plus a traded-until-exit check

## Open / deferred
- 4h candles.
