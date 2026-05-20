# Audit Report — SOLUSDT 4h

Generated : 2026-04-25 13:58:48 UTC
Source    : SOLUSDT_4h_start_2021-10-15_end_2026-04-22.parquet
Rows      : 9,901

## 🟢 Trust Score: 100.0 / 100

## Summary

| Check | Status | Affected | % of rows |
|-------|--------|:--------:|----------:|
| Completeness | ✅ PASS | 0 | 0.000% |
| Duplicate timestamps | ✅ PASS | 0 | 0.000% |
| Zero / negative prices | ✅ PASS | 0 | 0.000% |
| OHLC logic | ✅ PASS | 0 | 0.000% |
| Price spikes (|log-ret| > 40%) | ✅ PASS | 0 | 0.000% |
| Stale prices (≥5 repeats) | ✅ PASS | 0 | 0.000% |
| Zero volume | ✅ PASS | 0 | 0.000% |
| Volume spikes (>10× rolling median) | ⚠️ WARN | 14 | 0.141% |
| Return profile | ✅ PASS | 0 | 0.000% |

---

## Check Details

### ✅ Completeness

100% complete (9,901 rows)

### ✅ Duplicate timestamps

0 duplicate timestamp(s)

### ✅ Zero / negative prices

0 candle(s) with zero or negative OHLC

### ✅ OHLC logic

0 violation(s) (High<Low/Open/Close or Low>Open/Close)

### ✅ Price spikes (|log-ret| > 40%)

0 spike(s) above 40% threshold

### ✅ Stale prices (≥5 repeats)

0 candle(s) inside a frozen-price run

### ✅ Zero volume

0 zero-volume candle(s) (0.00%)

### ⚠️ Volume spikes (>10× rolling median)

14 spike(s) above 10× rolling median

_First 10 flagged rows:_

| Date                      |    Open |    High |    Low |   Close |           Volume |   volume_ratio |
|:--------------------------|--------:|--------:|-------:|--------:|-----------------:|---------------:|
| 2022-01-22 08:00:00+00:00 | 100.35  | 103.775 | 87.505 |  98.685 | 898060           |           12.1 |
| 2022-10-13 12:00:00+00:00 |  28.78  |  29.93  | 27.6   |  29.635 |      5.86983e+06 |           15.6 |
| 2022-11-08 16:00:00+00:00 |  27.69  |  31.84  | 18.03  |  22.76  |      2.81235e+07 |           16.9 |
| 2022-11-09 08:00:00+00:00 |  18.215 |  18.235 | 13.34  |  17.42  |      3.96751e+07 |           17.2 |
| 2022-11-09 12:00:00+00:00 |  17.42  |  18.54  | 12.24  |  12.835 |      2.57522e+07 |           11.2 |
| 2022-11-09 16:00:00+00:00 |  12.835 |  14.245 |  8.565 |  11.16  |      5.58895e+07 |           21   |
| 2022-11-09 20:00:00+00:00 |  11.16  |  11.68  |  7.535 |  10.61  |      3.79769e+07 |           12.4 |
| 2022-12-14 16:00:00+00:00 |  14.48  |  14.96  | 14.175 |  14.3   |      8.29072e+06 |           11.2 |
| 2022-12-29 20:00:00+00:00 |   8.775 |  10.96  |  7.85  |   9.61  |      5.16481e+07 |           27.2 |
| 2023-04-11 12:00:00+00:00 |  22.232 |  23.487 | 22.138 |  23.311 |      7.57745e+06 |           11.5 |

### ✅ Return profile

mean=-0.00006  std=0.02102  skew=-0.20  excess-kurt=12.4

