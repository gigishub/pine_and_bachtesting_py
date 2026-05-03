# Bear Strategy -- Setup 2 Candle Trigger: KDE Upper (4h) + 15m bar quality  (entry_tf=15m  kde_tf=4h)

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
| `rvol_window` | `96` |
| `rvol_threshold` | `1.0` |
| `wick_ratio_threshold` | `0.5` |
| `breakdown_close_pct` | `0.25` |
| `roc_period` | `3` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 15m) --

  BTCUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    45.41  1.248  22.7     21088
bearish_rvol          48.51  1.413  35.0      3422
upper_wick_rejection  43.94  1.176  21.4      3143
breakdown_bar         44.94  1.224  21.7      5492
roc_negative          45.23  1.238  23.3     10828
bearish_engulf        44.18  1.187  22.2      2775

    bearish_rvol            covers 16.2% of baseline bars  !! LOW
    upper_wick_rejection    covers 14.9% of baseline bars  !! LOW
    breakdown_bar           covers 26.0% of baseline bars  !! LOW
    roc_negative            covers 51.3% of baseline bars
    bearish_engulf          covers 13.2% of baseline bars  !! LOW

  ETHUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    49.83  1.490  20.8     21024
bearish_rvol          51.67  1.604  29.9      3559
upper_wick_rejection  47.88  1.378  18.9      3114
breakdown_bar         50.17  1.510  20.1      5141
roc_negative          50.71  1.544  21.2     11050
bearish_engulf        49.80  1.488  19.2      2697

    bearish_rvol            covers 16.9% of baseline bars  !! LOW
    upper_wick_rejection    covers 14.8% of baseline bars  !! LOW
    breakdown_bar           covers 24.5% of baseline bars  !! LOW
    roc_negative            covers 52.6% of baseline bars
    bearish_engulf          covers 12.8% of baseline bars  !! LOW

  SOLUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    46.71  1.315  20.6     21965
bearish_rvol          49.31  1.459  29.3      3691
upper_wick_rejection  46.12  1.284  19.4      3194
breakdown_bar         46.69  1.314  20.8      5519
roc_negative          46.31  1.294  21.5     11401
bearish_engulf        45.65  1.260  20.2      2771

    bearish_rvol            covers 16.8% of baseline bars  !! LOW
    upper_wick_rejection    covers 14.5% of baseline bars  !! LOW
    breakdown_bar           covers 25.1% of baseline bars  !! LOW
    roc_negative            covers 51.9% of baseline bars
    bearish_engulf          covers 12.6% of baseline bars  !! LOW

  BNBUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    47.65  1.365  20.3     17502
bearish_rvol          47.08  1.334  32.1      2774
upper_wick_rejection  46.31  1.294  18.6      2410
breakdown_bar         47.54  1.359  19.9      4535
roc_negative          47.08  1.334  21.9      8917
bearish_engulf        46.89  1.324  21.0      2269

    bearish_rvol            covers 15.8% of baseline bars  !! LOW
    upper_wick_rejection    covers 13.8% of baseline bars  !! LOW
    breakdown_bar           covers 25.9% of baseline bars  !! LOW
    roc_negative            covers 50.9% of baseline bars
    bearish_engulf          covers 13.0% of baseline bars  !! LOW

  XRPUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    48.07  1.389  22.4     20784
bearish_rvol          49.26  1.456  31.5      3374
upper_wick_rejection  48.22  1.397  18.7      3007
breakdown_bar         46.19  1.288  20.5      5111
roc_negative          47.25  1.344  23.4     10573
bearish_engulf        47.48  1.356  21.4      2660

    bearish_rvol            covers 16.2% of baseline bars  !! LOW
    upper_wick_rejection    covers 14.5% of baseline bars  !! LOW
    breakdown_bar           covers 24.6% of baseline bars  !! LOW
    roc_negative            covers 50.9% of baseline bars
    bearish_engulf          covers 12.8% of baseline bars  !! LOW


-- Setup 2 Candle Trigger (15m) -- Verdict --

  Baseline (kde_upper_baseline on 15m):  avg WR 47.5%  avg PF 1.361
  KDE (4h): window=200  bw=1  |  RVOL: 96 bars (24h) threshold=1  |  wick=0.5  breakdown=0.25  roc=3bars

  [Bar quality  ]  bearish_rvol            WR lift +1.6pp  avg PF 1.453  PF lift +0.092  3/5 pairs  [OK]  warn: WR 3p, low# 5p
    BTCUSDT     WR 48.5%  PF 1.413  lift +0.165 / req 0.10  n=3,422  cov 16%!  [OK]
    ETHUSDT     WR 51.7%  PF 1.604  lift +0.114 / req 0.10  n=3,559  WR!  cov 17%!  [OK]
    SOLUSDT     WR 49.3%  PF 1.459  lift +0.144 / req 0.10  n=3,691  cov 17%!  [OK]
    BNBUSDT     WR 47.1%  PF 1.334  lift -0.031 / req 0.10  n=2,774  WR!  cov 16%!  [--]
    XRPUSDT     WR 49.3%  PF 1.456  lift +0.068 / req 0.10  n=3,374  WR!  cov 16%!  [--]
  [Bar quality  ]  upper_wick_rejection    WR lift -1.0pp  avg PF 1.306  PF lift -0.056  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 43.9%  PF 1.176  lift -0.072 / req 0.10  n=3,143  WR!  cov 15%!  [--]
    ETHUSDT     WR 47.9%  PF 1.378  lift -0.112 / req 0.10  n=3,114  WR!  cov 15%!  [--]
    SOLUSDT     WR 46.1%  PF 1.284  lift -0.031 / req 0.10  n=3,194  WR!  cov 15%!  [--]
    BNBUSDT     WR 46.3%  PF 1.294  lift -0.072 / req 0.10  n=2,410  WR!  cov 14%!  [--]
    XRPUSDT     WR 48.2%  PF 1.397  lift +0.008 / req 0.10  n=3,007  WR!  cov 14%!  [--]
  [Bar quality  ]  breakdown_bar           WR lift -0.4pp  avg PF 1.339  PF lift -0.022  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 44.9%  PF 1.224  lift -0.024 / req 0.10  n=5,492  WR!  cov 26%!  [--]
    ETHUSDT     WR 50.2%  PF 1.510  lift +0.020 / req 0.10  n=5,141  WR!  cov 24%!  [--]
    SOLUSDT     WR 46.7%  PF 1.314  lift -0.001 / req 0.10  n=5,519  WR!  cov 25%!  [--]
    BNBUSDT     WR 47.5%  PF 1.359  lift -0.006 / req 0.10  n=4,535  WR!  cov 26%!  [--]
    XRPUSDT     WR 46.2%  PF 1.288  lift -0.101 / req 0.10  n=5,111  WR!  cov 25%!  [--]
  [Momentum     ]  roc_negative            WR lift -0.2pp  avg PF 1.351  PF lift -0.011  1/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 45.2%  PF 1.238  lift -0.009 / req 0.05  n=10,828  WR!  cov 51%  [--]
    ETHUSDT     WR 50.7%  PF 1.544  lift +0.053 / req 0.05  n=11,050  WR!  cov 53%  [OK]
    SOLUSDT     WR 46.3%  PF 1.294  lift -0.021 / req 0.05  n=11,401  WR!  cov 52%  [--]
    BNBUSDT     WR 47.1%  PF 1.334  lift -0.031 / req 0.10  n=8,917  WR!  cov 51%  [--]
    XRPUSDT     WR 47.3%  PF 1.344  lift -0.045 / req 0.05  n=10,573  WR!  cov 51%  [--]
  [Pattern      ]  bearish_engulf          WR lift -0.7pp  avg PF 1.323  PF lift -0.038  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 44.2%  PF 1.187  lift -0.061 / req 0.10  n=2,775  WR!  cov 13%!  [--]
    ETHUSDT     WR 49.8%  PF 1.488  lift -0.002 / req 0.10  n=2,697  WR!  cov 13%!  [--]
    SOLUSDT     WR 45.7%  PF 1.260  lift -0.055 / req 0.10  n=2,771  WR!  cov 13%!  [--]
    BNBUSDT     WR 46.9%  PF 1.324  lift -0.041 / req 0.10  n=2,269  WR!  cov 13%!  [--]
    XRPUSDT     WR 47.5%  PF 1.356  lift -0.032 / req 0.10  n=2,660  WR!  cov 13%!  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 CANDLE TRIGGER (15m) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.361  |  Best: bearish_rvol  (avg PF 1.453)

  Warnings (results valid -- interpret with care):
    !! [bearish_rvol] WR lift below threshold on: ETHUSDT, BNBUSDT, XRPUSDT
    !! [bearish_rvol] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [upper_wick_rejection] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [upper_wick_rejection] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [breakdown_bar] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [breakdown_bar] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [roc_negative] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [bearish_engulf] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [bearish_engulf] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Bar quality]
      [OK] bearish_rvol              avg PF 1.453
      [--] breakdown_bar
      [--] upper_wick_rejection
    [Momentum]
      [--] roc_negative
    [Pattern]
      [--] bearish_engulf

  Proceed using confirmed 15m candle trigger(s) for setup 3 construction.
```
