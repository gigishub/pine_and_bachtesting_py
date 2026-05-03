# Bear Strategy -- Setup 2 Trigger 5  (entry_tf=4h  kde_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `4h` |
| `kde_tf` | `4h` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `kde_window` | `200` |
| `kde_bandwidth_mult` | `1.0` |
| `bb_period` | `20` |
| `bb_std` | `2.0` |
| `kc_period` | `20` |
| `kc_atr_mult` | `2.0` |
| `vol_vel_lookback` | `20` |
| `squeeze_lookback` | `20` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 4h) --

  BTCUSDT
                          wr_%     pf   dur  n_trades
population                                           
kde_upper_baseline       46.74  1.316  18.2      1318
momentum_close           58.00  2.071  41.9       100
falling_tunnel           50.00  1.500  15.5       208
volatility_velocity      43.79  1.168  21.1       676
squeeze_snap             50.00  1.500   7.2        20
lower_expansion          48.09  1.390  22.8       603
keltner_squeeze_release  52.79  1.677  19.8       610

    momentum_close              covers 7.6% of baseline bars  !! LOW
    falling_tunnel              covers 15.8% of baseline bars  !! LOW
    volatility_velocity         covers 51.3% of baseline bars
    squeeze_snap                covers 1.5% of baseline bars  !! LOW
    lower_expansion             covers 45.8% of baseline bars
    keltner_squeeze_release     covers 46.3% of baseline bars

  ETHUSDT
                          wr_%     pf   dur  n_trades
population                                           
kde_upper_baseline       48.63  1.420  22.0      1314
momentum_close           49.59  1.475  56.0       121
falling_tunnel           50.00  1.500  32.8       172
volatility_velocity      48.20  1.396  25.6       724
squeeze_snap             76.92  5.000  16.7        13
lower_expansion          47.70  1.368  30.2       587
keltner_squeeze_release  52.71  1.672  26.5       628

    momentum_close              covers 9.2% of baseline bars  !! LOW
    falling_tunnel              covers 13.1% of baseline bars  !! LOW
    volatility_velocity         covers 55.1% of baseline bars
    squeeze_snap                covers 1.0% of baseline bars  !! LOW
    lower_expansion             covers 44.7% of baseline bars
    keltner_squeeze_release     covers 47.8% of baseline bars

  SOLUSDT
                          wr_%     pf   dur  n_trades
population                                           
kde_upper_baseline       47.02  1.331  19.9      1359
momentum_close           55.41  1.864  19.5        74
falling_tunnel           43.29  1.145  20.6       231
volatility_velocity      47.13  1.337  19.1       696
squeeze_snap             57.14  2.000  14.0        28
lower_expansion          47.56  1.361  21.7       595
keltner_squeeze_release  51.91  1.619  21.5       603

    momentum_close              covers 5.4% of baseline bars  !! LOW
    falling_tunnel              covers 17.0% of baseline bars  !! LOW
    volatility_velocity         covers 51.2% of baseline bars
    squeeze_snap                covers 2.1% of baseline bars  !! LOW
    lower_expansion             covers 43.8% of baseline bars
    keltner_squeeze_release     covers 44.4% of baseline bars

  BNBUSDT
                          wr_%     pf   dur  n_trades
population                                           
kde_upper_baseline       50.18  1.511  19.2      1082
momentum_close           44.93  1.224  51.2        69
falling_tunnel           56.90  1.980  26.1       174
volatility_velocity      53.61  1.733  22.3       610
squeeze_snap             75.00  4.500  30.3        16
lower_expansion          53.50  1.726  26.9       486
keltner_squeeze_release  48.73  1.426  17.3       474

    momentum_close              covers 6.4% of baseline bars  !! LOW
    falling_tunnel              covers 16.1% of baseline bars  !! LOW
    volatility_velocity         covers 56.4% of baseline bars
    squeeze_snap                covers 1.5% of baseline bars  !! LOW
    lower_expansion             covers 44.9% of baseline bars
    keltner_squeeze_release     covers 43.8% of baseline bars

  XRPUSDT
                          wr_%      pf   dur  n_trades
population                                            
kde_upper_baseline       52.78   1.677  18.6      1294
momentum_close           46.67   1.312  28.5        90
falling_tunnel           59.46   2.200  17.3       222
volatility_velocity      49.69   1.481  20.0       640
squeeze_snap             90.24  13.875  10.4        41
lower_expansion          52.44   1.654  20.6       574
keltner_squeeze_release  50.00   1.500  19.7       472

    momentum_close              covers 7.0% of baseline bars  !! LOW
    falling_tunnel              covers 17.2% of baseline bars  !! LOW
    volatility_velocity         covers 49.5% of baseline bars
    squeeze_snap                covers 3.2% of baseline bars  !! LOW
    lower_expansion             covers 44.4% of baseline bars
    keltner_squeeze_release     covers 36.5% of baseline bars


-- Setup 2 Trigger 5 (4h) -- Verdict --

  Baseline (kde_upper_baseline on 4h):  avg WR 49.1%  avg PF 1.451
  KDE (4h): window=200  bw=1  |  BB(20,2std)  KC(20,2atr)

  [Volatility  ]  momentum_close              WR lift +1.8pp  avg PF 1.589  PF lift +0.138  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 58.0%  PF 2.071  lift +0.755 / req 0.10  n=100  WR!  cov 8%!  [OK]
    ETHUSDT     WR 49.6%  PF 1.475  lift +0.055 / req 0.10  n=121  WR!  cov 9%!  [--]
    SOLUSDT     WR 55.4%  PF 1.864  lift +0.532 / req 0.10  n=74  WR!  cov 5%!  [OK]
    BNBUSDT     WR 44.9%  PF 1.224  lift -0.287 / req 0.10  n=69  WR!  cov 6%!  [--]
    XRPUSDT     WR 46.7%  PF 1.312  lift -0.364 / req 0.10  n=90  WR!  cov 7%!  [--]
  [Volatility  ]  falling_tunnel              WR lift +2.9pp  avg PF 1.665  PF lift +0.214  3/5 pairs  [OK]  warn: WR 5p, low# 5p
    BTCUSDT     WR 50.0%  PF 1.500  lift +0.184 / req 0.10  n=208  WR!  cov 16%!  [OK]
    ETHUSDT     WR 50.0%  PF 1.500  lift +0.080 / req 0.10  n=172  WR!  cov 13%!  [--]
    SOLUSDT     WR 43.3%  PF 1.145  lift -0.186 / req 0.10  n=231  WR!  cov 17%!  [--]
    BNBUSDT     WR 56.9%  PF 1.980  lift +0.469 / req 0.10  n=174  WR!  cov 16%!  [OK]
    XRPUSDT     WR 59.5%  PF 2.200  lift +0.523 / req 0.10  n=222  WR!  cov 17%!  [OK]
  [Volatility  ]  volatility_velocity         WR lift -0.6pp  avg PF 1.423  PF lift -0.028  1/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 43.8%  PF 1.168  lift -0.148 / req 0.10  n=676  WR!  cov 51%  [--]
    ETHUSDT     WR 48.2%  PF 1.396  lift -0.024 / req 0.10  n=724  WR!  cov 55%  [--]
    SOLUSDT     WR 47.1%  PF 1.337  lift +0.006 / req 0.10  n=696  WR!  cov 51%  [--]
    BNBUSDT     WR 53.6%  PF 1.733  lift +0.222 / req 0.10  n=610  WR!  cov 56%  [OK]
    XRPUSDT     WR 49.7%  PF 1.481  lift -0.195 / req 0.10  n=640  WR!  cov 49%  [--]
  [Volatility  ]  squeeze_snap                WR lift +20.8pp  avg PF 5.375  PF lift +3.924  5/5 pairs  [OK]  warn: WR 4p, low# 5p
    BTCUSDT     WR 50.0%  PF 1.500  lift +0.184 / req 0.10  n=20  WR!  cov 2%!  [OK]
    ETHUSDT     WR 76.9%  PF 5.000  lift +3.580 / req 0.10  n=13  WR!  cov 1%!  [OK]
    SOLUSDT     WR 57.1%  PF 2.000  lift +0.669 / req 0.10  n=28  WR!  cov 2%!  [OK]
    BNBUSDT     WR 75.0%  PF 4.500  lift +2.989 / req 0.10  n=16  WR!  cov 1%!  [OK]
    XRPUSDT     WR 90.2%  PF 13.875  lift +12.198 / req 0.10  n=41  cov 3%!  [OK]
  [Volatility  ]  lower_expansion             WR lift +0.8pp  avg PF 1.500  PF lift +0.049  1/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 48.1%  PF 1.390  lift +0.074 / req 0.10  n=603  WR!  cov 46%  [--]
    ETHUSDT     WR 47.7%  PF 1.368  lift -0.052 / req 0.10  n=587  WR!  cov 45%  [--]
    SOLUSDT     WR 47.6%  PF 1.361  lift +0.029 / req 0.10  n=595  WR!  cov 44%  [--]
    BNBUSDT     WR 53.5%  PF 1.726  lift +0.215 / req 0.10  n=486  WR!  cov 45%  [OK]
    XRPUSDT     WR 52.4%  PF 1.654  lift -0.023 / req 0.10  n=574  WR!  cov 44%  [--]
  [Volatility  ]  keltner_squeeze_release     WR lift +2.2pp  avg PF 1.579  PF lift +0.128  3/5 pairs  [OK]  warn: WR 4p
    BTCUSDT     WR 52.8%  PF 1.677  lift +0.361 / req 0.10  n=610  cov 46%  [OK]
    ETHUSDT     WR 52.7%  PF 1.672  lift +0.252 / req 0.10  n=628  WR!  cov 48%  [OK]
    SOLUSDT     WR 51.9%  PF 1.619  lift +0.288 / req 0.10  n=603  WR!  cov 44%  [OK]
    BNBUSDT     WR 48.7%  PF 1.426  lift -0.085 / req 0.10  n=474  WR!  cov 44%  [--]
    XRPUSDT     WR 50.0%  PF 1.500  lift -0.177 / req 0.10  n=472  WR!  cov 36%  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 5 (4h) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.451  |  Best: squeeze_snap  (avg PF 5.375)

  Warnings (results valid -- interpret with care):
    !! [momentum_close] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [momentum_close] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [falling_tunnel] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [falling_tunnel] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [volatility_velocity] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [squeeze_snap] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT
    !! [squeeze_snap] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [lower_expansion] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [keltner_squeeze_release] WR lift below threshold on: ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Volatility]
      [OK] falling_tunnel              avg PF 1.665
      [OK] keltner_squeeze_release     avg PF 1.579
      [OK] squeeze_snap                avg PF 5.375
      [--] lower_expansion
      [--] momentum_close
      [--] volatility_velocity

  Proceed using confirmed BB/KC signal(s) for setup 3 construction.
```
