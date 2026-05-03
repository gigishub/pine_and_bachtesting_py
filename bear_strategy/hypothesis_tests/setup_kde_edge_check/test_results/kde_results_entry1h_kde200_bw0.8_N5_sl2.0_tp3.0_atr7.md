# Bear Strategy — KDE Price Cluster Edge Check  (entry_tf=1h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `1h` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `window` | `200` |
| `bandwidth_mult` | `0.8` |
| `kde_n_points` | `500` |
| `value_area_pct` | `0.7` |
| `lower_duration` | `5` |

```text

── Per-Pair Results ──

  BTCUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      44.05  1.181  20.4     23400
kde_upper        47.34  1.348  21.0      5376
kde_lower        43.36  1.148  20.6     18076
kde_lower_fresh  51.58  1.598  24.4      2148
    kde_upper covers 23.0% of regime bars  
    kde_lower covers 77.2% of regime bars  
    kde_lower_fresh covers 9.2% of regime bars  

  ETHUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      45.01  1.228  20.0     23688
kde_upper        53.47  1.724  21.0      5392
kde_lower        42.77  1.121  19.7     18480
kde_lower_fresh  52.18  1.636  19.8      2528
    kde_upper covers 22.8% of regime bars  
    kde_lower covers 78.0% of regime bars  
    kde_lower_fresh covers 10.7% of regime bars  

  SOLUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      44.92  1.223  19.5     22275
kde_upper        48.22  1.397  18.7      5759
kde_lower        43.88  1.173  19.9     16580
kde_lower_fresh  46.13  1.285  20.9      2120
    kde_upper covers 25.9% of regime bars  
    kde_lower covers 74.4% of regime bars  
    kde_lower_fresh covers 9.5% of regime bars  

  BNBUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      44.95  1.225  19.1     19979
kde_upper        51.53  1.594  21.1      4491
kde_lower        42.90  1.127  18.9     15596
kde_lower_fresh  42.70  1.118  21.2      1944
    kde_upper covers 22.5% of regime bars  
    kde_lower covers 78.1% of regime bars  
    kde_lower_fresh covers 9.7% of regime bars  

  XRPUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      47.02  1.331  21.6     23934
kde_upper        51.31  1.581  22.1      5303
kde_lower        45.88  1.271  21.9     18715
kde_lower_fresh  51.18  1.573  29.0      1860
    kde_upper covers 22.2% of regime bars  
    kde_lower covers 78.2% of regime bars  
    kde_lower_fresh covers 7.8% of regime bars  

── KDE Price Cluster Edge Verdict ──

  Baseline (regime_only):  avg WR 45.2%  avg PF 1.238
  KDE config:  window=200  bw_mult=0.8  lower_duration=5

  kde_upper           avg WR lift +5.18pp  avg PF 1.529  avg PF lift +0.291  pairs ≥ threshold: 5/5  ✅  ⚠️ low count 5p
    BTCUSDT     WR 47.34%  lift +3.29pp / req 1.69pp  PF 1.348  lift +0.168 / req 0.100  trades 5,376  ⚠️ cov 23.0%  ✅
    ETHUSDT     WR 53.47%  lift +8.46pp / req 1.69pp  PF 1.724  lift +0.496 / req 0.100  trades 5,392  ⚠️ cov 22.8%  ✅
    SOLUSDT     WR 48.22%  lift +3.30pp / req 1.64pp  PF 1.397  lift +0.174 / req 0.100  trades 5,759  ⚠️ cov 25.9%  ✅
    BNBUSDT     WR 51.53%  lift +6.57pp / req 1.86pp  PF 1.594  lift +0.369 / req 0.100  trades 4,491  ⚠️ cov 22.5%  ✅
    XRPUSDT     WR 51.31%  lift +4.29pp / req 1.71pp  PF 1.581  lift +0.250 / req 0.100  trades 5,303  ⚠️ cov 22.2%  ✅

  kde_lower           avg WR lift -1.43pp  avg PF 1.168  avg PF lift -0.070  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p
    BTCUSDT     WR 43.36%  lift -0.69pp / req 0.92pp  PF 1.148  lift -0.033 / req 0.050  trades 18,076  ⚠️ WR  cov 77.2%  ❌
    ETHUSDT     WR 42.77%  lift -2.24pp / req 0.91pp  PF 1.121  lift -0.107 / req 0.050  trades 18,480  ⚠️ WR  cov 78.0%  ❌
    SOLUSDT     WR 43.88%  lift -1.04pp / req 0.97pp  PF 1.173  lift -0.051 / req 0.050  trades 16,580  ⚠️ WR  cov 74.4%  ❌
    BNBUSDT     WR 42.90%  lift -2.06pp / req 1.00pp  PF 1.127  lift -0.098 / req 0.050  trades 15,596  ⚠️ WR  cov 78.1%  ❌
    XRPUSDT     WR 45.88%  lift -1.14pp / req 0.91pp  PF 1.271  lift -0.060 / req 0.050  trades 18,715  ⚠️ WR  cov 78.2%  ❌

  kde_lower_fresh     avg WR lift +3.57pp  avg PF 1.442  avg PF lift +0.204  pairs ≥ threshold: 3/5  ❌  ⚠️ WR 2p  ⚠️ low count 5p
    BTCUSDT     WR 51.58%  lift +7.54pp / req 2.68pp  PF 1.598  lift +0.417 / req 0.100  trades 2,148  ⚠️ cov 9.2%  ✅
    ETHUSDT     WR 52.18%  lift +7.17pp / req 2.47pp  PF 1.636  lift +0.409 / req 0.100  trades 2,528  ⚠️ cov 10.7%  ✅
    SOLUSDT     WR 46.13%  lift +1.21pp / req 2.70pp  PF 1.285  lift +0.061 / req 0.100  trades 2,120  ⚠️ WR  ⚠️ cov 9.5%  ❌
    BNBUSDT     WR 42.70%  lift -2.26pp / req 2.82pp  PF 1.118  lift -0.107 / req 0.100  trades 1,944  ⚠️ WR  ⚠️ cov 9.7%  ❌
    XRPUSDT     WR 51.18%  lift +4.17pp / req 2.89pp  PF 1.573  lift +0.242 / req 0.100  trades 1,860  ⚠️ cov 7.8%  ✅

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  consistent across ≥ 4 of 5 pairs

  ✅  KDE CLUSTER EDGE CONFIRMED — at least one population creates predictive edge.
      Best performer: kde_upper  (avg PF 1.529)
      Warnings (results valid but interpret with care):
        ⚠️  [kde_upper] low trade count (<30% of regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
        ⚠️  [kde_lower] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
        ⚠️  [kde_lower_fresh] WR lift below threshold on: SOLUSDT, BNBUSDT
        ⚠️  [kde_lower_fresh] low trade count (<30% of regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
      Proceed to the next setup step.

  ── Population Interpretation ──
      kde_upper       ✅ — opening above the POC (cluster resistance reclaim) adds mean-reversion short edge within the bear regime.
      kde_lower       ❌ — unrestricted POC breakdown does not add reliable edge.
      kde_lower_fresh ❌ — lower_duration=5 qualifier does not help.
```
