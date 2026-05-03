# Bear Strategy -- Setup 2 Trigger 4  (entry_tf=1h  kde_tf=4h)

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
| `rsi_ma_threshold` | `50.0` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 1h) --

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  47.76  1.371  20.9      5272
rsi_below_50        49.73  1.484  24.0      2634
mfi_below_50        49.78  1.487  22.5      2772
rsi_ma_below_50     49.92  1.495  23.7      2416
rsi_below_ma        47.98  1.384  22.6      3076

    rsi_below_50        covers 50.0% of baseline bars
    mfi_below_50        covers 52.6% of baseline bars  !! HIGH
    rsi_ma_below_50     covers 45.8% of baseline bars
    rsi_below_ma        covers 58.3% of baseline bars  !! HIGH

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  53.79  1.746  21.0      5256
rsi_below_50        57.74  2.049  24.9      2707
mfi_below_50        56.22  1.926  23.9      2878
rsi_ma_below_50     59.55  2.208  25.1      2393
rsi_below_ma        54.29  1.782  21.5      3240

    rsi_below_50        covers 51.5% of baseline bars  !! HIGH
    mfi_below_50        covers 54.8% of baseline bars  !! HIGH
    rsi_ma_below_50     covers 45.5% of baseline bars
    rsi_below_ma        covers 61.6% of baseline bars  !! HIGH

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  48.91  1.436  18.8      5475
rsi_below_50        51.22  1.575  19.8      2870
mfi_below_50        50.81  1.550  20.0      3068
rsi_ma_below_50     53.64  1.736  19.7      2554
rsi_below_ma        47.87  1.377  20.1      3261

    rsi_below_50        covers 52.4% of baseline bars  !! HIGH
    mfi_below_50        covers 56.0% of baseline bars  !! HIGH
    rsi_ma_below_50     covers 46.6% of baseline bars
    rsi_below_ma        covers 59.6% of baseline bars  !! HIGH

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.36  1.584  21.1      4367
rsi_below_50        54.16  1.772  23.7      2271
mfi_below_50        52.31  1.645  22.9      2386
rsi_ma_below_50     55.89  1.901  24.0      2011
rsi_below_ma        50.70  1.543  23.1      2637

    rsi_below_50        covers 52.0% of baseline bars  !! HIGH
    mfi_below_50        covers 54.6% of baseline bars  !! HIGH
    rsi_ma_below_50     covers 46.0% of baseline bars
    rsi_below_ma        covers 60.4% of baseline bars  !! HIGH

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.86  1.616  22.3      5195
rsi_below_50        50.47  1.529  25.5      2861
mfi_below_50        52.60  1.665  23.9      2861
rsi_ma_below_50     51.25  1.577  25.3      2689
rsi_below_ma        51.84  1.614  24.1      3077

    rsi_below_50        covers 55.1% of baseline bars  !! HIGH
    mfi_below_50        covers 55.1% of baseline bars  !! HIGH
    rsi_ma_below_50     covers 51.8% of baseline bars  !! HIGH
    rsi_below_ma        covers 59.2% of baseline bars  !! HIGH


-- Setup 2 Trigger 4 (1h) -- Verdict --

  Baseline (kde_upper_baseline on 1h):  avg WR 50.7%  avg PF 1.551
  KDE (4h): window=200  bw=1  |  RSI(14)h50  MFI(14)h50  RSI/EMA(9)h50  RSI<EMA(9)

  [Oscillator  ]  rsi_below_50        WR lift +1.9pp  avg PF 1.682  PF lift +0.131  4/5 pairs  [OK]  warn: WR 3p
    BTCUSDT     WR 49.7%  PF 1.484  lift +0.113 / req 0.10  n=2,634  WR!  cov 50%  [OK]
    ETHUSDT     WR 57.7%  PF 2.049  lift +0.304 / req 0.10  n=2,707  cov 52%  [OK]
    SOLUSDT     WR 51.2%  PF 1.575  lift +0.139 / req 0.10  n=2,870  WR!  cov 52%  [OK]
    BNBUSDT     WR 54.2%  PF 1.772  lift +0.188 / req 0.10  n=2,271  cov 52%  [OK]
    XRPUSDT     WR 50.5%  PF 1.529  lift -0.087 / req 0.10  n=2,861  WR!  cov 55%  [--]
  [Volume      ]  mfi_below_50        WR lift +1.6pp  avg PF 1.655  PF lift +0.104  3/5 pairs  [OK]  warn: WR 4p
    BTCUSDT     WR 49.8%  PF 1.487  lift +0.116 / req 0.10  n=2,772  WR!  cov 53%  [OK]
    ETHUSDT     WR 56.2%  PF 1.926  lift +0.180 / req 0.10  n=2,878  cov 55%  [OK]
    SOLUSDT     WR 50.8%  PF 1.550  lift +0.114 / req 0.10  n=3,068  WR!  cov 56%  [OK]
    BNBUSDT     WR 52.3%  PF 1.645  lift +0.061 / req 0.10  n=2,386  WR!  cov 55%  [--]
    XRPUSDT     WR 52.6%  PF 1.665  lift +0.049 / req 0.10  n=2,861  WR!  cov 55%  [--]
  [Oscillator  ]  rsi_ma_below_50     WR lift +3.3pp  avg PF 1.783  PF lift +0.233  4/5 pairs  [OK]  warn: WR 2p
    BTCUSDT     WR 49.9%  PF 1.495  lift +0.124 / req 0.10  n=2,416  WR!  cov 46%  [OK]
    ETHUSDT     WR 59.5%  PF 2.208  lift +0.462 / req 0.10  n=2,393  cov 46%  [OK]
    SOLUSDT     WR 53.6%  PF 1.736  lift +0.299 / req 0.10  n=2,554  cov 47%  [OK]
    BNBUSDT     WR 55.9%  PF 1.901  lift +0.317 / req 0.10  n=2,011  cov 46%  [OK]
    XRPUSDT     WR 51.2%  PF 1.577  lift -0.039 / req 0.10  n=2,689  WR!  cov 52%  [--]
  [Oscillator  ]  rsi_below_ma        WR lift -0.2pp  avg PF 1.540  PF lift -0.011  0/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 48.0%  PF 1.384  lift +0.012 / req 0.10  n=3,076  WR!  cov 58%  [--]
    ETHUSDT     WR 54.3%  PF 1.782  lift +0.036 / req 0.10  n=3,240  WR!  cov 62%  [--]
    SOLUSDT     WR 47.9%  PF 1.377  lift -0.059 / req 0.10  n=3,261  WR!  cov 60%  [--]
    BNBUSDT     WR 50.7%  PF 1.543  lift -0.041 / req 0.10  n=2,637  WR!  cov 60%  [--]
    XRPUSDT     WR 51.8%  PF 1.614  lift -0.001 / req 0.10  n=3,077  WR!  cov 59%  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 4 (1h) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.551  |  Best: rsi_ma_below_50  (avg PF 1.783)

  Warnings (results valid -- interpret with care):
    !! [rsi_below_50] WR lift below threshold on: BTCUSDT, SOLUSDT, XRPUSDT
    !! [mfi_below_50] WR lift below threshold on: BTCUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rsi_ma_below_50] WR lift below threshold on: BTCUSDT, XRPUSDT
    !! [rsi_below_ma] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Oscillator]
      [OK] rsi_below_50          avg PF 1.682
      [OK] rsi_ma_below_50       avg PF 1.783
      [--] rsi_below_ma
    [Volume]
      [OK] mfi_below_50          avg PF 1.655

  Proceed using confirmed positional filter(s) for setup 3 construction.
```
