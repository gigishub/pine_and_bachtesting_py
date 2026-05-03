# Bear Strategy -- Setup 2 Trigger 6  (entry_tf=15m  kde_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `15m` |
| `kde_tf` | `4h` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `kde_window` | `200` |
| `kde_bandwidth_mult` | `1.0` |
| `macd_fast` | `12` |
| `macd_slow` | `26` |
| `macd_signal` | `9` |
| `histogram_lookback` | `20` |
| `cross_velocity_slope_threshold` | `0.05` |
| `zero_line_margin` | `0.01` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 15m) --

  BTCUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    45.41  1.248  22.7     21088
zero_line_rejection     NaN    NaN   NaN         0
histogram_peak_roll   44.07  1.182  19.9      4320
rapid_separation      45.71  1.263  25.1      5797
signal_line_wall      45.41  1.248  29.7      5941
histogram_twin_peaks  49.61  1.477  20.1      1024
cross_velocity        45.05  1.230  23.9       788

    zero_line_rejection         covers 0.0% of baseline bars  !! LOW
    histogram_peak_roll         covers 20.5% of baseline bars  !! LOW
    rapid_separation            covers 27.5% of baseline bars  !! LOW
    signal_line_wall            covers 28.2% of baseline bars  !! LOW
    histogram_twin_peaks        covers 4.9% of baseline bars  !! LOW
    cross_velocity              covers 3.7% of baseline bars  !! LOW

  ETHUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    49.83  1.490  20.8     21024
zero_line_rejection     NaN    NaN   NaN         0
histogram_peak_roll   48.11  1.390  17.3      4170
rapid_separation      50.69  1.542  22.4      5806
signal_line_wall      52.02  1.626  26.7      6382
histogram_twin_peaks  52.33  1.647  16.1       965
cross_velocity        50.51  1.531  21.4       788

    zero_line_rejection         covers 0.0% of baseline bars  !! LOW
    histogram_peak_roll         covers 19.8% of baseline bars  !! LOW
    rapid_separation            covers 27.6% of baseline bars  !! LOW
    signal_line_wall            covers 30.4% of baseline bars
    histogram_twin_peaks        covers 4.6% of baseline bars  !! LOW
    cross_velocity              covers 3.7% of baseline bars  !! LOW

  SOLUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    46.71  1.315  20.6     21965
zero_line_rejection   48.28  1.400  11.5        87
histogram_peak_roll   47.35  1.349  18.9      4448
rapid_separation      45.06  1.230  21.7      6056
signal_line_wall      46.38  1.297  25.3      6462
histogram_twin_peaks  43.68  1.163  17.5      1092
cross_velocity        53.44  1.722  24.3       247

    zero_line_rejection         covers 0.4% of baseline bars  !! LOW
    histogram_peak_roll         covers 20.3% of baseline bars  !! LOW
    rapid_separation            covers 27.6% of baseline bars  !! LOW
    signal_line_wall            covers 29.4% of baseline bars  !! LOW
    histogram_twin_peaks        covers 5.0% of baseline bars  !! LOW
    cross_velocity              covers 1.1% of baseline bars  !! LOW

  BNBUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    47.65  1.365  20.3     17502
zero_line_rejection    0.00  0.000  40.8         5
histogram_peak_roll   46.87  1.323  17.4      3527
rapid_separation      47.59  1.362  23.3      4875
signal_line_wall      47.87  1.377  26.5      5200
histogram_twin_peaks  43.57  1.158  14.5       948
cross_velocity        47.85  1.376  31.7       489

    zero_line_rejection         covers 0.0% of baseline bars  !! LOW
    histogram_peak_roll         covers 20.2% of baseline bars  !! LOW
    rapid_separation            covers 27.9% of baseline bars  !! LOW
    signal_line_wall            covers 29.7% of baseline bars  !! LOW
    histogram_twin_peaks        covers 5.4% of baseline bars  !! LOW
    cross_velocity              covers 2.8% of baseline bars  !! LOW

  XRPUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    48.07  1.389  22.4     20784
zero_line_rejection   44.92  1.223  23.5      5309
histogram_peak_roll   48.56  1.416  18.5      4452
rapid_separation      48.31  1.402  24.9      5618
signal_line_wall      46.81  1.320  29.7      6264
histogram_twin_peaks  51.16  1.571  21.4       995
cross_velocity          NaN    NaN   NaN         0

    zero_line_rejection         covers 25.5% of baseline bars  !! LOW
    histogram_peak_roll         covers 21.4% of baseline bars  !! LOW
    rapid_separation            covers 27.0% of baseline bars  !! LOW
    signal_line_wall            covers 30.1% of baseline bars
    histogram_twin_peaks        covers 4.8% of baseline bars  !! LOW
    cross_velocity              covers 0.0% of baseline bars  !! LOW


-- Setup 2 Trigger 6 (15m) -- Verdict --

  Baseline (kde_upper_baseline on 15m):  avg WR 47.5%  avg PF 1.361
  KDE (4h): window=200  bw=1  |  MACD(12,26,9)

  [Reversal  ]  zero_line_rejection         WR lift -16.4pp  avg PF 0.874  PF lift -0.482  0/5 pairs  [XX]  warn: WR 3p, low# 5p
    BTCUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0%!  [--]
    ETHUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0%!  [--]
    SOLUSDT     WR 48.3%  PF 1.400  lift +0.085 / req 0.10  n=87  WR!  cov 0%!  [--]
    BNBUSDT     WR 0.0%  PF 0.000  lift -1.365 / req 0.10  n=5  WR!  cov 0%!  [--]
    XRPUSDT     WR 44.9%  PF 1.223  lift -0.165 / req 0.10  n=5,309  WR!  cov 26%!  [--]
  [Exhaustion]  histogram_peak_roll         WR lift -0.5pp  avg PF 1.332  PF lift -0.029  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 44.1%  PF 1.182  lift -0.066 / req 0.10  n=4,320  WR!  cov 20%!  [--]
    ETHUSDT     WR 48.1%  PF 1.390  lift -0.100 / req 0.10  n=4,170  WR!  cov 20%!  [--]
    SOLUSDT     WR 47.3%  PF 1.349  lift +0.034 / req 0.10  n=4,448  WR!  cov 20%!  [--]
    BNBUSDT     WR 46.9%  PF 1.323  lift -0.042 / req 0.10  n=3,527  WR!  cov 20%!  [--]
    XRPUSDT     WR 48.6%  PF 1.416  lift +0.028 / req 0.10  n=4,452  WR!  cov 21%!  [--]
  [Momentum  ]  rapid_separation            WR lift -0.1pp  avg PF 1.360  PF lift -0.002  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 45.7%  PF 1.263  lift +0.015 / req 0.10  n=5,797  WR!  cov 27%!  [--]
    ETHUSDT     WR 50.7%  PF 1.542  lift +0.052 / req 0.10  n=5,806  WR!  cov 28%!  [--]
    SOLUSDT     WR 45.1%  PF 1.230  lift -0.084 / req 0.10  n=6,056  WR!  cov 28%!  [--]
    BNBUSDT     WR 47.6%  PF 1.362  lift -0.003 / req 0.10  n=4,875  WR!  cov 28%!  [--]
    XRPUSDT     WR 48.3%  PF 1.402  lift +0.013 / req 0.10  n=5,618  WR!  cov 27%!  [--]
  [Regime    ]  signal_line_wall            WR lift +0.2pp  avg PF 1.374  PF lift +0.012  1/5 pairs  [XX]  warn: WR 4p, low# 3p
    BTCUSDT     WR 45.4%  PF 1.248  lift -0.000 / req 0.10  n=5,941  WR!  cov 28%!  [--]
    ETHUSDT     WR 52.0%  PF 1.626  lift +0.136 / req 0.10  n=6,382  cov 30%  [OK]
    SOLUSDT     WR 46.4%  PF 1.297  lift -0.017 / req 0.10  n=6,462  WR!  cov 29%!  [--]
    BNBUSDT     WR 47.9%  PF 1.377  lift +0.012 / req 0.10  n=5,200  WR!  cov 30%!  [--]
    XRPUSDT     WR 46.8%  PF 1.320  lift -0.069 / req 0.10  n=6,264  WR!  cov 30%  [--]
  [Divergence]  histogram_twin_peaks        WR lift +0.5pp  avg PF 1.403  PF lift +0.042  3/5 pairs  [OK]  warn: WR 4p, low# 5p
    BTCUSDT     WR 49.6%  PF 1.477  lift +0.229 / req 0.10  n=1,024  cov 5%!  [OK]
    ETHUSDT     WR 52.3%  PF 1.647  lift +0.157 / req 0.10  n=965  WR!  cov 5%!  [OK]
    SOLUSDT     WR 43.7%  PF 1.163  lift -0.151 / req 0.10  n=1,092  WR!  cov 5%!  [--]
    BNBUSDT     WR 43.6%  PF 1.158  lift -0.207 / req 0.10  n=948  WR!  cov 5%!  [--]
    XRPUSDT     WR 51.2%  PF 1.571  lift +0.182 / req 0.10  n=995  WR!  cov 5%!  [OK]
  [Reversal  ]  cross_velocity              WR lift +1.8pp  avg PF 1.465  PF lift +0.110  1/5 pairs  [XX]  warn: WR 4p, low# 5p
    BTCUSDT     WR 45.1%  PF 1.230  lift -0.018 / req 0.10  n=788  WR!  cov 4%!  [--]
    ETHUSDT     WR 50.5%  PF 1.531  lift +0.041 / req 0.10  n=788  WR!  cov 4%!  [--]
    SOLUSDT     WR 53.4%  PF 1.722  lift +0.407 / req 0.10  n=247  WR!  cov 1%!  [OK]
    BNBUSDT     WR 47.9%  PF 1.376  lift +0.011 / req 0.10  n=489  WR!  cov 3%!  [--]
    XRPUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0%!  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 6 (15m) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.361  |  Best: histogram_twin_peaks  (avg PF 1.403)

  Warnings (results valid -- interpret with care):
    !! [zero_line_rejection] WR lift below threshold on: SOLUSDT, BNBUSDT, XRPUSDT
    !! [zero_line_rejection] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [histogram_peak_roll] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [histogram_peak_roll] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rapid_separation] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rapid_separation] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [signal_line_wall] WR lift below threshold on: BTCUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [signal_line_wall] low trade count (<30% baseline) on: BTCUSDT, SOLUSDT, BNBUSDT
    !! [histogram_twin_peaks] WR lift below threshold on: ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [histogram_twin_peaks] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [cross_velocity] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT
    !! [cross_velocity] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Reversal]
      [--] cross_velocity
      [--] zero_line_rejection
    [Exhaustion]
      [--] histogram_peak_roll
    [Momentum]
      [--] rapid_separation
    [Regime]
      [--] signal_line_wall
    [Divergence]
      [OK] histogram_twin_peaks        avg PF 1.403

  Proceed using confirmed MACD signal(s) for setup 3 construction.
```
