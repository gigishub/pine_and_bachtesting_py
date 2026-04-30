# Bear Strategy — KDE Price Cluster Edge Check  (entry_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `4h` |
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
regime_only      43.76  1.167  22.4      5850
kde_upper        46.79  1.319  17.8      1310
kde_lower        43.09  1.136  24.0      4558
kde_lower_fresh  50.18  1.511  24.0       550
    kde_upper covers 22.4% of regime bars  
    kde_lower covers 77.9% of regime bars  
    kde_lower_fresh covers 9.4% of regime bars  

  ETHUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      41.95  1.084  22.6      5922
kde_upper        48.92  1.436  21.1      1292
kde_lower        39.98  0.999  23.2      4665
kde_lower_fresh  42.74  1.120  30.3       606
    kde_upper covers 21.8% of regime bars  
    kde_lower covers 78.8% of regime bars  
    kde_lower_fresh covers 10.2% of regime bars  

  SOLUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      43.55  1.157  22.4      5557
kde_upper        46.93  1.326  19.8      1351
kde_lower        42.44  1.106  23.1      4225
kde_lower_fresh  40.11  1.005  19.4       536
    kde_upper covers 24.3% of regime bars  
    kde_lower covers 76.0% of regime bars  
    kde_lower_fresh covers 9.6% of regime bars  

  BNBUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      45.56  1.255  19.1      4980
kde_upper        50.19  1.511  18.5      1072
kde_lower        44.30  1.193  19.4      3930
kde_lower_fresh  53.19  1.705  20.3       470
    kde_upper covers 21.5% of regime bars  
    kde_lower covers 78.9% of regime bars  
    kde_lower_fresh covers 9.4% of regime bars  

  XRPUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      43.04  1.133  22.3      5976
kde_upper        52.37  1.650  17.9      1285
kde_lower        40.50  1.021  23.6      4719
kde_lower_fresh  49.67  1.480  28.0       453
    kde_upper covers 21.5% of regime bars  
    kde_lower covers 79.0% of regime bars  
    kde_lower_fresh covers 7.6% of regime bars  

── KDE Price Cluster Edge Verdict ──

  Baseline (regime_only):  avg WR 43.6%  avg PF 1.159
  KDE config:  window=200  bw_mult=1  lower_duration=5

  kde_upper           avg WR lift +5.47pp  avg PF 1.449  avg PF lift +0.289  pairs ≥ threshold: 5/5  ✅  ⚠️ WR 1p  ⚠️ low count 5p  ⚠️ weak regime 1p
    BTCUSDT     WR 46.79%  lift +3.03pp / req 3.43pp  PF 1.319  lift +0.152 / req 0.100  trades 1,310  ⚠️ WR  ⚠️ cov 22.4%  ✅
    ETHUSDT     WR 48.92%  lift +6.97pp / req 3.43pp  PF 1.436  lift +0.353 / req 0.100  trades 1,292  ⚠️ cov 21.8%  ⚠️ reg PF 1.084  ✅
    SOLUSDT     WR 46.93%  lift +3.38pp / req 3.37pp  PF 1.326  lift +0.169 / req 0.100  trades 1,351  ⚠️ cov 24.3%  ✅
    BNBUSDT     WR 50.19%  lift +4.62pp / req 3.80pp  PF 1.511  lift +0.256 / req 0.100  trades 1,072  ⚠️ cov 21.5%  ✅
    XRPUSDT     WR 52.37%  lift +9.33pp / req 3.45pp  PF 1.650  lift +0.516 / req 0.100  trades 1,285  ⚠️ cov 21.5%  ✅

  kde_lower           avg WR lift -1.51pp  avg PF 1.091  avg PF lift -0.068  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p  ⚠️ weak regime 1p
    BTCUSDT     WR 43.09%  lift -0.67pp / req 1.84pp  PF 1.136  lift -0.031 / req 0.100  trades 4,558  ⚠️ WR  cov 77.9%  ❌
    ETHUSDT     WR 39.98%  lift -1.97pp / req 1.81pp  PF 0.999  lift -0.085 / req 0.100  trades 4,665  ⚠️ WR  cov 78.8%  ⚠️ reg PF 1.084  ❌
    SOLUSDT     WR 42.44%  lift -1.11pp / req 1.91pp  PF 1.106  lift -0.051 / req 0.100  trades 4,225  ⚠️ WR  cov 76.0%  ❌
    BNBUSDT     WR 44.30%  lift -1.26pp / req 1.99pp  PF 1.193  lift -0.062 / req 0.100  trades 3,930  ⚠️ WR  cov 78.9%  ❌
    XRPUSDT     WR 40.50%  lift -2.54pp / req 1.80pp  PF 1.021  lift -0.113 / req 0.100  trades 4,719  ⚠️ WR  cov 79.0%  ❌

  kde_lower_fresh     avg WR lift +3.61pp  avg PF 1.364  avg PF lift +0.205  pairs ≥ threshold: 3/5  ❌  ⚠️ WR 2p  ⚠️ low count 5p  ⚠️ weak regime 1p
    BTCUSDT     WR 50.18%  lift +6.42pp / req 5.29pp  PF 1.511  lift +0.344 / req 0.100  trades 550  ⚠️ cov 9.4%  ✅
    ETHUSDT     WR 42.74%  lift +0.79pp / req 5.01pp  PF 1.120  lift +0.036 / req 0.100  trades 606  ⚠️ WR  ⚠️ cov 10.2%  ⚠️ reg PF 1.084  ❌
    SOLUSDT     WR 40.11%  lift -3.44pp / req 5.35pp  PF 1.005  lift -0.152 / req 0.100  trades 536  ⚠️ WR  ⚠️ cov 9.6%  ❌
    BNBUSDT     WR 53.19%  lift +7.63pp / req 5.74pp  PF 1.705  lift +0.449 / req 0.100  trades 470  ⚠️ cov 9.4%  ✅
    XRPUSDT     WR 49.67%  lift +6.63pp / req 5.82pp  PF 1.480  lift +0.347 / req 0.100  trades 453  ⚠️ cov 7.6%  ✅

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  consistent across ≥ 4 of 5 pairs

  ✅  KDE CLUSTER EDGE CONFIRMED — at least one population creates predictive edge.
      Best performer: kde_upper  (avg PF 1.449)
      Warnings (results valid but interpret with care):
        ⚠️  [kde_upper] WR lift below threshold on: BTCUSDT
        ⚠️  [kde_upper] low trade count (<30% of regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
        ⚠️  [kde_upper] weak regime baseline (PF < 1.1) on: ETHUSDT
        ⚠️  [kde_lower] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
        ⚠️  [kde_lower] weak regime baseline (PF < 1.1) on: ETHUSDT
        ⚠️  [kde_lower_fresh] WR lift below threshold on: ETHUSDT, SOLUSDT
        ⚠️  [kde_lower_fresh] low trade count (<30% of regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
        ⚠️  [kde_lower_fresh] weak regime baseline (PF < 1.1) on: ETHUSDT
      Proceed to the next setup step.

  ── Population Interpretation ──
      kde_upper       ✅ — opening above the POC (cluster resistance reclaim) adds mean-reversion short edge within the bear regime.
      kde_lower       ❌ — unrestricted POC breakdown does not add reliable edge.
      kde_lower_fresh ❌ — lower_duration=5 qualifier does not help.
```
