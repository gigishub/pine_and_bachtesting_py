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
| `rsi_period` | `14` |
| `rsi_threshold` | `50.0` |
| `mfi_period` | `14` |
| `mfi_threshold` | `50.0` |
| `rsi_ma_period` | `9` |
| `rsi_ma_type` | `ema` |
| `bb_period` | `20` |
| `bb_std` | `2.0` |
| `ema_rvol_period` | `20` |
| `ema_rvol_lookback` | `20` |
| `ema_rvol_threshold` | `1.1` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 1h) --

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  47.76  1.371  20.9      5272
rsi_cross_50        46.85  1.322  20.0       333
mfi_cross_50        42.26  1.098  18.3       310
rsi_cross_ma        48.59  1.418  17.4       638
bb_expand_down      51.31  1.581  27.8      1224
ema_rvol_cross      45.83  1.269  23.9       168

    rsi_cross_50      covers 6.3% of baseline bars  !! LOW
    mfi_cross_50      covers 5.9% of baseline bars  !! LOW
    rsi_cross_ma      covers 12.1% of baseline bars  !! LOW
    bb_expand_down    covers 23.2% of baseline bars  !! LOW
    ema_rvol_cross    covers 3.2% of baseline bars  !! LOW

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  53.79  1.746  21.0      5256
rsi_cross_50        57.75  2.050  18.8       329
mfi_cross_50        49.83  1.490  18.1       287
rsi_cross_ma        52.80  1.678  17.5       608
bb_expand_down      58.87  2.147  25.7      1296
ema_rvol_cross      50.30  1.518  23.5       169

    rsi_cross_50      covers 6.3% of baseline bars  !! LOW
    mfi_cross_50      covers 5.5% of baseline bars  !! LOW
    rsi_cross_ma      covers 11.6% of baseline bars  !! LOW
    bb_expand_down    covers 24.7% of baseline bars  !! LOW
    ema_rvol_cross    covers 3.2% of baseline bars  !! LOW

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  48.91  1.436  18.8      5475
rsi_cross_50        46.29  1.293  18.9       337
mfi_cross_50        47.48  1.356  22.5       318
rsi_cross_ma        51.19  1.573  16.6       629
bb_expand_down      50.62  1.538  22.7      1284
ema_rvol_cross      45.66  1.261  23.5       173

    rsi_cross_50      covers 6.2% of baseline bars  !! LOW
    mfi_cross_50      covers 5.8% of baseline bars  !! LOW
    rsi_cross_ma      covers 11.5% of baseline bars  !! LOW
    bb_expand_down    covers 23.5% of baseline bars  !! LOW
    ema_rvol_cross    covers 3.2% of baseline bars  !! LOW

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.36  1.584  21.1      4367
rsi_cross_50        53.05  1.695  21.5       279
mfi_cross_50        50.77  1.547  21.0       260
rsi_cross_ma        52.79  1.677  18.2       502
bb_expand_down      52.51  1.658  25.1      1057
ema_rvol_cross      54.74  1.815  25.9       137

    rsi_cross_50      covers 6.4% of baseline bars  !! LOW
    mfi_cross_50      covers 6.0% of baseline bars  !! LOW
    rsi_cross_ma      covers 11.5% of baseline bars  !! LOW
    bb_expand_down    covers 24.2% of baseline bars  !! LOW
    ema_rvol_cross    covers 3.1% of baseline bars  !! LOW

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.86  1.616  22.3      5195
rsi_cross_50        55.99  1.908  21.9       384
mfi_cross_50        56.15  1.920  20.1       301
rsi_cross_ma        50.62  1.538  19.9       646
bb_expand_down      51.61  1.600  25.3      1240
ema_rvol_cross      58.08  2.079  23.2       167

    rsi_cross_50      covers 7.4% of baseline bars  !! LOW
    mfi_cross_50      covers 5.8% of baseline bars  !! LOW
    rsi_cross_ma      covers 12.4% of baseline bars  !! LOW
    bb_expand_down    covers 23.9% of baseline bars  !! LOW
    ema_rvol_cross    covers 3.2% of baseline bars  !! LOW


-- Setup 2 Trigger 3 (1h) -- Verdict --

  Baseline (kde_upper_baseline on 1h):  avg WR 50.7%  avg PF 1.551
  KDE (4h): window=200  bw=1  |  RSI(14)<50  MFI(14)<50  RSI/EMA(9)  BB(20,2std)

  [Oscillator  ]  rsi_cross_50      WR lift +1.2pp  avg PF 1.654  PF lift +0.103  3/5 pairs  [OK]  warn: WR 5p, low# 5p
    BTCUSDT     WR 46.8%  PF 1.322  lift -0.049 / req 0.10  n=333  WR!  cov 6%!  [--]
    ETHUSDT     WR 57.8%  PF 2.050  lift +0.305 / req 0.10  n=329  WR!  cov 6%!  [OK]
    SOLUSDT     WR 46.3%  PF 1.293  lift -0.143 / req 0.10  n=337  WR!  cov 6%!  [--]
    BNBUSDT     WR 53.0%  PF 1.695  lift +0.111 / req 0.10  n=279  WR!  cov 6%!  [OK]
    XRPUSDT     WR 56.0%  PF 1.908  lift +0.293 / req 0.10  n=384  WR!  cov 7%!  [OK]
  [Volume      ]  mfi_cross_50      WR lift -1.4pp  avg PF 1.482  PF lift -0.068  1/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 42.3%  PF 1.098  lift -0.274 / req 0.10  n=310  WR!  cov 6%!  [--]
    ETHUSDT     WR 49.8%  PF 1.490  lift -0.256 / req 0.10  n=287  WR!  cov 5%!  [--]
    SOLUSDT     WR 47.5%  PF 1.356  lift -0.080 / req 0.10  n=318  WR!  cov 6%!  [--]
    BNBUSDT     WR 50.8%  PF 1.547  lift -0.037 / req 0.10  n=260  WR!  cov 6%!  [--]
    XRPUSDT     WR 56.1%  PF 1.920  lift +0.305 / req 0.10  n=301  WR!  cov 6%!  [OK]
  [Oscillator  ]  rsi_cross_ma      WR lift +0.5pp  avg PF 1.577  PF lift +0.026  1/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 48.6%  PF 1.418  lift +0.046 / req 0.10  n=638  WR!  cov 12%!  [--]
    ETHUSDT     WR 52.8%  PF 1.678  lift -0.068 / req 0.10  n=608  WR!  cov 12%!  [--]
    SOLUSDT     WR 51.2%  PF 1.573  lift +0.137 / req 0.10  n=629  WR!  cov 11%!  [OK]
    BNBUSDT     WR 52.8%  PF 1.677  lift +0.093 / req 0.10  n=502  WR!  cov 11%!  [--]
    XRPUSDT     WR 50.6%  PF 1.538  lift -0.078 / req 0.10  n=646  WR!  cov 12%!  [--]
  [Volatility  ]  bb_expand_down    WR lift +2.2pp  avg PF 1.705  PF lift +0.154  3/5 pairs  [OK]  warn: WR 4p, low# 5p
    BTCUSDT     WR 51.3%  PF 1.581  lift +0.209 / req 0.10  n=1,224  WR!  cov 23%!  [OK]
    ETHUSDT     WR 58.9%  PF 2.147  lift +0.401 / req 0.10  n=1,296  cov 25%!  [OK]
    SOLUSDT     WR 50.6%  PF 1.538  lift +0.102 / req 0.10  n=1,284  WR!  cov 23%!  [OK]
    BNBUSDT     WR 52.5%  PF 1.658  lift +0.074 / req 0.10  n=1,057  WR!  cov 24%!  [--]
    XRPUSDT     WR 51.6%  PF 1.600  lift -0.016 / req 0.10  n=1,240  WR!  cov 24%!  [--]
  [Trend+Vol   ]  ema_rvol_cross    WR lift +0.2pp  avg PF 1.588  PF lift +0.038  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 45.8%  PF 1.269  lift -0.102 / req 0.10  n=168  WR!  cov 3%!  [--]
    ETHUSDT     WR 50.3%  PF 1.518  lift -0.228 / req 0.10  n=169  WR!  cov 3%!  [--]
    SOLUSDT     WR 45.7%  PF 1.261  lift -0.176 / req 0.10  n=173  WR!  cov 3%!  [--]
    BNBUSDT     WR 54.7%  PF 1.815  lift +0.230 / req 0.10  n=137  WR!  cov 3%!  [OK]
    XRPUSDT     WR 58.1%  PF 2.079  lift +0.463 / req 0.10  n=167  WR!  cov 3%!  [OK]

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
      [OK] rsi_cross_50        avg PF 1.654
      [--] rsi_cross_ma
    [Volume]
      [--] mfi_cross_50
    [Volatility]
      [OK] bb_expand_down      avg PF 1.705
    [Trend+Vol]
      [--] ema_rvol_cross

  Proceed using confirmed trigger(s) for setup 3 construction.
```
