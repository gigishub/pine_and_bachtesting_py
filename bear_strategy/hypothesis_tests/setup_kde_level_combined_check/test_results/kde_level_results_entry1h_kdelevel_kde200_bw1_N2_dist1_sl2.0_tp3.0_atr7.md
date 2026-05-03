# Bear Strategy -- KDE + Level Proximity Combined Check  (entry_tf=1h  kde_tf=4h)

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
| `kde_lower_duration` | `2` |
| `vwap_anchor` | `daily` |
| `vpvr_window` | `50` |
| `vpvr_n_bins` | `50` |
| `setup_distance_atr` | `1.0` |

```text

-- Per-Pair Results --

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         44.25  1.191  20.4     23544
kde_gate            48.38  1.406  21.4      5752
kde_upper           47.76  1.371  20.9      5272
kde_lower_fresh     54.91  1.826  27.0      1080
vwap_only           45.31  1.243  19.4      8683
vpvr_only           50.49  1.530  25.8      1022
near_setup          45.73  1.264  19.9      9414
kde_gate_and_vwap   48.28  1.400  20.7      2293
kde_gate_and_vpvr   43.24  1.143  29.2       377
kde_gate_and_near   47.75  1.371  21.5      2538
kde_upper_and_vwap  47.45  1.355  20.7      2101
kde_upper_and_vpvr  42.57  1.112  28.4       350
kde_upper_and_near  46.90  1.325  21.3      2324
kde_lower_and_vwap  61.74  2.421  23.0       447
kde_lower_and_vpvr  49.12  1.448  55.9        57
kde_lower_and_near  60.86  2.332  25.8       488

    kde_gate                  covers 24.4% of regime bars  !! LOW
    kde_upper                 covers 22.4% of regime bars  !! LOW
    kde_lower_fresh           covers 4.6% of regime bars  !! LOW
    vwap_only                 covers 36.9% of regime bars
    vpvr_only                 covers 4.3% of regime bars  !! LOW
    near_setup                covers 40.0% of regime bars
    kde_gate_and_vwap         covers 9.7% of regime bars  !! LOW
    kde_gate_and_vpvr         covers 1.6% of regime bars  !! LOW
    kde_gate_and_near         covers 10.8% of regime bars  !! LOW
    kde_upper_and_vwap        covers 8.9% of regime bars  !! LOW
    kde_upper_and_vpvr        covers 1.5% of regime bars  !! LOW
    kde_upper_and_near        covers 9.9% of regime bars  !! LOW
    kde_lower_and_vwap        covers 1.9% of regime bars  !! LOW
    kde_lower_and_vpvr        covers 0.2% of regime bars  !! LOW
    kde_lower_and_near        covers 2.1% of regime bars  !! LOW

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         45.01  1.228  19.9     23904
kde_gate            53.39  1.718  21.0      5784
kde_upper           53.79  1.746  21.0      5256
kde_lower_fresh     51.77  1.610  21.6      1184
vwap_only           46.30  1.293  18.6      8805
vpvr_only           47.72  1.369  21.4       876
near_setup          46.54  1.306  18.8      9433
kde_gate_and_vwap   55.94  1.904  18.4      2249
kde_gate_and_vpvr   50.00  1.500  23.8       330
kde_gate_and_near   55.19  1.847  18.9      2468
kde_upper_and_vwap  56.71  1.965  17.9      2049
kde_upper_and_vpvr  50.67  1.541  23.9       300
kde_upper_and_near  56.06  1.913  18.4      2246
kde_lower_and_vwap  51.93  1.620  22.7       441
kde_lower_and_vpvr  54.72  1.812  29.9        53
kde_lower_and_near  51.68  1.604  23.4       476

    kde_gate                  covers 24.2% of regime bars  !! LOW
    kde_upper                 covers 22.0% of regime bars  !! LOW
    kde_lower_fresh           covers 5.0% of regime bars  !! LOW
    vwap_only                 covers 36.8% of regime bars
    vpvr_only                 covers 3.7% of regime bars  !! LOW
    near_setup                covers 39.5% of regime bars
    kde_gate_and_vwap         covers 9.4% of regime bars  !! LOW
    kde_gate_and_vpvr         covers 1.4% of regime bars  !! LOW
    kde_gate_and_near         covers 10.3% of regime bars  !! LOW
    kde_upper_and_vwap        covers 8.6% of regime bars  !! LOW
    kde_upper_and_vpvr        covers 1.3% of regime bars  !! LOW
    kde_upper_and_near        covers 9.4% of regime bars  !! LOW
    kde_lower_and_vwap        covers 1.8% of regime bars  !! LOW
    kde_lower_and_vpvr        covers 0.2% of regime bars  !! LOW
    kde_lower_and_near        covers 2.0% of regime bars  !! LOW

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         44.84  1.219  19.5     22371
kde_gate            49.01  1.442  19.0      5927
kde_upper           48.91  1.436  18.8      5475
kde_lower_fresh     48.41  1.407  22.8      1068
vwap_only           45.23  1.239  18.2      8211
vpvr_only           42.94  1.129  21.5       871
near_setup          45.18  1.236  18.5      8849
kde_gate_and_vwap   50.38  1.523  17.8      2233
kde_gate_and_vpvr   48.19  1.395  16.3       415
kde_gate_and_near   50.66  1.540  17.4      2505
kde_upper_and_vwap  50.29  1.518  17.5      2060
kde_upper_and_vpvr  48.16  1.393  15.3       380
kde_upper_and_near  50.48  1.529  17.1      2314
kde_lower_and_vwap  48.43  1.409  21.5       415
kde_lower_and_vpvr  46.38  1.297  30.9        69
kde_lower_and_near  49.55  1.473  21.8       448

    kde_gate                  covers 26.5% of regime bars  !! LOW
    kde_upper                 covers 24.5% of regime bars  !! LOW
    kde_lower_fresh           covers 4.8% of regime bars  !! LOW
    vwap_only                 covers 36.7% of regime bars
    vpvr_only                 covers 3.9% of regime bars  !! LOW
    near_setup                covers 39.6% of regime bars
    kde_gate_and_vwap         covers 10.0% of regime bars  !! LOW
    kde_gate_and_vpvr         covers 1.9% of regime bars  !! LOW
    kde_gate_and_near         covers 11.2% of regime bars  !! LOW
    kde_upper_and_vwap        covers 9.2% of regime bars  !! LOW
    kde_upper_and_vpvr        covers 1.7% of regime bars  !! LOW
    kde_upper_and_near        covers 10.3% of regime bars  !! LOW
    kde_lower_and_vwap        covers 1.9% of regime bars  !! LOW
    kde_lower_and_vpvr        covers 0.3% of regime bars  !! LOW
    kde_lower_and_near        covers 2.0% of regime bars  !! LOW

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         44.88  1.222  19.0     20243
kde_gate            51.14  1.570  20.8      4767
kde_upper           51.36  1.584  21.1      4367
kde_lower_fresh     50.00  1.500  24.1       920
vwap_only           45.76  1.266  18.2      7213
vpvr_only           57.43  2.023  18.3       606
near_setup          46.34  1.295  18.1      7627
kde_gate_and_vwap   51.96  1.623  20.2      1859
kde_gate_and_vpvr   61.73  2.419  17.2       243
kde_gate_and_near   52.53  1.660  19.7      1997
kde_upper_and_vwap  52.87  1.683  20.4      1706
kde_upper_and_vpvr  61.70  2.417  16.4       235
kde_upper_and_near  53.37  1.717  19.9      1838
kde_lower_and_vwap  44.38  1.197  22.6       365
kde_lower_and_vpvr  40.91  1.038  23.8        22
kde_lower_and_near  44.39  1.197  22.6       383

    kde_gate                  covers 23.5% of regime bars  !! LOW
    kde_upper                 covers 21.6% of regime bars  !! LOW
    kde_lower_fresh           covers 4.5% of regime bars  !! LOW
    vwap_only                 covers 35.6% of regime bars
    vpvr_only                 covers 3.0% of regime bars  !! LOW
    near_setup                covers 37.7% of regime bars
    kde_gate_and_vwap         covers 9.2% of regime bars  !! LOW
    kde_gate_and_vpvr         covers 1.2% of regime bars  !! LOW
    kde_gate_and_near         covers 9.9% of regime bars  !! LOW
    kde_upper_and_vwap        covers 8.4% of regime bars  !! LOW
    kde_upper_and_vpvr        covers 1.2% of regime bars  !! LOW
    kde_upper_and_near        covers 9.1% of regime bars  !! LOW
    kde_lower_and_vwap        covers 1.8% of regime bars  !! LOW
    kde_lower_and_vpvr        covers 0.1% of regime bars  !! LOW
    kde_lower_and_near        covers 1.9% of regime bars  !! LOW

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         47.17  1.339  22.3     24598
kde_gate            51.81  1.613  22.3      5599
kde_upper           51.86  1.616  22.3      5195
kde_lower_fresh     49.34  1.461  31.9       908
vwap_only           48.44  1.409  22.6      9398
vpvr_only           52.43  1.653  23.4       637
near_setup          48.67  1.422  22.7      9840
kde_gate_and_vwap   51.72  1.607  23.4      2361
kde_gate_and_vpvr   62.65  2.516  19.7       257
kde_gate_and_near   52.55  1.661  23.0      2514
kde_upper_and_vwap  52.01  1.626  23.7      2186
kde_upper_and_vpvr  62.29  2.478  19.3       236
kde_upper_and_near  52.74  1.674  23.3      2321
kde_lower_and_vwap  49.07  1.445  34.2       377
kde_lower_and_vpvr  47.92  1.380  23.4        48
kde_lower_and_near  49.64  1.478  33.1       411

    kde_gate                  covers 22.8% of regime bars  !! LOW
    kde_upper                 covers 21.1% of regime bars  !! LOW
    kde_lower_fresh           covers 3.7% of regime bars  !! LOW
    vwap_only                 covers 38.2% of regime bars
    vpvr_only                 covers 2.6% of regime bars  !! LOW
    near_setup                covers 40.0% of regime bars
    kde_gate_and_vwap         covers 9.6% of regime bars  !! LOW
    kde_gate_and_vpvr         covers 1.0% of regime bars  !! LOW
    kde_gate_and_near         covers 10.2% of regime bars  !! LOW
    kde_upper_and_vwap        covers 8.9% of regime bars  !! LOW
    kde_upper_and_vpvr        covers 1.0% of regime bars  !! LOW
    kde_upper_and_near        covers 9.4% of regime bars  !! LOW
    kde_lower_and_vwap        covers 1.5% of regime bars  !! LOW
    kde_lower_and_vpvr        covers 0.2% of regime bars  !! LOW
    kde_lower_and_near        covers 1.7% of regime bars  !! LOW


-- KDE + Level Combined -- Verdict --

  Baseline (regime_only):  avg WR 45.2%  avg PF 1.240
  KDE (4h): window=200  bw=1  lower_dur=2  |  VWAP: daily  VPVR: 50d  |  dist=1xATR


  [KDE gate     ]  kde_gate                  WR lift +5.5pp  avg PF 1.550  PF lift +0.310  5/5 pairs  [OK]  warn: low# 5p
    BTCUSDT     WR 48.4%  PF 1.406  lift +0.215 / req 0.10  n=5,752  cov 24%!  [OK]
    ETHUSDT     WR 53.4%  PF 1.718  lift +0.490 / req 0.10  n=5,784  cov 24%!  [OK]
    SOLUSDT     WR 49.0%  PF 1.442  lift +0.223 / req 0.10  n=5,927  cov 26%!  [OK]
    BNBUSDT     WR 51.1%  PF 1.570  lift +0.349 / req 0.10  n=4,767  cov 24%!  [OK]
    XRPUSDT     WR 51.8%  PF 1.613  lift +0.274 / req 0.10  n=5,599  cov 23%!  [OK]

  [KDE upper    ]  kde_upper                 WR lift +5.5pp  avg PF 1.551  PF lift +0.311  5/5 pairs  [OK]  warn: low# 5p
    BTCUSDT     WR 47.8%  PF 1.371  lift +0.181 / req 0.10  n=5,272  cov 22%!  [OK]
    ETHUSDT     WR 53.8%  PF 1.746  lift +0.518 / req 0.10  n=5,256  cov 22%!  [OK]
    SOLUSDT     WR 48.9%  PF 1.436  lift +0.217 / req 0.10  n=5,475  cov 24%!  [OK]
    BNBUSDT     WR 51.4%  PF 1.584  lift +0.362 / req 0.10  n=4,367  cov 22%!  [OK]
    XRPUSDT     WR 51.9%  PF 1.616  lift +0.277 / req 0.10  n=5,195  cov 21%!  [OK]
  [KDE lower    ]  kde_lower_fresh           WR lift +5.7pp  avg PF 1.561  PF lift +0.321  5/5 pairs  [OK]  warn: WR 2p, low# 5p
    BTCUSDT     WR 54.9%  PF 1.826  lift +0.636 / req 0.10  n=1,080  cov 5%!  [OK]
    ETHUSDT     WR 51.8%  PF 1.610  lift +0.383 / req 0.10  n=1,184  cov 5%!  [OK]
    SOLUSDT     WR 48.4%  PF 1.407  lift +0.188 / req 0.10  n=1,068  WR!  cov 5%!  [OK]
    BNBUSDT     WR 50.0%  PF 1.500  lift +0.278 / req 0.10  n=920  cov 5%!  [OK]
    XRPUSDT     WR 49.3%  PF 1.461  lift +0.122 / req 0.10  n=908  WR!  cov 4%!  [OK]

  [Level        ]  vwap_only                 WR lift +1.0pp  avg PF 1.290  PF lift +0.050  0/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 45.3%  PF 1.243  lift +0.052 / req 0.10  n=8,683  WR!  cov 37%  [--]
    ETHUSDT     WR 46.3%  PF 1.293  lift +0.066 / req 0.10  n=8,805  WR!  cov 37%  [--]
    SOLUSDT     WR 45.2%  PF 1.239  lift +0.019 / req 0.10  n=8,211  WR!  cov 37%  [--]
    BNBUSDT     WR 45.8%  PF 1.266  lift +0.044 / req 0.10  n=7,213  WR!  cov 36%  [--]
    XRPUSDT     WR 48.4%  PF 1.409  lift +0.070 / req 0.10  n=9,398  WR!  cov 38%  [--]
  [Level        ]  vpvr_only                 WR lift +5.0pp  avg PF 1.541  PF lift +0.301  4/5 pairs  [OK]  warn: WR 2p, low# 5p
    BTCUSDT     WR 50.5%  PF 1.530  lift +0.339 / req 0.10  n=1,022  cov 4%!  [OK]
    ETHUSDT     WR 47.7%  PF 1.369  lift +0.141 / req 0.10  n=876  WR!  cov 4%!  [OK]
    SOLUSDT     WR 42.9%  PF 1.129  lift -0.091 / req 0.10  n=871  WR!  cov 4%!  [--]
    BNBUSDT     WR 57.4%  PF 2.023  lift +0.802 / req 0.10  n=606  cov 3%!  [OK]
    XRPUSDT     WR 52.4%  PF 1.653  lift +0.314 / req 0.10  n=637  cov 3%!  [OK]
  [Level        ]  near_setup                WR lift +1.3pp  avg PF 1.305  PF lift +0.065  0/5 pairs  [XX]  warn: WR 1p
    BTCUSDT     WR 45.7%  PF 1.264  lift +0.073 / req 0.10  n=9,414  cov 40%  [--]
    ETHUSDT     WR 46.5%  PF 1.306  lift +0.078 / req 0.10  n=9,433  cov 39%  [--]
    SOLUSDT     WR 45.2%  PF 1.236  lift +0.017 / req 0.10  n=8,849  WR!  cov 40%  [--]
    BNBUSDT     WR 46.3%  PF 1.295  lift +0.074 / req 0.10  n=7,627  cov 38%  [--]
    XRPUSDT     WR 48.7%  PF 1.422  lift +0.083 / req 0.10  n=9,840  cov 40%  [--]

  [Gate x VWAP  ]  kde_gate_and_vwap         WR lift +6.4pp  avg PF 1.611  PF lift +0.372  5/5 pairs  [OK]  warn: low# 5p
    BTCUSDT     WR 48.3%  PF 1.400  lift +0.209 / req 0.10  n=2,293  cov 10%!  [OK]
    ETHUSDT     WR 55.9%  PF 1.904  lift +0.676 / req 0.10  n=2,249  cov 9%!  [OK]
    SOLUSDT     WR 50.4%  PF 1.523  lift +0.304 / req 0.10  n=2,233  cov 10%!  [OK]
    BNBUSDT     WR 52.0%  PF 1.623  lift +0.401 / req 0.10  n=1,859  cov 9%!  [OK]
    XRPUSDT     WR 51.7%  PF 1.607  lift +0.267 / req 0.10  n=2,361  cov 10%!  [OK]
  [Gate x VPVR  ]  kde_gate_and_vpvr         WR lift +7.9pp  avg PF 1.795  PF lift +0.555  4/5 pairs  [OK]  warn: WR 3p, low# 5p
    BTCUSDT     WR 43.2%  PF 1.143  lift -0.048 / req 0.10  n=377  WR!  cov 2%!  [--]
    ETHUSDT     WR 50.0%  PF 1.500  lift +0.272 / req 0.10  n=330  WR!  cov 1%!  [OK]
    SOLUSDT     WR 48.2%  PF 1.395  lift +0.176 / req 0.10  n=415  WR!  cov 2%!  [OK]
    BNBUSDT     WR 61.7%  PF 2.419  lift +1.198 / req 0.10  n=243  cov 1%!  [OK]
    XRPUSDT     WR 62.6%  PF 2.516  lift +1.177 / req 0.10  n=257  cov 1%!  [OK]
  [Gate x Near  ]  kde_gate_and_near         WR lift +6.5pp  avg PF 1.616  PF lift +0.376  5/5 pairs  [OK]  warn: low# 5p
    BTCUSDT     WR 47.8%  PF 1.371  lift +0.180 / req 0.10  n=2,538  cov 11%!  [OK]
    ETHUSDT     WR 55.2%  PF 1.847  lift +0.619 / req 0.10  n=2,468  cov 10%!  [OK]
    SOLUSDT     WR 50.7%  PF 1.540  lift +0.321 / req 0.10  n=2,505  cov 11%!  [OK]
    BNBUSDT     WR 52.5%  PF 1.660  lift +0.438 / req 0.10  n=1,997  cov 10%!  [OK]
    XRPUSDT     WR 52.5%  PF 1.661  lift +0.322 / req 0.10  n=2,514  cov 10%!  [OK]

  [Upper x VWAP ]  kde_upper_and_vwap        WR lift +6.6pp  avg PF 1.629  PF lift +0.389  5/5 pairs  [OK]  warn: low# 5p
    BTCUSDT     WR 47.5%  PF 1.355  lift +0.164 / req 0.10  n=2,101  cov 9%!  [OK]
    ETHUSDT     WR 56.7%  PF 1.965  lift +0.737 / req 0.10  n=2,049  cov 9%!  [OK]
    SOLUSDT     WR 50.3%  PF 1.518  lift +0.298 / req 0.10  n=2,060  cov 9%!  [OK]
    BNBUSDT     WR 52.9%  PF 1.683  lift +0.461 / req 0.10  n=1,706  cov 8%!  [OK]
    XRPUSDT     WR 52.0%  PF 1.626  lift +0.287 / req 0.10  n=2,186  cov 9%!  [OK]
  [Upper x VPVR ]  kde_upper_and_vpvr        WR lift +7.8pp  avg PF 1.788  PF lift +0.548  4/5 pairs  [OK]  warn: WR 3p, low# 5p
    BTCUSDT     WR 42.6%  PF 1.112  lift -0.079 / req 0.10  n=350  WR!  cov 1%!  [--]
    ETHUSDT     WR 50.7%  PF 1.541  lift +0.313 / req 0.10  n=300  WR!  cov 1%!  [OK]
    SOLUSDT     WR 48.2%  PF 1.393  lift +0.174 / req 0.10  n=380  WR!  cov 2%!  [OK]
    BNBUSDT     WR 61.7%  PF 2.417  lift +1.195 / req 0.10  n=235  cov 1%!  [OK]
    XRPUSDT     WR 62.3%  PF 2.478  lift +1.138 / req 0.10  n=236  cov 1%!  [OK]
  [Upper x Near ]  kde_upper_and_near        WR lift +6.7pp  avg PF 1.632  PF lift +0.392  5/5 pairs  [OK]  warn: low# 5p
    BTCUSDT     WR 46.9%  PF 1.325  lift +0.134 / req 0.10  n=2,324  cov 10%!  [OK]
    ETHUSDT     WR 56.1%  PF 1.913  lift +0.686 / req 0.10  n=2,246  cov 9%!  [OK]
    SOLUSDT     WR 50.5%  PF 1.529  lift +0.309 / req 0.10  n=2,314  cov 10%!  [OK]
    BNBUSDT     WR 53.4%  PF 1.717  lift +0.495 / req 0.10  n=1,838  cov 9%!  [OK]
    XRPUSDT     WR 52.7%  PF 1.674  lift +0.335 / req 0.10  n=2,321  cov 9%!  [OK]

  [Lower x VWAP ]  kde_lower_and_vwap        WR lift +5.9pp  avg PF 1.619  PF lift +0.379  4/5 pairs  [OK]  warn: WR 3p, low# 5p
    BTCUSDT     WR 61.7%  PF 2.421  lift +1.230 / req 0.10  n=447  cov 2%!  [OK]
    ETHUSDT     WR 51.9%  PF 1.620  lift +0.393 / req 0.10  n=441  cov 2%!  [OK]
    SOLUSDT     WR 48.4%  PF 1.409  lift +0.190 / req 0.10  n=415  WR!  cov 2%!  [OK]
    BNBUSDT     WR 44.4%  PF 1.197  lift -0.025 / req 0.10  n=365  WR!  cov 2%!  [--]
    XRPUSDT     WR 49.1%  PF 1.445  lift +0.106 / req 0.10  n=377  WR!  cov 2%!  [OK]
  [Lower x VPVR ]  kde_lower_and_vpvr        WR lift +2.6pp  avg PF 1.395  PF lift +0.156  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 49.1%  PF 1.448  lift +0.258 / req 0.10  n=57  WR!  cov 0%!  [OK]
    ETHUSDT     WR 54.7%  PF 1.812  lift +0.585 / req 0.10  n=53  WR!  cov 0%!  [OK]
    SOLUSDT     WR 46.4%  PF 1.297  lift +0.078 / req 0.10  n=69  WR!  cov 0%!  [--]
    BNBUSDT     WR 40.9%  PF 1.038  lift -0.183 / req 0.10  n=22  WR!  cov 0%!  [--]
    XRPUSDT     WR 47.9%  PF 1.380  lift +0.041 / req 0.10  n=48  WR!  cov 0%!  [--]
  [Lower x Near ]  kde_lower_and_near        WR lift +6.0pp  avg PF 1.617  PF lift +0.377  4/5 pairs  [OK]  warn: WR 3p, low# 5p
    BTCUSDT     WR 60.9%  PF 2.332  lift +1.142 / req 0.10  n=488  cov 2%!  [OK]
    ETHUSDT     WR 51.7%  PF 1.604  lift +0.377 / req 0.10  n=476  cov 2%!  [OK]
    SOLUSDT     WR 49.6%  PF 1.473  lift +0.254 / req 0.10  n=448  WR!  cov 2%!  [OK]
    BNBUSDT     WR 44.4%  PF 1.197  lift -0.024 / req 0.10  n=383  WR!  cov 2%!  [--]
    XRPUSDT     WR 49.6%  PF 1.478  lift +0.139 / req 0.10  n=411  WR!  cov 2%!  [OK]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  KDE + LEVEL EDGE CONFIRMED -- confirmed populations below.
        Best performer: kde_gate_and_vpvr  (avg PF 1.795)

  Warnings (results valid -- interpret with care):
    !! [kde_gate] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_upper] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_lower_fresh] WR lift below threshold on: SOLUSDT, XRPUSDT
    !! [kde_lower_fresh] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [vwap_only] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [vpvr_only] WR lift below threshold on: ETHUSDT, SOLUSDT
    !! [vpvr_only] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [near_setup] WR lift below threshold on: SOLUSDT
    !! [kde_gate_and_vwap] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_gate_and_vpvr] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT
    !! [kde_gate_and_vpvr] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_gate_and_near] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_upper_and_vwap] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_upper_and_vpvr] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT
    !! [kde_upper_and_vpvr] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_upper_and_near] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_lower_and_vwap] WR lift below threshold on: SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_lower_and_vwap] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_lower_and_vpvr] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_lower_and_vpvr] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_lower_and_near] WR lift below threshold on: SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_lower_and_near] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [KDE gate (combined OR)]
      [OK] kde_gate                    avg PF 1.550
    [KDE signal (standalone)]
      [OK] kde_lower_fresh             avg PF 1.561
      [OK] kde_upper                   avg PF 1.551
    [Level signal (standalone)]
      [OK] vpvr_only                   avg PF 1.541
      [--] near_setup
      [--] vwap_only
    [kde_gate x level]
      [OK] kde_gate_and_near           avg PF 1.616
      [OK] kde_gate_and_vpvr           avg PF 1.795
      [OK] kde_gate_and_vwap           avg PF 1.611
    [kde_upper x level]
      [OK] kde_upper_and_near          avg PF 1.632
      [OK] kde_upper_and_vpvr          avg PF 1.788
      [OK] kde_upper_and_vwap          avg PF 1.629
    [kde_lower_fresh x level]
      [OK] kde_lower_and_near          avg PF 1.617
      [OK] kde_lower_and_vwap          avg PF 1.619
      [--] kde_lower_and_vpvr

  Proceed to next setup step using confirmed populations.
```
