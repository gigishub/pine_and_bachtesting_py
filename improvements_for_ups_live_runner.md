Improvement areas (short + precise)

1. MarketData fallback persistence
- Add persistent closed-history cache in LiveMarketDataService (file or local DB).
- Save latest closed_history after processing each closed bar.
- On startup or WS gap, load cached data first; if valid, skip full REST bootstrap and quick replay.
- Improves recovery and reduces data race complexity.

2. Runner state persistence/resume
- RunnerSessionState (pending_entry_*, pending_stop_*) is currently in-memory.
- Persist this state periodically (disk/DB) for crash-safe resume.
- On restart, reload state and re-sync against exchange order/position status.

3. Bar-processing path cleanup
- attach_stops_for_pending_fill_if_needed() is called from both BarProcessor and LoopRunner timeout path.
- Consider centralizing in PendingExecutionService.sync_pending_state() to avoid duplicate logic.

4. Explicit failure-safe layering
- In BarProcessor, catch exceptions in strategy.compute and orders.get_current_position, log, and skip the bar (do not crash).
- Keep state consistent when API hiccups show temporary undefined position.

5. Strategy precomputation (new)
- Precompute as much strategy work as possible ahead of the close (indicator series + aggregated expected conditions).
- At closed-bar handoff, only evaluate final condition flags and execute entry/exit.
- Reduces runtime per-bar decision latency and keeps behavior deterministic.


6. Order submission latency optimization

takes already a second to process previous candle so issue likely there.

sample
====
[2026-03-26 15:26:53 UTC] Starting live runner symbol=XRPUSDT category=linear tf=1m dry_run=False mode=ws
[2026-03-26 15:26:54 UTC] WebSocket mode active. Warmup candles=399 last=2026-03-26 15:25:00+00:00
[2026-03-26 15:27:01 UTC] Signal details: price_above_ma=False long_conditions=False bearish_pb=True long_entry=False open_long=False short_conditions=True bullish_pb=True short_entry=False open_short=False
[2026-03-26 15:27:01 UTC] Processed candle 2026-03-26 15:26:00+00:00 pos=none
[2026-03-26 15:28:01 UTC] Signal details: price_above_ma=False long_conditions=False bearish_pb=True long_entry=False open_long=False short_conditions=True bullish_pb=True short_entry=False open_short=False
[2026-03-26 15:28:01 UTC] Processed candle 2026-03-26 15:27:00+00:00 pos=none
====

Likely problem:

the path from bar-close signal → EntryService.try_entry → orders.place_entry is delayed by pre-check work, sleep timers, or deferred execution path.
result: order is constructed/ sent late even though conditions were ready.
Solution suggestion:

at bar handoff, evaluate entry condition exactly once and immediately call orders.place_entry.
move heavy computation (indicators/risk setup) out of hot path (precompute, cached values).
remove non-essential delay (time.sleep(0.2) and extra pending checks) in order submission route.


7. is tp actually a limit order since its getting coundted as a mark in tp/sl 

i e 
XRPUSDT
Perp
USDT Perpetuals
Buy
TP 1.3549 (Mark)
SL 1.3612 (Mark)
TP 1.3549
SL Market
38.8 XRP
--
Close Short
2026-03-26 15:31:01
60dc2912
993c2c4f
Untriggered
XRPUSDT
Perp
USDT Perpetuals
Buy
TP 1.3549 (Mark)
SL 1.3612 (Mark)
TP 1.3549
SL Market
27.2 XRP
--
Close Short
2026-03-26 15:30:09
6fb8e827
a8c9ffc5
Untriggered
