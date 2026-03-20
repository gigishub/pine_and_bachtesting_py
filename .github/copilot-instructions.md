# Copilot Workspace Instructions

## Project
Python backtesting workspace. Strategies are written in Python using backtesting.py.

## Documentation
Local copies of framework docs are saved in `docs/`. Always check them before answering questions about those libraries.

| Library | Index file |
|---------|-----------|
| backtesting.py | `docs/backtesting/_index.md` |

When working with backtesting.py:
1. Read `docs/backtesting/_index.md` to find the right file.
2. Read only the relevant file(s) from `docs/backtesting/`.
3. Do not guess API signatures — verify from the docs.

## Conventions
- Virtual environment: `.venv/`
- Run scripts with: `source .venv/bin/activate && python <script>.py`
- Strategies go long only (use `self.position.close()` to exit, not `self.sell()`) unless shorting is explicitly requested.
