# RVOL Setup Edge Check

```text

── Per-Pair Results ──

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         42.67  1.116  21.1     94176
rvol_spike          43.82  1.170  37.4      7241
rvol_spike_bearish  42.60  1.113  36.5      3819
rvol_spike_down     42.60  1.113  36.5      3819
    rvol_spike covers 7.7% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 4.1% of regime bars  ⚠️  LOW
    rvol_spike_down covers 4.1% of regime bars  ⚠️  LOW

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         43.60  1.159  20.1     95616
rvol_spike          44.13  1.185  35.4      7138
rvol_spike_bearish  44.23  1.190  34.0      3778
rvol_spike_down     44.23  1.190  34.0      3778
    rvol_spike covers 7.5% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 4.0% of regime bars  ⚠️  LOW
    rvol_spike_down covers 4.0% of regime bars  ⚠️  LOW

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         43.90  1.174  20.1     89549
rvol_spike          45.28  1.241  32.3      6416
rvol_spike_bearish  44.59  1.207  30.5      3395
rvol_spike_down     44.59  1.207  30.5      3395
    rvol_spike covers 7.2% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 3.8% of regime bars  ⚠️  LOW
    rvol_spike_down covers 3.8% of regime bars  ⚠️  LOW

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         43.39  1.150  18.4     81006
rvol_spike          43.37  1.149  29.3      5856
rvol_spike_bearish  42.44  1.106  30.0      2978
rvol_spike_down     42.44  1.106  30.0      2978
    rvol_spike covers 7.2% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 3.7% of regime bars  ⚠️  LOW
    rvol_spike_down covers 3.7% of regime bars  ⚠️  LOW

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         45.23  1.239  21.8     98398
rvol_spike          45.23  1.239  40.9      6684
rvol_spike_bearish  44.78  1.216  37.8      3593
rvol_spike_down     44.78  1.216  37.8      3593
    rvol_spike covers 6.8% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 3.7% of regime bars  ⚠️  LOW
    rvol_spike_down covers 3.7% of regime bars  ⚠️  LOW

── RVOL Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 43.8%  avg PF 1.168
  RVOL config: threshold=1.5×  vol_ma_len=20  min_bars_active=2

  rvol_spike              avg WR lift +0.61pp  avg PF 1.197  avg PF lift +0.029  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 43.82%  lift +1.15pp / req 1.45pp  PF 1.170  lift +0.054 / req 0.100  trades 7,241  cov 7.7% ⚠️  ❌
    ETHUSDT     WR 44.13%  lift +0.53pp / req 1.47pp  PF 1.185  lift +0.025 / req 0.100  trades 7,138  cov 7.5% ⚠️  ❌
    SOLUSDT     WR 45.28%  lift +1.38pp / req 1.55pp  PF 1.241  lift +0.068 / req 0.100  trades 6,416  cov 7.2% ⚠️  ❌
    BNBUSDT     WR 43.37%  lift -0.01pp / req 1.62pp  PF 1.149  lift -0.001 / req 0.100  trades 5,856  cov 7.2% ⚠️  ❌
    XRPUSDT     WR 45.23%  lift -0.01pp / req 1.52pp  PF 1.239  lift -0.000 / req 0.100  trades 6,684  cov 6.8% ⚠️  ❌

  rvol_spike_bearish      avg WR lift -0.03pp  avg PF 1.167  avg PF lift -0.001  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 42.60%  lift -0.07pp / req 2.00pp  PF 1.113  lift -0.003 / req 0.100  trades 3,819  cov 4.1% ⚠️  ❌
    ETHUSDT     WR 44.23%  lift +0.63pp / req 2.02pp  PF 1.190  lift +0.030 / req 0.100  trades 3,778  cov 4.0% ⚠️  ❌
    SOLUSDT     WR 44.59%  lift +0.70pp / req 2.13pp  PF 1.207  lift +0.034 / req 0.100  trades 3,395  cov 3.8% ⚠️  ❌
    BNBUSDT     WR 42.44%  lift -0.94pp / req 2.27pp  PF 1.106  lift -0.043 / req 0.100  trades 2,978  cov 3.7% ⚠️  ❌
    XRPUSDT     WR 44.78%  lift -0.45pp / req 2.08pp  PF 1.216  lift -0.022 / req 0.100  trades 3,593  cov 3.7% ⚠️  ❌

  rvol_spike_down         avg WR lift -0.03pp  avg PF 1.167  avg PF lift -0.001  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 42.60%  lift -0.07pp / req 2.00pp  PF 1.113  lift -0.003 / req 0.100  trades 3,819  cov 4.1% ⚠️  ❌
    ETHUSDT     WR 44.23%  lift +0.63pp / req 2.02pp  PF 1.190  lift +0.030 / req 0.100  trades 3,778  cov 4.0% ⚠️  ❌
    SOLUSDT     WR 44.59%  lift +0.70pp / req 2.13pp  PF 1.207  lift +0.034 / req 0.100  trades 3,395  cov 3.8% ⚠️  ❌
    BNBUSDT     WR 42.44%  lift -0.94pp / req 2.27pp  PF 1.106  lift -0.043 / req 0.100  trades 2,978  cov 3.7% ⚠️  ❌
    XRPUSDT     WR 44.78%  lift -0.45pp / req 2.08pp  PF 1.216  lift -0.022 / req 0.100  trades 3,593  cov 3.7% ⚠️  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 500,  consistent across ≥ 4 of 5 pairs

  ❌  RVOL EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Increase min_bars_active (reduces noise on lower TF)
        • Try rvol_threshold = 2.0 (stricter spike definition)
        • Try vol_ma_len = 10 or 50
        • Try a different entry_tf in config.py
        • Re-examine whether setup layer is needed before trigger layer
```
