from __future__ import annotations

"""Compatibility entrypoint for the UPS live runner.

The implementation lives under `UPS_py_v2/live/ups_runner/strategy_runner/runner.py`.

to run:
python -m UPS_py_v2.live.ups_live_runner 
"""

try:
    from .ups_runner.strategy_runner.runner import LiveRunner, UPSLiveRunner, main
except ImportError:  # Supports direct execution: python UPS_py_v2/live/ups_live_runner.py
    from UPS_py_v2.live.ups_runner.strategy_runner.runner import LiveRunner, UPSLiveRunner, main

__all__ = ["LiveRunner", "UPSLiveRunner", "main"]

if __name__ == "__main__":
    main()
