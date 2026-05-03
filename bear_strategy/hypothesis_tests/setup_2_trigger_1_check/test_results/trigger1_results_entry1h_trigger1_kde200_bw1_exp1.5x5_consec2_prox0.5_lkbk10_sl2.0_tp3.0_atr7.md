# Bear Strategy -- Setup 2 Trigger 1  (entry_tf=1h  kde_tf=4h)

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
| `zone_touch_lookback` | `10` |
| `zone_touch_low_lookback` | `15` |
| `retest_lookback` | `25` |
| `atr_short_period` | `5` |
| `atr_expansion_mult` | `1.5` |
| `consec_bearish_n` | `2` |
| `retest_proximity_atr` | `0.5` |
| `rsi_period` | `14` |
| `rsi_threshold` | `50.0` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 1h) --

  BTCUSDT
                       wr_%     pf    dur  n_trades
population                                         
kde_upper_baseline    47.76  1.371   20.9      5272
trigger_1_atr_exp     53.33  1.714  102.5        30
trigger_2_consec      53.98  1.760   41.2       113
trigger_3_lower_high  50.70  1.543   30.4        71
trigger_4_low_viol    48.85  1.433   33.2       131
trigger_5_retest      63.64  2.625   71.3        11
trigger_6_rsi_below   49.73  1.484   24.0      2634

    trigger_1_atr_exp           covers 0.6% of baseline bars  !! LOW
    trigger_2_consec            covers 2.1% of baseline bars  !! LOW
    trigger_3_lower_high        covers 1.3% of baseline bars  !! LOW
    trigger_4_low_viol          covers 2.5% of baseline bars  !! LOW
    trigger_5_retest            covers 0.2% of baseline bars  !! LOW
    trigger_6_rsi_below         covers 50.0% of baseline bars

  ETHUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    53.79  1.746  21.0      5256
trigger_1_atr_exp     47.37  1.350  36.9        38
trigger_2_consec      50.68  1.542  28.0       146
trigger_3_lower_high  54.21  1.776  27.5       107
trigger_4_low_viol    57.67  2.043  28.8       163
trigger_5_retest      35.00  0.808  21.9        20
trigger_6_rsi_below   57.74  2.049  24.9      2707

    trigger_1_atr_exp           covers 0.7% of baseline bars  !! LOW
    trigger_2_consec            covers 2.8% of baseline bars  !! LOW
    trigger_3_lower_high        covers 2.0% of baseline bars  !! LOW
    trigger_4_low_viol          covers 3.1% of baseline bars  !! LOW
    trigger_5_retest            covers 0.4% of baseline bars  !! LOW
    trigger_6_rsi_below         covers 51.5% of baseline bars

  SOLUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    48.91  1.436  18.8      5475
trigger_1_atr_exp     52.38  1.650  34.6        21
trigger_2_consec      55.91  1.902  23.8        93
trigger_3_lower_high  52.73  1.673  27.1        55
trigger_4_low_viol    60.40  2.288  25.7       101
trigger_5_retest      45.45  1.250  19.3        11
trigger_6_rsi_below   51.22  1.575  19.8      2870

    trigger_1_atr_exp           covers 0.4% of baseline bars  !! LOW
    trigger_2_consec            covers 1.7% of baseline bars  !! LOW
    trigger_3_lower_high        covers 1.0% of baseline bars  !! LOW
    trigger_4_low_viol          covers 1.8% of baseline bars  !! LOW
    trigger_5_retest            covers 0.2% of baseline bars  !! LOW
    trigger_6_rsi_below         covers 52.4% of baseline bars

  BNBUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    51.36  1.584  21.1      4367
trigger_1_atr_exp     40.00  1.000  29.5        30
trigger_2_consec      48.28  1.400  29.2       116
trigger_3_lower_high  46.99  1.330  28.3        83
trigger_4_low_viol    46.06  1.281  33.1       165
trigger_5_retest      56.25  1.929  23.8        16
trigger_6_rsi_below   54.16  1.772  23.7      2271

    trigger_1_atr_exp           covers 0.7% of baseline bars  !! LOW
    trigger_2_consec            covers 2.7% of baseline bars  !! LOW
    trigger_3_lower_high        covers 1.9% of baseline bars  !! LOW
    trigger_4_low_viol          covers 3.8% of baseline bars  !! LOW
    trigger_5_retest            covers 0.4% of baseline bars  !! LOW
    trigger_6_rsi_below         covers 52.0% of baseline bars

  XRPUSDT
                       wr_%     pf    dur  n_trades
population                                         
kde_upper_baseline    51.86  1.616   22.3      5195
trigger_1_atr_exp     48.00  1.385  106.3        25
trigger_2_consec      44.44  1.200   42.9       126
trigger_3_lower_high  56.76  1.969   55.7        74
trigger_4_low_viol    47.65  1.365   78.3       149
trigger_5_retest      45.45  1.250   20.9        11
trigger_6_rsi_below   50.47  1.529   25.5      2861

    trigger_1_atr_exp           covers 0.5% of baseline bars  !! LOW
    trigger_2_consec            covers 2.4% of baseline bars  !! LOW
    trigger_3_lower_high        covers 1.4% of baseline bars  !! LOW
    trigger_4_low_viol          covers 2.9% of baseline bars  !! LOW
    trigger_5_retest            covers 0.2% of baseline bars  !! LOW
    trigger_6_rsi_below         covers 55.1% of baseline bars


-- Setup 2 Trigger 1 (1h) -- Verdict --

  Baseline (kde_upper_baseline on 1h):  avg WR 50.7%  avg PF 1.551
  KDE (4h): window=200  bw=1  |  touch_lookback=10  low_lookback=15  retest_lookback=25
  exp_mult=1.5×5-ATR  consec=2  retest_prox=0.5 ATR  RSI(14)<50

  [Zone-Sequence]  trigger_1_atr_exp           WR lift -2.5pp  avg PF 1.420  PF lift -0.131  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 53.3%  PF 1.714  lift +0.343 / req 0.10  n=30  WR!  cov 1%!  [OK]
    ETHUSDT     WR 47.4%  PF 1.350  lift -0.396 / req 0.10  n=38  WR!  cov 1%!  [--]
    SOLUSDT     WR 52.4%  PF 1.650  lift +0.214 / req 0.10  n=21  WR!  cov 0%!  [OK]
    BNBUSDT     WR 40.0%  PF 1.000  lift -0.584 / req 0.10  n=30  WR!  cov 1%!  [--]
    XRPUSDT     WR 48.0%  PF 1.385  lift -0.231 / req 0.10  n=25  WR!  cov 0%!  [--]
  [Zone-Sequence]  trigger_2_consec            WR lift -0.1pp  avg PF 1.561  PF lift +0.010  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 54.0%  PF 1.760  lift +0.388 / req 0.10  n=113  WR!  cov 2%!  [OK]
    ETHUSDT     WR 50.7%  PF 1.542  lift -0.204 / req 0.10  n=146  WR!  cov 3%!  [--]
    SOLUSDT     WR 55.9%  PF 1.902  lift +0.466 / req 0.10  n=93  WR!  cov 2%!  [OK]
    BNBUSDT     WR 48.3%  PF 1.400  lift -0.184 / req 0.10  n=116  WR!  cov 3%!  [--]
    XRPUSDT     WR 44.4%  PF 1.200  lift -0.416 / req 0.10  n=126  WR!  cov 2%!  [--]
  [Zone-Sequence]  trigger_3_lower_high        WR lift +1.5pp  avg PF 1.658  PF lift +0.107  3/5 pairs  [OK]  warn: WR 5p, low# 5p
    BTCUSDT     WR 50.7%  PF 1.543  lift +0.171 / req 0.10  n=71  WR!  cov 1%!  [OK]
    ETHUSDT     WR 54.2%  PF 1.776  lift +0.030 / req 0.10  n=107  WR!  cov 2%!  [--]
    SOLUSDT     WR 52.7%  PF 1.673  lift +0.237 / req 0.10  n=55  WR!  cov 1%!  [OK]
    BNBUSDT     WR 47.0%  PF 1.330  lift -0.254 / req 0.10  n=83  WR!  cov 2%!  [--]
    XRPUSDT     WR 56.8%  PF 1.969  lift +0.353 / req 0.10  n=74  WR!  cov 1%!  [OK]
  [Zone-Sequence]  trigger_4_low_viol          WR lift +1.4pp  avg PF 1.682  PF lift +0.131  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 48.9%  PF 1.433  lift +0.061 / req 0.10  n=131  WR!  cov 2%!  [--]
    ETHUSDT     WR 57.7%  PF 2.043  lift +0.298 / req 0.10  n=163  WR!  cov 3%!  [OK]
    SOLUSDT     WR 60.4%  PF 2.288  lift +0.851 / req 0.10  n=101  WR!  cov 2%!  [OK]
    BNBUSDT     WR 46.1%  PF 1.281  lift -0.303 / req 0.10  n=165  WR!  cov 4%!  [--]
    XRPUSDT     WR 47.7%  PF 1.365  lift -0.250 / req 0.10  n=149  WR!  cov 3%!  [--]
  [Zone-Sequence]  trigger_5_retest            WR lift -1.6pp  avg PF 1.572  PF lift +0.022  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 63.6%  PF 2.625  lift +1.254 / req 0.10  n=11  WR!  cov 0%!  [OK]
    ETHUSDT     WR 35.0%  PF 0.808  lift -0.938 / req 0.10  n=20  WR!  cov 0%!  [--]
    SOLUSDT     WR 45.5%  PF 1.250  lift -0.186 / req 0.10  n=11  WR!  cov 0%!  [--]
    BNBUSDT     WR 56.2%  PF 1.929  lift +0.345 / req 0.10  n=16  WR!  cov 0%!  [OK]
    XRPUSDT     WR 45.5%  PF 1.250  lift -0.366 / req 0.10  n=11  WR!  cov 0%!  [--]
  [Momentum     ]  trigger_6_rsi_below         WR lift +1.9pp  avg PF 1.682  PF lift +0.131  4/5 pairs  [OK]  warn: WR 3p
    BTCUSDT     WR 49.7%  PF 1.484  lift +0.113 / req 0.10  n=2,634  WR!  cov 50%  [OK]
    ETHUSDT     WR 57.7%  PF 2.049  lift +0.304 / req 0.10  n=2,707  cov 52%  [OK]
    SOLUSDT     WR 51.2%  PF 1.575  lift +0.139 / req 0.10  n=2,870  WR!  cov 52%  [OK]
    BNBUSDT     WR 54.2%  PF 1.772  lift +0.188 / req 0.10  n=2,271  cov 52%  [OK]
    XRPUSDT     WR 50.5%  PF 1.529  lift -0.087 / req 0.10  n=2,861  WR!  cov 55%  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 1 (1h) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.551  |  Best: trigger_6_rsi_below  (avg PF 1.682)

  Warnings (results valid -- interpret with care):
    !! [trigger_1_atr_exp] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [trigger_1_atr_exp] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [trigger_2_consec] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [trigger_2_consec] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [trigger_3_lower_high] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [trigger_3_lower_high] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [trigger_4_low_viol] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [trigger_4_low_viol] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [trigger_5_retest] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [trigger_5_retest] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [trigger_6_rsi_below] WR lift below threshold on: BTCUSDT, SOLUSDT, XRPUSDT

  -- Confirmed populations --
    [Zone-Sequence Triggers]
      [OK] trigger_3_lower_high          avg PF 1.658
      [--] trigger_1_atr_exp
      [--] trigger_2_consec
      [--] trigger_4_low_viol
      [--] trigger_5_retest
    [Momentum]
      [OK] trigger_6_rsi_below           avg PF 1.682

  Proceed using confirmed zone-sequence trigger(s) for setup 3 construction.
```
