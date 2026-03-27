# Python Build Instructions

General best practices for writing clean, maintainable Python in this project.

---

## ⚠️ Before Writing Any Code or Creating Any Files

Always establish context first. If anything below is unclear — **ask before proceeding. Never assume.**

1. **What is the project root?**
   Where is the top-level directory? What is the entry point?
   If not obvious from context, ask before placing any files.

2. **Where does this new code belong?**
   Is this a new top-level module, or a sub-feature inside an existing one?
   - Adding to an existing domain → place it inside that module, not at root
   - Genuinely new domain → only then create a new top-level directory

3. **What already exists nearby?**
   Before creating a file, check if something relevant already exists in a parent or sibling directory.
   Avoid duplicating `config.py`, `runner.py`, `__init__.py`, or helpers that already live elsewhere.

4. **Is the word "project" referring to the whole repo, or a subfolder/feature?**
   In a nested codebase the scope of "the project" can be ambiguous.
   If it's unclear, ask which scope is meant before placing any files.

---

## Project Structure

All structure is relative to the **module root** — the closest directory with an `__init__.py` that represents the feature being built.

For example, in a larger project this might look like:
- `my_project/` — project root
- `my_project/api/auth/` — module root for authentication logic
- `my_project/data/processing/` — module root for data processing logic

**Do not create a new top-level directory unless the feature is clearly a new domain.** Domains are broad, independent concerns. A new helper, connector, or filter is not — it belongs inside an existing one.

Typical layout inside a module root:

```
<module_root>/
├── __init__.py
├── config.py           # module-level constants and env config
├── common/             # shared helpers used within this module only
├── <sub_feature>/      # create a subdir when a concept grows to 2+ files
│   ├── __init__.py
│   └── ...
└── tests/
    └── test_<n>.py
```

One-off utilities (manual backfills, diagnostics, data migrations) that don't belong in any module go in `scripts/` at the project root — not in `main.py` and not cluttering a module.

When a script starts importing from 3+ places or grows past ~150 lines, convert it into a subdirectory.

---

## Separation of Concerns

Each function and file does one thing. Do not mix I/O, logic, and output in the same function.

```python
# ❌ avoid
def process():
    data = open("file.txt").read()
    result = data.upper()
    print(result)

# ✅ preferred — each piece is independently testable and reusable
def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

def transform(text: str) -> str:
    return text.upper()
```

**fetch**, **parse**, **transform**, **output**, and **log** should be separate concerns — never collapsed into one function or file.

---

## Type Hints

Add type hints to all function signatures.

```python
def calculate_pnl(entry: float, exit: float, qty: float) -> float:
    return (exit - entry) * qty
```

---

## Comments

Comment on *why*, not *what*. Add a block comment when multiple lines run together as a logical step.

```python
# ❌ noise
i = i + 1  # increment i

# ✅ explains reasoning
# Bybit returns server time in milliseconds; convert to seconds for consistency
timestamp = server_time / 1000
```

For multi-step sequences:

```python
# --- Normalize OHLCV data before feeding to strategy ---
df = df.dropna(subset=["close"])
df["close"] = df["close"].astype(float)
df = df.sort_values("timestamp").reset_index(drop=True)
```

---

## Logging

**Never use `print()` outside of entry-point scripts.** Use Python's `logging` module everywhere else. Print statements vanish silently in production; logs are traceable, filterable, and persistent.

Set up a logger once per module at the top of the file:

```python
import logging

logger = logging.getLogger(__name__)
```

Configure the root logger once in your entry point only:

```python
# live/ups_live_runner.py (entry point)
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),                        # console
        logging.FileHandler("logs/live_runner.log"),    # file
    ]
)
```

Use the right level:

```python
logger.debug("Candle fetched: %s", candle)       # verbose, dev only
logger.info("Order placed: %s @ %s", side, price) # normal operational events
logger.warning("Retrying fetch, attempt %d", n)   # recoverable issues
logger.error("Order failed: %s", err)             # something went wrong
logger.critical("Exchange connection lost")        # system-level failure
```

---

## Exception Handling

**Never silence exceptions.** A bare `except: pass` means a failure or corrupted state goes completely unnoticed.

```python
# ❌ dangerous — failure disappears silently
try:
    place_order(symbol, qty)
except:
    pass

# ❌ still bad — logged but execution continues as if nothing happened
try:
    place_order(symbol, qty)
except Exception as e:
    logger.error(e)

# ✅ catch specifically, handle deliberately
try:
    place_order(symbol, qty)
except InsufficientFundsError as e:
    logger.error("Insufficient funds for order: %s", e)
    raise  # re-raise if the caller needs to know
except ExchangeConnectionError as e:
    logger.critical("Exchange unreachable: %s", e)
    raise
```

Rules:
- Catch the **most specific exception** available, not `Exception` or bare `except`
- Always log the error with context before handling or re-raising
- If you catch and don't re-raise, you must have a deliberate reason — add a comment explaining why
- Never suppress an exception in critical execution paths or state management

---

## Config and Secrets

No hardcoded values. Use `.env` + `python-dotenv`:

```python
# config.py (inside the relevant module root)
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")
SYMBOL = os.getenv("SYMBOL", "BTCUSDT")
```

`.env` → in `.gitignore`. Commit `.env.example` with placeholder keys.

---

## Dependencies

```
# requirements.txt at project root
python-dotenv==1.0.0
requests==2.31.0
ccxt==4.2.0
pytest==8.0.0
```

For larger projects, split into `requirements.txt` (runtime) and `requirements-dev.txt` (testing/tooling).

---

## Testing

Write a test after any non-trivial function. Tests live in a `tests/` folder at the **module root** they belong to — not always at the project root.

```
my_project/
├── data/
│   ├── fetch.py
│   └── tests/
│       └── test_fetch.py           ← scoped to data module
├── api/
│   └── tests/
│       └── test_auth.py            ← scoped to api module
```

### Default: pytest

```bash
pytest data/tests/
pytest api/tests/
pytest  # runs all discovered tests from project root
```

```python
# backtest/tests/test_fetch.py
from backtest.fetch import parse_candles

def test_parse_candles_returns_expected_keys():
    raw = [[1710000000000, "65000", "65500", "64800", "65200", "10.5"]]
    result = parse_candles(raw)
    assert "close" in result.columns

def test_parse_candles_empty():
    assert parse_candles([]).empty
```

### Lightweight alternative: plain assert script

For quick smoke tests with no framework:

```python
# tests/run_tests.py
from backtest.fetch import parse_candles

def test_parse_candles():
    raw = [[1710000000000, "65000", "65500", "64800", "65200", "10.5"]]
    assert "close" in parse_candles(raw).columns
    print("✓ parse_candles")

if __name__ == "__main__":
    test_parse_candles()
    print("All tests passed.")
```

```bash
python tests/run_tests.py
```

Use pytest for anything beyond a handful of functions.

---

## Git Hygiene

- **Small, focused commits** — one logical change per commit. Not "misc fixes."
- **Meaningful commit messages** — `fix: order size rounding on partial fills` not `update stuff`
- **Never commit `.env`** — add it to `.gitignore` before the first commit, not after
- **Delete dead code, don't comment it out** — git has the history. Commented-out logic is a reliability hazard and clutters the codebase.
- **One branch per feature or fix** — don't build two things on the same branch

Suggested commit message format:
```
<type>: <short description>

feat: add KuCoin candle fetcher
fix: correct timestamp offset in backtest fetch
refactor: split order_manager into place and cancel modules
chore: update ccxt to 4.3.0
```

---

## Changelog

Keep a `CHANGELOG.md` at the project root. Knowing *when* behavior changed and *why* is essential for diagnosing bugs and understanding the evolution of the codebase.

```markdown
# Changelog

## [unreleased]
- Refactored order_manager to separate place and cancel logic

## [2024-03-15]
- Fixed: timestamp offset bug in backtest fetch causing 1-candle lookahead
- Changed: switched default symbol from ETHUSDT to BTCUSDT

## [2024-03-01]
- Added: KuCoin candle fetcher
- Added: stats_logger for live session summaries
```

Minimum entry: **date — what changed — why it changed.**

---

## Naming

| Thing | Convention | Example |
|---|---|---|
| Variables / functions | `snake_case` | `fetch_candles` |
| Classes | `PascalCase` | `OrderManager` |
| Constants | `UPPER_SNAKE` | `MAX_RETRIES` |
| Files / modules | `snake_case` | `order_manager.py` |

---

## Pre-Commit Checklist

- [ ] Confirmed project root and which module this belongs to before creating files
- [ ] No new top-level directory created without a clear domain reason
- [ ] Functions are small and single-purpose
- [ ] Type hints on all function signatures
- [ ] Non-obvious logic has a comment
- [ ] No `print()` outside entry-point scripts — using `logger` instead
- [ ] No silenced exceptions — every `except` block logs and handles deliberately
- [ ] No hardcoded secrets or paths
- [ ] Dead code deleted, not commented out
- [ ] A test exists for new logic, placed in the correct `tests/` folder
- [ ] `CHANGELOG.md` updated if behavior changed
- [ ] `requirements.txt` is up to date
- [ ] `.env` is not staged for commit