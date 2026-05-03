# Trigger Search 1  (entry_tf=1h  kde_tf=4h  baseline=rsi_ma_ema5<50)

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
| `rsi_period` | `14` |
| `rsi_ma_period` | `5` |
| `rsi_ma_type` | `ema` |
| `rsi_ma_threshold` | `50.0` |
| `atr_expansion_mult` | `1.5` |
| `macd_fast` | `12` |
| `macd_slow` | `26` |
| `macd_signal` | `9` |
| `rsi_cross_threshold` | `50.0` |
| `ema_fast` | `9` |
| `ema_slow` | `20` |
| `bb_period` | `20` |
| `bb_std` | `2.0` |

```text

-- Per-Pair Results  (baseline = rsi_ma_ema5<50  entry_tf=1h) --

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  47.76  1.371  20.9      5272
rsi_ma_baseline     50.24  1.515  23.5      2490
bearish_engulfing     NaN    NaN   NaN         0
break_prior_low     51.33  1.582  25.4       676
atr_expansion       50.26  1.516  38.6       189
macd_cross          45.35  1.245  23.2        86
rsi_cross_50        52.14  1.634  14.8       117
ema_cross           45.64  1.259  20.8       149
close_below_bb      58.21  2.090  38.5       414

    bearish_engulfing       covers 0.0% of rsi_ma_baseline  !! LOW
    break_prior_low         covers 27.1% of rsi_ma_baseline
    atr_expansion           covers 7.6% of rsi_ma_baseline
    macd_cross              covers 3.5% of rsi_ma_baseline  !! LOW
    rsi_cross_50            covers 4.7% of rsi_ma_baseline  !! LOW
    ema_cross               covers 6.0% of rsi_ma_baseline
    close_below_bb          covers 16.6% of rsi_ma_baseline

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  53.79  1.746  21.0      5256
rsi_ma_baseline     58.23  2.091  24.9      2528
bearish_engulfing     NaN    NaN   NaN         0
break_prior_low     58.52  2.116  28.4       675
atr_expansion       55.93  1.904  41.2       236
macd_cross          58.54  2.118  30.6        82
rsi_cross_50        62.50  2.500  16.9        96
ema_cross           54.73  1.813  20.5       148
close_below_bb      60.38  2.286  44.6       472

    bearish_engulfing       covers 0.0% of rsi_ma_baseline  !! LOW
    break_prior_low         covers 26.7% of rsi_ma_baseline
    atr_expansion           covers 9.3% of rsi_ma_baseline
    macd_cross              covers 3.2% of rsi_ma_baseline  !! LOW
    rsi_cross_50            covers 3.8% of rsi_ma_baseline  !! LOW
    ema_cross               covers 5.9% of rsi_ma_baseline
    close_below_bb          covers 18.7% of rsi_ma_baseline

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  48.91  1.436  18.8      5475
rsi_ma_baseline     52.60  1.665  19.7      2673
bearish_engulfing     NaN    NaN   NaN         0
break_prior_low     51.83  1.614  21.9       710
atr_expansion       55.49  1.870  28.5       173
macd_cross          52.27  1.643  24.1        88
rsi_cross_50        50.94  1.558  18.0       106
ema_cross           43.67  1.163  25.5       158
close_below_bb      54.25  1.779  32.1       400

    bearish_engulfing       covers 0.0% of rsi_ma_baseline  !! LOW
    break_prior_low         covers 26.6% of rsi_ma_baseline
    atr_expansion           covers 6.5% of rsi_ma_baseline
    macd_cross              covers 3.3% of rsi_ma_baseline  !! LOW
    rsi_cross_50            covers 4.0% of rsi_ma_baseline  !! LOW
    ema_cross               covers 5.9% of rsi_ma_baseline
    close_below_bb          covers 15.0% of rsi_ma_baseline

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.36  1.584  21.1      4367
rsi_ma_baseline     54.50  1.797  23.9      2143
bearish_engulfing     NaN    NaN   NaN         0
break_prior_low     52.36  1.649  25.0       571
atr_expansion       51.88  1.617  33.5       160
macd_cross          57.14  2.000  20.4        70
rsi_cross_50        54.55  1.800  26.2        88
ema_cross           50.00  1.500  25.0       142
close_below_bb      51.23  1.575  39.3       326

    bearish_engulfing       covers 0.0% of rsi_ma_baseline  !! LOW
    break_prior_low         covers 26.6% of rsi_ma_baseline
    atr_expansion           covers 7.5% of rsi_ma_baseline
    macd_cross              covers 3.3% of rsi_ma_baseline  !! LOW
    rsi_cross_50            covers 4.1% of rsi_ma_baseline  !! LOW
    ema_cross               covers 6.6% of rsi_ma_baseline
    close_below_bb          covers 15.2% of rsi_ma_baseline

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.86  1.616  22.3      5195
rsi_ma_baseline     51.47  1.591  25.3      2788
bearish_engulfing     NaN    NaN   NaN         0
break_prior_low     50.07  1.504  25.7       689
atr_expansion       53.76  1.744  39.0       186
macd_cross          52.68  1.670  21.3       112
rsi_cross_50        61.39  2.385  21.3       158
ema_cross           58.64  2.127  30.2       162
close_below_bb      53.03  1.694  47.5       379

    bearish_engulfing       covers 0.0% of rsi_ma_baseline  !! LOW
    break_prior_low         covers 24.7% of rsi_ma_baseline
    atr_expansion           covers 6.7% of rsi_ma_baseline
    macd_cross              covers 4.0% of rsi_ma_baseline  !! LOW
    rsi_cross_50            covers 5.7% of rsi_ma_baseline
    ema_cross               covers 5.8% of rsi_ma_baseline
    close_below_bb          covers 13.6% of rsi_ma_baseline


-- Trigger Search 1 (1h) -- Verdict --

  [ref]  kde_upper_baseline:   avg WR 50.7%  avg PF 1.551
  [base] rsi_ma_ema5<50:   avg WR 53.4%  avg PF 1.732  [+0.181 vs ref]
  KDE (4h): window=200  bw=1  |  ATR×1.5  MACD(12,26,9)  RSI cross 50  EMA(9,20)  BB(20,2.0std)

  [Price Action]  bearish_engulfing       WR lift +nanpp  avg PF nan  PF lift +nan  cov 0.0%  0/5 pairs  [XX]  warn: sparse 5p
    BTCUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0.0%!  [--]
    ETHUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0.0%!  [--]
    SOLUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0.0%!  [--]
    BNBUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0.0%!  [--]
    XRPUSDT     WR nan%  PF nan  lift +nan / req 0.10  n=0  cov 0.0%!  [--]
  [Price Action]  break_prior_low         WR lift -0.6pp  avg PF 1.693  PF lift -0.038  cov 26.4%  0/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 51.3%  PF 1.582  lift +0.068 / req 0.10  n=676  WR!  cov 27.1%  [--]
    ETHUSDT     WR 58.5%  PF 2.116  lift +0.025 / req 0.10  n=675  WR!  cov 26.7%  [--]
    SOLUSDT     WR 51.8%  PF 1.614  lift -0.051 / req 0.10  n=710  WR!  cov 26.6%  [--]
    BNBUSDT     WR 52.4%  PF 1.649  lift -0.148 / req 0.10  n=571  WR!  cov 26.6%  [--]
    XRPUSDT     WR 50.1%  PF 1.504  lift -0.087 / req 0.10  n=689  WR!  cov 24.7%  [--]
  [Price Action]  atr_expansion           WR lift +0.1pp  avg PF 1.730  PF lift -0.001  cov 7.5%  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 50.3%  PF 1.516  lift +0.001 / req 0.10  n=189  WR!  cov 7.6%  [--]
    ETHUSDT     WR 55.9%  PF 1.904  lift -0.187 / req 0.10  n=236  WR!  cov 9.3%  [--]
    SOLUSDT     WR 55.5%  PF 1.870  lift +0.206 / req 0.10  n=173  WR!  cov 6.5%  [OK]
    BNBUSDT     WR 51.9%  PF 1.617  lift -0.180 / req 0.10  n=160  WR!  cov 7.5%  [--]
    XRPUSDT     WR 53.8%  PF 1.744  lift +0.153 / req 0.10  n=186  WR!  cov 6.7%  [OK]
  [Momentum   ]  macd_cross              WR lift -0.2pp  avg PF 1.735  PF lift +0.003  cov 3.5%  1/5 pairs  [XX]  warn: WR 5p, sparse 5p
    BTCUSDT     WR 45.3%  PF 1.245  lift -0.270 / req 0.10  n=86  WR!  cov 3.5%!  [--]
    ETHUSDT     WR 58.5%  PF 2.118  lift +0.027 / req 0.10  n=82  WR!  cov 3.2%!  [--]
    SOLUSDT     WR 52.3%  PF 1.643  lift -0.022 / req 0.10  n=88  WR!  cov 3.3%!  [--]
    BNBUSDT     WR 57.1%  PF 2.000  lift +0.203 / req 0.10  n=70  WR!  cov 3.3%!  [OK]
    XRPUSDT     WR 52.7%  PF 1.670  lift +0.079 / req 0.10  n=112  WR!  cov 4.0%!  [--]
  [Momentum   ]  rsi_cross_50            WR lift +2.9pp  avg PF 1.975  PF lift +0.244  cov 4.4%  3/5 pairs  [OK]  warn: WR 5p, sparse 4p
    BTCUSDT     WR 52.1%  PF 1.634  lift +0.119 / req 0.10  n=117  WR!  cov 4.7%!  [OK]
    ETHUSDT     WR 62.5%  PF 2.500  lift +0.409 / req 0.10  n=96  WR!  cov 3.8%!  [OK]
    SOLUSDT     WR 50.9%  PF 1.558  lift -0.107 / req 0.10  n=106  WR!  cov 4.0%!  [--]
    BNBUSDT     WR 54.5%  PF 1.800  lift +0.003 / req 0.10  n=88  WR!  cov 4.1%!  [--]
    XRPUSDT     WR 61.4%  PF 2.385  lift +0.794 / req 0.10  n=158  WR!  cov 5.7%  [OK]
  [Momentum   ]  ema_cross               WR lift -2.9pp  avg PF 1.572  PF lift -0.159  cov 6.0%  1/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 45.6%  PF 1.259  lift -0.255 / req 0.10  n=149  WR!  cov 6.0%  [--]
    ETHUSDT     WR 54.7%  PF 1.813  lift -0.277 / req 0.10  n=148  WR!  cov 5.9%  [--]
    SOLUSDT     WR 43.7%  PF 1.163  lift -0.502 / req 0.10  n=158  WR!  cov 5.9%  [--]
    BNBUSDT     WR 50.0%  PF 1.500  lift -0.297 / req 0.10  n=142  WR!  cov 6.6%  [--]
    XRPUSDT     WR 58.6%  PF 2.127  lift +0.536 / req 0.10  n=162  WR!  cov 5.8%  [OK]
  [Volatility ]  close_below_bb          WR lift +2.0pp  avg PF 1.885  PF lift +0.153  cov 15.8%  4/5 pairs  [OK]  warn: WR 4p, low# 2p
    BTCUSDT     WR 58.2%  PF 2.090  lift +0.575 / req 0.10  n=414  cov 16.6%  [OK]
    ETHUSDT     WR 60.4%  PF 2.286  lift +0.195 / req 0.10  n=472  WR!  cov 18.7%  [OK]
    SOLUSDT     WR 54.2%  PF 1.779  lift +0.114 / req 0.10  n=400  WR!  cov 15.0%  [OK]
    BNBUSDT     WR 51.2%  PF 1.575  lift -0.221 / req 0.10  n=326  WR!  cov 15.2%  [--]
    XRPUSDT     WR 53.0%  PF 1.694  lift +0.103 / req 0.10  n=379  WR!  cov 13.6%  [OK]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs  (vs rsi_ma_baseline)

  [OK]  TRIGGER SEARCH 1 (1h) CONFIRMED -- 2 event trigger(s) improve on rsi_ma_baseline.
        rsi_ma_baseline avg PF 1.732  |  Best: rsi_cross_50  (avg PF 1.975)

  -- Confirmed triggers --
    [Momentum]
      [OK] rsi_cross_50           avg PF 1.975
      [--] macd_cross             
      [--] ema_cross              
    [Volatility]
      [OK] close_below_bb         avg PF 1.885
    [Price Action]
      [--] bearish_engulfing      
      [--] break_prior_low        
      [--] atr_expansion          

  These event triggers can be used as entry timing signals in Setup 3.

  Warnings (results valid -- interpret with care):
    !! [bearish_engulfing] very sparse (<5% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [break_prior_low] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [atr_expansion] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [macd_cross] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [macd_cross] very sparse (<5% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rsi_cross_50] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rsi_cross_50] very sparse (<5% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT
    !! [ema_cross] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [close_below_bb] WR lift below threshold on: ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
```
