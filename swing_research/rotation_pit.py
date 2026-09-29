"""Point-in-time momentum rotation backtest on all Binance USDT pairs, including delisted ones.

Each rebalance day: universe = top N coins by 30-day median dollar volume (with min history),
pick the top_k by lookback return, hold equal weight until the next rebalance. Decided on the close,
traded at the next open, holdings drift between rebalances.
"""

from __future__ import annotations

import glob
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "crypto_data" / "data_binance" / "1d"
TEST_START = pd.Timestamp("2024-10-01", tz="UTC")
START = pd.Timestamp("2018-01-01", tz="UTC")
MAX_GAP_DAYS = 7


@dataclass(frozen=True)
class Params:
    lookback: int = 30         # days of return used for ranking
    top_k: int = 3
    universe_n: int = 30       # top N by dollar volume
    liq_window: int = 30       # days of median dollar volume used for the universe ranking
    min_history: int = 60      # days listed before eligible
    rebalance_every: int = 7
    rebalance_offset: int = 0  # which day of the cycle to rebalance on
    btc_filter: bool = True    # only hold coins while BTC's lookback return > 0
    require_positive: bool = False  # only hold coins whose own lookback return > 0
    cost: float = 0.0015       # per side: 0.1% fee + 0.05% slippage
    select: str = "momentum"   # "momentum" | "random" | "all" | "btc"
    seed: int = 0


def load_panel() -> dict[str, pd.DataFrame]:
    """Wide open/close/dollar-volume frames; a symbol with a >7-day gap is split into separate coins."""
    opens, closes, vols = {}, {}, {}
    for path in sorted(glob.glob(str(DATA / "*.parquet"))):
        sym = Path(path).stem
        df = pd.read_parquet(path)
        seg = (df.index.to_series().diff() > pd.Timedelta(days=MAX_GAP_DAYS)).cumsum()
        for i, part in df.groupby(seg):
            name = sym if i == 0 else f"{sym}~{i + 1}"
            opens[name], closes[name], vols[name] = part["open"], part["close"], part["quote_volume"]
    now = pd.Timestamp.now(tz="UTC").normalize()
    frames = {k: pd.DataFrame(v).sort_index() for k, v in [("open", opens), ("close", closes), ("dvol", vols)]}
    return {k: f[(f.index >= START - pd.Timedelta(days=200)) & (f.index < now)] for k, f in frames.items()}


def precompute(panel: dict[str, pd.DataFrame]) -> dict:
    o, c, v = panel["open"], panel["close"], panel["dvol"]
    listed_days = c.notna().cumsum()
    liq = {w: v.rolling(w, min_periods=int(w * 2 / 3)).median() for w in (30, 180)}
    # hold return from this open to the next open; on a coin's last bar, exit at its close
    nxt = o.shift(-1)
    last_bar = c.notna() & c.shift(-1).isna()
    hold = (nxt / o).where(~last_bar, c / o)
    return {"open": o, "close": c, "listed_days": listed_days, "liq": liq, "hold": hold.fillna(1.0)}


def targets(pc: dict, p: Params, day: int, rng: np.random.Generator) -> dict[str, float]:
    c, t = pc["close"], pc["close"].index[day]
    alive = c.iloc[day].notna() & (pc["listed_days"].iloc[day] >= p.min_history)
    liq = pc["liq"][p.liq_window].iloc[day].where(alive).dropna()
    universe = liq.nlargest(p.universe_n).index
    if len(universe) < p.top_k:
        return {}
    mom = (c.iloc[day] / c.iloc[day - p.lookback] - 1)
    if p.btc_filter and not (mom.get("BTCUSDT", np.nan) > 0):
        return {}
    if p.select == "btc":
        return {"BTCUSDT": 1.0}
    if p.select == "all":
        picks = list(universe)
    elif p.select == "random":
        picks = list(rng.choice(universe, size=p.top_k, replace=False))
    else:
        m = mom.reindex(universe).dropna()
        if p.require_positive:
            m = m[m > 0]
        picks = list(m.nlargest(p.top_k).index)
    return {s: 1.0 / len(picks) for s in picks} if picks else {}


def run(pc: dict, p: Params) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Daily equity (at each open), daily turnover, and number of coins held."""
    idx = pc["close"].index
    hold = pc["hold"]
    start = max(idx.searchsorted(START), p.lookback + 1)
    rng = np.random.default_rng(p.seed)
    cols = {s: i for i, s in enumerate(hold.columns)}
    H, C = hold.to_numpy(), pc["close"].to_numpy()
    pos = np.zeros(len(cols))  # value per coin
    cash, pending = 1.0, None
    eq, turn, held = [], [], []
    for d in range(start, len(idx) - 1):
        total = cash + pos.sum()
        traded = 0.0
        if pending is not None:  # trade at this open
            w = np.zeros_like(pos)
            for s, wt in pending.items():
                w[cols[s]] = wt
            traded = np.abs(w * total - pos).sum()
            total -= traded * p.cost
            pos = w * total
            cash = total - pos.sum()
            pending = None
        eq.append(cash + pos.sum())
        turn.append(traded / max(eq[-1], 1e-12))
        held.append(int((pos > 0).sum()))
        pos = pos * H[d]  # move to next open (coins that stop trading exit at their last close)
        dead = np.isnan(C[d + 1]) & (pos > 0)
        if dead.any():
            cash += pos[dead].sum() * (1 - p.cost)
            pos[dead] = 0
        if (d - start) % p.rebalance_every == p.rebalance_offset % p.rebalance_every:
            pending = targets(pc, p, d, rng)
    out_idx = idx[start:len(idx) - 1]
    return pd.Series(eq, out_idx), pd.Series(turn, out_idx), pd.Series(held, out_idx)


def stats(eq: pd.Series, start=None, end=None) -> dict:
    e = eq.loc[start:end]
    e = e / e.iloc[0]
    yrs = (e.index[-1] - e.index[0]).days / 365.25
    r = e.pct_change().dropna()
    return {"CAGR%": 100 * (e.iloc[-1] ** (1 / yrs) - 1), "maxDD%": 100 * (e / e.cummax() - 1).min(),
            "Sharpe": r.mean() / r.std() * np.sqrt(365) if r.std() > 0 else np.nan}
