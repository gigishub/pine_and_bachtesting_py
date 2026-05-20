# Audit Report — ETHUSDT 1d

Generated : 2026-04-25 13:58:47 UTC
Source    : ETHUSDT_1d_start_2021-03-15_end_2026-04-22.parquet
Rows      : 1,865

## 🟢 Trust Score: 100.0 / 100

## Summary

| Check | Status | Affected | % of rows |
|-------|--------|:--------:|----------:|
| Completeness | ✅ PASS | 0 | 0.000% |
| Duplicate timestamps | ✅ PASS | 0 | 0.000% |
| Zero / negative prices | ✅ PASS | 0 | 0.000% |
| OHLC logic | ✅ PASS | 0 | 0.000% |
| Price spikes (|log-ret| > 50%) | ✅ PASS | 0 | 0.000% |
| Stale prices (≥5 repeats) | ✅ PASS | 0 | 0.000% |
| Zero volume | ✅ PASS | 0 | 0.000% |
| Volume spikes (>10× rolling median) | ⚠️ WARN | 1 | 0.054% |
| Return profile | ✅ PASS | 0 | 0.000% |

---

## Check Details

### ✅ Completeness

100% complete (1,865 rows)

### ✅ Duplicate timestamps

0 duplicate timestamp(s)

### ✅ Zero / negative prices

0 candle(s) with zero or negative OHLC

### ✅ OHLC logic

0 violation(s) (High<Low/Open/Close or Low>Open/Close)

### ✅ Price spikes (|log-ret| > 50%)

0 spike(s) above 50% threshold

### ✅ Stale prices (≥5 repeats)

0 candle(s) inside a frozen-price run

### ✅ Zero volume

0 zero-volume candle(s) (0.00%)

### ⚠️ Volume spikes (>10× rolling median)

1 spike(s) above 10× rolling median

_First 1 flagged rows:_

| Date                      |    Open |   High |    Low |   Close |      Volume |   volume_ratio |
|:--------------------------|--------:|-------:|-------:|--------:|------------:|---------------:|
| 2022-06-13 00:00:00+00:00 | 1434.25 |   1455 | 1161.6 | 1208.85 | 3.82705e+06 |             10 |

### ✅ Return profile

mean=0.00015  std=0.03995  skew=-0.25  excess-kurt=5.4

