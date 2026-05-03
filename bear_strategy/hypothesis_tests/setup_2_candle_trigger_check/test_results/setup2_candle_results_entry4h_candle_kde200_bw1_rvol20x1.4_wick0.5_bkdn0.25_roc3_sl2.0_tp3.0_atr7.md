# Bear Strategy -- Setup 2 Candle Trigger: KDE Upper (4h) + 4h bar quality  (entry_tf=4h  kde_tf=4h)

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
| `rvol_window` | `20` |
| `rvol_threshold` | `1.4` |
| `wick_ratio_threshold` | `0.5` |
| `breakdown_close_pct` | `0.25` |
| `roc_period` | `3` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 4h) --

  BTCUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    46.74  1.316  18.2      1318
bearish_rvol          49.23  1.455  27.2       195
upper_wick_rejection  50.24  1.514  15.9       211
breakdown_bar         46.58  1.308  17.5       307
roc_negative          47.51  1.358  19.9       722
bearish_engulf        49.45  1.467  17.0       182

    bearish_rvol            covers 14.8% of baseline bars  !! LOW
    upper_wick_rejection    covers 16.0% of baseline bars  !! LOW
    breakdown_bar           covers 23.3% of baseline bars  !! LOW
    roc_negative            covers 54.8% of baseline bars
    bearish_engulf          covers 13.8% of baseline bars  !! LOW

  ETHUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    48.63  1.420  22.0      1314
bearish_rvol          49.77  1.486  28.4       219
upper_wick_rejection  50.51  1.531  19.2       196
breakdown_bar         50.68  1.541  25.7       294
roc_negative          50.06  1.504  24.2       771
bearish_engulf        49.13  1.449  28.9       173

    bearish_rvol            covers 16.7% of baseline bars  !! LOW
    upper_wick_rejection    covers 14.9% of baseline bars  !! LOW
    breakdown_bar           covers 22.4% of baseline bars  !! LOW
    roc_negative            covers 58.7% of baseline bars
    bearish_engulf          covers 13.2% of baseline bars  !! LOW

  SOLUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    47.02  1.331  19.9      1359
bearish_rvol          51.18  1.572  22.0       170
upper_wick_rejection  45.18  1.236  19.4       197
breakdown_bar         46.05  1.280  19.8       367
roc_negative          47.14  1.338  20.7       770
bearish_engulf        49.71  1.483  18.5       175

    bearish_rvol            covers 12.5% of baseline bars  !! LOW
    upper_wick_rejection    covers 14.5% of baseline bars  !! LOW
    breakdown_bar           covers 27.0% of baseline bars  !! LOW
    roc_negative            covers 56.7% of baseline bars
    bearish_engulf          covers 12.9% of baseline bars  !! LOW

  BNBUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    50.18  1.511  19.2      1082
bearish_rvol          51.35  1.583  29.5       148
upper_wick_rejection  50.67  1.541  16.2       150
breakdown_bar         50.00  1.500  24.2       272
roc_negative          51.20  1.574  22.8       623
bearish_engulf        50.68  1.541  19.9       148

    bearish_rvol            covers 13.7% of baseline bars  !! LOW
    upper_wick_rejection    covers 13.9% of baseline bars  !! LOW
    breakdown_bar           covers 25.1% of baseline bars  !! LOW
    roc_negative            covers 57.6% of baseline bars
    bearish_engulf          covers 13.7% of baseline bars  !! LOW

  XRPUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    52.78  1.677  18.6      1294
bearish_rvol          52.41  1.652  29.8       145
upper_wick_rejection  52.31  1.645  15.9       195
breakdown_bar         54.08  1.767  20.3       294
roc_negative          55.12  1.842  20.4       733
bearish_engulf        62.43  2.493  14.5       181

    bearish_rvol            covers 11.2% of baseline bars  !! LOW
    upper_wick_rejection    covers 15.1% of baseline bars  !! LOW
    breakdown_bar           covers 22.7% of baseline bars  !! LOW
    roc_negative            covers 56.6% of baseline bars
    bearish_engulf          covers 14.0% of baseline bars  !! LOW


-- Setup 2 Candle Trigger (4h) -- Verdict --

  Baseline (kde_upper_baseline on 4h):  avg WR 49.1%  avg PF 1.451
  KDE (4h): window=200  bw=1  |  RVOL: 20 bars (5h) threshold=1.4  |  wick=0.5  breakdown=0.25  roc=3bars

  [Bar quality  ]  bearish_rvol            WR lift +1.7pp  avg PF 1.550  PF lift +0.099  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 49.2%  PF 1.455  lift +0.138 / req 0.10  n=195  WR!  cov 15%!  [OK]
    ETHUSDT     WR 49.8%  PF 1.486  lift +0.066 / req 0.10  n=219  WR!  cov 17%!  [--]
    SOLUSDT     WR 51.2%  PF 1.572  lift +0.241 / req 0.10  n=170  WR!  cov 13%!  [OK]
    BNBUSDT     WR 51.4%  PF 1.583  lift +0.072 / req 0.10  n=148  WR!  cov 14%!  [--]
    XRPUSDT     WR 52.4%  PF 1.652  lift -0.025 / req 0.10  n=145  WR!  cov 11%!  [--]
  [Bar quality  ]  upper_wick_rejection    WR lift +0.7pp  avg PF 1.493  PF lift +0.042  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 50.2%  PF 1.514  lift +0.198 / req 0.10  n=211  WR!  cov 16%!  [OK]
    ETHUSDT     WR 50.5%  PF 1.531  lift +0.111 / req 0.10  n=196  WR!  cov 15%!  [OK]
    SOLUSDT     WR 45.2%  PF 1.236  lift -0.095 / req 0.10  n=197  WR!  cov 14%!  [--]
    BNBUSDT     WR 50.7%  PF 1.541  lift +0.029 / req 0.10  n=150  WR!  cov 14%!  [--]
    XRPUSDT     WR 52.3%  PF 1.645  lift -0.032 / req 0.10  n=195  WR!  cov 15%!  [--]
  [Bar quality  ]  breakdown_bar           WR lift +0.4pp  avg PF 1.479  PF lift +0.028  1/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 46.6%  PF 1.308  lift -0.008 / req 0.10  n=307  WR!  cov 23%!  [--]
    ETHUSDT     WR 50.7%  PF 1.541  lift +0.121 / req 0.10  n=294  WR!  cov 22%!  [OK]
    SOLUSDT     WR 46.0%  PF 1.280  lift -0.051 / req 0.10  n=367  WR!  cov 27%!  [--]
    BNBUSDT     WR 50.0%  PF 1.500  lift -0.011 / req 0.10  n=272  WR!  cov 25%!  [--]
    XRPUSDT     WR 54.1%  PF 1.767  lift +0.090 / req 0.10  n=294  WR!  cov 23%!  [--]
  [Momentum     ]  roc_negative            WR lift +1.1pp  avg PF 1.523  PF lift +0.072  1/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 47.5%  PF 1.358  lift +0.041 / req 0.10  n=722  WR!  cov 55%  [--]
    ETHUSDT     WR 50.1%  PF 1.504  lift +0.084 / req 0.10  n=771  WR!  cov 59%  [--]
    SOLUSDT     WR 47.1%  PF 1.338  lift +0.007 / req 0.10  n=770  WR!  cov 57%  [--]
    BNBUSDT     WR 51.2%  PF 1.574  lift +0.063 / req 0.10  n=623  WR!  cov 58%  [--]
    XRPUSDT     WR 55.1%  PF 1.842  lift +0.165 / req 0.10  n=733  WR!  cov 57%  [OK]
  [Pattern      ]  bearish_engulf          WR lift +3.2pp  avg PF 1.687  PF lift +0.236  3/5 pairs  [OK]  warn: WR 4p, low# 5p
    BTCUSDT     WR 49.5%  PF 1.467  lift +0.151 / req 0.10  n=182  WR!  cov 14%!  [OK]
    ETHUSDT     WR 49.1%  PF 1.449  lift +0.029 / req 0.10  n=173  WR!  cov 13%!  [--]
    SOLUSDT     WR 49.7%  PF 1.483  lift +0.152 / req 0.10  n=175  WR!  cov 13%!  [OK]
    BNBUSDT     WR 50.7%  PF 1.541  lift +0.030 / req 0.10  n=148  WR!  cov 14%!  [--]
    XRPUSDT     WR 62.4%  PF 2.493  lift +0.816 / req 0.10  n=181  cov 14%!  [OK]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 CANDLE TRIGGER (4h) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.451  |  Best: bearish_engulf  (avg PF 1.687)

  Warnings (results valid -- interpret with care):
    !! [bearish_rvol] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [bearish_rvol] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [upper_wick_rejection] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [upper_wick_rejection] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [breakdown_bar] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [breakdown_bar] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [roc_negative] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [bearish_engulf] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT
    !! [bearish_engulf] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Bar quality]
      [--] bearish_rvol
      [--] breakdown_bar
      [--] upper_wick_rejection
    [Momentum]
      [--] roc_negative
    [Pattern]
      [OK] bearish_engulf            avg PF 1.687

  Proceed using confirmed 15m candle trigger(s) for setup 3 construction.
```
