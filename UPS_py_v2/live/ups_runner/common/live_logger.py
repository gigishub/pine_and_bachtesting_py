from __future__ import annotations

from datetime import datetime, timezone


class LiveLogger:
    """Timestamped stdout logger."""

    def log(self, msg: str) -> None:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now} UTC] {msg}", flush=True)
