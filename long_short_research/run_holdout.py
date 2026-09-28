"""Frozen stack on validation and test (run once). Same metric as the layer checks."""

from __future__ import annotations

import edge_check as ec
import ideas

FROZEN = [("btc_ret20", "long"), ("btc_ret20", "short"), ("btc_bot_filter", "long")]  # last = live-bot benchmark


def main() -> None:
    d = ec.build()
    u = d["universe"]
    for label, period in (("train", ec.TRAIN), ("validation", ec.VALID), ("test", ec.TEST)):
        res = []
        for name, side in FROZEN:
            fn, kw = ideas.REGIME[name]
            lm, sm = fn(d, **kw)
            res.append(ec.evaluate(d, name, side, lm if side == "long" else sm, u, period=period))
        ec.show(ec.table(res), f"{label} {period[0].date()} → {min(period[1], u.index[-1]).date()}")


if __name__ == "__main__":
    main()
