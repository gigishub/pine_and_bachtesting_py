# Swing research — PLAN

## Start
- Live bot (`btc_sol_hetzner_momentum_bot/`): long-only daily trend strategy on BTC and SOL
  (KuCoin spot). Entry: close above EMA240 and EMA10, and no recent volatility spike.
  Exit: trailing stop, checked on the daily close.
- No measured baseline for the live bot yet.
- Earlier research (`bear_strategy/`, 15m–4h) got lost in details. Lessons:
  `summery30-03_may.md`, `Falsification_apporach.md`.

## Goal
1. Know how good the live bot really is, and improve it only where the evidence is clear.
2. Find at least one more swing strategy (4h or daily, holds of days to weeks, few
   trades so fees stay small) that holds up on data it was not tuned on.
3. Only then: add a trade-quality filter (probability/meta-label or LLM) on top.

## Done when
- The live bot's baseline is measured, net of fees, on BTC and SOL plus other coins.
- A candidate strategy beats its baseline on the test period (from 2024-10-01), on most
  coins, net of 0.1% fees per side, and is written up with the exact rules.

## Rules for every test
- Train: data start → 2024-09-30. Test: 2024-10-01 → today. Tune on train only.
- Fees: 0.1% per side. Signals use the closed bar; fills happen at the next bar's open.
- Judge on many coins, not just BTC/SOL: a real edge shows up on most of them.

## Milestones
- [x] M1 — Baseline of the live bot (replica backtest, net of fees, per coin, train vs test)
- [ ] M2 — Cheap improvements to the live bot (exits, regime filter, sizing), tested on train and confirmed on test
  - Tested: BTC trend filter + vol sizing pass (see VERIFICATION_PHASE_A). Next: decide and wire into the live bot.
- [ ] M3 — New swing candidates on 4h/daily
- [ ] M4 — Trade-quality filter (probability of a good trade) on the best candidate

## Open / deferred
- Bot reconstructs its position from 700 bars of history, not from the real exchange
  balance. A failed order leaves the bot believing it is in a trade. Worth fixing.
- 1h data: possible lower-timeframe early signals for later.
- ALGO and XLM 4h failed to download (Bybit 'Get kline failed'); retry.
- Rotation: test with BTC filter + vol sizing, and as a diversifier next to the live bot.
- Survivorship: coin list chosen in 2026; judge on 2021 majors.
