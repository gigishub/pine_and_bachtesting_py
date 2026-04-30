# Bear Strategy — Step 2: Setup Level Edge Check  (entry_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `4h` |
| `context_tf` | `1d` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `setup_distance_atr` | `0.5` |
| `vpvr_window` | `200` |

```text

── Per-Pair Results ──

  BTCUSDT
                  wr_%     pf   dur  n_trades
population                                   
all_regime       43.61  1.160  22.3      5886
near_setup       44.39  1.198  18.4      1730
away_from_setup  43.48  1.154  24.1      4126
vpvr_only        50.91  1.556  17.7       603
vwap_only        44.11  1.184  18.6      1290

  ETHUSDT
                  wr_%     pf   dur  n_trades
population                                   
all_regime       41.97  1.085  22.5      5976
near_setup       45.08  1.231  20.0      1797
away_from_setup  40.58  1.024  23.7      4125
vpvr_only        42.74  1.120  18.5       627
vwap_only        45.54  1.254  20.0      1322

  SOLUSDT
                  wr_%     pf   dur  n_trades
population                                   
all_regime       43.36  1.148  22.3      5581
near_setup       43.75  1.167  20.4      1424
away_from_setup  43.48  1.154  23.1      4133
vpvr_only        40.84  1.036  19.3       595
vwap_only        43.34  1.147  20.3      1036

  BNBUSDT
                  wr_%     pf   dur  n_trades
population                                   
all_regime       45.44  1.249  19.0      5046
near_setup       51.16  1.572  19.4      1331
away_from_setup  43.60  1.160  18.9      3697
vpvr_only        55.86  1.898  21.4       401
vwap_only        50.62  1.538  19.4      1047

  XRPUSDT
                  wr_%     pf   dur  n_trades
population                                   
all_regime       43.64  1.162  23.9      6141
near_setup       50.00  1.500  21.9      1572
away_from_setup  41.22  1.052  22.8      4551
vpvr_only        55.26  1.853  27.4       342
vwap_only        49.78  1.487  20.5      1372

── Setup Level Edge Verdict ──

  Baseline (away_from_setup):  avg WR 42.5%  avg PF 1.109

  near_setup            avg WR lift +4.40pp  avg PF 1.333  avg PF lift +0.225  pairs ≥ threshold: 3/5  ✅  ⚠️ WR 2p  ⚠️ weak regime 2p
    BTCUSDT     WR 44.39%  lift +0.91pp / req 2.98pp  PF 1.198  lift +0.044 / req 0.100  trades 1,730  ⚠️ WR  ❌
    ETHUSDT     WR 45.08%  lift +4.49pp / req 2.90pp  PF 1.231  lift +0.207 / req 0.100  trades 1,797  ✅
    SOLUSDT     WR 43.75%  lift +0.27pp / req 3.28pp  PF 1.167  lift +0.013 / req 0.100  trades 1,424  ⚠️ WR  ❌
    BNBUSDT     WR 51.16%  lift +7.56pp / req 3.40pp  PF 1.572  lift +0.412 / req 0.100  trades 1,331  ✅
    XRPUSDT     WR 50.00%  lift +8.78pp / req 3.10pp  PF 1.500  lift +0.448 / req 0.100  trades 1,572  ✅

  vpvr_only             avg WR lift +6.65pp  avg PF 1.492  avg PF lift +0.384  pairs ≥ threshold: 3/5  ✅  ⚠️ WR 2p  ⚠️ low count 5p  ⚠️ weak regime 2p
    BTCUSDT     WR 50.91%  lift +7.43pp / req 5.05pp  PF 1.556  lift +0.402 / req 0.100  trades 603  ✅
    ETHUSDT     WR 42.74%  lift +2.16pp / req 4.90pp  PF 1.120  lift +0.095 / req 0.100  trades 627  ⚠️ WR  ❌
    SOLUSDT     WR 40.84%  lift -2.64pp / req 5.08pp  PF 1.036  lift -0.118 / req 0.100  trades 595  ⚠️ WR  ❌
    BNBUSDT     WR 55.86%  lift +12.26pp / req 6.19pp  PF 1.898  lift +0.739 / req 0.100  trades 401  ✅
    XRPUSDT     WR 55.26%  lift +14.04pp / req 6.65pp  PF 1.853  lift +0.801 / req 0.100  trades 342  ✅

  vwap_only             avg WR lift +4.20pp  avg PF 1.322  avg PF lift +0.213  pairs ≥ threshold: 3/5  ✅  ⚠️ WR 2p  ⚠️ low count 2p  ⚠️ weak regime 2p
    BTCUSDT     WR 44.11%  lift +0.63pp / req 3.45pp  PF 1.184  lift +0.030 / req 0.100  trades 1,290  ⚠️ WR  ❌
    ETHUSDT     WR 45.54%  lift +4.96pp / req 3.38pp  PF 1.254  lift +0.230 / req 0.100  trades 1,322  ✅
    SOLUSDT     WR 43.34%  lift -0.14pp / req 3.85pp  PF 1.147  lift -0.007 / req 0.100  trades 1,036  ⚠️ WR  ❌
    BNBUSDT     WR 50.62%  lift +7.02pp / req 3.83pp  PF 1.538  lift +0.378 / req 0.100  trades 1,047  ✅
    XRPUSDT     WR 49.78%  lift +8.56pp / req 3.32pp  PF 1.487  lift +0.435 / req 0.100  trades 1,372  ✅

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02 if n>50k / 0.05 if n≥10k / 0.10 if n<10k,  consistent across ≥ 3 pairs

  ✅  SETUP EDGE CONFIRMED — at least one setup level creates predictive resistance.
      Best performer: vpvr_only  (avg PF 1.492)
      Warnings (results valid but interpret with care):
        ⚠️  [near_setup] WR lift below threshold on: BTCUSDT, SOLUSDT
        ⚠️  [near_setup] weak regime baseline (PF < 1.1) on: ETHUSDT, XRPUSDT
        ⚠️  [vpvr_only] WR lift below threshold on: ETHUSDT, SOLUSDT
        ⚠️  [vpvr_only] low trade count (<30% of regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
        ⚠️  [vpvr_only] weak regime baseline (PF < 1.1) on: ETHUSDT, XRPUSDT
        ⚠️  [vwap_only] WR lift below threshold on: BTCUSDT, SOLUSDT
        ⚠️  [vwap_only] low trade count (<30% of regime) on: SOLUSDT, BNBUSDT
        ⚠️  [vwap_only] weak regime baseline (PF < 1.1) on: ETHUSDT, XRPUSDT
      Proceed to Step 3 (trigger confirmation).

  ── Component Decision ──
      VPVR outperforms combined → consider cutting AVWAP.
```
