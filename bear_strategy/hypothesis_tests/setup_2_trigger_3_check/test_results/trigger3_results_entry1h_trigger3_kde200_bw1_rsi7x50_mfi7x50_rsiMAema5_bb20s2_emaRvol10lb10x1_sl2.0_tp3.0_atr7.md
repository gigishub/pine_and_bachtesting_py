# Bear Strategy -- Setup 2 Trigger 3  (entry_tf=1h  kde_tf=4h)

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
| `rsi_period` | `7` |
| `rsi_threshold` | `50.0` |
| `mfi_period` | `7` |
| `mfi_threshold` | `50.0` |
| `rsi_ma_period` | `5` |
| `rsi_ma_type` | `ema` |
| `bb_period` | `20` |
| `bb_std` | `2.0` |
| `ema_rvol_period` | `10` |
| `ema_rvol_lookback` | `10` |
| `ema_rvol_threshold` | `1` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 1h) --

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  47.76  1.371  20.9      5272
rsi_cross_50        47.37  1.350  17.4       475
mfi_cross_50        45.32  1.243  17.5       459
rsi_cross_ma        45.82  1.269  18.6       838
bb_expand_down      51.31  1.581  27.8      1224
ema_rvol_cross      48.19  1.395  17.6       249

    rsi_cross_50      covers 9.0% of baseline bars  !! LOW
    mfi_cross_50      covers 8.7% of baseline bars  !! LOW
    rsi_cross_ma      covers 15.9% of baseline bars  !! LOW
    bb_expand_down    covers 23.2% of baseline bars  !! LOW
    ema_rvol_cross    covers 4.7% of baseline bars  !! LOW

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  53.79  1.746  21.0      5256
rsi_cross_50        57.11  1.998  17.6       478
mfi_cross_50        54.23  1.777  17.8       426
rsi_cross_ma        52.31  1.645  18.5       780
bb_expand_down      58.87  2.147  25.7      1296
ema_rvol_cross      52.28  1.643  21.8       241

    rsi_cross_50      covers 9.1% of baseline bars  !! LOW
    mfi_cross_50      covers 8.1% of baseline bars  !! LOW
    rsi_cross_ma      covers 14.8% of baseline bars  !! LOW
    bb_expand_down    covers 24.7% of baseline bars  !! LOW
    ema_rvol_cross    covers 4.6% of baseline bars  !! LOW

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  48.91  1.436  18.8      5475
rsi_cross_50        47.26  1.344  18.0       493
mfi_cross_50        47.93  1.381  18.2       459
rsi_cross_ma        48.86  1.433  17.5       835
bb_expand_down      50.62  1.538  22.7      1284
ema_rvol_cross      48.16  1.394  19.3       245

    rsi_cross_50      covers 9.0% of baseline bars  !! LOW
    mfi_cross_50      covers 8.4% of baseline bars  !! LOW
    rsi_cross_ma      covers 15.3% of baseline bars  !! LOW
    bb_expand_down    covers 23.5% of baseline bars  !! LOW
    ema_rvol_cross    covers 4.5% of baseline bars  !! LOW

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.36  1.584  21.1      4367
rsi_cross_50        55.12  1.842  18.7       381
mfi_cross_50        51.78  1.611  19.0       365
rsi_cross_ma        50.31  1.519  18.2       650
bb_expand_down      52.51  1.658  25.1      1057
ema_rvol_cross      56.72  1.966  17.3       201

    rsi_cross_50      covers 8.7% of baseline bars  !! LOW
    mfi_cross_50      covers 8.4% of baseline bars  !! LOW
    rsi_cross_ma      covers 14.9% of baseline bars  !! LOW
    bb_expand_down    covers 24.2% of baseline bars  !! LOW
    ema_rvol_cross    covers 4.6% of baseline bars  !! LOW

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.86  1.616  22.3      5195
rsi_cross_50        52.03  1.627  19.7       517
mfi_cross_50        52.67  1.669  19.7       450
rsi_cross_ma        49.82  1.489  19.5       819
bb_expand_down      51.61  1.600  25.3      1240
ema_rvol_cross      55.51  1.872  20.8       263

    rsi_cross_50      covers 10.0% of baseline bars  !! LOW
    mfi_cross_50      covers 8.7% of baseline bars  !! LOW
    rsi_cross_ma      covers 15.8% of baseline bars  !! LOW
    bb_expand_down    covers 23.9% of baseline bars  !! LOW
    ema_rvol_cross    covers 5.1% of baseline bars  !! LOW


-- Setup 2 Trigger 3 (1h) -- Verdict --

  Baseline (kde_upper_baseline on 1h):  avg WR 50.7%  avg PF 1.551
  KDE (4h): window=200  bw=1  |  RSI(7)<50  MFI(7)<50  RSI/EMA(5)  BB(20,2std)

  [Oscillator  ]  rsi_cross_50      WR lift +1.0pp  avg PF 1.632  PF lift +0.082  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 47.4%  PF 1.350  lift -0.021 / req 0.10  n=475  WR!  cov 9%!  [--]
    ETHUSDT     WR 57.1%  PF 1.998  lift +0.252 / req 0.10  n=478  WR!  cov 9%!  [OK]
    SOLUSDT     WR 47.3%  PF 1.344  lift -0.092 / req 0.10  n=493  WR!  cov 9%!  [--]
    BNBUSDT     WR 55.1%  PF 1.842  lift +0.258 / req 0.10  n=381  WR!  cov 9%!  [OK]
    XRPUSDT     WR 52.0%  PF 1.627  lift +0.011 / req 0.10  n=517  WR!  cov 10%!  [--]
  [Volume      ]  mfi_cross_50      WR lift -0.4pp  avg PF 1.536  PF lift -0.015  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 45.3%  PF 1.243  lift -0.128 / req 0.10  n=459  WR!  cov 9%!  [--]
    ETHUSDT     WR 54.2%  PF 1.777  lift +0.031 / req 0.10  n=426  WR!  cov 8%!  [--]
    SOLUSDT     WR 47.9%  PF 1.381  lift -0.055 / req 0.10  n=459  WR!  cov 8%!  [--]
    BNBUSDT     WR 51.8%  PF 1.611  lift +0.027 / req 0.10  n=365  WR!  cov 8%!  [--]
    XRPUSDT     WR 52.7%  PF 1.669  lift +0.053 / req 0.10  n=450  WR!  cov 9%!  [--]
  [Oscillator  ]  rsi_cross_ma      WR lift -1.3pp  avg PF 1.471  PF lift -0.080  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 45.8%  PF 1.269  lift -0.103 / req 0.10  n=838  WR!  cov 16%!  [--]
    ETHUSDT     WR 52.3%  PF 1.645  lift -0.101 / req 0.10  n=780  WR!  cov 15%!  [--]
    SOLUSDT     WR 48.9%  PF 1.433  lift -0.003 / req 0.10  n=835  WR!  cov 15%!  [--]
    BNBUSDT     WR 50.3%  PF 1.519  lift -0.065 / req 0.10  n=650  WR!  cov 15%!  [--]
    XRPUSDT     WR 49.8%  PF 1.489  lift -0.127 / req 0.10  n=819  WR!  cov 16%!  [--]
  [Volatility  ]  bb_expand_down    WR lift +2.2pp  avg PF 1.705  PF lift +0.154  3/5 pairs  [OK]  warn: WR 4p, low# 5p
    BTCUSDT     WR 51.3%  PF 1.581  lift +0.209 / req 0.10  n=1,224  WR!  cov 23%!  [OK]
    ETHUSDT     WR 58.9%  PF 2.147  lift +0.401 / req 0.10  n=1,296  cov 25%!  [OK]
    SOLUSDT     WR 50.6%  PF 1.538  lift +0.102 / req 0.10  n=1,284  WR!  cov 23%!  [OK]
    BNBUSDT     WR 52.5%  PF 1.658  lift +0.074 / req 0.10  n=1,057  WR!  cov 24%!  [--]
    XRPUSDT     WR 51.6%  PF 1.600  lift -0.016 / req 0.10  n=1,240  WR!  cov 24%!  [--]
  [Trend+Vol   ]  ema_rvol_cross    WR lift +1.4pp  avg PF 1.654  PF lift +0.103  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 48.2%  PF 1.395  lift +0.024 / req 0.10  n=249  WR!  cov 5%!  [--]
    ETHUSDT     WR 52.3%  PF 1.643  lift -0.102 / req 0.10  n=241  WR!  cov 5%!  [--]
    SOLUSDT     WR 48.2%  PF 1.394  lift -0.042 / req 0.10  n=245  WR!  cov 4%!  [--]
    BNBUSDT     WR 56.7%  PF 1.966  lift +0.381 / req 0.10  n=201  WR!  cov 5%!  [OK]
    XRPUSDT     WR 55.5%  PF 1.872  lift +0.256 / req 0.10  n=263  WR!  cov 5%!  [OK]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 3 (1h) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.551  |  Best: bb_expand_down  (avg PF 1.705)

  Warnings (results valid -- interpret with care):
    !! [rsi_cross_50] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rsi_cross_50] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [mfi_cross_50] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [mfi_cross_50] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rsi_cross_ma] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rsi_cross_ma] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [bb_expand_down] WR lift below threshold on: BTCUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [bb_expand_down] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [ema_rvol_cross] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [ema_rvol_cross] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Oscillator]
      [--] rsi_cross_50
      [--] rsi_cross_ma
    [Volume]
      [--] mfi_cross_50
    [Volatility]
      [OK] bb_expand_down      avg PF 1.705
    [Trend+Vol]
      [--] ema_rvol_cross

  Proceed using confirmed trigger(s) for setup 3 construction.
```
