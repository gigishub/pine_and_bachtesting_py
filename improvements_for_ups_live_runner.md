Improvement areas (short + precise)
MarketData fallback persistence

Add persistent state (file/db) in LiveMarketDataService.
Save latest closed_history after each bar.
On startup / WS gap, read local cached df first; if valid, avoid full REST bootstrap/ replay.
This is exactly your “fallback df” idea.
Runner state persistence/resume

RunnerSessionState (pending order, stop/target) is in-memory.
To harden disruption, persist this state periodically.
On restart, restore pending_entry_* + pending_stop_*, re-check order status.
Remove small duplication in bar-logic callbacks

attach_stops_for_pending_fill_if_needed() is called from 2 places (BarProcessor, LoopRunner cold path).
Could be a single PendingExecutionService.sync_pending_state() invoked in one step easily.
Explicit failure-safe layering

In BarProcessor, if strategy.compute raises, log + skip, do not crash.
Same with orders.get_current_position(); ensure no false “flat” if API error.