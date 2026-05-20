# Audit Report — ETHUSDT 1h

Generated : 2026-04-25 13:58:47 UTC
Source    : ETHUSDT_1h_start_2021-03-15_end_2026-04-22.parquet
Rows      : 44,737

## 🟢 Trust Score: 99.9 / 100

## Summary

| Check | Status | Affected | % of rows |
|-------|--------|:--------:|----------:|
| Completeness | ✅ PASS | 0 | 0.000% |
| Duplicate timestamps | ✅ PASS | 0 | 0.000% |
| Zero / negative prices | ✅ PASS | 0 | 0.000% |
| OHLC logic | ✅ PASS | 0 | 0.000% |
| Price spikes (|log-ret| > 30%) | ✅ PASS | 0 | 0.000% |
| Stale prices (≥5 repeats) | ✅ PASS | 0 | 0.000% |
| Zero volume | ✅ PASS | 0 | 0.000% |
| Volume spikes (>10× rolling median) | ⚠️ WARN | 214 | 0.478% |
| Return profile | ✅ PASS | 0 | 0.000% |

---

## Check Details

### ✅ Completeness

100% complete (44,737 rows)

### ✅ Duplicate timestamps

0 duplicate timestamp(s)

### ✅ Zero / negative prices

0 candle(s) with zero or negative OHLC

### ✅ OHLC logic

0 violation(s) (High<Low/Open/Close or Low>Open/Close)

### ✅ Price spikes (|log-ret| > 30%)

0 spike(s) above 30% threshold

### ✅ Stale prices (≥5 repeats)

0 candle(s) inside a frozen-price run

### ✅ Zero volume

0 zero-volume candle(s) (0.00%)

### ⚠️ Volume spikes (>10× rolling median)

214 spike(s) above 10× rolling median

_First 10 flagged rows:_

| Date                      |    Open |    High |     Low |   Close |   Volume |   volume_ratio |
|:--------------------------|--------:|--------:|--------:|--------:|---------:|---------------:|
| 2021-03-24 20:00:00+00:00 | 1636.8  | 1637.45 | 1581.05 | 1612.6  |  24469.9 |           10.4 |
| 2021-04-18 03:00:00+00:00 | 2255    | 2270.15 | 1927.7  | 2157.75 | 140046   |           39.4 |
| 2021-05-10 20:00:00+00:00 | 3996.15 | 3996.15 | 3662.4  | 3906.35 |  80315.1 |           11.4 |
| 2021-05-13 00:00:00+00:00 | 3829.2  | 3974.7  | 3508.05 | 3895.25 | 118579   |           18.2 |
| 2021-05-19 11:00:00+00:00 | 2861.1  | 2870    | 2437.45 | 2723    | 115406   |           12.6 |
| 2021-05-19 12:00:00+00:00 | 2723    | 2772.45 | 1970.75 | 2332.9  | 258540   |           24.4 |
| 2021-05-19 13:00:00+00:00 | 2332.9  | 2499.05 | 1778.95 | 2411.45 | 437185   |           37.9 |
| 2021-05-19 14:00:00+00:00 | 2411.45 | 2619.9  | 2205.1  | 2613.9  | 120125   |           10.3 |
| 2021-05-21 14:00:00+00:00 | 2724.05 | 2762.6  | 2375.35 | 2520.9  | 101782   |           12.2 |
| 2021-07-26 01:00:00+00:00 | 2258.6  | 2334.5  | 2256.5  | 2314.7  | 140494   |           24   |

### ✅ Return profile

mean=0.00000  std=0.00802  skew=-0.60  excess-kurt=17.1

