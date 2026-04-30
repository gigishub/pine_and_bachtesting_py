# Bear Strategy — KDE Price Cluster Edge Check  (entry_tf=1h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `1h` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `window` | `200` |
| `bandwidth_mult` | `1.0` |
| `kde_n_points` | `500` |
| `value_area_pct` | `0.7` |
| `lower_duration` | `5` |

```text

── Per-Pair Results ──

  BTCUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      44.10  1.183  20.4     23424
kde_upper        46.31  1.294  18.7      8436
kde_lower        42.99  1.131  21.2     15004
kde_lower_fresh  44.00  1.178  21.1      2091
    kde_upper covers 36.0% of regime bars  
    kde_lower covers 64.1% of regime bars  
    kde_lower_fresh covers 8.9% of regime bars  

  ETHUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      44.92  1.223  19.9     23825
kde_upper        47.49  1.357  18.3      9021
kde_lower        43.34  1.147  21.0     14824
kde_lower_fresh  41.86  1.080  20.7      2126
    kde_upper covers 37.9% of regime bars  
    kde_lower covers 62.2% of regime bars  
    kde_lower_fresh covers 8.9% of regime bars  

  SOLUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      44.92  1.223  19.5     22275
kde_upper        46.21  1.289  18.4      7931
kde_lower        44.30  1.193  20.3     14383
kde_lower_fresh  49.36  1.462  21.4      1805
    kde_upper covers 35.6% of regime bars  
    kde_lower covers 64.6% of regime bars  
    kde_lower_fresh covers 8.1% of regime bars  

  BNBUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      44.97  1.226  19.0     20171
kde_upper        45.28  1.241  17.6      6923
kde_lower        44.77  1.216  19.8     13265
kde_lower_fresh  46.83  1.321  21.3      1768
    kde_upper covers 34.3% of regime bars  
    kde_lower covers 65.8% of regime bars  
    kde_lower_fresh covers 8.8% of regime bars  

  XRPUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      47.04  1.332  21.5     24534
kde_upper        48.23  1.398  20.2      8602
kde_lower        46.36  1.296  22.3     15954
kde_lower_fresh  47.04  1.333  25.5      2115
    kde_upper covers 35.1% of regime bars  
    kde_lower covers 65.0% of regime bars  
    kde_lower_fresh covers 8.6% of regime bars  

── KDE Price Cluster Edge Verdict ──

  Baseline (regime_only):  avg WR 45.2%  avg PF 1.238
  KDE config:  window=200  bw_mult=1  lower_duration=5

  kde_upper           avg WR lift +1.52pp  avg PF 1.316  avg PF lift +0.078  pairs ≥ threshold: 2/5  ❌  ⚠️ WR 3p
    BTCUSDT     WR 46.31%  lift +2.21pp / req 1.35pp  PF 1.294  lift +0.111 / req 0.100  trades 8,436  cov 36.0%  ✅
    ETHUSDT     WR 47.49%  lift +2.57pp / req 1.31pp  PF 1.357  lift +0.133 / req 0.100  trades 9,021  cov 37.9%  ✅
    SOLUSDT     WR 46.21%  lift +1.29pp / req 1.40pp  PF 1.289  lift +0.065 / req 0.100  trades 7,931  ⚠️ WR  cov 35.6%  ❌
    BNBUSDT     WR 45.28%  lift +0.32pp / req 1.49pp  PF 1.241  lift +0.016 / req 0.100  trades 6,923  ⚠️ WR  cov 34.3%  ❌
    XRPUSDT     WR 48.23%  lift +1.19pp / req 1.35pp  PF 1.398  lift +0.065 / req 0.100  trades 8,602  ⚠️ WR  cov 35.1%  ❌

  kde_lower           avg WR lift -0.84pp  avg PF 1.197  avg PF lift -0.041  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p
    BTCUSDT     WR 42.99%  lift -1.11pp / req 1.01pp  PF 1.131  lift -0.052 / req 0.050  trades 15,004  ⚠️ WR  cov 64.1%  ❌
    ETHUSDT     WR 43.34%  lift -1.58pp / req 1.02pp  PF 1.147  lift -0.076 / req 0.050  trades 14,824  ⚠️ WR  cov 62.2%  ❌
    SOLUSDT     WR 44.30%  lift -0.62pp / req 1.04pp  PF 1.193  lift -0.030 / req 0.050  trades 14,383  ⚠️ WR  cov 64.6%  ❌
    BNBUSDT     WR 44.77%  lift -0.19pp / req 1.08pp  PF 1.216  lift -0.010 / req 0.050  trades 13,265  ⚠️ WR  cov 65.8%  ❌
    XRPUSDT     WR 46.36%  lift -0.68pp / req 0.99pp  PF 1.296  lift -0.036 / req 0.050  trades 15,954  ⚠️ WR  cov 65.0%  ❌

  kde_lower_fresh     avg WR lift +0.63pp  avg PF 1.275  avg PF lift +0.037  pairs ≥ threshold: 1/5  ❌  ⚠️ WR 4p  ⚠️ low count 5p
    BTCUSDT     WR 44.00%  lift -0.10pp / req 2.71pp  PF 1.178  lift -0.005 / req 0.100  trades 2,091  ⚠️ WR  ⚠️ cov 8.9%  ❌
    ETHUSDT     WR 41.86%  lift -3.06pp / req 2.70pp  PF 1.080  lift -0.143 / req 0.100  trades 2,126  ⚠️ WR  ⚠️ cov 8.9%  ❌
    SOLUSDT     WR 49.36%  lift +4.44pp / req 2.93pp  PF 1.462  lift +0.239 / req 0.100  trades 1,805  ⚠️ cov 8.1%  ✅
    BNBUSDT     WR 46.83%  lift +1.87pp / req 2.96pp  PF 1.321  lift +0.096 / req 0.100  trades 1,768  ⚠️ WR  ⚠️ cov 8.8%  ❌
    XRPUSDT     WR 47.04%  lift +0.00pp / req 2.71pp  PF 1.333  lift +0.000 / req 0.100  trades 2,115  ⚠️ WR  ⚠️ cov 8.6%  ❌

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  consistent across ≥ 4 of 5 pairs

  ❌  KDE CLUSTER EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Adjust window (currently 200) — try 100 or 300
        • Adjust bandwidth_mult (currently 1) — try 0.5 or 2.0
        • Adjust lower_duration (currently 5) — try 3 or 10
        • Try a different entry_tf in config.py
        • KDE clusters may need volume weighting for consistent edge
```
