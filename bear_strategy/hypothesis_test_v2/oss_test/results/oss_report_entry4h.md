## OOS Test: BEAR STRATEGY  |  Entry TF: 4h
_OOS window: 2023-11-02 → 2026-04-22  |  Baseline: random (all candles)  |  Updated: 2026-05-13_

> **Purpose**: verify that the promoted strategy (regime + setup + trigger)
> generalises to completely unseen data.  The baseline is every warmed candle
> — a pure random entry.  PASS requires PF lift ≥ 0.10 AND WR z-score ≥ 1.0.

### Summary
| strategy | avg PF | avg PF lift | pairs OK | verdict |
|----------|--------|-------------|----------|---------|
| bear_rsi_vp_session_poc_or_hvn_break | 1.062 | +0.019 | 1/9 | PASS |

### Per-Strategy Detail

**bear_rsi_vp_session_poc_or_hvn_break**  avg PF 1.062  avg lift +0.019  1/9 pairs  PASS
  ADAUSDT     WR 43.0%  PF 1.130  lift -0.015 / req 0.10  z=-0.1 / req 1.0  n=142  cov 2.6%  [--]
  BNBUSDT     WR 48.4%  PF 1.409  lift +0.500 / req 0.10  z=1.8 / req 1.0  n=64  cov 1.2%  [OK]
  BTCUSDT     WR 39.1%  PF 0.961  lift -0.002 / req 0.10  z=-0.0 / req 1.0  n=105  cov 1.9%  [--]
  DOTUSDT     WR 42.2%  PF 1.095  lift -0.079 / req 0.10  z=-0.4 / req 1.0  n=128  cov 2.4%  [--]
  ETHUSDT     WR 38.7%  PF 0.949  lift +0.054 / req 0.10  z=0.3 / req 1.0  n=111  cov 2.1%  [--]
  LTCUSDT     WR 33.1%  PF 0.741  lift -0.247 / req 0.10  z=-1.5 / req 1.0  n=130  cov 2.4%  [--]
  SOLUSDT     WR 37.1%  PF 0.885  lift -0.067 / req 0.10  z=-0.3 / req 1.0  n=62  cov 1.1%  [--]
  XLMUSDT     WR 47.8%  PF 1.371  lift +0.090 / req 0.10  z=0.4 / req 1.0  n=111  cov 2.1%  [!-]
  XRPUSDT     WR 40.5%  PF 1.020  lift -0.065 / req 0.10  z=-0.3 / req 1.0  n=126  cov 2.3%  [--]

### Population Comparison

#### ADAUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 43.3% | 1.145 | 5,384 |
| bear_rsi_vp_session_poc_or_hvn_break | 43.0% | 1.130 | 142 |

#### BNBUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 37.7% | 0.909 | 5,387 |
| bear_rsi_vp_session_poc_or_hvn_break | 48.4% | 1.409 | 64 |

#### BTCUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 39.1% | 0.963 | 5,396 |
| bear_rsi_vp_session_poc_or_hvn_break | 39.1% | 0.961 | 105 |

#### DOTUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 43.9% | 1.174 | 5,374 |
| bear_rsi_vp_session_poc_or_hvn_break | 42.2% | 1.095 | 128 |

#### ETHUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 37.4% | 0.895 | 5,383 |
| bear_rsi_vp_session_poc_or_hvn_break | 38.7% | 0.949 | 111 |

#### LTCUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 39.7% | 0.988 | 5,378 |
| bear_rsi_vp_session_poc_or_hvn_break | 33.1% | 0.741 | 130 |

#### SOLUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 38.8% | 0.952 | 5,386 |
| bear_rsi_vp_session_poc_or_hvn_break | 37.1% | 0.885 | 62 |

#### XLMUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 46.1% | 1.281 | 5,401 |
| bear_rsi_vp_session_poc_or_hvn_break | 47.8% | 1.371 | 111 |

#### XRPUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 42.0% | 1.085 | 5,381 |
| bear_rsi_vp_session_poc_or_hvn_break | 40.5% | 1.020 | 126 |
