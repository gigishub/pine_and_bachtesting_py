# Bear Strategy -- Setup 2 Trigger 6  (entry_tf=4h  kde_tf=4h)

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
| `macd_fast` | `12` |
| `macd_slow` | `26` |
| `macd_signal` | `9` |
| `histogram_lookback` | `20` |
| `cross_velocity_slope_threshold` | `0.05` |
| `zero_line_margin` | `0.01` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 4h) --

  BTCUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    46.74  1.316  18.2      1318
zero_line_rejection     NaN    NaN   NaN         0
histogram_peak_roll   41.42  1.060  15.1       367
rapid_separation      52.31  1.645  23.3       390
signal_line_wall      50.00  1.500  20.7       238
histogram_twin_peaks  40.79  1.033  14.3        76
cross_velocity        46.88  1.324  18.2        64

    zero_line_rejection         covers 0.0% of baseline bars  !! LOW
    histogram_peak_roll         covers 27.8% of baseline bars  !! LOW
    rapid_separation            covers 29.6% of baseline bars  !! LOW
    signal_line_wall            covers 18.1% of baseline bars  !! LOW
    histogram_twin_peaks        covers 5.8% of baseline bars  !! LOW
    cross_velocity              covers 4.9% of baseline bars  !! LOW

  ETHUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    48.63  1.420  22.0      1314
zero_line_rejection     NaN    NaN   NaN         0
histogram_peak_roll   45.28  1.241  17.0       413
rapid_separation      52.42  1.652  28.7       414
signal_line_wall      43.43  1.152  44.2       198
histogram_twin_peaks  55.45  1.867  13.9       110
cross_velocity        51.25  1.577  17.9        80

    zero_line_rejection         covers 0.0% of baseline bars  !! LOW
    histogram_peak_roll         covers 31.4% of baseline bars
    rapid_separation            covers 31.5% of baseline bars
    signal_line_wall            covers 15.1% of baseline bars  !! LOW
    histogram_twin_peaks        covers 8.4% of baseline bars  !! LOW
    cross_velocity              covers 6.1% of baseline bars  !! LOW

  SOLUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    47.02  1.331  19.9      1359
zero_line_rejection     NaN    NaN   NaN         0
histogram_peak_roll   47.23  1.342  18.6       451
rapid_separation      51.04  1.564  20.5       384
signal_line_wall      45.13  1.234  19.5       226
histogram_twin_peaks  39.20  0.967  17.7       125
cross_velocity        43.40  1.150  21.2        53

    zero_line_rejection         covers 0.0% of baseline bars  !! LOW
    histogram_peak_roll         covers 33.2% of baseline bars
    rapid_separation            covers 28.3% of baseline bars  !! LOW
    signal_line_wall            covers 16.6% of baseline bars  !! LOW
    histogram_twin_peaks        covers 9.2% of baseline bars  !! LOW
    cross_velocity              covers 3.9% of baseline bars  !! LOW

  BNBUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    50.18  1.511  19.2      1082
zero_line_rejection     NaN    NaN   NaN         0
histogram_peak_roll   47.91  1.379  15.3       382
rapid_separation      49.19  1.452  25.6       307
signal_line_wall      47.83  1.375  31.0       161
histogram_twin_peaks  53.27  1.710  13.2       107
cross_velocity        53.57  1.731  22.4        56

    zero_line_rejection         covers 0.0% of baseline bars  !! LOW
    histogram_peak_roll         covers 35.3% of baseline bars
    rapid_separation            covers 28.4% of baseline bars  !! LOW
    signal_line_wall            covers 14.9% of baseline bars  !! LOW
    histogram_twin_peaks        covers 9.9% of baseline bars  !! LOW
    cross_velocity              covers 5.2% of baseline bars  !! LOW

  XRPUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    52.78  1.677  18.6      1294
zero_line_rejection   60.56  2.303  20.0       180
histogram_peak_roll   50.80  1.549  17.8       376
rapid_separation      52.90  1.684  21.5       397
signal_line_wall      60.63  2.310  20.1       254
histogram_twin_peaks  43.43  1.152  17.8        99
cross_velocity          NaN    NaN   NaN         0

    zero_line_rejection         covers 13.9% of baseline bars  !! LOW
    histogram_peak_roll         covers 29.1% of baseline bars  !! LOW
    rapid_separation            covers 30.7% of baseline bars
    signal_line_wall            covers 19.6% of baseline bars  !! LOW
    histogram_twin_peaks        covers 7.7% of baseline bars  !! LOW
    cross_velocity              covers 0.0% of baseline bars  !! LOW


-- Setup 2 Trigger 6 (4h) -- Verdict --

  Baseline (kde_upper_baseline on 4h):  avg WR 49.1%  avg PF 1.451
  KDE (4h): window=200  bw=1  |  MACD(12,26,9)

  [Reversal  ]  zero_line_rejection         WR lift +7.8pp  avg PF 2.303  PF lift +0.626  1/5 pairs  [XX]  warn: WR 1p, low# 5p
    BTCUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0%!  [--]
    ETHUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0%!  [--]
    SOLUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0%!  [--]
    BNBUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0%!  [--]
    XRPUSDT     WR 60.6%  PF 2.303  lift +0.626 / req 0.10  n=180  WR!  cov 14%!  [OK]
  [Exhaustion]  histogram_peak_roll         WR lift -2.5pp  avg PF 1.314  PF lift -0.137  0/5 pairs  [XX]  warn: WR 5p, low# 2p
    BTCUSDT     WR 41.4%  PF 1.060  lift -0.256 / req 0.10  n=367  WR!  cov 28%!  [--]
    ETHUSDT     WR 45.3%  PF 1.241  lift -0.179 / req 0.10  n=413  WR!  cov 31%  [--]
    SOLUSDT     WR 47.2%  PF 1.342  lift +0.011 / req 0.10  n=451  WR!  cov 33%  [--]
    BNBUSDT     WR 47.9%  PF 1.379  lift -0.132 / req 0.10  n=382  WR!  cov 35%  [--]
    XRPUSDT     WR 50.8%  PF 1.549  lift -0.128 / req 0.10  n=376  WR!  cov 29%!  [--]
  [Momentum  ]  rapid_separation            WR lift +2.5pp  avg PF 1.600  PF lift +0.148  3/5 pairs  [OK]  warn: WR 5p, low# 3p
    BTCUSDT     WR 52.3%  PF 1.645  lift +0.329 / req 0.10  n=390  WR!  cov 30%!  [OK]
    ETHUSDT     WR 52.4%  PF 1.652  lift +0.232 / req 0.10  n=414  WR!  cov 32%  [OK]
    SOLUSDT     WR 51.0%  PF 1.564  lift +0.233 / req 0.10  n=384  WR!  cov 28%!  [OK]
    BNBUSDT     WR 49.2%  PF 1.452  lift -0.059 / req 0.10  n=307  WR!  cov 28%!  [--]
    XRPUSDT     WR 52.9%  PF 1.684  lift +0.008 / req 0.10  n=397  WR!  cov 31%  [--]
  [Regime    ]  signal_line_wall            WR lift +0.3pp  avg PF 1.514  PF lift +0.063  2/5 pairs  [XX]  warn: WR 4p, low# 5p
    BTCUSDT     WR 50.0%  PF 1.500  lift +0.184 / req 0.10  n=238  WR!  cov 18%!  [OK]
    ETHUSDT     WR 43.4%  PF 1.152  lift -0.268 / req 0.10  n=198  WR!  cov 15%!  [--]
    SOLUSDT     WR 45.1%  PF 1.234  lift -0.097 / req 0.10  n=226  WR!  cov 17%!  [--]
    BNBUSDT     WR 47.8%  PF 1.375  lift -0.136 / req 0.10  n=161  WR!  cov 15%!  [--]
    XRPUSDT     WR 60.6%  PF 2.310  lift +0.633 / req 0.10  n=254  cov 20%!  [OK]
  [Divergence]  histogram_twin_peaks        WR lift -2.6pp  avg PF 1.346  PF lift -0.105  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 40.8%  PF 1.033  lift -0.283 / req 0.10  n=76  WR!  cov 6%!  [--]
    ETHUSDT     WR 55.5%  PF 1.867  lift +0.447 / req 0.10  n=110  WR!  cov 8%!  [OK]
    SOLUSDT     WR 39.2%  PF 0.967  lift -0.364 / req 0.10  n=125  WR!  cov 9%!  [--]
    BNBUSDT     WR 53.3%  PF 1.710  lift +0.199 / req 0.10  n=107  WR!  cov 10%!  [OK]
    XRPUSDT     WR 43.4%  PF 1.152  lift -0.525 / req 0.10  n=99  WR!  cov 8%!  [--]
  [Reversal  ]  cross_velocity              WR lift +0.6pp  avg PF 1.445  PF lift +0.051  2/5 pairs  [XX]  warn: WR 4p, low# 5p
    BTCUSDT     WR 46.9%  PF 1.324  lift +0.007 / req 0.10  n=64  WR!  cov 5%!  [--]
    ETHUSDT     WR 51.2%  PF 1.577  lift +0.157 / req 0.10  n=80  WR!  cov 6%!  [OK]
    SOLUSDT     WR 43.4%  PF 1.150  lift -0.181 / req 0.10  n=53  WR!  cov 4%!  [--]
    BNBUSDT     WR 53.6%  PF 1.731  lift +0.220 / req 0.10  n=56  WR!  cov 5%!  [OK]
    XRPUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0%!  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 6 (4h) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.451  |  Best: rapid_separation  (avg PF 1.600)

  Warnings (results valid -- interpret with care):
    !! [zero_line_rejection] WR lift below threshold on: XRPUSDT
    !! [zero_line_rejection] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [histogram_peak_roll] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [histogram_peak_roll] low trade count (<30% baseline) on: BTCUSDT, XRPUSDT
    !! [rapid_separation] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rapid_separation] low trade count (<30% baseline) on: BTCUSDT, SOLUSDT, BNBUSDT
    !! [signal_line_wall] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT
    !! [signal_line_wall] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [histogram_twin_peaks] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
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
      [OK] rapid_separation            avg PF 1.600
    [Regime]
      [--] signal_line_wall
    [Divergence]
      [--] histogram_twin_peaks

  Proceed using confirmed MACD signal(s) for setup 3 construction.
```
