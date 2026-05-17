## OOS Test: BEAR STRATEGY  |  Entry TF: 1h
_OOS window: 2023-11-02 → 2026-04-22  |  Baseline: random (all candles)  |  Updated: 2026-05-13_

> **Purpose**: verify that the promoted strategy (regime + setup + trigger)
> generalises to completely unseen data.  The baseline is every warmed candle
> — a pure random entry.  PASS requires PF lift ≥ 0.10 AND WR z-score ≥ 1.0.

### Summary
| strategy | avg PF | avg PF lift | pairs OK | verdict |
|----------|--------|-------------|----------|---------|
| bear_rsi_vp_session_poc_or_hvn_break | 1.078 | -0.008 | 1/9 | PASS |

### Per-Strategy Detail

**bear_rsi_vp_session_poc_or_hvn_break**  avg PF 1.078  avg lift -0.008  1/9 pairs  PASS
  ADAUSDT     WR 43.7%  PF 1.165  lift -0.047 / req 0.10  z=-0.5 / req 1.0  n=604  cov 2.8%  [--]
  BNBUSDT     WR 34.6%  PF 0.793  lift -0.185 / req 0.10  z=-1.6 / req 1.0  n=266  cov 1.2%  [--]
  BTCUSDT     WR 36.4%  PF 0.860  lift -0.096 / req 0.10  z=-1.0 / req 1.0  n=428  cov 2.0%  [--]
  DOTUSDT     WR 45.8%  PF 1.270  lift +0.070 / req 0.10  z=0.6 / req 1.0  n=517  cov 2.4%  [--]
  ETHUSDT     WR 40.4%  PF 1.017  lift +0.046 / req 0.10  z=0.5 / req 1.0  n=438  cov 2.0%  [--]
  LTCUSDT     WR 37.6%  PF 0.906  lift -0.165 / req 0.10  z=-1.9 / req 1.0  n=571  cov 2.6%  [--]
  SOLUSDT     WR 42.0%  PF 1.088  lift +0.046 / req 0.10  z=0.4 / req 1.0  n=314  cov 1.5%  [--]
  XLMUSDT     WR 48.2%  PF 1.397  lift +0.218 / req 0.10  z=2.0 / req 1.0  n=537  cov 2.5%  [OK]
  XRPUSDT     WR 44.5%  PF 1.202  lift +0.042 / req 0.10  z=0.4 / req 1.0  n=517  cov 2.4%  [--]

### Population Comparison

#### ADAUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 44.7% | 1.212 | 21,619 |
| bear_rsi_vp_session_poc_or_hvn_break | 43.7% | 1.165 | 604 |

#### BNBUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 39.5% | 0.978 | 21,629 |
| bear_rsi_vp_session_poc_or_hvn_break | 34.6% | 0.793 | 266 |

#### BTCUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 38.9% | 0.956 | 21,623 |
| bear_rsi_vp_session_poc_or_hvn_break | 36.4% | 0.860 | 428 |

#### DOTUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 44.5% | 1.200 | 21,606 |
| bear_rsi_vp_session_poc_or_hvn_break | 45.8% | 1.270 | 517 |

#### ETHUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 39.3% | 0.971 | 21,606 |
| bear_rsi_vp_session_poc_or_hvn_break | 40.4% | 1.017 | 438 |

#### LTCUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 41.7% | 1.071 | 21,625 |
| bear_rsi_vp_session_poc_or_hvn_break | 37.6% | 0.906 | 571 |

#### SOLUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 41.0% | 1.042 | 21,620 |
| bear_rsi_vp_session_poc_or_hvn_break | 42.0% | 1.088 | 314 |

#### XLMUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 44.0% | 1.179 | 21,627 |
| bear_rsi_vp_session_poc_or_hvn_break | 48.2% | 1.397 | 537 |

#### XRPUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 43.6% | 1.160 | 21,623 |
| bear_rsi_vp_session_poc_or_hvn_break | 44.5% | 1.202 | 517 |
