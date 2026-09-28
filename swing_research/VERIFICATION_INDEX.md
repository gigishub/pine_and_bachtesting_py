# Swing research — VERIFICATION_INDEX

## Current truths
- Live bot works on BTC/SOL but not on the median coin; drawdowns ~45–55% → [Phase A: Live bot baseline](VERIFICATION_PHASE_A.md#live-bot-baseline-btc-sol-22-coins)
- BTC-trend entry filter improves the live bot, robust across settings → [Phase A: BTC trend filter](VERIFICATION_PHASE_A.md#btc-trend-entry-filter-btc_ret_20-robust)
- Volatility sizing cuts drawdown ~15 points at no return cost → [Phase A: Vol sizing](VERIFICATION_PHASE_A.md#volatility-sizing-atr-drawdown)
- Per-coin Donchian / time-series momentum: no edge in train → [Phase A: Donchian and tsmom](VERIFICATION_PHASE_A.md#donchian-and-tsmom-per-coin-fail-in-train)
- Weekly momentum rotation: positive in train and test, but inflated by survivorship and with 50–65% drawdowns → [Phase A: Rotation](VERIFICATION_PHASE_A.md#momentum-rotation-survivorship-bias)

## Phases
- [Phase A](VERIFICATION_PHASE_A.md) — baseline of the live bot, first filters, first new candidates (1d + 4h, 22 coins)
