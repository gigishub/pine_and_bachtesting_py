# Bear Strategy -- Setup 2 Trigger: KDE Upper (4h) + 15m signals  (entry_tf=15m  kde_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `15m` |
| `kde_tf` | `4h` |
| `context_tf` | `1d` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `kde_window` | `200` |
| `kde_bandwidth_mult` | `1.0` |
| `vwap_anchor` | `daily` |
| `vpvr_window` | `50` |
| `vpvr_n_bins` | `50` |
| `setup_distance_atr` | `1.0` |
| `rvol_window` | `20` |
| `rvol_threshold` | `1.4` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 15m) --

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  45.41  1.248  22.7     21088
vwap_only           46.77  1.318  24.5      4561
vpvr_only           35.12  0.812  33.0       652
near_setup          45.45  1.250  25.5      5072
rvol_only           47.15  1.338  30.1      4172
vwap_and_rvol       48.77  1.428  34.8       773
vpvr_and_rvol       36.11  0.848  43.5       144
near_and_rvol       46.49  1.303  36.1       882

    vwap_only               covers 21.6% of baseline bars  !! LOW
    vpvr_only               covers 3.1% of baseline bars  !! LOW
    near_setup              covers 24.1% of baseline bars  !! LOW
    rvol_only               covers 19.8% of baseline bars  !! LOW
    vwap_and_rvol           covers 3.7% of baseline bars  !! LOW
    vpvr_and_rvol           covers 0.7% of baseline bars  !! LOW
    near_and_rvol           covers 4.2% of baseline bars  !! LOW

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  49.83  1.490  20.8     21024
vwap_only           50.32  1.519  20.1      4426
vpvr_only           48.55  1.415  37.2       517
near_setup          50.24  1.514  21.5      4835
rvol_only           50.46  1.528  27.4      4259
vwap_and_rvol       49.21  1.453  27.6       823
vpvr_and_rvol       47.45  1.354  50.7       137
near_and_rvol       49.09  1.446  29.5       935

    vwap_only               covers 21.1% of baseline bars  !! LOW
    vpvr_only               covers 2.5% of baseline bars  !! LOW
    near_setup              covers 23.0% of baseline bars  !! LOW
    rvol_only               covers 20.3% of baseline bars  !! LOW
    vwap_and_rvol           covers 3.9% of baseline bars  !! LOW
    vpvr_and_rvol           covers 0.7% of baseline bars  !! LOW
    near_and_rvol           covers 4.4% of baseline bars  !! LOW

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  46.71  1.315  20.6     21965
vwap_only           46.54  1.306  20.3      4703
vpvr_only           44.60  1.208  18.5       713
near_setup          46.45  1.301  20.1      5287
rvol_only           48.48  1.411  25.7      4299
vwap_and_rvol       49.22  1.454  25.7       831
vpvr_and_rvol       49.69  1.482  19.4       163
near_and_rvol       49.38  1.463  24.8       972

    vwap_only               covers 21.4% of baseline bars  !! LOW
    vpvr_only               covers 3.2% of baseline bars  !! LOW
    near_setup              covers 24.1% of baseline bars  !! LOW
    rvol_only               covers 19.6% of baseline bars  !! LOW
    vwap_and_rvol           covers 3.8% of baseline bars  !! LOW
    vpvr_and_rvol           covers 0.7% of baseline bars  !! LOW
    near_and_rvol           covers 4.4% of baseline bars  !! LOW

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  47.65  1.365  20.3     17502
vwap_only           50.65  1.540  21.9      3597
vpvr_only           52.01  1.626  17.1       398
near_setup          50.70  1.543  21.5      3919
rvol_only           48.46  1.410  26.4      3739
vwap_and_rvol       52.65  1.668  26.7       754
vpvr_and_rvol       55.84  1.897  19.8        77
near_and_rvol       52.73  1.674  26.0       823

    vwap_only               covers 20.6% of baseline bars  !! LOW
    vpvr_only               covers 2.3% of baseline bars  !! LOW
    near_setup              covers 22.4% of baseline bars  !! LOW
    rvol_only               covers 21.4% of baseline bars  !! LOW
    vwap_and_rvol           covers 4.3% of baseline bars  !! LOW
    vpvr_and_rvol           covers 0.4% of baseline bars  !! LOW
    near_and_rvol           covers 4.7% of baseline bars  !! LOW

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  48.07  1.389  22.4     20784
vwap_only           47.60  1.363  26.2      4861
vpvr_only           57.35  2.017  28.0       415
near_setup          48.26  1.399  26.4      5141
rvol_only           47.94  1.381  29.8      3963
vwap_and_rvol       46.62  1.310  45.4       843
vpvr_and_rvol       58.06  2.077  40.9        93
near_and_rvol       47.85  1.377  45.4       909

    vwap_only               covers 23.4% of baseline bars  !! LOW
    vpvr_only               covers 2.0% of baseline bars  !! LOW
    near_setup              covers 24.7% of baseline bars  !! LOW
    rvol_only               covers 19.1% of baseline bars  !! LOW
    vwap_and_rvol           covers 4.1% of baseline bars  !! LOW
    vpvr_and_rvol           covers 0.4% of baseline bars  !! LOW
    near_and_rvol           covers 4.4% of baseline bars  !! LOW


-- Setup 2 Trigger (15m) -- Verdict --

  Baseline (kde_upper_baseline on 15m):  avg WR 47.5%  avg PF 1.361
  KDE (4h): window=200  bw=1  |  dist=1xATR(15m)  |  RVOL: 20 bars (5h) threshold=1.4


  [Level only   ]  vwap_only               WR lift +0.8pp  avg PF 1.409  PF lift +0.048  1/5 pairs  [XX]  warn: WR 4p, low# 5p
    BTCUSDT     WR 46.8%  PF 1.318  lift +0.070 / req 0.10  n=4,561  WR!  cov 22%!  [--]
    ETHUSDT     WR 50.3%  PF 1.519  lift +0.029 / req 0.10  n=4,426  WR!  cov 21%!  [--]
    SOLUSDT     WR 46.5%  PF 1.306  lift -0.009 / req 0.10  n=4,703  WR!  cov 21%!  [--]
    BNBUSDT     WR 50.7%  PF 1.540  lift +0.174 / req 0.10  n=3,597  cov 21%!  [OK]
    XRPUSDT     WR 47.6%  PF 1.363  lift -0.026 / req 0.10  n=4,861  WR!  cov 23%!  [--]
  [Level only   ]  vpvr_only               WR lift -0.0pp  avg PF 1.416  PF lift +0.054  2/5 pairs  [XX]  warn: WR 4p, low# 5p
    BTCUSDT     WR 35.1%  PF 0.812  lift -0.436 / req 0.10  n=652  WR!  cov 3%!  [--]
    ETHUSDT     WR 48.5%  PF 1.415  lift -0.075 / req 0.10  n=517  WR!  cov 2%!  [--]
    SOLUSDT     WR 44.6%  PF 1.208  lift -0.107 / req 0.10  n=713  WR!  cov 3%!  [--]
    BNBUSDT     WR 52.0%  PF 1.626  lift +0.260 / req 0.10  n=398  WR!  cov 2%!  [OK]
    XRPUSDT     WR 57.3%  PF 2.017  lift +0.628 / req 0.10  n=415  cov 2%!  [OK]
  [Level only   ]  near_setup              WR lift +0.7pp  avg PF 1.401  PF lift +0.040  1/5 pairs  [XX]  warn: WR 4p, low# 5p
    BTCUSDT     WR 45.4%  PF 1.250  lift +0.002 / req 0.10  n=5,072  WR!  cov 24%!  [--]
    ETHUSDT     WR 50.2%  PF 1.514  lift +0.024 / req 0.10  n=4,835  WR!  cov 23%!  [--]
    SOLUSDT     WR 46.5%  PF 1.301  lift -0.014 / req 0.10  n=5,287  WR!  cov 24%!  [--]
    BNBUSDT     WR 50.7%  PF 1.543  lift +0.177 / req 0.10  n=3,919  cov 22%!  [OK]
    XRPUSDT     WR 48.3%  PF 1.399  lift +0.011 / req 0.10  n=5,141  WR!  cov 25%!  [--]

  [RVOL only    ]  rvol_only               WR lift +1.0pp  avg PF 1.414  PF lift +0.052  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 47.1%  PF 1.338  lift +0.090 / req 0.10  n=4,172  WR!  cov 20%!  [--]
    ETHUSDT     WR 50.5%  PF 1.528  lift +0.038 / req 0.10  n=4,259  WR!  cov 20%!  [--]
    SOLUSDT     WR 48.5%  PF 1.411  lift +0.096 / req 0.10  n=4,299  WR!  cov 20%!  [--]
    BNBUSDT     WR 48.5%  PF 1.410  lift +0.045 / req 0.10  n=3,739  WR!  cov 21%!  [--]
    XRPUSDT     WR 47.9%  PF 1.381  lift -0.007 / req 0.10  n=3,963  WR!  cov 19%!  [--]

  [Level + RVOL ]  vwap_and_rvol           WR lift +1.8pp  avg PF 1.463  PF lift +0.101  3/5 pairs  [OK]  warn: WR 4p, low# 5p
    BTCUSDT     WR 48.8%  PF 1.428  lift +0.180 / req 0.10  n=773  WR!  cov 4%!  [OK]
    ETHUSDT     WR 49.2%  PF 1.453  lift -0.037 / req 0.10  n=823  WR!  cov 4%!  [--]
    SOLUSDT     WR 49.2%  PF 1.454  lift +0.139 / req 0.10  n=831  WR!  cov 4%!  [OK]
    BNBUSDT     WR 52.7%  PF 1.668  lift +0.303 / req 0.10  n=754  cov 4%!  [OK]
    XRPUSDT     WR 46.6%  PF 1.310  lift -0.079 / req 0.10  n=843  WR!  cov 4%!  [--]
  [Level + RVOL ]  vpvr_and_rvol           WR lift +1.9pp  avg PF 1.532  PF lift +0.170  3/5 pairs  [OK]  warn: WR 5p, low# 5p
    BTCUSDT     WR 36.1%  PF 0.848  lift -0.400 / req 0.10  n=144  WR!  cov 1%!  [--]
    ETHUSDT     WR 47.4%  PF 1.354  lift -0.136 / req 0.10  n=137  WR!  cov 1%!  [--]
    SOLUSDT     WR 49.7%  PF 1.482  lift +0.167 / req 0.10  n=163  WR!  cov 1%!  [OK]
    BNBUSDT     WR 55.8%  PF 1.897  lift +0.532 / req 0.10  n=77  WR!  cov 0%!  [OK]
    XRPUSDT     WR 58.1%  PF 2.077  lift +0.688 / req 0.10  n=93  WR!  cov 0%!  [OK]
  [Level + RVOL ]  near_and_rvol           WR lift +1.6pp  avg PF 1.453  PF lift +0.091  2/5 pairs  [XX]  warn: WR 4p, low# 5p
    BTCUSDT     WR 46.5%  PF 1.303  lift +0.055 / req 0.10  n=882  WR!  cov 4%!  [--]
    ETHUSDT     WR 49.1%  PF 1.446  lift -0.044 / req 0.10  n=935  WR!  cov 4%!  [--]
    SOLUSDT     WR 49.4%  PF 1.463  lift +0.149 / req 0.10  n=972  WR!  cov 4%!  [OK]
    BNBUSDT     WR 52.7%  PF 1.674  lift +0.308 / req 0.10  n=823  cov 5%!  [OK]
    XRPUSDT     WR 47.9%  PF 1.377  lift -0.012 / req 0.10  n=909  WR!  cov 4%!  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER (15m) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.361  |  Best: vpvr_and_rvol  (avg PF 1.532)

  Warnings (results valid -- interpret with care):
    !! [vwap_only] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT
    !! [vwap_only] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [vpvr_only] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT
    !! [vpvr_only] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [near_setup] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT
    !! [near_setup] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rvol_only] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rvol_only] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [vwap_and_rvol] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT
    !! [vwap_and_rvol] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [vpvr_and_rvol] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [vpvr_and_rvol] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [near_and_rvol] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT
    !! [near_and_rvol] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Level proximity]
      [--] near_setup
      [--] vpvr_only
      [--] vwap_only
    [RVOL]
      [--] rvol_only
    [Level + RVOL]
      [OK] vpvr_and_rvol           avg PF 1.532
      [OK] vwap_and_rvol           avg PF 1.463
      [--] near_and_rvol

  Proceed to setup 3 using confirmed 15m trigger combination(s).
```
