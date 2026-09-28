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
  - Decision: BTC gets the BTC-trend entry filter only. SOL stays unchanged. Vol sizing is skipped
    (barely changes BTC).
  - **Change:** BTC opens a new trade only if its 20-day return (prior close vs 20 closes before) is
    ≥ -3%. Exits, stops and SOL are untouched. Implemented as a config option (`StrategyParams.ret_min`,
    `None` = off) so it can be switched back with one line.
  - Steps:
    - [x] M2.1 — Redesign the bot into `btc_sol_hetzner_momentum_bot/bot/` (config, data, signals,
      exchange, runner) with the filter as `StrategyParams.ret_min`. Signals are pure (no I/O), so
      research and live use the same code. Runner compares the strategy with the real holding
      (sells leftovers, never chases a missed entry), uses closed candles only, 1500-bar history,
      and has `--dry-run`. Old files stay untouched until switch day.
    - [x] M2.2 — Tests in `btc_sol_hetzner_momentum_bot/tests/` (39 pass): filter off = old bot
      bar for bar on all 22 coins (trades, stops); filter on = research result; the daily decision
      from a 1500-bar window = full-history replay for the last 120 days; runner action table and
      no orders in dry run. A deliberate change (caution stop 0.2 → 0.3) makes the parity tests fail.
      Returns cross-checked with vectorbt (BTC +782% / +1176%, same trades and max DD).
    - [x] M2.3 — Dry run on the server: new BTC logic runs daily in log-only mode next to the live
      bot for ~2 weeks. This checks the plumbing (data, timing, no crashes), not the edge — with ~12
      trades/yr, 2 weeks shows 0–1 trades.
      - Pushed to the bot repo (`4624c5f`, only new files). Tests pass on the server stack (Python 3.12,
        pandas 3.0.1, numpy 2.2.6, no pyarrow, ccxt 4.5.42): 12/12 runner tests, parity tests skip (no
        research data on server, expected). Manual dry run placed no orders and agreed with the live
        bot's actual 00:00 BTC exit on 2026-09-28.
      - Cron added 2026-09-28: `15 0 * * * /root/projects/trading_bot/run_dry.sh >> /root/projects/trading_bot/dry_run.log 2>&1`.
        Started running via SSH from this session (`~/.ssh/config` host `hetzner`, key `id_ed25519`,
        now in the macOS agent/Keychain). First automatic run: 2026-09-29 00:15 UTC.
      - Watch for through M2.4: `dry_run.log` fills in as expected (no exceptions, one line per
        coin per night) and `bot/` decisions keep matching `trading_midnight_utc.log`'s actual actions.
    - [ ] M2.4 — Switch day: both rules must agree on the BTC state (in trade / flat). If they
      disagree, wait until they agree. (Checked on live KuCoin data for 2026-09-28: both sell BTC
      at this open and hold SOL.)
    - [ ] M2.5 — Go live. Stop criteria set in advance: roll back if, after 15 new BTC trades, PF < 1,
      or if the BTC drawdown exceeds 40% (worse than anything seen: -38% train, -12% test).
- [ ] M3 — New swing candidates on 4h/daily
- [ ] M4 — Trade-quality filter (probability of a good trade) on the best candidate

## Open / deferred
- Bot reconstructs its position from 700 bars of history, not from the real exchange
  balance. A failed order leaves the bot believing it is in a trade. Worth fixing.
  (Fixed in the new bot's runner, which checks the real holding — see M2.1.)
- Old bot's `wait_for_candle_completion` accepts the just-opened current-period candle as soon as
  KuCoin returns it (seen accepting ~13s after 00:00 on 2026-09-28), then computes today's signal
  off it via shift(1). If KuCoin ever returns that fresh candle with an unsettled/wrong close, the
  signal could be wrong for one day. The new bot avoids this: `closed_candles()` only ever returns
  bars that are fully finished. No evidence yet this has caused a bad decision (new and old bot
  agreed on 2026-09-28's BTC exit) — flagging so it isn't lost, not urgent.
- 1h data: possible lower-timeframe early signals for later.
- ALGO and XLM 4h failed to download (Bybit 'Get kline failed'); retry.
- Rotation: test with BTC filter + vol sizing, and as a diversifier next to the live bot.
- Survivorship: coin list chosen in 2026; judge on 2021 majors.
