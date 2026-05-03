# Bear Strategy -- Setup 2 Trigger 6  (entry_tf=1h  kde_tf=4h)

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
| `macd_fast` | `12` |
| `macd_slow` | `26` |
| `macd_signal` | `9` |
| `histogram_lookback` | `20` |
| `cross_velocity_slope_threshold` | `0.05` |
| `zero_line_margin` | `0.01` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 1h) --

  BTCUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    47.76  1.371  20.9      5272
zero_line_rejection     NaN    NaN   NaN         0
histogram_peak_roll   45.36  1.245  17.8      1208
rapid_separation      48.22  1.397  25.0      1717
signal_line_wall      54.88  1.825  27.8      1301
histogram_twin_peaks  49.72  1.483  19.4       358
cross_velocity        43.53  1.156  20.5       255

    zero_line_rejection         covers 0.0% of baseline bars  !! LOW
    histogram_peak_roll         covers 22.9% of baseline bars  !! LOW
    rapid_separation            covers 32.6% of baseline bars
    signal_line_wall            covers 24.7% of baseline bars  !! LOW
    histogram_twin_peaks        covers 6.8% of baseline bars  !! LOW
    cross_velocity              covers 4.8% of baseline bars  !! LOW

  ETHUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    53.79  1.746  21.0      5256
zero_line_rejection     NaN    NaN   NaN         0
histogram_peak_roll   52.93  1.687  17.4      1143
rapid_separation      53.70  1.740  24.8      1849
signal_line_wall      60.75  2.321  31.5      1340
histogram_twin_peaks  44.97  1.226  17.7       358
cross_velocity        51.24  1.576  23.4       242

    zero_line_rejection         covers 0.0% of baseline bars  !! LOW
    histogram_peak_roll         covers 21.7% of baseline bars  !! LOW
    rapid_separation            covers 35.2% of baseline bars
    signal_line_wall            covers 25.5% of baseline bars  !! LOW
    histogram_twin_peaks        covers 6.8% of baseline bars  !! LOW
    cross_velocity              covers 4.6% of baseline bars  !! LOW

  SOLUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    48.91  1.436  18.8      5475
zero_line_rejection   33.33  0.750   7.7         6
histogram_peak_roll   45.82  1.268  16.6      1231
rapid_separation      47.68  1.367  22.1      1833
signal_line_wall      55.83  1.896  21.8      1347
histogram_twin_peaks  47.96  1.382  18.4       392
cross_velocity        49.03  1.443  22.7       155

    zero_line_rejection         covers 0.1% of baseline bars  !! LOW
    histogram_peak_roll         covers 22.5% of baseline bars  !! LOW
    rapid_separation            covers 33.5% of baseline bars
    signal_line_wall            covers 24.6% of baseline bars  !! LOW
    histogram_twin_peaks        covers 7.2% of baseline bars  !! LOW
    cross_velocity              covers 2.8% of baseline bars  !! LOW

  BNBUSDT
                        wr_%     pf   dur  n_trades
population                                         
kde_upper_baseline     51.36  1.584  21.1      4367
zero_line_rejection   100.00    inf   7.0         1
histogram_peak_roll    50.86  1.552  18.2       932
rapid_separation       50.13  1.508  25.0      1492
signal_line_wall       55.00  1.833  25.4      1080
histogram_twin_peaks   53.65  1.736  21.7       233
cross_velocity         52.22  1.640  21.1       180

    zero_line_rejection         covers 0.0% of baseline bars  !! LOW
    histogram_peak_roll         covers 21.3% of baseline bars  !! LOW
    rapid_separation            covers 34.2% of baseline bars
    signal_line_wall            covers 24.7% of baseline bars  !! LOW
    histogram_twin_peaks        covers 5.3% of baseline bars  !! LOW
    cross_velocity              covers 4.1% of baseline bars  !! LOW

  XRPUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    51.86  1.616  22.3      5195
zero_line_rejection   51.19  1.573  26.1      1176
histogram_peak_roll   49.60  1.476  19.5      1117
rapid_separation      53.13  1.700  26.2      1662
signal_line_wall      51.48  1.592  29.6      1484
histogram_twin_peaks  51.42  1.588  16.9       282
cross_velocity          NaN    NaN   NaN         0

    zero_line_rejection         covers 22.6% of baseline bars  !! LOW
    histogram_peak_roll         covers 21.5% of baseline bars  !! LOW
    rapid_separation            covers 32.0% of baseline bars
    signal_line_wall            covers 28.6% of baseline bars  !! LOW
    histogram_twin_peaks        covers 5.4% of baseline bars  !! LOW
    cross_velocity              covers 0.0% of baseline bars  !! LOW


-- Setup 2 Trigger 6 (1h) -- Verdict --

  Baseline (kde_upper_baseline on 1h):  avg WR 50.7%  avg PF 1.551
  KDE (4h): window=200  bw=1  |  MACD(12,26,9)

  [Reversal  ]  zero_line_rejection         WR lift +10.8pp  avg PF inf  PF lift +inf  1/5 pairs  [XX]  warn: WR 3p, low# 5p
    BTCUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0%!  [--]
    ETHUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0%!  [--]
    SOLUSDT     WR 33.3%  PF 0.750  lift -0.686 / req 0.10  n=6  WR!  cov 0%!  [--]
    BNBUSDT     WR 100.0%  PF inf  lift +inf / req 0.10  n=1  WR!  cov 0%!  [OK]
    XRPUSDT     WR 51.2%  PF 1.573  lift -0.043 / req 0.10  n=1,176  WR!  cov 23%!  [--]
  [Exhaustion]  histogram_peak_roll         WR lift -1.8pp  avg PF 1.446  PF lift -0.105  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 45.4%  PF 1.245  lift -0.126 / req 0.10  n=1,208  WR!  cov 23%!  [--]
    ETHUSDT     WR 52.9%  PF 1.687  lift -0.059 / req 0.10  n=1,143  WR!  cov 22%!  [--]
    SOLUSDT     WR 45.8%  PF 1.268  lift -0.168 / req 0.10  n=1,231  WR!  cov 22%!  [--]
    BNBUSDT     WR 50.9%  PF 1.552  lift -0.032 / req 0.10  n=932  WR!  cov 21%!  [--]
    XRPUSDT     WR 49.6%  PF 1.476  lift -0.140 / req 0.10  n=1,117  WR!  cov 22%!  [--]
  [Momentum  ]  rapid_separation            WR lift -0.2pp  avg PF 1.543  PF lift -0.008  0/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 48.2%  PF 1.397  lift +0.026 / req 0.10  n=1,717  WR!  cov 33%  [--]
    ETHUSDT     WR 53.7%  PF 1.740  lift -0.006 / req 0.10  n=1,849  WR!  cov 35%  [--]
    SOLUSDT     WR 47.7%  PF 1.367  lift -0.069 / req 0.10  n=1,833  WR!  cov 33%  [--]
    BNBUSDT     WR 50.1%  PF 1.508  lift -0.076 / req 0.10  n=1,492  WR!  cov 34%  [--]
    XRPUSDT     WR 53.1%  PF 1.700  lift +0.085 / req 0.10  n=1,662  WR!  cov 32%  [--]
  [Regime    ]  signal_line_wall            WR lift +4.9pp  avg PF 1.893  PF lift +0.343  4/5 pairs  [OK]  warn: WR 2p, low# 5p
    BTCUSDT     WR 54.9%  PF 1.825  lift +0.453 / req 0.10  n=1,301  cov 25%!  [OK]
    ETHUSDT     WR 60.7%  PF 2.321  lift +0.576 / req 0.10  n=1,340  cov 25%!  [OK]
    SOLUSDT     WR 55.8%  PF 1.896  lift +0.460 / req 0.10  n=1,347  cov 25%!  [OK]
    BNBUSDT     WR 55.0%  PF 1.833  lift +0.249 / req 0.10  n=1,080  WR!  cov 25%!  [OK]
    XRPUSDT     WR 51.5%  PF 1.592  lift -0.024 / req 0.10  n=1,484  WR!  cov 29%!  [--]
  [Divergence]  histogram_twin_peaks        WR lift -1.2pp  avg PF 1.483  PF lift -0.068  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 49.7%  PF 1.483  lift +0.112 / req 0.10  n=358  WR!  cov 7%!  [OK]
    ETHUSDT     WR 45.0%  PF 1.226  lift -0.520 / req 0.10  n=358  WR!  cov 7%!  [--]
    SOLUSDT     WR 48.0%  PF 1.382  lift -0.054 / req 0.10  n=392  WR!  cov 7%!  [--]
    BNBUSDT     WR 53.6%  PF 1.736  lift +0.152 / req 0.10  n=233  WR!  cov 5%!  [OK]
    XRPUSDT     WR 51.4%  PF 1.588  lift -0.028 / req 0.10  n=282  WR!  cov 5%!  [--]
  [Reversal  ]  cross_velocity              WR lift -1.5pp  avg PF 1.454  PF lift -0.081  0/5 pairs  [XX]  warn: WR 4p, low# 5p
    BTCUSDT     WR 43.5%  PF 1.156  lift -0.215 / req 0.10  n=255  WR!  cov 5%!  [--]
    ETHUSDT     WR 51.2%  PF 1.576  lift -0.170 / req 0.10  n=242  WR!  cov 5%!  [--]
    SOLUSDT     WR 49.0%  PF 1.443  lift +0.007 / req 0.10  n=155  WR!  cov 3%!  [--]
    BNBUSDT     WR 52.2%  PF 1.640  lift +0.055 / req 0.10  n=180  WR!  cov 4%!  [--]
    XRPUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0%!  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 6 (1h) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.551  |  Best: signal_line_wall  (avg PF 1.893)

  Warnings (results valid -- interpret with care):
    !! [zero_line_rejection] WR lift below threshold on: SOLUSDT, BNBUSDT, XRPUSDT
    !! [zero_line_rejection] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [histogram_peak_roll] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [histogram_peak_roll] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rapid_separation] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [signal_line_wall] WR lift below threshold on: BNBUSDT, XRPUSDT
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
      [--] rapid_separation
    [Regime]
      [OK] signal_line_wall            avg PF 1.893
    [Divergence]
      [--] histogram_twin_peaks

  Proceed using confirmed MACD signal(s) for setup 3 construction.
```
