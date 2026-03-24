from __future__ import annotations

"""Compatibility entrypoint for the UPS live runner.

The implementation now lives under `UPS_py/live/ups_runner/runner.py`.
"""

try:
    from .ups_runner.runner import UPSLiveRunner, main
except ImportError:  # Supports direct execution: python UPS_py/live/ups_live_runner.py
    from UPS_py.live.ups_runner.runner import UPSLiveRunner, main

__all__ = ["UPSLiveRunner", "main"]

if __name__ == "__main__":
    main()
