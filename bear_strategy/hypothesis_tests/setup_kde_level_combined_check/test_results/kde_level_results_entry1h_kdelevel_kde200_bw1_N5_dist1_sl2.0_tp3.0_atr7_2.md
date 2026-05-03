# Bear Strategy — KDE + Level Proximity Combined Check  (entry_tf=1h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `1h` |
| `kde_tf` | `4h` |
| `context_tf` | `1d` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `kde_window` | `200` |
| `kde_bandwidth_mult` | `1.0` |
| `kde_lower_duration` | `5` |
| `vwap_anchor` | `daily` |
| `vpvr_window` | `50` |
| `vpvr_n_bins` | `50` |
| `setup_distance_atr` | `1.0` |

```text

── Per-Pair Results ──

  BTCUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   44.25  1.191  20.4     23544
kde_gate      48.88  1.434  21.3      6884
vwap_only     45.31  1.243  19.4      8683
vpvr_only     50.49  1.530  25.8      1022
near_setup    45.73  1.264  19.9      9414
kde_and_vwap  48.49  1.412  20.1      2718
kde_and_vpvr  45.27  1.241  27.2       455
kde_and_near  48.17  1.394  20.8      3025
    kde_gate            covers 29.2% of regime bars  ⚠️  LOW
    vwap_only           covers 36.9% of regime bars
    vpvr_only           covers 4.3% of regime bars  ⚠️  LOW
    near_setup          covers 40.0% of regime bars
    kde_and_vwap        covers 11.5% of regime bars  ⚠️  LOW
    kde_and_vpvr        covers 1.9% of regime bars  ⚠️  LOW
    kde_and_near        covers 12.8% of regime bars  ⚠️  LOW

  ETHUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   45.01  1.228  19.9     23904
kde_gate      52.84  1.681  20.4      7004
vwap_only     46.30  1.293  18.6      8805
vpvr_only     47.72  1.369  21.4       876
near_setup    46.54  1.306  18.8      9433
kde_and_vwap  54.42  1.791  18.5      2740
kde_and_vpvr  53.54  1.728  21.5       424
kde_and_near  54.46  1.793  18.9      3030
    kde_gate            covers 29.3% of regime bars  ⚠️  LOW
    vwap_only           covers 36.8% of regime bars
    vpvr_only           covers 3.7% of regime bars  ⚠️  LOW
    near_setup          covers 39.5% of regime bars
    kde_and_vwap        covers 11.5% of regime bars  ⚠️  LOW
    kde_and_vpvr        covers 1.8% of regime bars  ⚠️  LOW
    kde_and_near        covers 12.7% of regime bars  ⚠️  LOW

  SOLUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   44.84  1.219  19.5     22371
kde_gate      48.58  1.417  19.2      7003
vwap_only     45.23  1.239  18.2      8211
vpvr_only     42.94  1.129  21.5       871
near_setup    45.18  1.236  18.5      8849
kde_and_vwap  50.92  1.556  17.9      2651
kde_and_vpvr  47.41  1.352  17.0       464
kde_and_near  51.10  1.567  17.6      2961
    kde_gate            covers 31.3% of regime bars
    vwap_only           covers 36.7% of regime bars
    vpvr_only           covers 3.9% of regime bars  ⚠️  LOW
    near_setup          covers 39.6% of regime bars
    kde_and_vwap        covers 11.9% of regime bars  ⚠️  LOW
    kde_and_vpvr        covers 2.1% of regime bars  ⚠️  LOW
    kde_and_near        covers 13.2% of regime bars  ⚠️  LOW

  BNBUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   44.88  1.222  19.0     20243
kde_gate      49.87  1.492  20.5      5707
vwap_only     45.76  1.266  18.2      7213
vpvr_only     57.43  2.023  18.3       606
near_setup    46.34  1.295  18.1      7627
kde_and_vwap  50.34  1.521  20.2      2177
kde_and_vpvr  59.93  2.243  18.1       277
kde_and_near  50.83  1.551  19.8      2345
    kde_gate            covers 28.2% of regime bars  ⚠️  LOW
    vwap_only           covers 35.6% of regime bars
    vpvr_only           covers 3.0% of regime bars  ⚠️  LOW
    near_setup          covers 37.7% of regime bars
    kde_and_vwap        covers 10.8% of regime bars  ⚠️  LOW
    kde_and_vpvr        covers 1.4% of regime bars  ⚠️  LOW
    kde_and_near        covers 11.6% of regime bars  ⚠️  LOW

  XRPUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   47.17  1.339  22.3     24598
kde_gate      51.62  1.600  23.1      6463
vwap_only     48.44  1.409  22.6      9398
vpvr_only     52.43  1.653  23.4       637
near_setup    48.67  1.422  22.7      9840
kde_and_vwap  51.75  1.609  24.3      2711
kde_and_vpvr  60.55  2.303  20.1       289
kde_and_near  52.38  1.650  24.0      2894
    kde_gate            covers 26.3% of regime bars  ⚠️  LOW
    vwap_only           covers 38.2% of regime bars
    vpvr_only           covers 2.6% of regime bars  ⚠️  LOW
    near_setup          covers 40.0% of regime bars
    kde_and_vwap        covers 11.0% of regime bars  ⚠️  LOW
    kde_and_vpvr        covers 1.2% of regime bars  ⚠️  LOW
    kde_and_near        covers 11.8% of regime bars  ⚠️  LOW


── KDE + Level Combined — Verdict ──

  Baseline (regime_only):  avg WR 45.2%  avg PF 1.240
  KDE: window=200  bw=1  lower_dur=5  |  VWAP: daily  VPVR: 50d  |  dist=1×ATR

  [KDE signal    ]  kde_gate            avg WR lift +5.13pp  avg PF 1.525  avg PF lift +0.285  pairs ≥ threshold: 5/5  ✅  ⚠️ low count 4p
    BTCUSDT     WR 48.88%  lift +4.63pp / req 1.50pp  PF 1.434  lift +0.244 / req 0.100  trades 6,884  ⚠️ cov 29.2%  ✅
    ETHUSDT     WR 52.84%  lift +7.83pp / req 1.49pp  PF 1.681  lift +0.453 / req 0.100  trades 7,004  ⚠️ cov 29.3%  ✅
    SOLUSDT     WR 48.58%  lift +3.74pp / req 1.49pp  PF 1.417  lift +0.198 / req 0.100  trades 7,003  cov 31.3%  ✅
    BNBUSDT     WR 49.87%  lift +4.98pp / req 1.65pp  PF 1.492  lift +0.271 / req 0.100  trades 5,707  ⚠️ cov 28.2%  ✅
    XRPUSDT     WR 51.62%  lift +4.45pp / req 1.55pp  PF 1.600  lift +0.261 / req 0.100  trades 6,463  ⚠️ cov 26.3%  ✅

  [Level signal  ]  vwap_only           avg WR lift +0.98pp  avg PF 1.290  avg PF lift +0.050  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p
    BTCUSDT     WR 45.31%  lift +1.05pp / req 1.33pp  PF 1.243  lift +0.052 / req 0.100  trades 8,683  ⚠️ WR  cov 36.9%  ❌
    ETHUSDT     WR 46.30%  lift +1.29pp / req 1.33pp  PF 1.293  lift +0.066 / req 0.100  trades 8,805  ⚠️ WR  cov 36.8%  ❌
    SOLUSDT     WR 45.23%  lift +0.39pp / req 1.37pp  PF 1.239  lift +0.019 / req 0.100  trades 8,211  ⚠️ WR  cov 36.7%  ❌
    BNBUSDT     WR 45.76%  lift +0.88pp / req 1.46pp  PF 1.266  lift +0.044 / req 0.100  trades 7,213  ⚠️ WR  cov 35.6%  ❌
    XRPUSDT     WR 48.44%  lift +1.27pp / req 1.29pp  PF 1.409  lift +0.070 / req 0.100  trades 9,398  ⚠️ WR  cov 38.2%  ❌

  [Level signal  ]  vpvr_only           avg WR lift +4.97pp  avg PF 1.541  avg PF lift +0.301  pairs ≥ threshold: 4/5  ✅  ⚠️ WR 2p  ⚠️ low count 5p
    BTCUSDT     WR 50.49%  lift +6.24pp / req 3.88pp  PF 1.530  lift +0.339 / req 0.100  trades 1,022  ⚠️ cov 4.3%  ✅
    ETHUSDT     WR 47.72%  lift +2.71pp / req 4.20pp  PF 1.369  lift +0.141 / req 0.100  trades 876  ⚠️ WR  ⚠️ cov 3.7%  ✅
    SOLUSDT     WR 42.94%  lift -1.90pp / req 4.21pp  PF 1.129  lift -0.091 / req 0.100  trades 871  ⚠️ WR  ⚠️ cov 3.9%  ❌
    BNBUSDT     WR 57.43%  lift +12.54pp / req 5.05pp  PF 2.023  lift +0.802 / req 0.100  trades 606  ⚠️ cov 3.0%  ✅
    XRPUSDT     WR 52.43%  lift +5.27pp / req 4.94pp  PF 1.653  lift +0.314 / req 0.100  trades 637  ⚠️ cov 2.6%  ✅

  [Level signal  ]  near_setup          avg WR lift +1.26pp  avg PF 1.305  avg PF lift +0.065  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 1p
    BTCUSDT     WR 45.73%  lift +1.48pp / req 1.28pp  PF 1.264  lift +0.073 / req 0.100  trades 9,414  cov 40.0%  ❌
    ETHUSDT     WR 46.54%  lift +1.53pp / req 1.28pp  PF 1.306  lift +0.078 / req 0.100  trades 9,433  cov 39.5%  ❌
    SOLUSDT     WR 45.18%  lift +0.34pp / req 1.32pp  PF 1.236  lift +0.017 / req 0.100  trades 8,849  ⚠️ WR  cov 39.6%  ❌
    BNBUSDT     WR 46.34%  lift +1.45pp / req 1.42pp  PF 1.295  lift +0.074 / req 0.100  trades 7,627  cov 37.7%  ❌
    XRPUSDT     WR 48.67%  lift +1.50pp / req 1.26pp  PF 1.422  lift +0.083 / req 0.100  trades 9,840  cov 40.0%  ❌

  [Combined      ]  kde_and_vwap        avg WR lift +5.96pp  avg PF 1.578  avg PF lift +0.338  pairs ≥ threshold: 5/5  ✅  ⚠️ low count 5p
    BTCUSDT     WR 48.49%  lift +4.24pp / req 2.38pp  PF 1.412  lift +0.221 / req 0.100  trades 2,718  ⚠️ cov 11.5%  ✅
    ETHUSDT     WR 54.42%  lift +9.41pp / req 2.38pp  PF 1.791  lift +0.563 / req 0.100  trades 2,740  ⚠️ cov 11.5%  ✅
    SOLUSDT     WR 50.92%  lift +6.08pp / req 2.41pp  PF 1.556  lift +0.337 / req 0.100  trades 2,651  ⚠️ cov 11.9%  ✅
    BNBUSDT     WR 50.34%  lift +5.46pp / req 2.66pp  PF 1.521  lift +0.299 / req 0.100  trades 2,177  ⚠️ cov 10.8%  ✅
    XRPUSDT     WR 51.75%  lift +4.59pp / req 2.40pp  PF 1.609  lift +0.270 / req 0.100  trades 2,711  ⚠️ cov 11.0%  ✅

  [Combined      ]  kde_and_vpvr        avg WR lift +8.11pp  avg PF 1.774  avg PF lift +0.534  pairs ≥ threshold: 4/5  ✅  ⚠️ WR 2p  ⚠️ low count 5p
    BTCUSDT     WR 45.27%  lift +1.02pp / req 5.82pp  PF 1.241  lift +0.050 / req 0.100  trades 455  ⚠️ WR  ⚠️ cov 1.9%  ❌
    ETHUSDT     WR 53.54%  lift +8.53pp / req 6.04pp  PF 1.728  lift +0.501 / req 0.100  trades 424  ⚠️ cov 1.8%  ✅
    SOLUSDT     WR 47.41%  lift +2.57pp / req 5.77pp  PF 1.352  lift +0.133 / req 0.100  trades 464  ⚠️ WR  ⚠️ cov 2.1%  ✅
    BNBUSDT     WR 59.93%  lift +15.04pp / req 7.47pp  PF 2.243  lift +1.022 / req 0.100  trades 277  ⚠️ cov 1.4%  ✅
    XRPUSDT     WR 60.55%  lift +13.39pp / req 7.34pp  PF 2.303  lift +0.964 / req 0.100  trades 289  ⚠️ cov 1.2%  ✅

  [Combined      ]  kde_and_near        avg WR lift +6.16pp  avg PF 1.591  avg PF lift +0.351  pairs ≥ threshold: 5/5  ✅  ⚠️ low count 5p
    BTCUSDT     WR 48.17%  lift +3.91pp / req 2.26pp  PF 1.394  lift +0.203 / req 0.100  trades 3,025  ⚠️ cov 12.8%  ✅
    ETHUSDT     WR 54.46%  lift +9.45pp / req 2.26pp  PF 1.793  lift +0.566 / req 0.100  trades 3,030  ⚠️ cov 12.7%  ✅
    SOLUSDT     WR 51.10%  lift +6.26pp / req 2.28pp  PF 1.567  lift +0.348 / req 0.100  trades 2,961  ⚠️ cov 13.2%  ✅
    BNBUSDT     WR 50.83%  lift +5.95pp / req 2.57pp  PF 1.551  lift +0.329 / req 0.100  trades 2,345  ⚠️ cov 11.6%  ✅
    XRPUSDT     WR 52.38%  lift +5.22pp / req 2.32pp  PF 1.650  lift +0.311 / req 0.100  trades 2,894  ⚠️ cov 11.8%  ✅

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  consistent across ≥ 3 of 5 pairs

  ✅  KDE + LEVEL EDGE CONFIRMED — at least one population creates predictive edge.
      Best performer: kde_and_vpvr  (avg PF 1.774)
      Warnings (results valid but interpret with care):
        ⚠️  [kde_gate] low trade count (<30% of regime) on: BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT
        ⚠️  [vwap_only] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
        ⚠️  [vpvr_only] WR lift below threshold on: ETHUSDT, SOLUSDT
        ⚠️  [vpvr_only] low trade count (<30% of regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
        ⚠️  [near_setup] WR lift below threshold on: SOLUSDT
        ⚠️  [kde_and_vwap] low trade count (<30% of regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
        ⚠️  [kde_and_vpvr] WR lift below threshold on: BTCUSDT, SOLUSDT
        ⚠️  [kde_and_vpvr] low trade count (<30% of regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
        ⚠️  [kde_and_near] low trade count (<30% of regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  ── Population Interpretation ──
      [KDE signal]
        kde_gate       ✅ — KDE edge (open-above-POC OR fresh-break) adds standalone edge.
      [Level signal]
        vpvr_only          ✅ — price near VPVR HVN (1d) alone adds short edge.
        near_setup         ❌ — level proximity (VWAP OR VPVR) alone does not add reliable edge.
        vwap_only          ❌ — daily VWAP proximity alone does not add reliable edge.
      [Combined]
        kde_and_near       ✅ — KDE gate + either level proximity is the strongest combination.
        kde_and_vpvr       ✅ — KDE gate + VPVR HVN proximity is the strongest signal combination.
        kde_and_vwap       ✅ — KDE gate + daily VWAP proximity is the strongest signal combination.

      Proceed to the next setup step with the confirmed populations.
```
