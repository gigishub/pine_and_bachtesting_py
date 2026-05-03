# Bear Strategy -- Setup 2 Trigger 1  (entry_tf=15m  kde_tf=4h)

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

-- Per-Pair Results (baseline = kde_upper_baseline on 15m) --

  BTCUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    45.41  1.248  22.7     21088
trigger_1_atr_exp     48.33  1.403  60.8       120
trigger_2_consec      49.18  1.452  42.8       368
trigger_3_lower_high  47.44  1.354  45.5       430
trigger_4_low_viol    45.45  1.250  42.9       891
trigger_5_retest      38.89  0.955  88.6        54
trigger_6_rsi_below   45.90  1.273  25.3     11707

    trigger_1_atr_exp           covers 0.6% of baseline bars  !! LOW
    trigger_2_consec            covers 1.7% of baseline bars  !! LOW
    trigger_3_lower_high        covers 2.0% of baseline bars  !! LOW
    trigger_4_low_viol          covers 4.2% of baseline bars  !! LOW
    trigger_5_retest            covers 0.3% of baseline bars  !! LOW
    trigger_6_rsi_below         covers 55.5% of baseline bars

  ETHUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    49.83  1.490  20.8     21024
trigger_1_atr_exp     47.69  1.368  49.1       130
trigger_2_consec      51.72  1.607  34.5       464
trigger_3_lower_high  48.28  1.400  28.5       524
trigger_4_low_viol    49.23  1.455  28.9      1044
trigger_5_retest      42.17  1.094  28.9        83
trigger_6_rsi_below   52.40  1.651  22.6     12227

    trigger_1_atr_exp           covers 0.6% of baseline bars  !! LOW
    trigger_2_consec            covers 2.2% of baseline bars  !! LOW
    trigger_3_lower_high        covers 2.5% of baseline bars  !! LOW
    trigger_4_low_viol          covers 5.0% of baseline bars  !! LOW
    trigger_5_retest            covers 0.4% of baseline bars  !! LOW
    trigger_6_rsi_below         covers 58.2% of baseline bars

  SOLUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    46.71  1.315  20.6     21965
trigger_1_atr_exp     52.13  1.633  43.2        94
trigger_2_consec      50.13  1.508  33.3       377
trigger_3_lower_high  50.00  1.500  33.2       398
trigger_4_low_viol    48.39  1.407  30.1       841
trigger_5_retest      54.17  1.773  39.1        48
trigger_6_rsi_below   46.90  1.325  22.0     12583

    trigger_1_atr_exp           covers 0.4% of baseline bars  !! LOW
    trigger_2_consec            covers 1.7% of baseline bars  !! LOW
    trigger_3_lower_high        covers 1.8% of baseline bars  !! LOW
    trigger_4_low_viol          covers 3.8% of baseline bars  !! LOW
    trigger_5_retest            covers 0.2% of baseline bars  !! LOW
    trigger_6_rsi_below         covers 57.3% of baseline bars

  BNBUSDT
                       wr_%     pf    dur  n_trades
population                                         
kde_upper_baseline    47.65  1.365   20.3     17502
trigger_1_atr_exp     44.44  1.200   42.7        90
trigger_2_consec      44.64  1.209   37.7       345
trigger_3_lower_high  43.38  1.149   48.4       408
trigger_4_low_viol    47.85  1.376   25.9       861
trigger_5_retest      29.73  0.635  172.9        37
trigger_6_rsi_below   47.85  1.376   22.1      9969

    trigger_1_atr_exp           covers 0.5% of baseline bars  !! LOW
    trigger_2_consec            covers 2.0% of baseline bars  !! LOW
    trigger_3_lower_high        covers 2.3% of baseline bars  !! LOW
    trigger_4_low_viol          covers 4.9% of baseline bars  !! LOW
    trigger_5_retest            covers 0.2% of baseline bars  !! LOW
    trigger_6_rsi_below         covers 57.0% of baseline bars

  XRPUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    48.07  1.389  22.4     20784
trigger_1_atr_exp     44.30  1.193  47.9        79
trigger_2_consec      48.60  1.418  32.5       321
trigger_3_lower_high  46.86  1.323  51.4       350
trigger_4_low_viol    46.60  1.309  73.3       749
trigger_5_retest      45.45  1.250  34.0        44
trigger_6_rsi_below   46.26  1.291  24.7     12125

    trigger_1_atr_exp           covers 0.4% of baseline bars  !! LOW
    trigger_2_consec            covers 1.5% of baseline bars  !! LOW
    trigger_3_lower_high        covers 1.7% of baseline bars  !! LOW
    trigger_4_low_viol          covers 3.6% of baseline bars  !! LOW
    trigger_5_retest            covers 0.2% of baseline bars  !! LOW
    trigger_6_rsi_below         covers 58.3% of baseline bars


-- Setup 2 Trigger 1 (15m) -- Verdict --

  Baseline (kde_upper_baseline on 15m):  avg WR 47.5%  avg PF 1.361
  KDE (4h): window=200  bw=1  |  touch_lookback=10  low_lookback=15  retest_lookback=25
  exp_mult=1.5×5-ATR  consec=2  retest_prox=0.5 ATR  RSI(14)<50

  [Zone-Sequence]  trigger_1_atr_exp           WR lift -0.2pp  avg PF 1.359  PF lift -0.002  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 48.3%  PF 1.403  lift +0.155 / req 0.10  n=120  WR!  cov 1%!  [OK]
    ETHUSDT     WR 47.7%  PF 1.368  lift -0.122 / req 0.10  n=130  WR!  cov 1%!  [--]
    SOLUSDT     WR 52.1%  PF 1.633  lift +0.319 / req 0.10  n=94  WR!  cov 0%!  [OK]
    BNBUSDT     WR 44.4%  PF 1.200  lift -0.165 / req 0.10  n=90  WR!  cov 1%!  [--]
    XRPUSDT     WR 44.3%  PF 1.193  lift -0.195 / req 0.10  n=79  WR!  cov 0%!  [--]
  [Zone-Sequence]  trigger_2_consec            WR lift +1.3pp  avg PF 1.439  PF lift +0.078  3/5 pairs  [OK]  warn: WR 5p, low# 5p
    BTCUSDT     WR 49.2%  PF 1.452  lift +0.204 / req 0.10  n=368  WR!  cov 2%!  [OK]
    ETHUSDT     WR 51.7%  PF 1.607  lift +0.117 / req 0.10  n=464  WR!  cov 2%!  [OK]
    SOLUSDT     WR 50.1%  PF 1.508  lift +0.193 / req 0.10  n=377  WR!  cov 2%!  [OK]
    BNBUSDT     WR 44.6%  PF 1.209  lift -0.156 / req 0.10  n=345  WR!  cov 2%!  [--]
    XRPUSDT     WR 48.6%  PF 1.418  lift +0.030 / req 0.10  n=321  WR!  cov 2%!  [--]
  [Zone-Sequence]  trigger_3_lower_high        WR lift -0.3pp  avg PF 1.345  PF lift -0.016  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 47.4%  PF 1.354  lift +0.106 / req 0.10  n=430  WR!  cov 2%!  [OK]
    ETHUSDT     WR 48.3%  PF 1.400  lift -0.090 / req 0.10  n=524  WR!  cov 2%!  [--]
    SOLUSDT     WR 50.0%  PF 1.500  lift +0.185 / req 0.10  n=398  WR!  cov 2%!  [OK]
    BNBUSDT     WR 43.4%  PF 1.149  lift -0.216 / req 0.10  n=408  WR!  cov 2%!  [--]
    XRPUSDT     WR 46.9%  PF 1.323  lift -0.066 / req 0.10  n=350  WR!  cov 2%!  [--]
  [Zone-Sequence]  trigger_4_low_viol          WR lift -0.0pp  avg PF 1.359  PF lift -0.002  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 45.5%  PF 1.250  lift +0.002 / req 0.10  n=891  WR!  cov 4%!  [--]
    ETHUSDT     WR 49.2%  PF 1.455  lift -0.035 / req 0.10  n=1,044  WR!  cov 5%!  [--]
    SOLUSDT     WR 48.4%  PF 1.407  lift +0.092 / req 0.10  n=841  WR!  cov 4%!  [--]
    BNBUSDT     WR 47.9%  PF 1.376  lift +0.011 / req 0.10  n=861  WR!  cov 5%!  [--]
    XRPUSDT     WR 46.6%  PF 1.309  lift -0.080 / req 0.10  n=749  WR!  cov 4%!  [--]
  [Zone-Sequence]  trigger_5_retest            WR lift -5.5pp  avg PF 1.141  PF lift -0.220  1/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 38.9%  PF 0.955  lift -0.293 / req 0.10  n=54  WR!  cov 0%!  [--]
    ETHUSDT     WR 42.2%  PF 1.094  lift -0.396 / req 0.10  n=83  WR!  cov 0%!  [--]
    SOLUSDT     WR 54.2%  PF 1.773  lift +0.458 / req 0.10  n=48  WR!  cov 0%!  [OK]
    BNBUSDT     WR 29.7%  PF 0.635  lift -0.731 / req 0.10  n=37  WR!  cov 0%!  [--]
    XRPUSDT     WR 45.5%  PF 1.250  lift -0.139 / req 0.10  n=44  WR!  cov 0%!  [--]
  [Momentum     ]  trigger_6_rsi_below         WR lift +0.3pp  avg PF 1.383  PF lift +0.022  1/5 pairs  [XX]  warn: WR 4p
    BTCUSDT     WR 45.9%  PF 1.273  lift +0.025 / req 0.05  n=11,707  WR!  cov 56%  [--]
    ETHUSDT     WR 52.4%  PF 1.651  lift +0.161 / req 0.05  n=12,227  cov 58%  [OK]
    SOLUSDT     WR 46.9%  PF 1.325  lift +0.010 / req 0.05  n=12,583  WR!  cov 57%  [--]
    BNBUSDT     WR 47.8%  PF 1.376  lift +0.011 / req 0.10  n=9,969  WR!  cov 57%  [--]
    XRPUSDT     WR 46.3%  PF 1.291  lift -0.097 / req 0.05  n=12,125  WR!  cov 58%  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 1 (15m) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.361  |  Best: trigger_2_consec  (avg PF 1.439)

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
    !! [trigger_6_rsi_below] WR lift below threshold on: BTCUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Zone-Sequence Triggers]
      [OK] trigger_2_consec              avg PF 1.439
      [--] trigger_1_atr_exp
      [--] trigger_3_lower_high
      [--] trigger_4_low_viol
      [--] trigger_5_retest
    [Momentum]
      [--] trigger_6_rsi_below

  Proceed using confirmed zone-sequence trigger(s) for setup 3 construction.
```
