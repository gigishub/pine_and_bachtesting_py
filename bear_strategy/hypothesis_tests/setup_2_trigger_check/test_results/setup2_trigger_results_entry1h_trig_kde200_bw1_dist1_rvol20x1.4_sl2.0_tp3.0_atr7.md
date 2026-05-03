# Bear Strategy -- Setup 2 Trigger: KDE Upper (4h) + 1h signals  (entry_tf=1h  kde_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `1h` |
| `kde_tf` | `4h` |
| `context_tf` | `1d` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `kde_window` | `200` |
| `kde_bandwidth_mult` | `1.0` |
| `vwap_anchor` | `daily` |
| `vpvr_window` | `50` |
| `vpvr_n_bins` | `50` |
| `setup_distance_atr` | `1.0` |
| `rvol_window` | `20` |
| `rvol_threshold` | `1.4` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 1h) --

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  47.76  1.371  20.9      5272
vwap_only           47.45  1.355  20.7      2101
vpvr_only           42.57  1.112  28.4       350
near_setup          46.90  1.325  21.3      2324
rvol_only           49.16  1.450  28.2      1131
vwap_and_rvol       48.91  1.436  32.3       366
vpvr_and_rvol       42.25  1.098  31.1        71
near_and_rvol       47.82  1.374  31.7       412

    vwap_only               covers 39.9% of baseline bars
    vpvr_only               covers 6.6% of baseline bars  !! LOW
    near_setup              covers 44.1% of baseline bars
    rvol_only               covers 21.5% of baseline bars  !! LOW
    vwap_and_rvol           covers 6.9% of baseline bars  !! LOW
    vpvr_and_rvol           covers 1.3% of baseline bars  !! LOW
    near_and_rvol           covers 7.8% of baseline bars  !! LOW

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  53.79  1.746  21.0      5256
vwap_only           56.71  1.965  17.9      2049
vpvr_only           50.67  1.541  23.9       300
near_setup          56.06  1.913  18.4      2246
rvol_only           54.56  1.801  32.1      1173
vwap_and_rvol       54.25  1.779  32.0       400
vpvr_and_rvol       37.70  0.908  39.4        61
near_and_rvol       52.37  1.649  31.6       443

    vwap_only               covers 39.0% of baseline bars
    vpvr_only               covers 5.7% of baseline bars  !! LOW
    near_setup              covers 42.7% of baseline bars
    rvol_only               covers 22.3% of baseline bars  !! LOW
    vwap_and_rvol           covers 7.6% of baseline bars  !! LOW
    vpvr_and_rvol           covers 1.2% of baseline bars  !! LOW
    near_and_rvol           covers 8.4% of baseline bars  !! LOW

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  48.91  1.436  18.8      5475
vwap_only           50.29  1.518  17.5      2060
vpvr_only           48.16  1.393  15.3       380
near_setup          50.48  1.529  17.1      2314
rvol_only           51.93  1.620  25.5      1063
vwap_and_rvol       50.33  1.520  23.4       300
vpvr_and_rvol       56.25  1.929  19.9        64
near_and_rvol       51.58  1.598  22.7       349

    vwap_only               covers 37.6% of baseline bars
    vpvr_only               covers 6.9% of baseline bars  !! LOW
    near_setup              covers 42.3% of baseline bars
    rvol_only               covers 19.4% of baseline bars  !! LOW
    vwap_and_rvol           covers 5.5% of baseline bars  !! LOW
    vpvr_and_rvol           covers 1.2% of baseline bars  !! LOW
    near_and_rvol           covers 6.4% of baseline bars  !! LOW

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.36  1.584  21.1      4367
vwap_only           52.87  1.683  20.4      1706
vpvr_only           61.70  2.417  16.4       235
near_setup          53.37  1.717  19.9      1838
rvol_only           49.89  1.493  27.9       904
vwap_and_rvol       52.09  1.631  25.9       311
vpvr_and_rvol       58.82  2.143  35.0        34
near_and_rvol       52.24  1.641  25.0       335

    vwap_only               covers 39.1% of baseline bars
    vpvr_only               covers 5.4% of baseline bars  !! LOW
    near_setup              covers 42.1% of baseline bars
    rvol_only               covers 20.7% of baseline bars  !! LOW
    vwap_and_rvol           covers 7.1% of baseline bars  !! LOW
    vpvr_and_rvol           covers 0.8% of baseline bars  !! LOW
    near_and_rvol           covers 7.7% of baseline bars  !! LOW

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.86  1.616  22.3      5195
vwap_only           52.01  1.626  23.7      2186
vpvr_only           62.29  2.478  19.3       236
near_setup          52.74  1.674  23.3      2321
rvol_only           53.89  1.753  30.6       989
vwap_and_rvol       51.66  1.603  38.8       362
vpvr_and_rvol       66.67  3.000  23.9        51
near_and_rvol       53.52  1.727  37.5       398

    vwap_only               covers 42.1% of baseline bars
    vpvr_only               covers 4.5% of baseline bars  !! LOW
    near_setup              covers 44.7% of baseline bars
    rvol_only               covers 19.0% of baseline bars  !! LOW
    vwap_and_rvol           covers 7.0% of baseline bars  !! LOW
    vpvr_and_rvol           covers 1.0% of baseline bars  !! LOW
    near_and_rvol           covers 7.7% of baseline bars  !! LOW


-- Setup 2 Trigger (1h) -- Verdict --

  Baseline (kde_upper_baseline on 1h):  avg WR 50.7%  avg PF 1.551
  KDE (4h): window=200  bw=1  |  dist=1xATR(1h)  |  RVOL: 20 bars (5h) threshold=1.4


  [Level only   ]  vwap_only               WR lift +1.1pp  avg PF 1.629  PF lift +0.079  1/5 pairs  [XX]  warn: WR 4p
    BTCUSDT     WR 47.5%  PF 1.355  lift -0.017 / req 0.10  n=2,101  WR!  cov 40%  [--]
    ETHUSDT     WR 56.7%  PF 1.965  lift +0.219 / req 0.10  n=2,049  cov 39%  [OK]
    SOLUSDT     WR 50.3%  PF 1.518  lift +0.081 / req 0.10  n=2,060  WR!  cov 38%  [--]
    BNBUSDT     WR 52.9%  PF 1.683  lift +0.099 / req 0.10  n=1,706  WR!  cov 39%  [--]
    XRPUSDT     WR 52.0%  PF 1.626  lift +0.010 / req 0.10  n=2,186  WR!  cov 42%  [--]
  [Level only   ]  vpvr_only               WR lift +2.3pp  avg PF 1.788  PF lift +0.237  2/5 pairs  [XX]  warn: WR 3p, low# 5p
    BTCUSDT     WR 42.6%  PF 1.112  lift -0.260 / req 0.10  n=350  WR!  cov 7%!  [--]
    ETHUSDT     WR 50.7%  PF 1.541  lift -0.205 / req 0.10  n=300  WR!  cov 6%!  [--]
    SOLUSDT     WR 48.2%  PF 1.393  lift -0.043 / req 0.10  n=380  WR!  cov 7%!  [--]
    BNBUSDT     WR 61.7%  PF 2.417  lift +0.833 / req 0.10  n=235  cov 5%!  [OK]
    XRPUSDT     WR 62.3%  PF 2.478  lift +0.862 / req 0.10  n=236  cov 5%!  [OK]
  [Level only   ]  near_setup              WR lift +1.2pp  avg PF 1.632  PF lift +0.081  2/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 46.9%  PF 1.325  lift -0.047 / req 0.10  n=2,324  WR!  cov 44%  [--]
    ETHUSDT     WR 56.1%  PF 1.913  lift +0.168 / req 0.10  n=2,246  WR!  cov 43%  [OK]
    SOLUSDT     WR 50.5%  PF 1.529  lift +0.093 / req 0.10  n=2,314  WR!  cov 42%  [--]
    BNBUSDT     WR 53.4%  PF 1.717  lift +0.133 / req 0.10  n=1,838  WR!  cov 42%  [OK]
    XRPUSDT     WR 52.7%  PF 1.674  lift +0.058 / req 0.10  n=2,321  WR!  cov 45%  [--]

  [RVOL only    ]  rvol_only               WR lift +1.2pp  avg PF 1.624  PF lift +0.073  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 49.2%  PF 1.450  lift +0.079 / req 0.10  n=1,131  WR!  cov 21%!  [--]
    ETHUSDT     WR 54.6%  PF 1.801  lift +0.055 / req 0.10  n=1,173  WR!  cov 22%!  [--]
    SOLUSDT     WR 51.9%  PF 1.620  lift +0.184 / req 0.10  n=1,063  WR!  cov 19%!  [OK]
    BNBUSDT     WR 49.9%  PF 1.493  lift -0.091 / req 0.10  n=904  WR!  cov 21%!  [--]
    XRPUSDT     WR 53.9%  PF 1.753  lift +0.138 / req 0.10  n=989  WR!  cov 19%!  [OK]

  [Level + RVOL ]  vwap_and_rvol           WR lift +0.7pp  avg PF 1.594  PF lift +0.043  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 48.9%  PF 1.436  lift +0.064 / req 0.10  n=366  WR!  cov 7%!  [--]
    ETHUSDT     WR 54.2%  PF 1.779  lift +0.033 / req 0.10  n=400  WR!  cov 8%!  [--]
    SOLUSDT     WR 50.3%  PF 1.520  lift +0.084 / req 0.10  n=300  WR!  cov 5%!  [--]
    BNBUSDT     WR 52.1%  PF 1.631  lift +0.047 / req 0.10  n=311  WR!  cov 7%!  [--]
    XRPUSDT     WR 51.7%  PF 1.603  lift -0.013 / req 0.10  n=362  WR!  cov 7%!  [--]
  [Level + RVOL ]  vpvr_and_rvol           WR lift +1.6pp  avg PF 1.815  PF lift +0.265  3/5 pairs  [OK]  warn: WR 5p, low# 5p
    BTCUSDT     WR 42.3%  PF 1.098  lift -0.274 / req 0.10  n=71  WR!  cov 1%!  [--]
    ETHUSDT     WR 37.7%  PF 0.908  lift -0.838 / req 0.10  n=61  WR!  cov 1%!  [--]
    SOLUSDT     WR 56.2%  PF 1.929  lift +0.492 / req 0.10  n=64  WR!  cov 1%!  [OK]
    BNBUSDT     WR 58.8%  PF 2.143  lift +0.559 / req 0.10  n=34  WR!  cov 1%!  [OK]
    XRPUSDT     WR 66.7%  PF 3.000  lift +1.384 / req 0.10  n=51  WR!  cov 1%!  [OK]
  [Level + RVOL ]  near_and_rvol           WR lift +0.8pp  avg PF 1.598  PF lift +0.047  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 47.8%  PF 1.374  lift +0.003 / req 0.10  n=412  WR!  cov 8%!  [--]
    ETHUSDT     WR 52.4%  PF 1.649  lift -0.096 / req 0.10  n=443  WR!  cov 8%!  [--]
    SOLUSDT     WR 51.6%  PF 1.598  lift +0.161 / req 0.10  n=349  WR!  cov 6%!  [OK]
    BNBUSDT     WR 52.2%  PF 1.641  lift +0.057 / req 0.10  n=335  WR!  cov 8%!  [--]
    XRPUSDT     WR 53.5%  PF 1.727  lift +0.111 / req 0.10  n=398  WR!  cov 8%!  [OK]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER (1h) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.551  |  Best: vpvr_and_rvol  (avg PF 1.815)

  Warnings (results valid -- interpret with care):
    !! [vwap_only] WR lift below threshold on: BTCUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [vpvr_only] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT
    !! [vpvr_only] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [near_setup] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rvol_only] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rvol_only] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [vwap_and_rvol] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [vwap_and_rvol] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [vpvr_and_rvol] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [vpvr_and_rvol] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [near_and_rvol] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [near_and_rvol] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Level proximity]
      [--] near_setup
      [--] vpvr_only
      [--] vwap_only
    [RVOL]
      [--] rvol_only
    [Level + RVOL]
      [OK] vpvr_and_rvol           avg PF 1.815
      [--] near_and_rvol
      [--] vwap_and_rvol

  Proceed to setup 3 using confirmed 15m trigger combination(s).
```
