# Bear Strategy -- Setup 2 Trigger 5  (entry_tf=1h  kde_tf=4h)

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
| `bb_period` | `20` |
| `bb_std` | `2.0` |
| `kc_period` | `20` |
| `kc_atr_mult` | `2.0` |
| `vol_vel_lookback` | `20` |
| `squeeze_lookback` | `20` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 1h) --

  BTCUSDT
                          wr_%     pf   dur  n_trades
population                                           
kde_upper_baseline       47.76  1.371  20.9      5272
momentum_close           57.97  2.069  38.6       433
falling_tunnel           50.56  1.534  19.2      1062
volatility_velocity      48.04  1.387  23.8      2864
squeeze_snap             46.46  1.302  14.3        99
lower_expansion          50.63  1.538  25.3      2552
keltner_squeeze_release  48.92  1.436  23.9      2212

    momentum_close              covers 8.2% of baseline bars  !! LOW
    falling_tunnel              covers 20.1% of baseline bars  !! LOW
    volatility_velocity         covers 54.3% of baseline bars
    squeeze_snap                covers 1.9% of baseline bars  !! LOW
    lower_expansion             covers 48.4% of baseline bars
    keltner_squeeze_release     covers 42.0% of baseline bars

  ETHUSDT
                          wr_%     pf   dur  n_trades
population                                           
kde_upper_baseline       53.79  1.746  21.0      5256
momentum_close           59.80  2.231  43.9       500
falling_tunnel           59.91  2.241  23.7      1090
volatility_velocity      54.25  1.779  23.0      2879
squeeze_snap             66.23  2.942  14.9        77
lower_expansion          56.84  1.975  26.0      2618
keltner_squeeze_release  53.75  1.744  26.2      2357

    momentum_close              covers 9.5% of baseline bars  !! LOW
    falling_tunnel              covers 20.7% of baseline bars  !! LOW
    volatility_velocity         covers 54.8% of baseline bars
    squeeze_snap                covers 1.5% of baseline bars  !! LOW
    lower_expansion             covers 49.8% of baseline bars
    keltner_squeeze_release     covers 44.8% of baseline bars

  SOLUSDT
                          wr_%     pf   dur  n_trades
population                                           
kde_upper_baseline       48.91  1.436  18.8      5475
momentum_close           53.05  1.695  32.0       426
falling_tunnel           52.53  1.660  17.9      1148
volatility_velocity      48.74  1.426  21.1      2930
squeeze_snap             54.46  1.793  20.9       101
lower_expansion          51.25  1.577  21.7      2630
keltner_squeeze_release  49.06  1.445  19.1      2495

    momentum_close              covers 7.8% of baseline bars  !! LOW
    falling_tunnel              covers 21.0% of baseline bars  !! LOW
    volatility_velocity         covers 53.5% of baseline bars
    squeeze_snap                covers 1.8% of baseline bars  !! LOW
    lower_expansion             covers 48.0% of baseline bars
    keltner_squeeze_release     covers 45.6% of baseline bars

  BNBUSDT
                          wr_%     pf   dur  n_trades
population                                           
kde_upper_baseline       51.36  1.584  21.1      4367
momentum_close           52.08  1.630  39.0       336
falling_tunnel           55.50  1.870  19.4       928
volatility_velocity      50.60  1.537  22.9      2405
squeeze_snap             48.94  1.438  13.8        94
lower_expansion          51.89  1.618  24.2      2170
keltner_squeeze_release  46.29  1.293  22.6      1912

    momentum_close              covers 7.7% of baseline bars  !! LOW
    falling_tunnel              covers 21.3% of baseline bars  !! LOW
    volatility_velocity         covers 55.1% of baseline bars
    squeeze_snap                covers 2.2% of baseline bars  !! LOW
    lower_expansion             covers 49.7% of baseline bars
    keltner_squeeze_release     covers 43.8% of baseline bars

  XRPUSDT
                          wr_%     pf   dur  n_trades
population                                           
kde_upper_baseline       51.86  1.616  22.3      5195
momentum_close           52.90  1.684  46.3       397
falling_tunnel           50.17  1.510  20.6      1166
volatility_velocity      53.51  1.726  24.9      2852
squeeze_snap             57.00  1.988  19.4       100
lower_expansion          52.84  1.680  26.9      2557
keltner_squeeze_release  47.43  1.353  25.5      1923

    momentum_close              covers 7.6% of baseline bars  !! LOW
    falling_tunnel              covers 22.4% of baseline bars  !! LOW
    volatility_velocity         covers 54.9% of baseline bars
    squeeze_snap                covers 1.9% of baseline bars  !! LOW
    lower_expansion             covers 49.2% of baseline bars
    keltner_squeeze_release     covers 37.0% of baseline bars


-- Setup 2 Trigger 5 (1h) -- Verdict --

  Baseline (kde_upper_baseline on 1h):  avg WR 50.7%  avg PF 1.551
  KDE (4h): window=200  bw=1  |  BB(20,2std)  KC(20,2atr)

  [Volatility  ]  momentum_close              WR lift +4.4pp  avg PF 1.862  PF lift +0.311  3/5 pairs  [OK]  warn: WR 3p, low# 5p
    BTCUSDT     WR 58.0%  PF 2.069  lift +0.697 / req 0.10  n=433  cov 8%!  [OK]
    ETHUSDT     WR 59.8%  PF 2.231  lift +0.486 / req 0.10  n=500  cov 10%!  [OK]
    SOLUSDT     WR 53.1%  PF 1.695  lift +0.259 / req 0.10  n=426  WR!  cov 8%!  [OK]
    BNBUSDT     WR 52.1%  PF 1.630  lift +0.046 / req 0.10  n=336  WR!  cov 8%!  [--]
    XRPUSDT     WR 52.9%  PF 1.684  lift +0.069 / req 0.10  n=397  WR!  cov 8%!  [--]
  [Volatility  ]  falling_tunnel              WR lift +3.0pp  avg PF 1.763  PF lift +0.213  4/5 pairs  [OK]  warn: WR 3p, low# 5p
    BTCUSDT     WR 50.6%  PF 1.534  lift +0.163 / req 0.10  n=1,062  WR!  cov 20%!  [OK]
    ETHUSDT     WR 59.9%  PF 2.241  lift +0.496 / req 0.10  n=1,090  cov 21%!  [OK]
    SOLUSDT     WR 52.5%  PF 1.660  lift +0.223 / req 0.10  n=1,148  WR!  cov 21%!  [OK]
    BNBUSDT     WR 55.5%  PF 1.870  lift +0.286 / req 0.10  n=928  cov 21%!  [OK]
    XRPUSDT     WR 50.2%  PF 1.510  lift -0.105 / req 0.10  n=1,166  WR!  cov 22%!  [--]
  [Volatility  ]  volatility_velocity         WR lift +0.3pp  avg PF 1.571  PF lift +0.020  1/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 48.0%  PF 1.387  lift +0.016 / req 0.10  n=2,864  WR!  cov 54%  [--]
    ETHUSDT     WR 54.3%  PF 1.779  lift +0.033 / req 0.10  n=2,879  WR!  cov 55%  [--]
    SOLUSDT     WR 48.7%  PF 1.426  lift -0.010 / req 0.10  n=2,930  WR!  cov 54%  [--]
    BNBUSDT     WR 50.6%  PF 1.537  lift -0.047 / req 0.10  n=2,405  WR!  cov 55%  [--]
    XRPUSDT     WR 53.5%  PF 1.726  lift +0.110 / req 0.10  n=2,852  WR!  cov 55%  [OK]
  [Volatility  ]  squeeze_snap                WR lift +3.9pp  avg PF 1.893  PF lift +0.342  3/5 pairs  [OK]  warn: WR 5p, low# 5p
    BTCUSDT     WR 46.5%  PF 1.302  lift -0.070 / req 0.10  n=99  WR!  cov 2%!  [--]
    ETHUSDT     WR 66.2%  PF 2.942  lift +1.197 / req 0.10  n=77  WR!  cov 1%!  [OK]
    SOLUSDT     WR 54.5%  PF 1.793  lift +0.357 / req 0.10  n=101  WR!  cov 2%!  [OK]
    BNBUSDT     WR 48.9%  PF 1.438  lift -0.147 / req 0.10  n=94  WR!  cov 2%!  [--]
    XRPUSDT     WR 57.0%  PF 1.988  lift +0.373 / req 0.10  n=100  WR!  cov 2%!  [OK]
  [Volatility  ]  lower_expansion             WR lift +2.0pp  avg PF 1.678  PF lift +0.127  3/5 pairs  [OK]  warn: WR 3p
    BTCUSDT     WR 50.6%  PF 1.538  lift +0.167 / req 0.10  n=2,552  cov 48%  [OK]
    ETHUSDT     WR 56.8%  PF 1.975  lift +0.229 / req 0.10  n=2,618  cov 50%  [OK]
    SOLUSDT     WR 51.3%  PF 1.577  lift +0.141 / req 0.10  n=2,630  WR!  cov 48%  [OK]
    BNBUSDT     WR 51.9%  PF 1.618  lift +0.034 / req 0.10  n=2,170  WR!  cov 50%  [--]
    XRPUSDT     WR 52.8%  PF 1.680  lift +0.065 / req 0.10  n=2,557  WR!  cov 49%  [--]
  [Volatility  ]  keltner_squeeze_release     WR lift -1.6pp  avg PF 1.454  PF lift -0.097  0/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 48.9%  PF 1.436  lift +0.065 / req 0.10  n=2,212  WR!  cov 42%  [--]
    ETHUSDT     WR 53.8%  PF 1.744  lift -0.002 / req 0.10  n=2,357  WR!  cov 45%  [--]
    SOLUSDT     WR 49.1%  PF 1.445  lift +0.008 / req 0.10  n=2,495  WR!  cov 46%  [--]
    BNBUSDT     WR 46.3%  PF 1.293  lift -0.291 / req 0.10  n=1,912  WR!  cov 44%  [--]
    XRPUSDT     WR 47.4%  PF 1.353  lift -0.263 / req 0.10  n=1,923  WR!  cov 37%  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 5 (1h) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.551  |  Best: squeeze_snap  (avg PF 1.893)

  Warnings (results valid -- interpret with care):
    !! [momentum_close] WR lift below threshold on: SOLUSDT, BNBUSDT, XRPUSDT
    !! [momentum_close] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [falling_tunnel] WR lift below threshold on: BTCUSDT, SOLUSDT, XRPUSDT
    !! [falling_tunnel] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [volatility_velocity] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [squeeze_snap] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [squeeze_snap] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [lower_expansion] WR lift below threshold on: SOLUSDT, BNBUSDT, XRPUSDT
    !! [keltner_squeeze_release] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Volatility]
      [OK] falling_tunnel              avg PF 1.763
      [OK] lower_expansion             avg PF 1.678
      [OK] momentum_close              avg PF 1.862
      [OK] squeeze_snap                avg PF 1.893
      [--] keltner_squeeze_release
      [--] volatility_velocity

  Proceed using confirmed BB/KC signal(s) for setup 3 construction.
```
