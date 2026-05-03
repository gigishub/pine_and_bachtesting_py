# Bear Strategy -- Setup 2 Trigger 7  (entry_tf=1h  kde_tf=4h)

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
| `divergence_lookback` | `20` |
| `impulse_lookback` | `20` |
| `wick_ratio` | `0.5` |
| `bb_period` | `20` |
| `bb_std` | `2.0` |
| `bb_proximity_pct` | `0.01` |
| `bb_lookback` | `10` |
| `ema_fast` | `9` |
| `ema_slow` | `20` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 1h) --

  BTCUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    47.76  1.371  20.9      5272
price_rsi_divergence  48.96  1.439  19.2       719
shrinking_impulse     51.09  1.567  21.9        92
bb_rounding           43.02  1.133  16.6      1139
ema_tightening        49.27  1.457  18.2      1157
ema_cross_down        45.78  1.267  20.7       166

    price_rsi_divergence        covers 13.6% of baseline bars  !! LOW
    shrinking_impulse           covers 1.7% of baseline bars  !! LOW
    bb_rounding                 covers 21.6% of baseline bars  !! LOW
    ema_tightening              covers 21.9% of baseline bars  !! LOW
    ema_cross_down              covers 3.1% of baseline bars  !! LOW

  ETHUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    53.79  1.746  21.0      5256
price_rsi_divergence  49.02  1.442  16.1       816
shrinking_impulse     44.44  1.200  18.4       117
bb_rounding           54.97  1.831  14.0       875
ema_tightening        59.45  2.199  20.8      1058
ema_cross_down        55.70  1.886  19.9       158

    price_rsi_divergence        covers 15.5% of baseline bars  !! LOW
    shrinking_impulse           covers 2.2% of baseline bars  !! LOW
    bb_rounding                 covers 16.6% of baseline bars  !! LOW
    ema_tightening              covers 20.1% of baseline bars  !! LOW
    ema_cross_down              covers 3.0% of baseline bars  !! LOW

  SOLUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    48.91  1.436  18.8      5475
price_rsi_divergence  45.17  1.236  19.7       870
shrinking_impulse     53.51  1.726  17.9       114
bb_rounding           46.30  1.293  15.9       568
ema_tightening        54.58  1.802  15.6      1202
ema_cross_down        43.86  1.172  24.4       171

    price_rsi_divergence        covers 15.9% of baseline bars  !! LOW
    shrinking_impulse           covers 2.1% of baseline bars  !! LOW
    bb_rounding                 covers 10.4% of baseline bars  !! LOW
    ema_tightening              covers 22.0% of baseline bars  !! LOW
    ema_cross_down              covers 3.1% of baseline bars  !! LOW

  BNBUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    51.36  1.584  21.1      4367
price_rsi_divergence  49.64  1.478  21.7       689
shrinking_impulse     51.47  1.591  17.6        68
bb_rounding           53.16  1.702  17.0       854
ema_tightening        56.79  1.972  19.1       942
ema_cross_down        48.70  1.424  24.0       154

    price_rsi_divergence        covers 15.8% of baseline bars  !! LOW
    shrinking_impulse           covers 1.6% of baseline bars  !! LOW
    bb_rounding                 covers 19.6% of baseline bars  !! LOW
    ema_tightening              covers 21.6% of baseline bars  !! LOW
    ema_cross_down              covers 3.5% of baseline bars  !! LOW

  XRPUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    51.86  1.616  22.3      5195
price_rsi_divergence  53.67  1.738  20.6       667
shrinking_impulse     48.68  1.423  18.6        76
bb_rounding           57.06  1.993  16.8       885
ema_tightening        51.93  1.620  20.7      1219
ema_cross_down        58.18  2.087  30.1       165

    price_rsi_divergence        covers 12.8% of baseline bars  !! LOW
    shrinking_impulse           covers 1.5% of baseline bars  !! LOW
    bb_rounding                 covers 17.0% of baseline bars  !! LOW
    ema_tightening              covers 23.5% of baseline bars  !! LOW
    ema_cross_down              covers 3.2% of baseline bars  !! LOW


-- Setup 2 Trigger 7 (1h) -- Verdict --

  Baseline (kde_upper_baseline on 1h):  avg WR 50.7%  avg PF 1.551
  KDE (4h): window=200  bw=1  |  RSI(14)  BB(20)  EMA(9,20)

  [Divergence ]  price_rsi_divergence        WR lift -1.4pp  avg PF 1.467  PF lift -0.084  1/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 49.0%  PF 1.439  lift +0.067 / req 0.10  n=719  WR!  cov 14%!  [--]
    ETHUSDT     WR 49.0%  PF 1.442  lift -0.303 / req 0.10  n=816  WR!  cov 16%!  [--]
    SOLUSDT     WR 45.2%  PF 1.236  lift -0.200 / req 0.10  n=870  WR!  cov 16%!  [--]
    BNBUSDT     WR 49.6%  PF 1.478  lift -0.106 / req 0.10  n=689  WR!  cov 16%!  [--]
    XRPUSDT     WR 53.7%  PF 1.738  lift +0.122 / req 0.10  n=667  WR!  cov 13%!  [OK]
  [Price Act  ]  shrinking_impulse           WR lift -0.9pp  avg PF 1.501  PF lift -0.049  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 51.1%  PF 1.567  lift +0.195 / req 0.10  n=92  WR!  cov 2%!  [OK]
    ETHUSDT     WR 44.4%  PF 1.200  lift -0.546 / req 0.10  n=117  WR!  cov 2%!  [--]
    SOLUSDT     WR 53.5%  PF 1.726  lift +0.290 / req 0.10  n=114  WR!  cov 2%!  [OK]
    BNBUSDT     WR 51.5%  PF 1.591  lift +0.007 / req 0.10  n=68  WR!  cov 2%!  [--]
    XRPUSDT     WR 48.7%  PF 1.423  lift -0.193 / req 0.10  n=76  WR!  cov 1%!  [--]
  [Volatility ]  bb_rounding                 WR lift +0.2pp  avg PF 1.591  PF lift +0.040  2/5 pairs  [XX]  warn: WR 4p, low# 5p
    BTCUSDT     WR 43.0%  PF 1.133  lift -0.239 / req 0.10  n=1,139  WR!  cov 22%!  [--]
    ETHUSDT     WR 55.0%  PF 1.831  lift +0.085 / req 0.10  n=875  WR!  cov 17%!  [--]
    SOLUSDT     WR 46.3%  PF 1.293  lift -0.143 / req 0.10  n=568  WR!  cov 10%!  [--]
    BNBUSDT     WR 53.2%  PF 1.702  lift +0.118 / req 0.10  n=854  WR!  cov 20%!  [OK]
    XRPUSDT     WR 57.1%  PF 1.993  lift +0.378 / req 0.10  n=885  cov 17%!  [OK]
  [Momentum   ]  ema_tightening              WR lift +3.7pp  avg PF 1.810  PF lift +0.259  3/5 pairs  [OK]  warn: WR 2p, low# 5p
    BTCUSDT     WR 49.3%  PF 1.457  lift +0.085 / req 0.10  n=1,157  WR!  cov 22%!  [--]
    ETHUSDT     WR 59.5%  PF 2.199  lift +0.454 / req 0.10  n=1,058  cov 20%!  [OK]
    SOLUSDT     WR 54.6%  PF 1.802  lift +0.366 / req 0.10  n=1,202  cov 22%!  [OK]
    BNBUSDT     WR 56.8%  PF 1.972  lift +0.388 / req 0.10  n=942  cov 22%!  [OK]
    XRPUSDT     WR 51.9%  PF 1.620  lift +0.005 / req 0.10  n=1,219  WR!  cov 23%!  [--]
  [EMA Cross  ]  ema_cross_down              WR lift -0.3pp  avg PF 1.567  PF lift +0.016  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 45.8%  PF 1.267  lift -0.105 / req 0.10  n=166  WR!  cov 3%!  [--]
    ETHUSDT     WR 55.7%  PF 1.886  lift +0.140 / req 0.10  n=158  WR!  cov 3%!  [OK]
    SOLUSDT     WR 43.9%  PF 1.172  lift -0.264 / req 0.10  n=171  WR!  cov 3%!  [--]
    BNBUSDT     WR 48.7%  PF 1.424  lift -0.160 / req 0.10  n=154  WR!  cov 4%!  [--]
    XRPUSDT     WR 58.2%  PF 2.087  lift +0.471 / req 0.10  n=165  WR!  cov 3%!  [OK]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 7 (1h) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.551  |  Best: ema_tightening  (avg PF 1.810)

  Warnings (results valid -- interpret with care):
    !! [price_rsi_divergence] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [price_rsi_divergence] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [shrinking_impulse] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [shrinking_impulse] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [bb_rounding] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT
    !! [bb_rounding] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [ema_tightening] WR lift below threshold on: BTCUSDT, XRPUSDT
    !! [ema_tightening] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [ema_cross_down] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [ema_cross_down] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Divergence]
      [--] price_rsi_divergence
    [Price Action]
      [--] shrinking_impulse
    [Volatility]
      [--] bb_rounding
    [Momentum]
      [OK] ema_tightening              avg PF 1.810

  Proceed using confirmed exhaustion signal(s) for setup 3 construction.
```
