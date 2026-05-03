# Bear Strategy -- Setup 2 Trigger 2  (entry_tf=1h  kde_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `1h` |
| `kde_tf` | `4h` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `kde_window` | `200` |
| `kde_bandwidth_mult` | `1.0` |
| `cmf_period` | `20` |
| `willr_period` | `14` |
| `willr_threshold` | `-20.0` |
| `roc_period` | `12` |
| `trix_period` | `15` |
| `trix_signal_period` | `9` |
| `fisher_period` | `9` |
| `fisher_extreme` | `1.5` |
| `ema_cross_period` | `20` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 1h) --

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  47.76  1.371  20.9      5272
cmf_cross           43.73  1.166  19.4       343
willr_cross         44.72  1.213  20.6       322
roc_cross           46.85  1.322  18.5       429
trix_cross          42.31  1.100  20.4       130
fisher_cross        44.24  1.190  19.7       495
ema_cross           47.33  1.348  19.5       393

    cmf_cross       covers 6.5% of baseline bars  !! LOW
    willr_cross     covers 6.1% of baseline bars  !! LOW
    roc_cross       covers 8.1% of baseline bars  !! LOW
    trix_cross      covers 2.5% of baseline bars  !! LOW
    fisher_cross    covers 9.4% of baseline bars  !! LOW
    ema_cross       covers 7.5% of baseline bars  !! LOW

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  53.79  1.746  21.0      5256
cmf_cross           56.07  1.915  19.0       321
willr_cross         46.89  1.324  19.9       305
roc_cross           52.99  1.691  16.2       385
trix_cross          54.26  1.780  18.6       129
fisher_cross        51.25  1.577  17.1       441
ema_cross           57.87  2.060  18.4       356

    cmf_cross       covers 6.1% of baseline bars  !! LOW
    willr_cross     covers 5.8% of baseline bars  !! LOW
    roc_cross       covers 7.3% of baseline bars  !! LOW
    trix_cross      covers 2.5% of baseline bars  !! LOW
    fisher_cross    covers 8.4% of baseline bars  !! LOW
    ema_cross       covers 6.8% of baseline bars  !! LOW

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  48.91  1.436  18.8      5475
cmf_cross           47.58  1.361  17.2       351
willr_cross         45.96  1.276  18.6       359
roc_cross           48.30  1.401  19.8       412
trix_cross          45.32  1.243  24.4       139
fisher_cross        49.51  1.471  17.5       515
ema_cross           48.06  1.388  18.7       387

    cmf_cross       covers 6.4% of baseline bars  !! LOW
    willr_cross     covers 6.6% of baseline bars  !! LOW
    roc_cross       covers 7.5% of baseline bars  !! LOW
    trix_cross      covers 2.5% of baseline bars  !! LOW
    fisher_cross    covers 9.4% of baseline bars  !! LOW
    ema_cross       covers 7.1% of baseline bars  !! LOW

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.36  1.584  21.1      4367
cmf_cross           49.81  1.488  22.3       257
willr_cross         43.32  1.146  19.0       277
roc_cross           50.15  1.509  16.9       331
trix_cross          43.86  1.172  18.8       114
fisher_cross        48.29  1.401  19.1       381
ema_cross           53.12  1.700  20.8       320

    cmf_cross       covers 5.9% of baseline bars  !! LOW
    willr_cross     covers 6.3% of baseline bars  !! LOW
    roc_cross       covers 7.6% of baseline bars  !! LOW
    trix_cross      covers 2.6% of baseline bars  !! LOW
    fisher_cross    covers 8.7% of baseline bars  !! LOW
    ema_cross       covers 7.3% of baseline bars  !! LOW

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.86  1.616  22.3      5195
cmf_cross           54.70  1.812  23.9       287
willr_cross         49.47  1.469  20.8       285
roc_cross           52.96  1.688  19.5       406
trix_cross          53.85  1.750  37.1       117
fisher_cross        52.19  1.638  20.7       456
ema_cross           57.25  2.008  20.3       414

    cmf_cross       covers 5.5% of baseline bars  !! LOW
    willr_cross     covers 5.5% of baseline bars  !! LOW
    roc_cross       covers 7.8% of baseline bars  !! LOW
    trix_cross      covers 2.3% of baseline bars  !! LOW
    fisher_cross    covers 8.8% of baseline bars  !! LOW
    ema_cross       covers 8.0% of baseline bars  !! LOW


-- Setup 2 Trigger 2 (1h) -- Verdict --

  Baseline (kde_upper_baseline on 1h):  avg WR 50.7%  avg PF 1.551
  KDE (4h): window=200  bw=1  |  CMF(20)  WR(14)<-20  ROC(12)  TRIX(15,9)  Fisher(9)>1.5  EMA(20)

  [Volume      ]  cmf_cross       WR lift -0.4pp  avg PF 1.548  PF lift -0.002  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 43.7%  PF 1.166  lift -0.206 / req 0.10  n=343  WR!  cov 7%!  [--]
    ETHUSDT     WR 56.1%  PF 1.915  lift +0.169 / req 0.10  n=321  WR!  cov 6%!  [OK]
    SOLUSDT     WR 47.6%  PF 1.361  lift -0.075 / req 0.10  n=351  WR!  cov 6%!  [--]
    BNBUSDT     WR 49.8%  PF 1.488  lift -0.096 / req 0.10  n=257  WR!  cov 6%!  [--]
    XRPUSDT     WR 54.7%  PF 1.812  lift +0.196 / req 0.10  n=287  WR!  cov 6%!  [OK]
  [Oscillator  ]  willr_cross     WR lift -4.7pp  avg PF 1.286  PF lift -0.265  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 44.7%  PF 1.213  lift -0.158 / req 0.10  n=322  WR!  cov 6%!  [--]
    ETHUSDT     WR 46.9%  PF 1.324  lift -0.422 / req 0.10  n=305  WR!  cov 6%!  [--]
    SOLUSDT     WR 46.0%  PF 1.276  lift -0.160 / req 0.10  n=359  WR!  cov 7%!  [--]
    BNBUSDT     WR 43.3%  PF 1.146  lift -0.438 / req 0.10  n=277  WR!  cov 6%!  [--]
    XRPUSDT     WR 49.5%  PF 1.469  lift -0.147 / req 0.10  n=285  WR!  cov 5%!  [--]
  [Oscillator  ]  roc_cross       WR lift -0.5pp  avg PF 1.522  PF lift -0.028  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 46.9%  PF 1.322  lift -0.049 / req 0.10  n=429  WR!  cov 8%!  [--]
    ETHUSDT     WR 53.0%  PF 1.691  lift -0.055 / req 0.10  n=385  WR!  cov 7%!  [--]
    SOLUSDT     WR 48.3%  PF 1.401  lift -0.035 / req 0.10  n=412  WR!  cov 8%!  [--]
    BNBUSDT     WR 50.2%  PF 1.509  lift -0.075 / req 0.10  n=331  WR!  cov 8%!  [--]
    XRPUSDT     WR 53.0%  PF 1.688  lift +0.073 / req 0.10  n=406  WR!  cov 8%!  [--]
  [Trend       ]  trix_cross      WR lift -2.8pp  avg PF 1.409  PF lift -0.142  1/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 42.3%  PF 1.100  lift -0.271 / req 0.10  n=130  WR!  cov 2%!  [--]
    ETHUSDT     WR 54.3%  PF 1.780  lift +0.034 / req 0.10  n=129  WR!  cov 2%!  [--]
    SOLUSDT     WR 45.3%  PF 1.243  lift -0.193 / req 0.10  n=139  WR!  cov 3%!  [--]
    BNBUSDT     WR 43.9%  PF 1.172  lift -0.412 / req 0.10  n=114  WR!  cov 3%!  [--]
    XRPUSDT     WR 53.8%  PF 1.750  lift +0.134 / req 0.10  n=117  WR!  cov 2%!  [OK]
  [Oscillator  ]  fisher_cross    WR lift -1.6pp  avg PF 1.455  PF lift -0.095  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 44.2%  PF 1.190  lift -0.181 / req 0.10  n=495  WR!  cov 9%!  [--]
    ETHUSDT     WR 51.2%  PF 1.577  lift -0.169 / req 0.10  n=441  WR!  cov 8%!  [--]
    SOLUSDT     WR 49.5%  PF 1.471  lift +0.035 / req 0.10  n=515  WR!  cov 9%!  [--]
    BNBUSDT     WR 48.3%  PF 1.401  lift -0.183 / req 0.10  n=381  WR!  cov 9%!  [--]
    XRPUSDT     WR 52.2%  PF 1.638  lift +0.022 / req 0.10  n=456  WR!  cov 9%!  [--]
  [Trend       ]  ema_cross       WR lift +2.0pp  avg PF 1.701  PF lift +0.150  3/5 pairs  [OK]  warn: WR 5p, low# 5p
    BTCUSDT     WR 47.3%  PF 1.348  lift -0.024 / req 0.10  n=393  WR!  cov 7%!  [--]
    ETHUSDT     WR 57.9%  PF 2.060  lift +0.314 / req 0.10  n=356  WR!  cov 7%!  [OK]
    SOLUSDT     WR 48.1%  PF 1.388  lift -0.048 / req 0.10  n=387  WR!  cov 7%!  [--]
    BNBUSDT     WR 53.1%  PF 1.700  lift +0.116 / req 0.10  n=320  WR!  cov 7%!  [OK]
    XRPUSDT     WR 57.2%  PF 2.008  lift +0.393 / req 0.10  n=414  WR!  cov 8%!  [OK]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 2 (1h) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.551  |  Best: ema_cross  (avg PF 1.701)

  Warnings (results valid -- interpret with care):
    !! [cmf_cross] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [cmf_cross] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [willr_cross] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [willr_cross] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [roc_cross] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [roc_cross] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [trix_cross] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [trix_cross] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [fisher_cross] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [fisher_cross] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [ema_cross] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [ema_cross] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Volume]
      [--] cmf_cross
    [Oscillator]
      [--] fisher_cross
      [--] roc_cross
      [--] willr_cross
    [Trend]
      [OK] ema_cross         avg PF 1.701
      [--] trix_cross

  Proceed using confirmed momentum-flip trigger(s) for setup 3 construction.
```
