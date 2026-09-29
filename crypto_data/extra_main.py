"""Download 1h candles for every perp that has a funding file but no candles in data/ (saved to data_extra/).

usage: python -m crypto_data.extra_main SHARD NSHARDS
Each coin starts at its first funding date, so no time is spent scanning before its listing.
"""
import logging
import sys
from pathlib import Path

import pandas as pd

from crypto_data.downloader import download_market_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
root = Path(__file__).parent
have = {d.name for d in (root / "data").iterdir() if d.is_dir()}
first = {}
for p in (root / "data_funding").rglob("*_funding_*.parquet"):
    sym = p.name.split("_funding")[0]
    if sym not in have:
        first[sym] = pd.read_parquet(p).index.min()
shard, n = int(sys.argv[1]), int(sys.argv[2])
for sym in sorted(first)[shard::n]:
    start = (first[sym] - pd.Timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
    download_market_data(symbols=[sym], timeframes=["1h"], start_time=start, output_dir=root / "data_extra")
