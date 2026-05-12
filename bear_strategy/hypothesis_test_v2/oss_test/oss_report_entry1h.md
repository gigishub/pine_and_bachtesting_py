## OOS Test: BEAR STRATEGY  |  Entry TF: 1h
_OOS window: 2023-11-02 → 2026-04-22  |  Baseline: random (all candles)  |  Updated: 2026-05-09_

> **Purpose**: verify that the promoted strategy (regime + setup + trigger)
> generalises to completely unseen data.  The baseline is every warmed candle
> — a pure random entry.  PASS requires PF lift ≥ 0.10 AND WR z-score ≥ 1.2.

### Summary
| strategy | avg PF | avg PF lift | pairs OK | verdict |
|----------|--------|-------------|----------|---------|
| bear_rsi_vp_session_poc_or_hvn_break | 1.325 | +0.239 | 4/9 | PASS |

### Per-Strategy Detail

**bear_rsi_vp_session_poc_or_hvn_break**  avg PF 1.325  avg lift +0.239  4/9 pairs  PASS
  ADAUSDT     WR 49.4%  PF 1.463  lift +0.251 / req 0.10  z=1.9 / req 1.2  n=401  cov 1.8%  [OK]
  BNBUSDT     WR 39.3%  PF 0.972  lift -0.006 / req 0.10  z=-0.0 / req 1.2  n=145  cov 0.7%!  [--]
  BTCUSDT     WR 41.9%  PF 1.080  lift +0.124 / req 0.10  z=0.9 / req 1.2  n=246  cov 1.1%  [--]
  DOTUSDT     WR 52.0%  PF 1.624  lift +0.424 / req 0.10  z=2.8 / req 1.2  n=352  cov 1.6%  [OK]
  ETHUSDT     WR 42.5%  PF 1.108  lift +0.137 / req 0.10  z=1.1 / req 1.2  n=299  cov 1.4%  [!-]
  LTCUSDT     WR 42.3%  PF 1.100  lift +0.029 / req 0.10  z=0.2 / req 1.2  n=312  cov 1.4%  [--]
  SOLUSDT     WR 41.7%  PF 1.073  lift +0.031 / req 0.10  z=0.2 / req 1.2  n=235  cov 1.1%  [--]
  XLMUSDT     WR 54.3%  PF 1.785  lift +0.606 / req 0.10  z=3.9 / req 1.2  n=357  cov 1.7%  [OK]
  XRPUSDT     WR 53.4%  PF 1.717  lift +0.557 / req 0.10  z=3.5 / req 1.2  n=311  cov 1.4%  [OK]

"ADAUSDT",
"DOTUSDT",
"ETHUSDT",
"XRPUSDT",
"XLMUSDT",
"LTCUSDT"


### Population Comparison

#### ADAUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 44.7% | 1.212 | 21,619 |
| bear_rsi_vp_session_poc_or_hvn_break | 49.4% | 1.463 | 401 |

#### BNBUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 39.5% | 0.978 | 21,629 |
| bear_rsi_vp_session_poc_or_hvn_break | 39.3% | 0.972 | 145 |

#### BTCUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 38.9% | 0.956 | 21,623 |
| bear_rsi_vp_session_poc_or_hvn_break | 41.9% | 1.080 | 246 |

#### DOTUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 44.5% | 1.200 | 21,606 |
| bear_rsi_vp_session_poc_or_hvn_break | 52.0% | 1.624 | 352 |

#### ETHUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 39.3% | 0.971 | 21,606 |
| bear_rsi_vp_session_poc_or_hvn_break | 42.5% | 1.108 | 299 |

#### LTCUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 41.7% | 1.071 | 21,625 |
| bear_rsi_vp_session_poc_or_hvn_break | 42.3% | 1.100 | 312 |

#### SOLUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 41.0% | 1.042 | 21,620 |
| bear_rsi_vp_session_poc_or_hvn_break | 41.7% | 1.073 | 235 |

#### XLMUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 44.0% | 1.179 | 21,627 |
| bear_rsi_vp_session_poc_or_hvn_break | 54.3% | 1.785 | 357 |

#### XRPUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 43.6% | 1.160 | 21,623 |
| bear_rsi_vp_session_poc_or_hvn_break | 53.4% | 1.717 | 311 |
