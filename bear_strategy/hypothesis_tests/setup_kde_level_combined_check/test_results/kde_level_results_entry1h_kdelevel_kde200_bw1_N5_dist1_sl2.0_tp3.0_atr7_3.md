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
| `kde_lower_duration` | `5` |
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
kde_gate            48.88  1.434  21.3      6884
kde_upper           47.76  1.371  20.9      5272
kde_lower_fresh     53.16  1.702  23.8      2216
vwap_only           45.31  1.243  19.4      8683
vpvr_only           50.49  1.530  25.8      1022
near_setup          45.73  1.264  19.9      9414
kde_gate_and_vwap   48.49  1.412  20.1      2718
kde_gate_and_vpvr   45.27  1.241  27.2       455
kde_gate_and_near   48.17  1.394  20.8      3025
kde_upper_and_vwap  47.45  1.355  20.7      2101
kde_upper_and_vpvr  42.57  1.112  28.4       350
kde_upper_and_near  46.90  1.325  21.3      2324
kde_lower_and_vwap  56.00  1.909  20.1       875
kde_lower_and_vpvr  53.24  1.708  33.1       139
kde_lower_and_near  55.67  1.884  21.5       979

    kde_gate                  covers 29.2% of regime bars  !! LOW
    kde_upper                 covers 22.4% of regime bars  !! LOW
    kde_lower_fresh           covers 9.4% of regime bars  !! LOW
    vwap_only                 covers 36.9% of regime bars
    vpvr_only                 covers 4.3% of regime bars  !! LOW
    near_setup                covers 40.0% of regime bars
    kde_gate_and_vwap         covers 11.5% of regime bars  !! LOW
    kde_gate_and_vpvr         covers 1.9% of regime bars  !! LOW
    kde_gate_and_near         covers 12.8% of regime bars  !! LOW
    kde_upper_and_vwap        covers 8.9% of regime bars  !! LOW
    kde_upper_and_vpvr        covers 1.5% of regime bars  !! LOW
    kde_upper_and_near        covers 9.9% of regime bars  !! LOW
    kde_lower_and_vwap        covers 3.7% of regime bars  !! LOW
    kde_lower_and_vpvr        covers 0.6% of regime bars  !! LOW
    kde_lower_and_near        covers 4.2% of regime bars  !! LOW

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         45.01  1.228  19.9     23904
kde_gate            52.84  1.681  20.4      7004
kde_upper           53.79  1.746  21.0      5256
kde_lower_fresh     51.16  1.571  19.7      2412
vwap_only           46.30  1.293  18.6      8805
vpvr_only           47.72  1.369  21.4       876
near_setup          46.54  1.306  18.8      9433
kde_gate_and_vwap   54.42  1.791  18.5      2740
kde_gate_and_vpvr   53.54  1.728  21.5       424
kde_gate_and_near   54.46  1.793  18.9      3030
kde_upper_and_vwap  56.71  1.965  17.9      2049
kde_upper_and_vpvr  50.67  1.541  23.9       300
kde_upper_and_near  56.06  1.913  18.4      2246
kde_lower_and_vwap  49.79  1.487  20.8       936
kde_lower_and_vpvr  61.90  2.438  19.3       147
kde_lower_and_near  51.63  1.601  20.8      1042

    kde_gate                  covers 29.3% of regime bars  !! LOW
    kde_upper                 covers 22.0% of regime bars  !! LOW
    kde_lower_fresh           covers 10.1% of regime bars  !! LOW
    vwap_only                 covers 36.8% of regime bars
    vpvr_only                 covers 3.7% of regime bars  !! LOW
    near_setup                covers 39.5% of regime bars
    kde_gate_and_vwap         covers 11.5% of regime bars  !! LOW
    kde_gate_and_vpvr         covers 1.8% of regime bars  !! LOW
    kde_gate_and_near         covers 12.7% of regime bars  !! LOW
    kde_upper_and_vwap        covers 8.6% of regime bars  !! LOW
    kde_upper_and_vpvr        covers 1.3% of regime bars  !! LOW
    kde_upper_and_near        covers 9.4% of regime bars  !! LOW
    kde_lower_and_vwap        covers 3.9% of regime bars  !! LOW
    kde_lower_and_vpvr        covers 0.6% of regime bars  !! LOW
    kde_lower_and_near        covers 4.4% of regime bars  !! LOW

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         44.84  1.219  19.5     22371
kde_gate            48.58  1.417  19.2      7003
kde_upper           48.91  1.436  18.8      5475
kde_lower_fresh     47.30  1.347  21.6      2152
vwap_only           45.23  1.239  18.2      8211
vpvr_only           42.94  1.129  21.5       871
near_setup          45.18  1.236  18.5      8849
kde_gate_and_vwap   50.92  1.556  17.9      2651
kde_gate_and_vpvr   47.41  1.352  17.0       464
kde_gate_and_near   51.10  1.567  17.6      2961
kde_upper_and_vwap  50.29  1.518  17.5      2060
kde_upper_and_vpvr  48.16  1.393  15.3       380
kde_upper_and_near  50.48  1.529  17.1      2314
kde_lower_and_vwap  51.14  1.570  19.9       837
kde_lower_and_vpvr  44.07  1.182  27.8       118
kde_lower_and_near  51.54  1.595  20.2       908

    kde_gate                  covers 31.3% of regime bars
    kde_upper                 covers 24.5% of regime bars  !! LOW
    kde_lower_fresh           covers 9.6% of regime bars  !! LOW
    vwap_only                 covers 36.7% of regime bars
    vpvr_only                 covers 3.9% of regime bars  !! LOW
    near_setup                covers 39.6% of regime bars
    kde_gate_and_vwap         covers 11.9% of regime bars  !! LOW
    kde_gate_and_vpvr         covers 2.1% of regime bars  !! LOW
    kde_gate_and_near         covers 13.2% of regime bars  !! LOW
    kde_upper_and_vwap        covers 9.2% of regime bars  !! LOW
    kde_upper_and_vpvr        covers 1.7% of regime bars  !! LOW
    kde_upper_and_near        covers 10.3% of regime bars  !! LOW
    kde_lower_and_vwap        covers 3.7% of regime bars  !! LOW
    kde_lower_and_vpvr        covers 0.5% of regime bars  !! LOW
    kde_lower_and_near        covers 4.1% of regime bars  !! LOW

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         44.88  1.222  19.0     20243
kde_gate            49.87  1.492  20.5      5707
kde_upper           51.36  1.584  21.1      4367
kde_lower_fresh     46.67  1.312  21.7      1860
vwap_only           45.76  1.266  18.2      7213
vpvr_only           57.43  2.023  18.3       606
near_setup          46.34  1.295  18.1      7627
kde_gate_and_vwap   50.34  1.521  20.2      2177
kde_gate_and_vpvr   59.93  2.243  18.1       277
kde_gate_and_near   50.83  1.551  19.8      2345
kde_upper_and_vwap  52.87  1.683  20.4      1706
kde_upper_and_vpvr  61.70  2.417  16.4       235
kde_upper_and_near  53.37  1.717  19.9      1838
kde_lower_and_vwap  42.75  1.120  21.6       683
kde_lower_and_vpvr  44.64  1.210  24.2        56
kde_lower_and_near  42.82  1.123  21.4       731

    kde_gate                  covers 28.2% of regime bars  !! LOW
    kde_upper                 covers 21.6% of regime bars  !! LOW
    kde_lower_fresh           covers 9.2% of regime bars  !! LOW
    vwap_only                 covers 35.6% of regime bars
    vpvr_only                 covers 3.0% of regime bars  !! LOW
    near_setup                covers 37.7% of regime bars
    kde_gate_and_vwap         covers 10.8% of regime bars  !! LOW
    kde_gate_and_vpvr         covers 1.4% of regime bars  !! LOW
    kde_gate_and_near         covers 11.6% of regime bars  !! LOW
    kde_upper_and_vwap        covers 8.4% of regime bars  !! LOW
    kde_upper_and_vpvr        covers 1.2% of regime bars  !! LOW
    kde_upper_and_near        covers 9.1% of regime bars  !! LOW
    kde_lower_and_vwap        covers 3.4% of regime bars  !! LOW
    kde_lower_and_vpvr        covers 0.3% of regime bars  !! LOW
    kde_lower_and_near        covers 3.6% of regime bars  !! LOW

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         47.17  1.339  22.3     24598
kde_gate            51.62  1.600  23.1      6463
kde_upper           51.86  1.616  22.3      5195
kde_lower_fresh     49.66  1.480  30.1      1780
vwap_only           48.44  1.409  22.6      9398
vpvr_only           52.43  1.653  23.4       637
near_setup          48.67  1.422  22.7      9840
kde_gate_and_vwap   51.75  1.609  24.3      2711
kde_gate_and_vpvr   60.55  2.303  20.1       289
kde_gate_and_near   52.38  1.650  24.0      2894
kde_upper_and_vwap  52.01  1.626  23.7      2186
kde_upper_and_vpvr  62.29  2.478  19.3       236
kde_upper_and_near  52.74  1.674  23.3      2321
kde_lower_and_vwap  50.34  1.521  32.6       731
kde_lower_and_vpvr  46.25  1.291  23.3        80
kde_lower_and_near  50.31  1.519  31.8       795

    kde_gate                  covers 26.3% of regime bars  !! LOW
    kde_upper                 covers 21.1% of regime bars  !! LOW
    kde_lower_fresh           covers 7.2% of regime bars  !! LOW
    vwap_only                 covers 38.2% of regime bars
    vpvr_only                 covers 2.6% of regime bars  !! LOW
    near_setup                covers 40.0% of regime bars
    kde_gate_and_vwap         covers 11.0% of regime bars  !! LOW
    kde_gate_and_vpvr         covers 1.2% of regime bars  !! LOW
    kde_gate_and_near         covers 11.8% of regime bars  !! LOW
    kde_upper_and_vwap        covers 8.9% of regime bars  !! LOW
    kde_upper_and_vpvr        covers 1.0% of regime bars  !! LOW
    kde_upper_and_near        covers 9.4% of regime bars  !! LOW
    kde_lower_and_vwap        covers 3.0% of regime bars  !! LOW
    kde_lower_and_vpvr        covers 0.3% of regime bars  !! LOW
    kde_lower_and_near        covers 3.2% of regime bars  !! LOW


-- KDE + Level Combined -- Verdict --

  Baseline (regime_only):  avg WR 45.2%  avg PF 1.240
  KDE (4h): window=200  bw=1  lower_dur=5  |  VWAP: daily  VPVR: 50d  |  dist=1xATR


  [KDE gate     ]  kde_gate                  WR lift +5.1pp  avg PF 1.525  PF lift +0.285  5/5 pairs  [OK]  warn: low# 4p
    BTCUSDT     WR 48.9%  PF 1.434  lift +0.244 / req 0.10  n=6,884  cov 29%!  [OK]
    ETHUSDT     WR 52.8%  PF 1.681  lift +0.453 / req 0.10  n=7,004  cov 29%!  [OK]
    SOLUSDT     WR 48.6%  PF 1.417  lift +0.198 / req 0.10  n=7,003  cov 31%  [OK]
    BNBUSDT     WR 49.9%  PF 1.492  lift +0.271 / req 0.10  n=5,707  cov 28%!  [OK]
    XRPUSDT     WR 51.6%  PF 1.600  lift +0.261 / req 0.10  n=6,463  cov 26%!  [OK]

  [KDE upper    ]  kde_upper                 WR lift +5.5pp  avg PF 1.551  PF lift +0.311  5/5 pairs  [OK]  warn: low# 5p
    BTCUSDT     WR 47.8%  PF 1.371  lift +0.181 / req 0.10  n=5,272  cov 22%!  [OK]
    ETHUSDT     WR 53.8%  PF 1.746  lift +0.518 / req 0.10  n=5,256  cov 22%!  [OK]
    SOLUSDT     WR 48.9%  PF 1.436  lift +0.217 / req 0.10  n=5,475  cov 24%!  [OK]
    BNBUSDT     WR 51.4%  PF 1.584  lift +0.362 / req 0.10  n=4,367  cov 22%!  [OK]
    XRPUSDT     WR 51.9%  PF 1.616  lift +0.277 / req 0.10  n=5,195  cov 21%!  [OK]
  [KDE lower    ]  kde_lower_fresh           WR lift +4.4pp  avg PF 1.483  PF lift +0.243  4/5 pairs  [OK]  warn: WR 3p, low# 5p
    BTCUSDT     WR 53.2%  PF 1.702  lift +0.512 / req 0.10  n=2,216  cov 9%!  [OK]
    ETHUSDT     WR 51.2%  PF 1.571  lift +0.344 / req 0.10  n=2,412  cov 10%!  [OK]
    SOLUSDT     WR 47.3%  PF 1.347  lift +0.127 / req 0.10  n=2,152  WR!  cov 10%!  [OK]
    BNBUSDT     WR 46.7%  PF 1.312  lift +0.091 / req 0.10  n=1,860  WR!  cov 9%!  [--]
    XRPUSDT     WR 49.7%  PF 1.480  lift +0.141 / req 0.10  n=1,780  WR!  cov 7%!  [OK]

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

  [Gate x VWAP  ]  kde_gate_and_vwap         WR lift +6.0pp  avg PF 1.578  PF lift +0.338  5/5 pairs  [OK]  warn: low# 5p
    BTCUSDT     WR 48.5%  PF 1.412  lift +0.221 / req 0.10  n=2,718  cov 12%!  [OK]
    ETHUSDT     WR 54.4%  PF 1.791  lift +0.563 / req 0.10  n=2,740  cov 11%!  [OK]
    SOLUSDT     WR 50.9%  PF 1.556  lift +0.337 / req 0.10  n=2,651  cov 12%!  [OK]
    BNBUSDT     WR 50.3%  PF 1.521  lift +0.299 / req 0.10  n=2,177  cov 11%!  [OK]
    XRPUSDT     WR 51.8%  PF 1.609  lift +0.270 / req 0.10  n=2,711  cov 11%!  [OK]
  [Gate x VPVR  ]  kde_gate_and_vpvr         WR lift +8.1pp  avg PF 1.774  PF lift +0.534  4/5 pairs  [OK]  warn: WR 2p, low# 5p
    BTCUSDT     WR 45.3%  PF 1.241  lift +0.050 / req 0.10  n=455  WR!  cov 2%!  [--]
    ETHUSDT     WR 53.5%  PF 1.728  lift +0.501 / req 0.10  n=424  cov 2%!  [OK]
    SOLUSDT     WR 47.4%  PF 1.352  lift +0.133 / req 0.10  n=464  WR!  cov 2%!  [OK]
    BNBUSDT     WR 59.9%  PF 2.243  lift +1.022 / req 0.10  n=277  cov 1%!  [OK]
    XRPUSDT     WR 60.6%  PF 2.303  lift +0.964 / req 0.10  n=289  cov 1%!  [OK]
  [Gate x Near  ]  kde_gate_and_near         WR lift +6.2pp  avg PF 1.591  PF lift +0.351  5/5 pairs  [OK]  warn: low# 5p
    BTCUSDT     WR 48.2%  PF 1.394  lift +0.203 / req 0.10  n=3,025  cov 13%!  [OK]
    ETHUSDT     WR 54.5%  PF 1.793  lift +0.566 / req 0.10  n=3,030  cov 13%!  [OK]
    SOLUSDT     WR 51.1%  PF 1.567  lift +0.348 / req 0.10  n=2,961  cov 13%!  [OK]
    BNBUSDT     WR 50.8%  PF 1.551  lift +0.329 / req 0.10  n=2,345  cov 12%!  [OK]
    XRPUSDT     WR 52.4%  PF 1.650  lift +0.311 / req 0.10  n=2,894  cov 12%!  [OK]

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

  [Lower x VWAP ]  kde_lower_and_vwap        WR lift +4.8pp  avg PF 1.521  PF lift +0.282  4/5 pairs  [OK]  warn: WR 2p, low# 5p
    BTCUSDT     WR 56.0%  PF 1.909  lift +0.718 / req 0.10  n=875  cov 4%!  [OK]
    ETHUSDT     WR 49.8%  PF 1.487  lift +0.260 / req 0.10  n=936  cov 4%!  [OK]
    SOLUSDT     WR 51.1%  PF 1.570  lift +0.350 / req 0.10  n=837  cov 4%!  [OK]
    BNBUSDT     WR 42.8%  PF 1.120  lift -0.101 / req 0.10  n=683  WR!  cov 3%!  [--]
    XRPUSDT     WR 50.3%  PF 1.521  lift +0.182 / req 0.10  n=731  WR!  cov 3%!  [OK]
  [Lower x VPVR ]  kde_lower_and_vpvr        WR lift +4.8pp  avg PF 1.565  PF lift +0.326  2/5 pairs  [XX]  warn: WR 4p, low# 5p
    BTCUSDT     WR 53.2%  PF 1.708  lift +0.517 / req 0.10  n=139  WR!  cov 1%!  [OK]
    ETHUSDT     WR 61.9%  PF 2.438  lift +1.210 / req 0.10  n=147  cov 1%!  [OK]
    SOLUSDT     WR 44.1%  PF 1.182  lift -0.038 / req 0.10  n=118  WR!  cov 1%!  [--]
    BNBUSDT     WR 44.6%  PF 1.210  lift -0.012 / req 0.10  n=56  WR!  cov 0%!  [--]
    XRPUSDT     WR 46.2%  PF 1.291  lift -0.048 / req 0.10  n=80  WR!  cov 0%!  [--]
  [Lower x Near ]  kde_lower_and_near        WR lift +5.2pp  avg PF 1.544  PF lift +0.305  4/5 pairs  [OK]  warn: WR 2p, low# 5p
    BTCUSDT     WR 55.7%  PF 1.884  lift +0.693 / req 0.10  n=979  cov 4%!  [OK]
    ETHUSDT     WR 51.6%  PF 1.601  lift +0.373 / req 0.10  n=1,042  cov 4%!  [OK]
    SOLUSDT     WR 51.5%  PF 1.595  lift +0.376 / req 0.10  n=908  cov 4%!  [OK]
    BNBUSDT     WR 42.8%  PF 1.123  lift -0.098 / req 0.10  n=731  WR!  cov 4%!  [--]
    XRPUSDT     WR 50.3%  PF 1.519  lift +0.180 / req 0.10  n=795  WR!  cov 3%!  [OK]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  KDE + LEVEL EDGE CONFIRMED -- confirmed populations below.
        Best performer: kde_upper_and_vpvr  (avg PF 1.788)

  Warnings (results valid -- interpret with care):
    !! [kde_gate] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT
    !! [kde_upper] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_lower_fresh] WR lift below threshold on: SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_lower_fresh] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [vwap_only] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [vpvr_only] WR lift below threshold on: ETHUSDT, SOLUSDT
    !! [vpvr_only] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [near_setup] WR lift below threshold on: SOLUSDT
    !! [kde_gate_and_vwap] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_gate_and_vpvr] WR lift below threshold on: BTCUSDT, SOLUSDT
    !! [kde_gate_and_vpvr] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_gate_and_near] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_upper_and_vwap] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_upper_and_vpvr] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT
    !! [kde_upper_and_vpvr] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_upper_and_near] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_lower_and_vwap] WR lift below threshold on: BNBUSDT, XRPUSDT
    !! [kde_lower_and_vwap] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_lower_and_vpvr] WR lift below threshold on: BTCUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_lower_and_vpvr] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [kde_lower_and_near] WR lift below threshold on: BNBUSDT, XRPUSDT
    !! [kde_lower_and_near] low trade count (<30% regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [KDE gate (combined OR)]
      [OK] kde_gate                    avg PF 1.525
    [KDE signal (standalone)]
      [OK] kde_lower_fresh             avg PF 1.483
      [OK] kde_upper                   avg PF 1.551
    [Level signal (standalone)]
      [OK] vpvr_only                   avg PF 1.541
      [--] near_setup
      [--] vwap_only
    [kde_gate x level]
      [OK] kde_gate_and_near           avg PF 1.591
      [OK] kde_gate_and_vpvr           avg PF 1.774
      [OK] kde_gate_and_vwap           avg PF 1.578
    [kde_upper x level]
      [OK] kde_upper_and_near          avg PF 1.632
      [OK] kde_upper_and_vpvr          avg PF 1.788
      [OK] kde_upper_and_vwap          avg PF 1.629
    [kde_lower_fresh x level]
      [OK] kde_lower_and_near          avg PF 1.544
      [OK] kde_lower_and_vwap          avg PF 1.521
      [--] kde_lower_and_vpvr

  Proceed to next setup step using confirmed populations.
```
