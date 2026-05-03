# Bear Strategy -- Setup 2 Trigger 3  (entry_tf=15m  kde_tf=4h)

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

-- Per-Pair Results (baseline = kde_upper_baseline on 15m) --

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  45.41  1.248  22.7     21088
rsi_cross_50        47.07  1.334  19.9      1313
mfi_cross_50        46.83  1.321  20.1      1119
rsi_cross_ma        44.09  1.183  19.8      2504
bb_expand_down      46.45  1.301  25.7      5001
ema_rvol_cross      49.40  1.465  25.2       502

    rsi_cross_50      covers 6.2% of baseline bars  !! LOW
    mfi_cross_50      covers 5.3% of baseline bars  !! LOW
    rsi_cross_ma      covers 11.9% of baseline bars  !! LOW
    bb_expand_down    covers 23.7% of baseline bars  !! LOW
    ema_rvol_cross    covers 2.4% of baseline bars  !! LOW

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  49.83  1.490  20.8     21024
rsi_cross_50        50.04  1.502  18.4      1291
mfi_cross_50        48.67  1.423  18.6      1056
rsi_cross_ma        47.71  1.369  18.0      2467
bb_expand_down      52.18  1.637  23.2      5320
ema_rvol_cross      48.03  1.387  21.6       458

    rsi_cross_50      covers 6.1% of baseline bars  !! LOW
    mfi_cross_50      covers 5.0% of baseline bars  !! LOW
    rsi_cross_ma      covers 11.7% of baseline bars  !! LOW
    bb_expand_down    covers 25.3% of baseline bars  !! LOW
    ema_rvol_cross    covers 2.2% of baseline bars  !! LOW

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  46.71  1.315  20.6     21965
rsi_cross_50        48.53  1.415  18.4      1331
mfi_cross_50        43.32  1.146  19.4      1092
rsi_cross_ma        44.21  1.189  20.0      2617
bb_expand_down      46.29  1.293  23.4      5425
ema_rvol_cross      49.60  1.476  20.9       498

    rsi_cross_50      covers 6.1% of baseline bars  !! LOW
    mfi_cross_50      covers 5.0% of baseline bars  !! LOW
    rsi_cross_ma      covers 11.9% of baseline bars  !! LOW
    bb_expand_down    covers 24.7% of baseline bars  !! LOW
    ema_rvol_cross    covers 2.3% of baseline bars  !! LOW

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  47.65  1.365  20.3     17502
rsi_cross_50        48.81  1.430  18.1      1051
mfi_cross_50        45.26  1.240  23.7       886
rsi_cross_ma        45.80  1.267  18.7      2083
bb_expand_down      46.68  1.313  23.8      4186
ema_rvol_cross      51.06  1.565  21.8       423

    rsi_cross_50      covers 6.0% of baseline bars  !! LOW
    mfi_cross_50      covers 5.1% of baseline bars  !! LOW
    rsi_cross_ma      covers 11.9% of baseline bars  !! LOW
    bb_expand_down    covers 23.9% of baseline bars  !! LOW
    ema_rvol_cross    covers 2.4% of baseline bars  !! LOW

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  48.07  1.389  22.4     20784
rsi_cross_50        47.16  1.339  20.0      1372
mfi_cross_50        46.67  1.312  19.8      1050
rsi_cross_ma        45.66  1.260  18.8      2521
bb_expand_down      45.21  1.238  24.4      4946
ema_rvol_cross      47.83  1.375  26.2       531

    rsi_cross_50      covers 6.6% of baseline bars  !! LOW
    mfi_cross_50      covers 5.1% of baseline bars  !! LOW
    rsi_cross_ma      covers 12.1% of baseline bars  !! LOW
    bb_expand_down    covers 23.8% of baseline bars  !! LOW
    ema_rvol_cross    covers 2.6% of baseline bars  !! LOW


-- Setup 2 Trigger 3 (15m) -- Verdict --

  Baseline (kde_upper_baseline on 15m):  avg WR 47.5%  avg PF 1.361
  KDE (4h): window=200  bw=1  |  RSI(14)<50  MFI(14)<50  RSI/EMA(9)  BB(20,2std)

  [Oscillator  ]  rsi_cross_50      WR lift +0.8pp  avg PF 1.404  PF lift +0.043  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 47.1%  PF 1.334  lift +0.086 / req 0.10  n=1,313  WR!  cov 6%!  [--]
    ETHUSDT     WR 50.0%  PF 1.502  lift +0.012 / req 0.10  n=1,291  WR!  cov 6%!  [--]
    SOLUSDT     WR 48.5%  PF 1.415  lift +0.100 / req 0.10  n=1,331  WR!  cov 6%!  [--]
    BNBUSDT     WR 48.8%  PF 1.430  lift +0.065 / req 0.10  n=1,051  WR!  cov 6%!  [--]
    XRPUSDT     WR 47.2%  PF 1.339  lift -0.050 / req 0.10  n=1,372  WR!  cov 7%!  [--]
  [Volume      ]  mfi_cross_50      WR lift -1.4pp  avg PF 1.288  PF lift -0.073  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 46.8%  PF 1.321  lift +0.073 / req 0.10  n=1,119  WR!  cov 5%!  [--]
    ETHUSDT     WR 48.7%  PF 1.423  lift -0.068 / req 0.10  n=1,056  WR!  cov 5%!  [--]
    SOLUSDT     WR 43.3%  PF 1.146  lift -0.169 / req 0.10  n=1,092  WR!  cov 5%!  [--]
    BNBUSDT     WR 45.3%  PF 1.240  lift -0.125 / req 0.10  n=886  WR!  cov 5%!  [--]
    XRPUSDT     WR 46.7%  PF 1.312  lift -0.076 / req 0.10  n=1,050  WR!  cov 5%!  [--]
  [Oscillator  ]  rsi_cross_ma      WR lift -2.0pp  avg PF 1.254  PF lift -0.108  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 44.1%  PF 1.183  lift -0.065 / req 0.10  n=2,504  WR!  cov 12%!  [--]
    ETHUSDT     WR 47.7%  PF 1.369  lift -0.121 / req 0.10  n=2,467  WR!  cov 12%!  [--]
    SOLUSDT     WR 44.2%  PF 1.189  lift -0.126 / req 0.10  n=2,617  WR!  cov 12%!  [--]
    BNBUSDT     WR 45.8%  PF 1.267  lift -0.098 / req 0.10  n=2,083  WR!  cov 12%!  [--]
    XRPUSDT     WR 45.7%  PF 1.260  lift -0.128 / req 0.10  n=2,521  WR!  cov 12%!  [--]
  [Volatility  ]  bb_expand_down    WR lift -0.2pp  avg PF 1.356  PF lift -0.005  1/5 pairs  [XX]  warn: WR 4p, low# 5p
    BTCUSDT     WR 46.5%  PF 1.301  lift +0.053 / req 0.10  n=5,001  WR!  cov 24%!  [--]
    ETHUSDT     WR 52.2%  PF 1.637  lift +0.147 / req 0.10  n=5,320  cov 25%!  [OK]
    SOLUSDT     WR 46.3%  PF 1.293  lift -0.022 / req 0.10  n=5,425  WR!  cov 25%!  [--]
    BNBUSDT     WR 46.7%  PF 1.313  lift -0.052 / req 0.10  n=4,186  WR!  cov 24%!  [--]
    XRPUSDT     WR 45.2%  PF 1.238  lift -0.151 / req 0.10  n=4,946  WR!  cov 24%!  [--]
  [Trend+Vol   ]  ema_rvol_cross    WR lift +1.7pp  avg PF 1.454  PF lift +0.092  3/5 pairs  [OK]  warn: WR 5p, low# 5p
    BTCUSDT     WR 49.4%  PF 1.465  lift +0.217 / req 0.10  n=502  WR!  cov 2%!  [OK]
    ETHUSDT     WR 48.0%  PF 1.387  lift -0.103 / req 0.10  n=458  WR!  cov 2%!  [--]
    SOLUSDT     WR 49.6%  PF 1.476  lift +0.161 / req 0.10  n=498  WR!  cov 2%!  [OK]
    BNBUSDT     WR 51.1%  PF 1.565  lift +0.200 / req 0.10  n=423  WR!  cov 2%!  [OK]
    XRPUSDT     WR 47.8%  PF 1.375  lift -0.013 / req 0.10  n=531  WR!  cov 3%!  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 3 (15m) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.361  |  Best: ema_rvol_cross  (avg PF 1.454)

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
      [--] bb_expand_down
    [Trend+Vol]
      [OK] ema_rvol_cross      avg PF 1.454

  Proceed using confirmed trigger(s) for setup 3 construction.
```
