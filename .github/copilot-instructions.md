# Copilot Workspace Instructions

## Project
Python backtesting workspace. Strategies are written in Python using backtesting.py.

## Documentation
Local copies of framework docs are saved in `docs/`. Always check them before answering questions about those libraries.

## Conventions
- Virtual environment: `.venv/`
- Run scripts with: `source .venv/bin/activate && python <script>.py`

## Copilot code style guidance
- Keep Python modules small (~<200 lines). If logic grows, split into a package with `__init__.py`.
- One responsibility per file; avoid mixing data-loading, processing, and output in one module.
- Keep I/O and side effects at the entrypoint level; business logic should be pure functions where feasible.
- Always add or update pytest coverage for nontrivial behavior (`tests/test_*.py`).

## Documentation references
- Full coding conventions in `/Users/andre/Documents/Python_local/pine_script/building_instructions/building_instructions_general.md`


## Python Agent Rules

1. **Ask before creating files** — confirm project root, module location, and what already exists nearby before placing anything.

2. **Put code where it belongs** — new files go inside the closest relevant existing module. Only create a new top-level directory for a genuinely new domain.

3. **One function, one job** — never mix I/O, logic, and output in the same function.

4. **Type hint every function signature.**

5. **Comment the why, not the what** — skip obvious comments; explain non-obvious reasoning.

6. **No `print()` outside entry points** — use `logging` everywhere else.

7. **Never silence exceptions** — every `except` block must log with context and either handle deliberately or re-raise.

8. **No hardcoded secrets or paths** — use `.env` + `python-dotenv`, never commit `.env`.

9. **Delete dead code, don't comment it out.**

10. **Write a test for every non-trivial function** — place it in a `tests/` folder at the relevant module root.