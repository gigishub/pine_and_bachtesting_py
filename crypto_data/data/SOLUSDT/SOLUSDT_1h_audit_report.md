# Audit Report — SOLUSDT 1h

Generated : 2026-04-25 13:58:48 UTC
Source    : SOLUSDT_1h_start_2021-10-15_end_2026-04-22.parquet
Rows      : 39,601

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
| Volume spikes (>10× rolling median) | ⚠️ WARN | 110 | 0.278% |
| Return profile | ⚠️ WARN | 1 | 0.003% |

---

## Check Details

### ✅ Completeness

100% complete (39,601 rows)

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

110 spike(s) above 10× rolling median

_First 10 flagged rows:_

| Date                      |    Open |    High |     Low |   Close |   Volume |   volume_ratio |
|:--------------------------|--------:|--------:|--------:|--------:|---------:|---------------:|
| 2021-10-27 08:00:00+00:00 | 194.315 | 195.685 | 174.76  | 192.205 | 407550   |           11.8 |
| 2021-11-10 21:00:00+00:00 | 230.035 | 233.7   | 215.5   | 228.54  | 267290   |           14.8 |
| 2021-11-21 18:00:00+00:00 | 221.48  | 233.195 | 220.65  | 230.065 |  90411.4 |           10.8 |
| 2021-11-26 08:00:00+00:00 | 201.29  | 201.385 | 185.245 | 190.46  | 152921   |           13.9 |
| 2021-12-04 05:00:00+00:00 | 192.98  | 194.405 | 166.695 | 192.9   | 413420   |           14.3 |
| 2022-01-05 19:00:00+00:00 | 163.935 | 164.38  | 157.415 | 158.625 |  74858.8 |           11   |
| 2022-01-05 20:00:00+00:00 | 158.625 | 159.695 | 155.01  | 156.47  |  69943.6 |           10.3 |
| 2022-01-05 22:00:00+00:00 | 153.46  | 154.33  | 144.36  | 151.42  |  98671.1 |           14.6 |
| 2022-01-10 14:00:00+00:00 | 135.445 | 135.585 | 129.705 | 133.255 | 183896   |           12.4 |
| 2022-04-30 23:00:00+00:00 |  85.32  |  86.13  |  81.595 |  84.52  | 457208   |           14.4 |

### ⚠️ Return profile

mean=-0.00001  std=0.01091  skew=-0.41  excess-kurt=32.9  ⚠ extreme kurtosis (32.9)

