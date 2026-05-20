# Audit Report — ETHUSDT 4h

Generated : 2026-04-25 13:58:47 UTC
Source    : ETHUSDT_4h_start_2021-03-15_end_2026-04-22.parquet
Rows      : 11,185

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
| Volume spikes (>10× rolling median) | ⚠️ WARN | 12 | 0.107% |
| Return profile | ✅ PASS | 0 | 0.000% |

---

## Check Details

### ✅ Completeness

100% complete (11,185 rows)

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

12 spike(s) above 10× rolling median

_First 10 flagged rows:_

| Date                      |    Open |    High |     Low |   Close |           Volume |   volume_ratio |
|:--------------------------|--------:|--------:|--------:|--------:|-----------------:|---------------:|
| 2021-05-19 12:00:00+00:00 | 2723    | 2780    | 1778.95 | 2748.15 | 871946           |           25.8 |
| 2021-09-07 12:00:00+00:00 | 3751.2  | 3777    | 2960    | 3451.85 | 245220           |           12.9 |
| 2022-11-08 16:00:00+00:00 | 1462    | 1580    | 1201.25 | 1312.75 |      3.168e+06   |           18.2 |
| 2023-07-13 16:00:00+00:00 | 1932.41 | 2014.99 | 1930.78 | 1995.89 | 621783           |           11.3 |
| 2023-08-17 12:00:00+00:00 | 1787.81 | 1793.53 | 1720.56 | 1738.93 | 334663           |           10.5 |
| 2023-08-17 20:00:00+00:00 | 1737.81 | 1739.05 | 1465.38 | 1680.59 | 923456           |           24.8 |
| 2023-08-29 12:00:00+00:00 | 1641.32 | 1735.95 | 1639.5  | 1715.21 | 498962           |           14.8 |
| 2023-10-16 12:00:00+00:00 | 1582.01 | 1642.37 | 1563.6  | 1576.6  | 583296           |           12.3 |
| 2024-08-05 00:00:00+00:00 | 2687.41 | 2695.74 | 2086.92 | 2311.65 |      1.87631e+06 |           10.4 |
| 2025-02-03 00:00:00+00:00 | 2868.61 | 2871.84 | 2079    | 2525.55 |      2.6802e+06  |           14.6 |

### ✅ Return profile

mean=0.00002  std=0.01589  skew=-0.32  excess-kurt=6.9

