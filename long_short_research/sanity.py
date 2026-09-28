"""Engine checks before trusting any edge result: known answers, random signal = no edge, peeking signal = edge."""

from __future__ import annotations

import numpy as np
import pandas as pd

import edge_check as ec


def main() -> None:
    d = ec.build()
    u, c, o = d["universe"], d["close"], d["open"]
    print(f"days {len(c)}, coins ever in universe: {int(u.any().sum())}, "
          f"median universe size in train: {u.loc[ec.TRAIN[0]:ec.TRAIN[1]].sum(axis=1).median():.0f}")
    print("ever in universe:", sorted(u.columns[u.any()]))

    # known answer: BTC 20-day forward return by hand
    t = pd.Timestamp("2021-03-01", tz="UTC")
    i = o.index.get_loc(t)
    manual = o["BTCUSDT"].iloc[i + 1 + 20] / o["BTCUSDT"].iloc[i + 1] - 1
    assert abs(d["fwd"][20].at[t, "BTCUSDT"] - manual) < 1e-12, "forward return mismatch"
    print("known answer BTC fwd20 OK")

    # delisting: a coin's last forward returns exit at its last close
    dead = [s for s in u.columns[u.any()] if c[s].last_valid_index() < c.index[-30]]
    for s in dead[:3]:
        last = c[s].last_valid_index()
        entries = o[s].loc[:last].dropna().index
        day = entries[-4] - pd.Timedelta(days=1)
        want = c[s].loc[last] / o[s].loc[entries[-4]] - 1
        got = d["fwd"][20].at[day, s]
        assert abs(got - want) < 1e-12, (s, got, want)
    print(f"delisted exit at last close OK ({dead[:3]})")

    base = u.copy()
    rng = np.random.default_rng(1)
    rand = pd.DataFrame(rng.random(u.shape) < 0.5, index=u.index, columns=u.columns)
    peek = d["fwd"][20] > 0
    res = [ec.evaluate(d, "random_half", "long", rand, base),
           ec.evaluate(d, "random_half", "short", rand, base),
           ec.evaluate(d, "peek_future", "long", peek, base),
           ec.evaluate(d, "peek_future", "short", ~peek, base)]
    ec.show(ec.table(res), "sanity: random must fail, peeking must pass")
    assert not res[0].passed and not res[1].passed, "random signal passed"
    assert res[2].passed and res[3].passed, "peeking signal failed"
    print("\nall sanity checks passed")


if __name__ == "__main__":
    main()
