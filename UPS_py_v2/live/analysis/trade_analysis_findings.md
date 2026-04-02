# Trade Analysis Findings

## Summary
- Total run configs: 18
- Configs with merged trades: 12
- Missing merged trades: 6 (`all_trades.json` not present)
- Total trades analyzed: 99
- Closed trades: 82
- entry_order_not_found_in_history: 9
- open_or_pending: 8
- Overall win rate: 34.1%
- Total closed PnL: -3.7558 USDT
- Fees: 2.1731 USDT
- Net (after fees): -5.9289 USDT
- Fee/|PnL| ratio: 57.9%

## Critical issue: BTCUSDT no executed trades
### Details
- BTC-USDT runs have signals, but all execution attempts hit `qty=0.000` (below min order quantity 0.001)
- `order size zero or below min notional; skipping long/short entry`
- Configuration:
  - `risk_per_trade_pct = 0.5%`
  - `min_notional_usdt = 5.0`
  - `auto_leverage_by_stop = true`

### Why
- Calculated order quantity too small for BTC at ~67k price and chosen stop distance.
- The available capital (per algo unit) is too low for 0.001 BTC minimum.

### Suggested fix
1. Increase BTC `risk_per_trade_pct` to 2-3%.
2. Consider fixed `fixed_order_qty = 0.001` for BTC to enforce minimum legible size.
3. Or allocate a larger BTC sub-account balance.
4. Add a critical alert when `qty < min_order_qty` to avoid silent no-order behavior.

## Medium issue: entry order not found in history (9 trades)
### Details
- 9 trades in `entry_order_not_found_in_history` status.
- Affected symbols: AVAXUSDT, COTIUSDT, WOOUSDT, ATOMUSDT.
- Timestamp cluster around 2026-03-29

### Why
- Merge/analysis tool likely pulls Bybit order history window too short.
- Entries may age out before reconciliation occurs.

### Suggested fix
1. Increase Bybit history fetch window or page count.
2. Persist entry order IDs in local DB/log at signal creation time.
3. Reconcile offline from local events plus API history.

## Ongoing but urgent position state issue
- 4 open_or_pending trades remain open after runner stop:
  - COTIUSDT (trail_stop_active): entry=0.01281 qty=1518
  - TRXUSDT (trail_stop_active): entry=0.31202 qty=60
  - WOOUSDT (default): entry=0.017623 qty=448.7
  - ATOMUSDT (default): entry=1.7321 qty=7.5

### Action
- Check bybit for these positions and TP/SL existence immediately.
- If runner stopped, close or reduce risk manually.

## Strategy performance observations
- All symbols net negative on sample window.
- ATOMUSDT and LTCUSDT have 0% win rate (sample 3 and 5 respectively).
- trail_stop_active profile is strongest (smallest loss magnitude).

### Suggestions
1. Review/benchmark positive filters in trailing stop profile for transfer back to default if consistent.
2. Evaluate minimum order size and risk step per symbol to reduce fee impact.
3. Focus on pair-specific tuning: reduce trade frequency where win rate <40% and losses dominate.

## Fee accounting
- Closed trade fee total: 2.1731 USDT.
- Fee-heavy trades (fee > |pnl|): 2 trades.
- Improve by increasing trade size vs fees or changing symbols/fees.

## Logging & monitoring recommendations
1. Distinguish WS timeout keepalive vs true disconnect.
2. Report skipped entries due quantity 0 as errors (currently appears as info)
3. Add Post-run health check report with:
   - orders placed / orders filled ratio.
   - open positions at end-of-run.
   - `entry_order_not_found` list.

## Next steps (immediate)
1. Adjust BTC quant size/risk and verify log now emits non-zero qty.
2. Patch `market-execution` in runner to fail loudly when qty < min notional.
3. Increase history window in analysis merge (bybit order history page or days).
4. Re-run from 2026-03-28/29 runs to collect missing `all_trades.json` if desired.
5. Perform position audit for 4 open trades still running.

---

## Reference tables (from data)
### Per-symbol lifecycle counts and quality
| Symbol | closed | entry_order_not_found | open_or_pending | win_rate | total_pnl | total_fees | net_pnl |
|---|---|---|---|---|---|---|---|
| ATOMUSDT | 3 | 1 | 1 | 0% | -0.3622 | 0.0398 | -0.4020 |
| AVAXUSDT | 22 | 1 | 0 | 40.9% | -1.0644 | 0.4962 | -1.5606 |
| COTIUSDT | 18 | 4 | 5 | 38.9% | -0.2762 | 0.4450 | -0.7212 |
| LTCUSDT | 5 | 0 | 0 | 0% | -0.7096 | 0.1516 | -0.8612 |
| TRXUSDT | 16 | 0 | 1 | 31.2% | -0.3886 | 0.6749 | -1.0635 |
| WOOUSDT | 18 | 3 | 1 | 38.9% | -0.9547 | 0.3656 | -1.3203 |

### Per-profile PnL
| Profile | trades | win_rate | total_pnl | avg_pnl |
|---|---|---|---|---|
| default | 32 | 31.2% | -2.1801 | -0.0681 |
| default_x20 | 20 | 40.0% | -1.0292 | -0.0515 |
| trail_stop_active | 30 | 33.3% | -0.5465 | -0.0182 |
