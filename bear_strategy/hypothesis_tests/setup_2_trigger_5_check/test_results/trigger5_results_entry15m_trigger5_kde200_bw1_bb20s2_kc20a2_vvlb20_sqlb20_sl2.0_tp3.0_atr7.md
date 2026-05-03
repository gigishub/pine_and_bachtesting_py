# Bear Strategy -- Setup 2 Trigger 5  (entry_tf=15m  kde_tf=4h)

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
| `bb_period` | `20` |
| `bb_std` | `2.0` |
| `kc_period` | `20` |
| `kc_atr_mult` | `2.0` |
| `vol_vel_lookback` | `20` |
| `squeeze_lookback` | `20` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 15m) --

  BTCUSDT
                          wr_%     pf   dur  n_trades
population                                           
kde_upper_baseline       45.41  1.248  22.7     21088
momentum_close           48.44  1.409  37.6      1348
falling_tunnel           45.51  1.253  24.8      5225
volatility_velocity      45.28  1.241  22.7     11328
squeeze_snap             43.38  1.149  17.0       521
lower_expansion          45.88  1.271  26.2     10879
keltner_squeeze_release  46.81  1.320  28.2      9155

    momentum_close              covers 6.4% of baseline bars  !! LOW
    falling_tunnel              covers 24.8% of baseline bars  !! LOW
    volatility_velocity         covers 53.7% of baseline bars
    squeeze_snap                covers 2.5% of baseline bars  !! LOW
    lower_expansion             covers 51.6% of baseline bars
    keltner_squeeze_release     covers 43.4% of baseline bars

  ETHUSDT
                          wr_%     pf   dur  n_trades
population                                           
kde_upper_baseline       49.83  1.490  20.8     21024
momentum_close           51.60  1.599  33.1      1533
falling_tunnel           51.40  1.587  22.2      5525
volatility_velocity      49.59  1.476  21.7     11232
squeeze_snap             53.67  1.738  14.9       490
lower_expansion          50.90  1.555  24.1     11266
keltner_squeeze_release  51.16  1.571  24.8      8862

    momentum_close              covers 7.3% of baseline bars  !! LOW
    falling_tunnel              covers 26.3% of baseline bars  !! LOW
    volatility_velocity         covers 53.4% of baseline bars
    squeeze_snap                covers 2.3% of baseline bars  !! LOW
    lower_expansion             covers 53.6% of baseline bars
    keltner_squeeze_release     covers 42.2% of baseline bars

  SOLUSDT
                          wr_%     pf   dur  n_trades
population                                           
kde_upper_baseline       46.71  1.315  20.6     21965
momentum_close           47.52  1.358  30.8      1429
falling_tunnel           46.90  1.325  22.0      5652
volatility_velocity      45.99  1.277  21.3     11815
squeeze_snap             45.66  1.260  15.4       530
lower_expansion          46.86  1.323  23.2     11671
keltner_squeeze_release  49.66  1.480  24.2      9440

    momentum_close              covers 6.5% of baseline bars  !! LOW
    falling_tunnel              covers 25.7% of baseline bars  !! LOW
    volatility_velocity         covers 53.8% of baseline bars
    squeeze_snap                covers 2.4% of baseline bars  !! LOW
    lower_expansion             covers 53.1% of baseline bars
    keltner_squeeze_release     covers 43.0% of baseline bars

  BNBUSDT
                          wr_%     pf   dur  n_trades
population                                           
kde_upper_baseline       47.65  1.365  20.3     17502
momentum_close           47.65  1.365  35.7      1211
falling_tunnel           47.10  1.335  20.5      4476
volatility_velocity      47.79  1.373  21.2      9309
squeeze_snap             42.41  1.104  14.2       349
lower_expansion          47.53  1.359  23.3      9133
keltner_squeeze_release  46.80  1.320  23.0      8457

    momentum_close              covers 6.9% of baseline bars  !! LOW
    falling_tunnel              covers 25.6% of baseline bars  !! LOW
    volatility_velocity         covers 53.2% of baseline bars
    squeeze_snap                covers 2.0% of baseline bars  !! LOW
    lower_expansion             covers 52.2% of baseline bars
    keltner_squeeze_release     covers 48.3% of baseline bars

  XRPUSDT
                          wr_%     pf   dur  n_trades
population                                           
kde_upper_baseline       48.07  1.389  22.4     20784
momentum_close           46.59  1.308  38.0      1318
falling_tunnel           44.57  1.206  23.2      5434
volatility_velocity      47.21  1.342  23.4     10976
squeeze_snap             45.05  1.230  16.5       546
lower_expansion          46.73  1.316  26.1     10914
keltner_squeeze_release  50.93  1.557  27.5      8838

    momentum_close              covers 6.3% of baseline bars  !! LOW
    falling_tunnel              covers 26.1% of baseline bars  !! LOW
    volatility_velocity         covers 52.8% of baseline bars
    squeeze_snap                covers 2.6% of baseline bars  !! LOW
    lower_expansion             covers 52.5% of baseline bars
    keltner_squeeze_release     covers 42.5% of baseline bars


-- Setup 2 Trigger 5 (15m) -- Verdict --

  Baseline (kde_upper_baseline on 15m):  avg WR 47.5%  avg PF 1.361
  KDE (4h): window=200  bw=1  |  BB(20,2std)  KC(20,2atr)

  [Volatility  ]  momentum_close              WR lift +0.8pp  avg PF 1.408  PF lift +0.047  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 48.4%  PF 1.409  lift +0.161 / req 0.10  n=1,348  WR!  cov 6%!  [OK]
    ETHUSDT     WR 51.6%  PF 1.599  lift +0.109 / req 0.10  n=1,533  WR!  cov 7%!  [OK]
    SOLUSDT     WR 47.5%  PF 1.358  lift +0.043 / req 0.10  n=1,429  WR!  cov 7%!  [--]
    BNBUSDT     WR 47.6%  PF 1.365  lift -0.000 / req 0.10  n=1,211  WR!  cov 7%!  [--]
    XRPUSDT     WR 46.6%  PF 1.308  lift -0.080 / req 0.10  n=1,318  WR!  cov 6%!  [--]
  [Volatility  ]  falling_tunnel              WR lift -0.4pp  avg PF 1.341  PF lift -0.020  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 45.5%  PF 1.253  lift +0.005 / req 0.10  n=5,225  WR!  cov 25%!  [--]
    ETHUSDT     WR 51.4%  PF 1.587  lift +0.097 / req 0.10  n=5,525  WR!  cov 26%!  [--]
    SOLUSDT     WR 46.9%  PF 1.325  lift +0.010 / req 0.10  n=5,652  WR!  cov 26%!  [--]
    BNBUSDT     WR 47.1%  PF 1.335  lift -0.030 / req 0.10  n=4,476  WR!  cov 26%!  [--]
    XRPUSDT     WR 44.6%  PF 1.206  lift -0.182 / req 0.10  n=5,434  WR!  cov 26%!  [--]
  [Volatility  ]  volatility_velocity         WR lift -0.4pp  avg PF 1.342  PF lift -0.020  0/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 45.3%  PF 1.241  lift -0.007 / req 0.05  n=11,328  WR!  cov 54%  [--]
    ETHUSDT     WR 49.6%  PF 1.476  lift -0.014 / req 0.05  n=11,232  WR!  cov 53%  [--]
    SOLUSDT     WR 46.0%  PF 1.277  lift -0.037 / req 0.05  n=11,815  WR!  cov 54%  [--]
    BNBUSDT     WR 47.8%  PF 1.373  lift +0.008 / req 0.10  n=9,309  WR!  cov 53%  [--]
    XRPUSDT     WR 47.2%  PF 1.342  lift -0.047 / req 0.05  n=10,976  WR!  cov 53%  [--]
  [Volatility  ]  squeeze_snap                WR lift -1.5pp  avg PF 1.296  PF lift -0.065  1/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 43.4%  PF 1.149  lift -0.099 / req 0.10  n=521  WR!  cov 2%!  [--]
    ETHUSDT     WR 53.7%  PF 1.738  lift +0.248 / req 0.10  n=490  WR!  cov 2%!  [OK]
    SOLUSDT     WR 45.7%  PF 1.260  lift -0.054 / req 0.10  n=530  WR!  cov 2%!  [--]
    BNBUSDT     WR 42.4%  PF 1.104  lift -0.261 / req 0.10  n=349  WR!  cov 2%!  [--]
    XRPUSDT     WR 45.1%  PF 1.230  lift -0.159 / req 0.10  n=546  WR!  cov 3%!  [--]
  [Volatility  ]  lower_expansion             WR lift +0.0pp  avg PF 1.365  PF lift +0.003  1/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 45.9%  PF 1.271  lift +0.024 / req 0.05  n=10,879  WR!  cov 52%  [--]
    ETHUSDT     WR 50.9%  PF 1.555  lift +0.065 / req 0.05  n=11,266  WR!  cov 54%  [OK]
    SOLUSDT     WR 46.9%  PF 1.323  lift +0.008 / req 0.05  n=11,671  WR!  cov 53%  [--]
    BNBUSDT     WR 47.5%  PF 1.359  lift -0.007 / req 0.10  n=9,133  WR!  cov 52%  [--]
    XRPUSDT     WR 46.7%  PF 1.316  lift -0.073 / req 0.05  n=10,914  WR!  cov 53%  [--]
  [Volatility  ]  keltner_squeeze_release     WR lift +1.5pp  avg PF 1.449  PF lift +0.088  2/5 pairs  [XX]  warn: WR 1p
    BTCUSDT     WR 46.8%  PF 1.320  lift +0.072 / req 0.10  n=9,155  cov 43%  [--]
    ETHUSDT     WR 51.2%  PF 1.571  lift +0.081 / req 0.10  n=8,862  cov 42%  [--]
    SOLUSDT     WR 49.7%  PF 1.480  lift +0.165 / req 0.10  n=9,440  cov 43%  [OK]
    BNBUSDT     WR 46.8%  PF 1.320  lift -0.046 / req 0.10  n=8,457  WR!  cov 48%  [--]
    XRPUSDT     WR 50.9%  PF 1.557  lift +0.168 / req 0.10  n=8,838  cov 43%  [OK]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [XX]  SETUP 2 TRIGGER 5 (15m) -- no BB/KC signal improves on kde_upper_baseline.
        Baseline avg PF was 1.361.
      Tuning ideas:
        * Adjust BB period (currently 20)
        * Adjust BB std (currently 2.0)
        * Adjust KC period (currently 20)
        * Adjust KC atr_mult (currently 2.0)
        * Try a different entry TF (currently 15m)
```
