# ✅ Trade analysis plan (no code)

## 1. Rebuild merged dataset

**Goal:** ensure the combined canonical dataset is available with:
- Bybit order/execution history
- signal logs

**What to get:**
- `live/analysis/runs/.../merged_trades` exists for all runs
- each run has `all_trades.json`
- each configured symbol/timeframe has a run folder

---

## 2. Trade quantity and symbol coverage

**Goal:** confirm trades were generated for each symbol (especially `BTCUSDT`).

**What to get:**
- count trade rows per symbol and run
- identify runs with zero trades
- for BTC zero-trade case: inspect raw `trade_logs` to check signal presence

---

## 3. Execution/results classification

**Goal:** understand lifecycle status and matching health.

**What to get:**
- counts for statuses:
  - `closed`
  - `open_or_pending`
  - `entry_order_not_found_in_history`
  - `signal_logged_no_entry_order`
  - others
- mismatch cases where strategy claims closed but no close order exists
- open/pending trades that may indicate fill problems

---

## 4. Stop-loss / exit rules validation

**Goal:** detect stop-loss / TP behavior anomalies.

**What to get:**
- closed trades where `exit_order_id` is missing or exit execution data is absent
- mismatched `signal_type` vs exit side in `lifecycle_status`
- closed status with `closed_pnl` missing

---

## 5. Fee accounting

**Goal:** measure realized trading cost and compute cost efficiency.

**What to get:**
- per trade total fees: entry + close
- aggregate fees by symbol and run
- fee-to-PnL ratio and fee-heavy trades
- fee currency usage (multi-currency if present)

---

## 6. Profit/Loss and risk performance

**Goal:** assess whether result distribution matches risk profile.

**What to get:**
- closed PnL totals per symbol and run
- win/loss counts + win rate
- average/median/worst/best closed PnL
- run-level drawdown signals (if available)
- compare with configured risk settings (`run_config.json` and profile-level risk rules)

---

## 7. Signal/order quality checks

**Goal:** capture orders where signal workflow or order fill behavior is broken.

**What to get:**
- signals with no entry fill
- pending orders never closed
- merged records with unknown matching metadata
- exit orders found but entry orders missing

---

## 8. Full run.log review across all pairs

**Goal:** detect runtime failures, warnings, disconnects, and operational issues that may not appear in merged trade outputs.

**What to get:**
- full inventory of `run.log` files under all active/inactive run folders for every pair
- error/warning counts by pair and by run attempt
- startup issues (config/env mismatches, missing symbols, invalid params)
- websocket/session issues (disconnects, reconnect loops, stale candles, timeouts)
- order lifecycle issues (submit/retry/fill/cancel failures, partial fills, API rejections)
- stop update issues (TP/SL update failures, repeated unchanged-stop errors, fallback behavior)
- per-pair incident summary with timestamp, severity, and required action

---

## 9. Root-cause and action items (prioritized)

**Goal:** convert findings into concrete fixes.

**What to get:**
- if BTC has no trades: verify runner active + symbol config + data feed
- if many `entry_order_not_found_in_history`: investigate API limits, window bounds, request completeness
- if stop-loss misses repeat: inspect stop order manager and `tpsl_policy` path
- if fees are too high: evaluate leverage, position sizing, and slippage

---

## 10. Ongoing reporting structure

**Goal:** produce repeatable audit output per run/symbol.

**Outcome per run/symbol:**
- traded / not traded
- results summary
- stop-loss integrity
- fee burden
- risk compliance

---

## 🔁 Process steps (how to execute)

1. Collect run folders by symbol/timeframe/config.
2. Ensure merged data in `.../merged_trades/all_trades.json`.
3. Review all `run.log` files for all pairs (active and inactive runs), then build an incident list.
4. Build summary table per run/symbol and compute metrics from above.
5. Cross-link log incidents with trade anomalies (missing exits, no trades, stop-loss inconsistencies).
6. Flag anomalies and classify by severity.
7. Document concise post-mortem:
   - what is broken (e.g., BTC no trades, SL misses)
   - severity (frequency, PnL impact)
   - suggested corrective path (config, API, stop manager)
