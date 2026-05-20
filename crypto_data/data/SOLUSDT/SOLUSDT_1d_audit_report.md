# Audit Report — SOLUSDT 1d

Generated : 2026-04-25 13:58:48 UTC
Source    : SOLUSDT_1d_start_2021-10-15_end_2026-04-22.parquet
Rows      : 1,651

## 🟢 Trust Score: 99.9 / 100

## Summary

| Check | Status | Affected | % of rows |
|-------|--------|:--------:|----------:|
| Completeness | ✅ PASS | 0 | 0.000% |
| Duplicate timestamps | ✅ PASS | 0 | 0.000% |
| Zero / negative prices | ✅ PASS | 0 | 0.000% |
| OHLC logic | ✅ PASS | 0 | 0.000% |
| Price spikes (|log-ret| > 50%) | ⚠️ WARN | 2 | 0.121% |
| Stale prices (≥5 repeats) | ✅ PASS | 0 | 0.000% |
| Zero volume | ✅ PASS | 0 | 0.000% |
| Volume spikes (>10× rolling median) | ⚠️ WARN | 5 | 0.303% |
| Return profile | ⚠️ WARN | 1 | 0.061% |

---

## Check Details

### ✅ Completeness

100% complete (1,651 rows)

### ✅ Duplicate timestamps

0 duplicate timestamp(s)

### ✅ Zero / negative prices

0 candle(s) with zero or negative OHLC

### ✅ OHLC logic

0 violation(s) (High<Low/Open/Close or Low>Open/Close)

### ⚠️ Price spikes (|log-ret| > 50%)

2 spike(s) above 50% threshold

_First 2 flagged rows:_

| Date                      |   Open |   High |   Low |   Close |   abs_log_return |
|:--------------------------|-------:|-------:|------:|--------:|-----------------:|
| 2022-11-09 00:00:00+00:00 |  23.9  |  23.9  | 7.535 |   10.61 |           0.8121 |
| 2022-11-10 00:00:00+00:00 |  10.61 |  19.08 | 9.21  |   17.56 |           0.5038 |

### ✅ Stale prices (≥5 repeats)

0 candle(s) inside a frozen-price run

### ✅ Zero volume

0 zero-volume candle(s) (0.00%)

### ⚠️ Volume spikes (>10× rolling median)

5 spike(s) above 10× rolling median

_First 5 flagged rows:_

| Date                      |   Open |   High |    Low |   Close |      Volume |   volume_ratio |
|:--------------------------|-------:|-------:|-------:|--------:|------------:|---------------:|
| 2022-11-08 00:00:00+00:00 | 29.59  |  31.84 | 18.03  |  23.9   | 5.94312e+07 |           14.9 |
| 2022-11-09 00:00:00+00:00 | 23.9   |  23.9  |  7.535 |  10.61  | 1.74523e+08 |           40.5 |
| 2022-11-10 00:00:00+00:00 | 10.61  |  19.08 |  9.21  |  17.56  | 9.86603e+07 |           20.1 |
| 2022-12-29 00:00:00+00:00 |  9.745 |  10.96 |  7.85  |   9.61  | 8.7098e+07  |           10.5 |
| 2023-01-03 00:00:00+00:00 | 11.26  |  13.91 | 10.965 |  13.335 | 9.15724e+07 |           10.3 |

### ⚠️ Return profile

mean=-0.00038  std=0.05416  skew=-1.51  excess-kurt=36.1  ⚠ extreme kurtosis (36.1)

