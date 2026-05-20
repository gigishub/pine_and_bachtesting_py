# Audit Report — ETHUSDT 15m

Generated : 2026-04-25 13:58:48 UTC
Source    : ETHUSDT_15m_start_2021-03-15_end_2026-04-22.parquet
Rows      : 178,945

## 🟢 Trust Score: 99.8 / 100

## Summary

| Check | Status | Affected | % of rows |
|-------|--------|:--------:|----------:|
| Completeness | ✅ PASS | 0 | 0.000% |
| Duplicate timestamps | ✅ PASS | 0 | 0.000% |
| Zero / negative prices | ✅ PASS | 0 | 0.000% |
| OHLC logic | ✅ PASS | 0 | 0.000% |
| Price spikes (|log-ret| > 20%) | ✅ PASS | 0 | 0.000% |
| Stale prices (≥5 repeats) | ✅ PASS | 0 | 0.000% |
| Zero volume | ⚠️ WARN | 2 | 0.001% |
| Volume spikes (>10× rolling median) | ⚠️ WARN | 1,715 | 0.958% |
| Return profile | ⚠️ WARN | 1 | 0.001% |

---

## Check Details

### ✅ Completeness

100% complete (178,945 rows)

### ✅ Duplicate timestamps

0 duplicate timestamp(s)

### ✅ Zero / negative prices

0 candle(s) with zero or negative OHLC

### ✅ OHLC logic

0 violation(s) (High<Low/Open/Close or Low>Open/Close)

### ✅ Price spikes (|log-ret| > 20%)

0 spike(s) above 20% threshold

### ✅ Stale prices (≥5 repeats)

0 candle(s) inside a frozen-price run

### ⚠️ Zero volume

2 zero-volume candle(s) (0.00%)

_First 2 flagged rows:_

| Date                      |    Open |    High |     Low |   Close |   Volume |
|:--------------------------|--------:|--------:|--------:|--------:|---------:|
| 2022-04-06 08:30:00+00:00 | 3338.55 | 3338.55 | 3338.55 | 3338.55 |        0 |
| 2022-04-06 08:45:00+00:00 | 3338.55 | 3338.55 | 3338.55 | 3338.55 |        0 |

### ⚠️ Volume spikes (>10× rolling median)

1715 spike(s) above 10× rolling median

_First 10 flagged rows:_

| Date                      |    Open |    High |     Low |   Close |   Volume |   volume_ratio |
|:--------------------------|--------:|--------:|--------:|--------:|---------:|---------------:|
| 2021-03-15 06:30:00+00:00 | 1834.95 | 1835.6  | 1800.5  | 1802.05 |  9936.53 |           14.9 |
| 2021-03-15 09:15:00+00:00 | 1785.05 | 1791.95 | 1743.9  | 1755.8  | 10336.8  |           11.7 |
| 2021-03-20 13:15:00+00:00 | 1858    | 1872.65 | 1858    | 1866.5  |  4023.77 |           19.8 |
| 2021-03-20 13:45:00+00:00 | 1857.3  | 1859.9  | 1841.4  | 1847.4  |  3915.37 |           15.9 |
| 2021-03-21 00:00:00+00:00 | 1806.85 | 1806.85 | 1787.25 | 1803.1  |  4376.21 |           12.9 |
| 2021-03-22 20:45:00+00:00 | 1704.15 | 1712.55 | 1673    | 1678.3  |  7942.81 |           16   |
| 2021-03-24 19:30:00+00:00 | 1658.55 | 1661.9  | 1626    | 1630.1  |  8098.3  |           16.7 |
| 2021-03-24 20:00:00+00:00 | 1636.8  | 1637.45 | 1603.15 | 1607.75 |  6185.19 |           12.7 |
| 2021-03-24 20:15:00+00:00 | 1607.75 | 1622.8  | 1587.85 | 1591.3  |  5615.82 |           11.4 |
| 2021-03-24 20:30:00+00:00 | 1591.25 | 1612.9  | 1581.05 | 1612.9  | 10080.7  |           20.1 |

### ⚠️ Return profile

mean=0.00000  std=0.00411  skew=-0.50  excess-kurt=53.9  ⚠ extreme kurtosis (53.9)

