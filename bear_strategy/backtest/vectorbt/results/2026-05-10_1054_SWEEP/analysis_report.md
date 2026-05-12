# Bear Strategy — Sweep Analysis Report

**Generated:** 2026-05-10 12:52  
**Sweep run:** `2026-05-10_1054_SWEEP`  
**File:** `bear_strategy/backtest/vectorbt/results/2026-05-10_1054_SWEEP/sweep_summary.csv`  

---

## Pass / Fail Gates

| Gate | Value |
|------|-------|
| Min SQN | 0.0 |
| Min Profit Factor | 1.0 |
| Min Trades | 10 |
| Min Win Rate % | 0.0 |
| Min Pairs Passing | 1 |

**Universe tested:** ADAUSDT, BNBUSDT, BTCUSDT, DOTUSDT, ETHUSDT, LTCUSDT, SOLUSDT, XLMUSDT, XRPUSDT (9 pairs)  
**Pairs included in this run:** ADAUSDT, BNBUSDT, BTCUSDT, DOTUSDT, ETHUSDT, LTCUSDT, SOLUSDT, XLMUSDT, XRPUSDT  
**Total combos in sweep:** 22  

---

## Executive Summary

- **22** combo(s) cleared the gates out of 22 tested.
- **Top combo (passing-pairs avg):** SL=2.5× TP=6.0×
  - Breadth Score: `0.1921`
  - Pairs: 7 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT, XRPUSDT
  - Avg Return: `16.69%`  |  SQN: `0.922` 🔴 weak
  - Profit Factor: `1.202` 🟡 ok  |  Sharpe: `0.610` 🟡 ok

---

## Ranked Combos

### All pairs averaged

|    | Signature       |   SL× |   TP× | Pairs (9 total)                                                   |   Breadth Score |   Avg Score (all pairs) |   Avg Return [%] |   Avg SQN |   Avg Profit Factor |   Avg Expectancy [%] |   Avg Win Rate [%] |   Avg Max. Drawdown [%] |   Avg Sharpe Ratio |   Avg # Trades |
|---:|:----------------|------:|------:|:------------------------------------------------------------------|----------------:|------------------------:|-----------------:|----------:|--------------------:|---------------------:|-------------------:|------------------------:|-------------------:|---------------:|
|  1 | SL=2.5× TP=6.0× |   2.5 |   6   | 7 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT, XRPUSDT |          0.161  |                  0.207  |           10.363 |     0.472 |               1.128 |                0.266 |             35.046 |                  13.438 |              0.39  |        113.889 |
|  2 | SL=3.0× TP=4.0× |   3   |   4   | 7 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT, XRPUSDT |          0.1503 |                  0.1933 |            7.19  |     0.46  |               1.101 |                0.173 |             48.681 |                  10.286 |              0.352 |        128.556 |
|  3 | SL=1.5× TP=6.0× |   1.5 |   6   | 7 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT, XRPUSDT |          0.1356 |                  0.1743 |           16.138 |     0.446 |               1.121 |                0.164 |             25.473 |                  20.431 |              0.426 |        152.667 |
|  4 | SL=3.0× TP=6.0× |   3   |   6   | 6 → ADAUSDT, BNBUSDT, DOTUSDT, SOLUSDT, XLMUSDT, XRPUSDT          |          0.1305 |                  0.1957 |            8.018 |     0.454 |               1.112 |                0.271 |             38.455 |                  10.782 |              0.351 |         98.889 |
|  5 | SL=3.0× TP=5.0× |   3   |   5   | 7 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT, XRPUSDT |          0.1298 |                  0.1669 |            6.831 |     0.233 |               1.1   |                0.127 |             42.812 |                   9.958 |              0.333 |        107.778 |
|  6 | SL=2.5× TP=3.0× |   2.5 |   3   | 6 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT, XRPUSDT          |          0.1253 |                  0.1879 |            4.135 |     0.471 |               1.061 |                0.147 |             51.214 |                  14.817 |              0.24  |        163.667 |
|  7 | SL=2.5× TP=4.0× |   2.5 |   4   | 6 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT          |          0.1213 |                  0.182  |            6.127 |     0.387 |               1.083 |                0.152 |             44.122 |                  13.735 |              0.285 |        146.667 |
|  8 | SL=2.0× TP=6.0× |   2   |   6   | 6 → ADAUSDT, BNBUSDT, DOTUSDT, SOLUSDT, XLMUSDT, XRPUSDT          |          0.1104 |                  0.1656 |            8.926 |     0.265 |               1.082 |                0.127 |             29.863 |                  16.936 |              0.297 |        135.333 |
|  9 | SL=1.5× TP=4.0× |   1.5 |   4   | 7 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT, XRPUSDT |          0.105  |                  0.135  |            4.596 |     0.264 |               1.045 |                0.069 |             32.635 |                  22.161 |              0.189 |        187.778 |
| 10 | SL=2.5× TP=5.0× |   2.5 |   5   | 5 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XRPUSDT                   |          0.0928 |                  0.167  |            7.367 |     0.198 |               1.098 |                0.124 |             38.775 |                  13.532 |              0.315 |        125     |
| 11 | SL=2.0× TP=4.0× |   2   |   4   | 6 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT          |          0.0911 |                  0.1366 |            2.822 |     0.139 |               1.03  |                0.051 |             38.225 |                  17.52  |              0.148 |        167.444 |
| 12 | SL=2.0× TP=3.0× |   2   |   3   | 5 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT                   |          0.0848 |                  0.1527 |            0.647 |     0.189 |               1.018 |                0.064 |             45.263 |                  19.057 |              0.096 |        184.556 |
| 13 | SL=1.5× TP=3.0× |   1.5 |   3   | 5 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XRPUSDT                   |          0.0821 |                  0.1479 |            0.135 |     0.161 |               1.02  |                0.052 |             38.849 |                  23.143 |              0.07  |        204.778 |
| 14 | SL=1.0× TP=6.0× |   1   |   6   | 5 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XRPUSDT                   |          0.0802 |                  0.1444 |           14.082 |     0.411 |               1.084 |                0.14  |             19.306 |                  28.89  |              0.296 |        175.778 |
| 15 | SL=1.5× TP=5.0× |   1.5 |   5   | 5 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XRPUSDT                   |          0.077  |                  0.1386 |            8.443 |     0.187 |               1.066 |                0.073 |             28.245 |                  22.169 |              0.261 |        165.222 |
| 16 | SL=1.0× TP=5.0× |   1   |   5   | 5 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XRPUSDT                   |          0.0766 |                  0.1379 |            9.652 |     0.3   |               1.057 |                0.103 |             21.813 |                  27.917 |              0.239 |        186.667 |
| 17 | SL=2.0× TP=5.0× |   2   |   5   | 5 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT                   |          0.0676 |                  0.1216 |            1.803 |    -0.141 |               1.022 |               -0.012 |             32.706 |                  18.273 |              0.108 |        145.667 |
| 18 | SL=1.0× TP=3.0× |   1   |   3   | 4 → BNBUSDT, DOTUSDT, SOLUSDT, XRPUSDT                            |          0.0579 |                  0.1304 |           -2.392 |    -0.022 |               1.002 |                0.027 |             30.66  |                  27.282 |             -0.004 |        222.778 |
| 19 | SL=1.5× TP=2.0× |   1.5 |   2   | 4 → BNBUSDT, DOTUSDT, SOLUSDT, XRPUSDT                            |          0.0482 |                  0.1083 |           -7.159 |    -0.207 |               0.962 |               -0.025 |             47.987 |                  23.333 |             -0.189 |        232.778 |
| 20 | SL=1.0× TP=4.0× |   1   |   4   | 3 → BNBUSDT, SOLUSDT, XRPUSDT                                     |          0.0421 |                  0.1263 |            1.723 |     0.166 |               1.028 |                0.056 |             25.203 |                  27.862 |              0.109 |        206.444 |
| 21 | SL=1.0× TP=2.0× |   1   |   2   | 3 → BNBUSDT, SOLUSDT, XRPUSDT                                     |          0.0389 |                  0.1167 |           -6.534 |    -0.165 |               0.98  |               -0.009 |             39.81  |                  27.658 |             -0.127 |        244.889 |
| 22 | SL=1.0× TP=1.5× |   1   |   1.5 | 2 → BNBUSDT, SOLUSDT                                              |          0.0181 |                  0.0815 |          -14.753 |    -0.482 |               0.918 |               -0.046 |             45.394 |                  29.158 |             -0.412 |        255.444 |

### Passing pairs averaged

|    | Signature       |   SL× |   TP× | Pairs (9 total)                                                   |   Breadth Score |   Avg Score (passing) |   Avg Return [%] |   Avg SQN |   Avg Profit Factor |   Avg Expectancy [%] |   Avg Win Rate [%] |   Avg Max. Drawdown [%] |   Avg Sharpe Ratio |   Avg # Trades |
|---:|:----------------|------:|------:|:------------------------------------------------------------------|----------------:|----------------------:|-----------------:|----------:|--------------------:|---------------------:|-------------------:|------------------------:|-------------------:|---------------:|
|  1 | SL=2.5× TP=6.0× |   2.5 |   6   | 7 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT, XRPUSDT |          0.1921 |                0.2469 |           16.689 |     0.922 |               1.202 |                0.522 |             36.643 |                  11.231 |              0.61  |        109.143 |
|  2 | SL=3.0× TP=4.0× |   3   |   4   | 7 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT, XRPUSDT |          0.1772 |                0.2278 |           11.963 |     0.824 |               1.167 |                0.348 |             50.336 |                   8.464 |              0.564 |        126.571 |
|  3 | SL=2.5× TP=3.0× |   2.5 |   3   | 6 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT, XRPUSDT          |          0.1659 |                0.2489 |           11.469 |     1.124 |               1.142 |                0.35  |             53.243 |                  12.022 |              0.545 |        148.833 |
|  4 | SL=3.0× TP=6.0× |   3   |   6   | 6 → ADAUSDT, BNBUSDT, DOTUSDT, SOLUSDT, XLMUSDT, XRPUSDT          |          0.1643 |                0.2465 |           14.826 |     0.848 |               1.213 |                0.538 |             40.651 |                   8.618 |              0.629 |         98.333 |
|  5 | SL=1.5× TP=6.0× |   1.5 |   6   | 7 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT, XRPUSDT |          0.1639 |                0.2107 |           25.464 |     0.775 |               1.189 |                0.284 |             26.63  |                  17.17  |              0.638 |        147.571 |
|  6 | SL=2.5× TP=4.0× |   2.5 |   4   | 6 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT          |          0.1575 |                0.2363 |           13.853 |     0.931 |               1.165 |                0.363 |             46.277 |                  10.618 |              0.58  |        136.833 |
|  7 | SL=3.0× TP=5.0× |   3   |   5   | 7 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT, XRPUSDT |          0.1496 |                0.1924 |           10.594 |     0.54  |               1.156 |                0.312 |             44.101 |                   8.969 |              0.495 |        106.286 |
|  8 | SL=2.0× TP=6.0× |   2   |   6   | 6 → ADAUSDT, BNBUSDT, DOTUSDT, SOLUSDT, XLMUSDT, XRPUSDT          |          0.1426 |                0.2139 |           20.032 |     0.736 |               1.182 |                0.335 |             31.832 |                  13.348 |              0.614 |        130.667 |
|  9 | SL=2.5× TP=5.0× |   2.5 |   5   | 5 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XRPUSDT                   |          0.1282 |                0.2308 |           16.297 |     0.777 |               1.211 |                0.412 |             41.383 |                  10.539 |              0.649 |        111.4   |
| 10 | SL=1.5× TP=4.0× |   1.5 |   4   | 7 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT, XRPUSDT |          0.1276 |                0.1641 |           13.274 |     0.555 |               1.101 |                0.146 |             33.985 |                  17.051 |              0.426 |        179.429 |
| 11 | SL=2.0× TP=3.0× |   2   |   3   | 5 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT                   |          0.1263 |                0.2273 |           11.324 |     1.024 |               1.11  |                0.282 |             47.783 |                  13.44  |              0.48  |        161.2   |
| 12 | SL=1.0× TP=6.0× |   1   |   6   | 5 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XRPUSDT                   |          0.1258 |                0.2264 |           38.044 |     0.963 |               1.228 |                0.321 |             21.442 |                  23.959 |              0.699 |        153     |
| 13 | SL=1.5× TP=3.0× |   1.5 |   3   | 5 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XRPUSDT                   |          0.1223 |                0.2201 |           16.911 |     0.925 |               1.14  |                0.219 |             41.694 |                  14.273 |              0.576 |        181.2   |
| 14 | SL=1.0× TP=5.0× |   1   |   5   | 5 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XRPUSDT                   |          0.1184 |                0.2131 |           30.606 |     0.916 |               1.178 |                0.273 |             23.839 |                  22.947 |              0.627 |        160.6   |
| 15 | SL=2.0× TP=4.0× |   2   |   4   | 6 → ADAUSDT, BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT          |          0.1163 |                0.1744 |           10.344 |     0.602 |               1.091 |                0.196 |             39.82  |                  13.625 |              0.391 |        155.833 |
| 16 | SL=1.5× TP=5.0× |   1.5 |   5   | 5 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XRPUSDT                   |          0.1097 |                0.1975 |           22.331 |     0.668 |               1.174 |                0.228 |             30.399 |                  15.654 |              0.618 |        146.8   |
| 17 | SL=1.0× TP=3.0× |   1   |   3   | 4 → BNBUSDT, DOTUSDT, SOLUSDT, XRPUSDT                            |          0.1069 |                0.2406 |           25.996 |     1.101 |               1.177 |                0.236 |             34.34  |                  18.025 |              0.681 |        191.5   |
| 18 | SL=2.0× TP=5.0× |   2   |   5   | 5 → BNBUSDT, DOTUSDT, ETHUSDT, SOLUSDT, XLMUSDT                   |          0.0916 |                0.1649 |           10.265 |     0.483 |               1.103 |                0.23  |             34.579 |                  13.483 |              0.378 |        125.6   |
| 19 | SL=1.0× TP=4.0× |   1   |   4   | 3 → BNBUSDT, SOLUSDT, XRPUSDT                                     |          0.0856 |                0.2569 |           37.179 |     1.076 |               1.251 |                0.252 |             29.429 |                  16.102 |              0.851 |        168     |
| 20 | SL=1.0× TP=2.0× |   1   |   2   | 3 → BNBUSDT, SOLUSDT, XRPUSDT                                     |          0.0809 |                0.2426 |           24.209 |     1.078 |               1.188 |                0.159 |             44.849 |                  15.293 |              0.735 |        199.333 |
| 21 | SL=1.5× TP=2.0× |   1.5 |   2   | 4 → BNBUSDT, DOTUSDT, SOLUSDT, XRPUSDT                            |          0.0754 |                0.1697 |            7.85  |     0.636 |               1.072 |                0.11  |             50.867 |                  13.541 |              0.344 |        206     |
| 22 | SL=1.0× TP=1.5× |   1   |   1.5 | 2 → BNBUSDT, SOLUSDT                                              |          0.0417 |                0.1877 |            9.524 |     0.78  |               1.093 |                0.104 |             50.49  |                  14.172 |              0.406 |        163     |

---

## Per-Pair Breakdown (Top 3 Combos)

### SL=2.5× TP=6.0×

- ✅ **Passing:** ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT, ADAUSDT, DOTUSDT, XLMUSDT
- ❌ **Failing:** BTCUSDT, LTCUSDT

|    | Symbol   | Pass   |   Score |   Return [%] |    SQN |   Profit Factor |   Expectancy [%] |   Win Rate [%] |   Max. Drawdown [%] |   Sharpe Ratio |   # Trades |
|---:|:---------|:-------|--------:|-------------:|-------:|----------------:|-----------------:|---------------:|--------------------:|---------------:|-----------:|
|  0 | BTCUSDT  | ❌     |  0.0814 |        0.817 | -0.264 |           1.008 |           -0.101 |         33.333 |              13.905 |          0.077 |        132 |
|  1 | LTCUSDT  | ❌     |  0.0526 |      -24.372 | -1.942 |           0.733 |           -1.164 |         25.581 |              28.421 |         -0.84  |        129 |
|  2 | ETHUSDT  | ✅     |  0.1811 |        1.194 |  0.752 |           1.016 |            0.448 |         33     |              13.487 |          0.094 |        100 |
|  3 | SOLUSDT  | ✅     |  0.1572 |       10.066 |  0.302 |           1.133 |            0.186 |         34.615 |              10.237 |          0.474 |        104 |
|  4 | XRPUSDT  | ✅     |  0.1923 |       16.184 |  0.556 |           1.178 |            0.292 |         36.283 |              13.034 |          0.58  |        113 |
|  5 | BNBUSDT  | ✅     |  0.3036 |       18.013 |  1.292 |           1.278 |            0.533 |         39.773 |               7.022 |          0.725 |         88 |
|  6 | ADAUSDT  | ✅     |  0.1778 |       15.654 |  0.48  |           1.145 |            0.229 |         35.211 |              11.746 |          0.517 |        142 |
|  7 | DOTUSDT  | ✅     |  0.4491 |       42.355 |  1.88  |           1.505 |            1.36  |         41.905 |               9.595 |          1.339 |        105 |
|  8 | XLMUSDT  | ✅     |  0.2676 |       13.358 |  1.195 |           1.157 |            0.61  |         35.714 |              13.494 |          0.539 |        112 |

### SL=3.0× TP=4.0×

- ✅ **Passing:** ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT, ADAUSDT, DOTUSDT, XLMUSDT
- ❌ **Failing:** BTCUSDT, LTCUSDT

|    | Symbol   | Pass   |   Score |   Return [%] |    SQN |   Profit Factor |   Expectancy [%] |   Win Rate [%] |   Max. Drawdown [%] |   Sharpe Ratio |   # Trades |
|---:|:---------|:-------|--------:|-------------:|-------:|----------------:|-----------------:|---------------:|--------------------:|---------------:|-----------:|
|  0 | BTCUSDT  | ❌     |  0.075  |       -3.242 | -0.059 |           0.964 |           -0.02  |         45.946 |              14.994 |         -0.09  |        148 |
|  1 | LTCUSDT  | ❌     |  0.0695 |      -15.789 | -1.575 |           0.782 |           -0.861 |         39.837 |              18.328 |         -0.693 |        123 |
|  2 | ETHUSDT  | ✅     |  0.1779 |        3.428 |  0.673 |           1.045 |            0.286 |         48.062 |              10.37  |          0.195 |        129 |
|  3 | SOLUSDT  | ✅     |  0.1226 |        5.767 |  0.087 |           1.092 |            0.046 |         47.748 |               8.502 |          0.362 |        111 |
|  4 | XRPUSDT  | ✅     |  0.1587 |       14.105 |  0.222 |           1.18  |            0.09  |         50.365 |               8.786 |          0.633 |        137 |
|  5 | BNBUSDT  | ✅     |  0.2994 |       11.836 |  1.355 |           1.228 |            0.462 |         53.191 |               5.937 |          0.635 |         94 |
|  6 | ADAUSDT  | ✅     |  0.2004 |       11.711 |  0.672 |           1.125 |            0.262 |         49.39  |               8.749 |          0.486 |        164 |
|  7 | DOTUSDT  | ✅     |  0.2549 |       15.318 |  0.93  |           1.206 |            0.548 |         50.794 |               9.961 |          0.68  |        126 |
|  8 | XLMUSDT  | ✅     |  0.3809 |       21.58  |  1.832 |           1.29  |            0.743 |         52.8   |               6.945 |          0.959 |        125 |

### SL=2.5× TP=3.0×

- ✅ **Passing:** ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT, DOTUSDT, XLMUSDT
- ❌ **Failing:** BTCUSDT, ADAUSDT, LTCUSDT

|    | Symbol   | Pass   |   Score |   Return [%] |    SQN |   Profit Factor |   Expectancy [%] |   Win Rate [%] |   Max. Drawdown [%] |   Sharpe Ratio |   # Trades |
|---:|:---------|:-------|--------:|-------------:|-------:|----------------:|-----------------:|---------------:|--------------------:|---------------:|-----------:|
|  0 | BTCUSDT  | ❌     |  0.0608 |      -14.91  | -0.528 |           0.862 |           -0.121 |         46.842 |              23.536 |         -0.57  |        190 |
|  1 | ADAUSDT  | ❌     |  0.0739 |       -3.571 | -0.691 |           0.968 |           -0.179 |         49.275 |              15.665 |         -0.079 |        207 |
|  2 | LTCUSDT  | ❌     |  0.0633 |      -13.115 | -1.28  |           0.87  |           -0.478 |         45.355 |              22.023 |         -0.461 |        183 |
|  3 | ETHUSDT  | ✅     |  0.1883 |        4.858 |  0.827 |           1.054 |            0.236 |         51.553 |              13.862 |          0.246 |        161 |
|  4 | SOLUSDT  | ✅     |  0.2578 |       12.915 |  1.041 |           1.172 |            0.384 |         52.857 |               9.381 |          0.716 |        140 |
|  5 | XRPUSDT  | ✅     |  0.1227 |        6.852 |  0.223 |           1.07  |            0.063 |         51.19  |              14.882 |          0.325 |        168 |
|  6 | BNBUSDT  | ✅     |  0.3001 |       11.157 |  1.489 |           1.186 |            0.361 |         56.25  |               6.779 |          0.579 |        112 |
|  7 | DOTUSDT  | ✅     |  0.3209 |       21.726 |  1.448 |           1.243 |            0.57  |         54.938 |               9.859 |          0.876 |        162 |
|  8 | XLMUSDT  | ✅     |  0.3035 |       11.308 |  1.713 |           1.127 |            0.484 |         52.667 |              17.367 |          0.525 |        150 |

---

## Gate Bottleneck Analysis

_Pairs failing across all combos by gate (rough count — a pair can fail multiple gates):_

- **SQN**: 7 pair(s) failing
- **Profit Factor**: 7 pair(s) failing
- **# Trades**: 7 pair(s) failing
- **Win Rate [%]**: 7 pair(s) failing

---

## SL × TP Pivot Tables (all pairs, all combos)

### Avg Return [%]

|   SL \ Return [%] |     1.5 |     2.0 |     3.0 |   4.0 |   5.0 |    6.0 |
|------------------:|--------:|--------:|--------:|------:|------:|-------:|
|               1   | -14.753 |  -6.534 |  -2.392 | 1.723 | 9.652 | 14.082 |
|               1.5 | nan     |  -7.159 |   0.135 | 4.596 | 8.443 | 16.138 |
|               2   | nan     | nan     |   0.647 | 2.822 | 1.803 |  8.926 |
|               2.5 | nan     | nan     |   4.135 | 6.127 | 7.367 | 10.363 |
|               3   | nan     | nan     | nan     | 7.19  | 6.831 |  8.018 |

### Avg SQN

|   SL \ SQN |     1.5 |     2.0 |     3.0 |   4.0 |    5.0 |   6.0 |
|-----------:|--------:|--------:|--------:|------:|-------:|------:|
|        1   |  -0.482 |  -0.165 |  -0.022 | 0.166 |  0.3   | 0.411 |
|        1.5 | nan     |  -0.207 |   0.161 | 0.264 |  0.187 | 0.446 |
|        2   | nan     | nan     |   0.189 | 0.139 | -0.141 | 0.265 |
|        2.5 | nan     | nan     |   0.471 | 0.387 |  0.198 | 0.472 |
|        3   | nan     | nan     | nan     | 0.46  |  0.233 | 0.454 |

### Avg Profit Factor

|   SL \ Profit Factor |     1.5 |     2.0 |     3.0 |   4.0 |   5.0 |   6.0 |
|---------------------:|--------:|--------:|--------:|------:|------:|------:|
|                  1   |   0.918 |   0.98  |   1.002 | 1.028 | 1.057 | 1.084 |
|                  1.5 | nan     |   0.962 |   1.02  | 1.045 | 1.066 | 1.121 |
|                  2   | nan     | nan     |   1.018 | 1.03  | 1.022 | 1.082 |
|                  2.5 | nan     | nan     |   1.061 | 1.083 | 1.098 | 1.128 |
|                  3   | nan     | nan     | nan     | 1.101 | 1.1   | 1.112 |

---

## Notes

- This report is generated from in-sample or out-of-sample sweep data.
  Always validate top combos on the **opposite window** before trading.
- Breadth Score = avg\_score × (passing\_pairs / total\_pairs).
  A combo that profits on 8/9 pairs with moderate edge outscores one
  that dominates on 2 pairs.
- See `TRANSLATION_GUIDE.md` for the full hypothesis-test → backtest pipeline.

_Report end._