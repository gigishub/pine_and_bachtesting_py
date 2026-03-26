"""Pull recent Bybit data and show raw structure."""
import sys
sys.path.insert(0, ".")

from pybit.unified_trading import HTTP
from UPS_py_v2.live.ups_runner.config import build_config_from_env
from datetime import datetime, timezone, timedelta

cfg = build_config_from_env()
s = HTTP(testnet=cfg.testnet, api_key=cfg.api_key, api_secret=cfg.api_secret)
start_7d = int((datetime.now(timezone.utc) - timedelta(days=7)).timestamp() * 1000)

SEP = "-" * 80

# ── 1. ORDER HISTORY ─────────────────────────────────────────────────────────
print(f"\n{'='*80}\n1. ORDER HISTORY (last 7 days, {cfg.symbol})\n{'='*80}")
oh = s.get_order_history(category="linear", symbol=cfg.symbol,
                          startTime=start_7d, limit=20)["result"]["list"]
print(f"Total returned: {len(oh)}\n")
for o in oh[:5]:
    print(SEP)
    print(f"  orderId        : {o['orderId']}")
    print(f"  orderLinkId    : {o.get('orderLinkId','')}")
    print(f"  side           : {o['side']}")
    print(f"  orderType      : {o['orderType']}")
    print(f"  orderStatus    : {o['orderStatus']}")
    print(f"  price          : {o['price']}")
    print(f"  qty            : {o['qty']}")
    print(f"  cumExecQty     : {o['cumExecQty']}")
    print(f"  cumExecFee     : {o.get('cumExecFee','')}")
    print(f"  avgPrice       : {o.get('avgPrice','')}")
    print(f"  stopOrderType  : {o.get('stopOrderType','')}")
    print(f"  triggerPrice   : {o.get('triggerPrice','')}")
    print(f"  cancelType     : {o.get('cancelType','')}")
    print(f"  createdTime    : {o['createdTime']}")
    print(f"  updatedTime    : {o['updatedTime']}")

# ── 2. EXECUTIONS ─────────────────────────────────────────────────────────────
print(f"\n{'='*80}\n2. EXECUTIONS / FILLS (last 7 days, {cfg.symbol})\n{'='*80}")
execs = s.get_executions(category="linear", symbol=cfg.symbol,
                          startTime=start_7d, limit=20)["result"]["list"]
print(f"Total returned: {len(execs)}\n")
for e in execs[:5]:
    print(SEP)
    print(f"  execId         : {e['execId']}")
    print(f"  orderId        : {e['orderId']}")
    print(f"  orderLinkId    : {e.get('orderLinkId','')}")
    print(f"  side           : {e['side']}")
    print(f"  orderType      : {e['orderType']}")
    print(f"  stopOrderType  : {e.get('stopOrderType','')}")
    print(f"  execPrice      : {e['execPrice']}")
    print(f"  execQty        : {e['execQty']}")
    print(f"  execValue      : {e['execValue']}")
    print(f"  execFee        : {e['execFee']} {e['feeCurrency']}")
    print(f"  feeRate        : {e['feeRate']}")
    print(f"  isMaker        : {e['isMaker']}")
    print(f"  execTime       : {e['execTime']}")
    print(f"  closedSize     : {e.get('closedSize','')}")

# ── 3. CLOSED PNL ─────────────────────────────────────────────────────────────
print(f"\n{'='*80}\n3. CLOSED PNL (last 7 days, {cfg.symbol})\n{'='*80}")
cp = s.get_closed_pnl(category="linear", symbol=cfg.symbol,
                        startTime=start_7d, limit=20)["result"]["list"]
print(f"Total returned: {len(cp)}\n")
for p in cp[:5]:
    print(SEP)
    print(f"  orderId        : {p['orderId']}")
    print(f"  side           : {p['side']}")
    print(f"  orderType      : {p['orderType']}")
    print(f"  execType       : {p['execType']}")
    print(f"  closedSize     : {p['closedSize']}")
    print(f"  avgEntryPrice  : {p['avgEntryPrice']}")
    print(f"  avgExitPrice   : {p['avgExitPrice']}")
    print(f"  closedPnl      : {p['closedPnl']}")
    print(f"  openFee        : {p['openFee']}")
    print(f"  closeFee       : {p['closeFee']}")
    print(f"  leverage       : {p['leverage']}")
    print(f"  fillCount      : {p['fillCount']}")
    print(f"  createdTime    : {p['createdTime']}")
    print(f"  updatedTime    : {p['updatedTime']}")
