# Swing research — VERIFICATION_INDEX

## Current truths
- Live bot works on BTC/SOL but not on the median coin; drawdowns ~45–55% → [Phase A: Live bot baseline](VERIFICATION_PHASE_A.md#live-bot-baseline-btc-sol-22-coins)
- BTC-trend entry filter improves the live bot, robust across settings → [Phase A: BTC trend filter](VERIFICATION_PHASE_A.md#btc-trend-entry-filter-btc_ret_20-robust)
- ret20 filter supplements the EMA240 trend filter; replacing it is worse → [Phase A: Trend vs ret20](VERIFICATION_PHASE_A.md#trend-filter-vs-ret20-filter-supplement-not-replace-btc)
- Volatility sizing cuts drawdown ~15 points at no return cost → [Phase A: Vol sizing](VERIFICATION_PHASE_A.md#volatility-sizing-atr-drawdown)
- Per-coin Donchian / time-series momentum: no edge in train → [Phase A: Donchian and tsmom](VERIFICATION_PHASE_A.md#donchian-and-tsmom-per-coin-fail-in-train)
- Momentum rotation on a point-in-time universe (incl. delisted coins) fails with a 30d-volume universe; on large caps (top 10 by 180d volume) it matches BTC-with-trend-filter return (~31–33%/yr) with worse drawdown (-78% vs -63%) → [Phase B: Rotation stable universe](VERIFICATION_PHASE_B.md#rotation-stable-universe-top-10-by-180d-volume)

## Phases
- [Phase A](VERIFICATION_PHASE_A.md) — baseline of the live bot, first filters, first new candidates (1d + 4h, 22 coins)
- [Phase B](VERIFICATION_PHASE_B.md) — momentum rotation on all Binance USDT pairs incl. delisted (point in time)
