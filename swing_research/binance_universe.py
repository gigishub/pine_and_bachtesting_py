"""Download daily candles for every Binance spot USDT pair, including delisted ones.

Listed pairs come from the REST API; delisted pairs from the monthly archive at data.binance.vision.
Saved as one parquet per symbol in crypto_data/data_binance/1d/.
"""

from __future__ import annotations

import io
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import requests

OUT = Path(__file__).resolve().parent.parent / "crypto_data" / "data_binance" / "1d"
API = "https://api.binance.com/api/v3/klines"
S3 = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"
ARCHIVE = "https://data.binance.vision/data/spot/monthly/klines"

STABLE_OR_FIAT = {"USDC", "BUSD", "TUSD", "USDP", "PAX", "DAI", "FDUSD", "USDSB", "SUSD", "UST", "USTC", "EUR", "GBP",
                  "AUD", "TRY", "BRL", "RUB", "UAH", "NGN", "ZAR", "BIDR", "IDRT", "BVND", "AEUR", "EURI", "XUSD",
                  "USD1", "BFUSD", "USDE", "RLUSD", "PAXG", "WBTC", "WBETH", "BETH", "BKRW", "VAI", "USDS", "FRAX"}
LEVERAGED = re.compile(r"(UP|DOWN|BULL|BEAR)USDT$")
COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume", "trades", "tb_base", "tb_quote", "ignore"]
session = requests.Session()


def s3_prefixes(prefix: str) -> list[str]:
    out, marker = [], ""
    while True:
        r = session.get(S3, params={"delimiter": "/", "prefix": prefix, "marker": marker}, timeout=30)
        root = ET.fromstring(r.content)
        ns = {"s": root.tag.split("}")[0][1:]}
        out += [p.find("s:Prefix", ns).text for p in root.findall("s:CommonPrefixes", ns)]
        out += [k.find("s:Key", ns).text for k in root.findall("s:Contents", ns)]
        if root.find("s:IsTruncated", ns).text != "true":
            return out
        marker = root.find("s:NextMarker", ns).text if root.find("s:NextMarker", ns) is not None else out[-1]


def wanted(sym: str) -> bool:
    return sym.endswith("USDT") and sym[:-4] not in STABLE_OR_FIAT and not LEVERAGED.search(sym)


def to_frame(rows) -> pd.DataFrame:
    df = pd.DataFrame(rows, columns=COLS)
    ts = pd.to_numeric(df["open_time"])
    ts = ts.where(ts < 1e14, ts // 1000)  # archive switched to microseconds in 2025
    df.index = pd.to_datetime(ts, unit="ms", utc=True)
    df.index.name = "Date"
    df = df[["open", "high", "low", "close", "volume", "quote_volume"]].astype(float)
    return df[~df.index.duplicated()].sort_index()


def from_api(sym: str) -> pd.DataFrame:
    rows, start = [], 0
    while True:
        r = session.get(API, params={"symbol": sym, "interval": "1d", "startTime": start, "limit": 1000}, timeout=30)
        r.raise_for_status()
        batch = r.json()
        rows += batch
        if len(batch) < 1000:
            return to_frame(rows)
        start = batch[-1][0] + 1


def from_archive(sym: str) -> pd.DataFrame:
    keys = [k for k in s3_prefixes(f"data/spot/monthly/klines/{sym}/1d/") if k.endswith(".zip")]
    rows = []
    for k in keys:
        r = session.get(f"https://data.binance.vision/{k}", timeout=30)
        if r.status_code != 200:
            continue
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            raw = pd.read_csv(z.open(z.namelist()[0]), header=None)
        if not str(raw.iloc[0, 0]).isdigit():
            raw = raw.iloc[1:]
        rows += raw.values.tolist()
    return to_frame(rows) if rows else pd.DataFrame()


def fetch(sym: str, listed: set[str]) -> str:
    path = OUT / f"{sym}.parquet"
    if path.exists():
        return f"skip {sym}"
    try:
        df = from_api(sym) if sym in listed else from_archive(sym)
    except Exception as e:  # noqa: BLE001
        return f"FAIL {sym}: {e}"
    if df.empty:
        return f"empty {sym}"
    df.to_parquet(path)
    return f"ok {sym} {'listed' if sym in listed else 'delisted'} {df.index[0].date()}→{df.index[-1].date()} ({len(df)})"


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    info = session.get("https://api.binance.com/api/v3/exchangeInfo", timeout=30).json()
    listed = {s["symbol"] for s in info["symbols"] if s["status"] == "TRADING" and s["quoteAsset"] == "USDT"}
    archived = {p.rstrip("/").split("/")[-1] for p in s3_prefixes("data/spot/monthly/klines/")}
    syms = sorted(s for s in archived | listed if wanted(s))
    print(f"{len(syms)} USDT pairs: {len(syms & listed if isinstance(syms, set) else set(syms) & listed)} listed, "
          f"{len(set(syms) - listed)} delisted", flush=True)
    with ThreadPoolExecutor(int(sys.argv[1]) if len(sys.argv) > 1 else 8) as ex:
        for i, msg in enumerate(ex.map(lambda s: fetch(s, listed), syms), 1):
            if not msg.startswith(("ok", "skip")) or i % 50 == 0:
                print(i, msg, flush=True)
    print("DONE")
