from __future__ import annotations

import json
import re
from dataclasses import asdict
from hashlib import sha1
from pathlib import Path

from ..ups_runner.config import LiveConfig


ROOT_DIR = Path(__file__).resolve().parents[3]
ANALYSIS_DIR = Path(__file__).resolve().parent
ANALYSIS_RUNS_DIR = ANALYSIS_DIR / "runs"
LEGACY_TRADE_LOG_DIR = ROOT_DIR / "trade_logs"
LEGACY_ANALYSIS_TRADE_LOG_DIR = ANALYSIS_DIR / "trade_logs"
LEGACY_ANALYSIS_MERGED_DIR = ANALYSIS_DIR / "merged_trades"
_CONFIG_EXCLUDE_FIELDS = {"api_key", "api_secret"}


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return slug or "default"


def config_public_dict(cfg: LiveConfig) -> dict:
    data = asdict(cfg)
    for key in _CONFIG_EXCLUDE_FIELDS:
        data.pop(key, None)
    return data


def config_fingerprint(cfg: LiveConfig) -> str:
    payload = json.dumps(config_public_dict(cfg), sort_keys=True, separators=(",", ":"))
    return sha1(payload.encode("utf-8")).hexdigest()[:10]


def get_run_dir(cfg: LiveConfig) -> Path:
    fingerprint = config_fingerprint(cfg)
    return (
        ANALYSIS_RUNS_DIR
        / _slug(cfg.profile)
        / _slug(cfg.symbol)
        / _slug(cfg.timeframe)
        / f"{_slug(cfg.category)}__cfg_{fingerprint}"
    )


def get_trade_log_dir(cfg: LiveConfig) -> Path:
    return get_run_dir(cfg) / "trade_logs"


def get_merged_trade_dir(cfg: LiveConfig) -> Path:
    return get_run_dir(cfg) / "merged_trades"


def get_run_config_snapshot_path(cfg: LiveConfig) -> Path:
    return get_run_dir(cfg) / "run_config.json"


def build_analysis_context(cfg: LiveConfig) -> dict[str, str]:
    run_dir = get_run_dir(cfg)
    return {
        "profile": cfg.profile,
        "symbol": cfg.symbol,
        "timeframe": cfg.timeframe,
        "category": cfg.category,
        "config_fingerprint": config_fingerprint(cfg),
        "run_dir": str(run_dir.relative_to(ROOT_DIR)),
    }


def write_run_config_snapshot(cfg: LiveConfig) -> None:
    path = get_run_config_snapshot_path(cfg)
    snapshot = {
        "analysis_context": build_analysis_context(cfg),
        "config": config_public_dict(cfg),
    }
    with open(path, "w") as handle:
        json.dump(snapshot, handle, indent=2, sort_keys=True)


def ensure_analysis_dirs(cfg: LiveConfig) -> None:
    run_dir = get_run_dir(cfg)
    run_dir.mkdir(parents=True, exist_ok=True)
    get_trade_log_dir(cfg).mkdir(parents=True, exist_ok=True)
    get_merged_trade_dir(cfg).mkdir(parents=True, exist_ok=True)
    write_run_config_snapshot(cfg)


def iter_trade_log_paths(log_dir: Path) -> list[Path]:
    seen_trade_ids: set[str] = set()
    paths: list[Path] = []

    for base_dir in [log_dir]:
        if not base_dir.exists():
            continue
        for path in sorted(base_dir.glob("*.json")):
            trade_id = path.stem
            if trade_id in seen_trade_ids:
                continue
            seen_trade_ids.add(trade_id)
            paths.append(path)

    return paths