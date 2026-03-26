from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .config import LiveConfig
from ..analysis.paths import build_analysis_context, ensure_analysis_dirs, get_trade_log_dir



class SignalLogger:
    """Write one JSON per trade signal to disk. No Bybit API calls — zero latency impact."""

    def __init__(self, cfg: LiveConfig, log_dir: Path | str | None = None) -> None:
        ensure_analysis_dirs(cfg)
        self.log_dir = Path(log_dir) if log_dir else get_trade_log_dir(cfg)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.analysis_context = build_analysis_context(cfg)

    @staticmethod
    def _entry_time_slug(raw_iso: str) -> str:
        dt = datetime.fromisoformat(raw_iso.replace("Z", "+00:00")).astimezone(timezone.utc)
        return dt.strftime("%Y%m%dT%H%M%S%fZ")

    def _allocate_entry_time_path(self, logged_at_utc: str) -> Path:
        base_name = self._entry_time_slug(logged_at_utc)
        path = self.log_dir / f"{base_name}.json"
        if not path.exists():
            return path
        suffix = 1
        while True:
            candidate = self.log_dir / f"{base_name}_{suffix}.json"
            if not candidate.exists():
                return candidate
            suffix += 1

    def _find_trade_path(self, trade_id: str) -> Path | None:
        for path in self.log_dir.glob("*.json"):
            try:
                with open(path) as handle:
                    record = json.load(handle)
            except (json.JSONDecodeError, OSError):
                continue
            if str(record.get("trade_id") or "") == trade_id:
                return path
        return None

    def log_entry_signal(self, trade_id: str, data: dict) -> None:
        """Save signal data to trade_logs/{trade_id}.json before order placement."""
        logged_at_utc = datetime.now(timezone.utc).isoformat()
        record = {
            "trade_id": trade_id,
            "logged_at_utc": logged_at_utc,
            "entry_order_id": None,  # filled in by save_entry_order_id after placement
            "analysis_context": self.analysis_context,
            **data,
        }
        path = self._allocate_entry_time_path(logged_at_utc)
        with open(path, "w") as f:
            json.dump(record, f, indent=2, default=str)

    def save_entry_order_id(self, trade_id: str, order_id: str) -> None:
        """Update signal JSON with the Bybit orderId after placement succeeds."""
        path = self._find_trade_path(trade_id)
        if path is None:
            return
        with open(path) as f:
            record = json.load(f)
        record["entry_order_id"] = order_id
        with open(path, "w") as f:
            json.dump(record, f, indent=2, default=str)
