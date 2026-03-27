from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..ups_runner.config import build_config_from_env
from .bybit_merge import build_bybit_client, fetch_symbol_bundle, iso_utc_from_ms, parse_float, parse_int
from .paths import ANALYSIS_RUNS_DIR, ROOT_DIR, ensure_analysis_dirs, get_merged_trade_dir, get_trade_log_dir, iter_trade_log_paths


'''
Normal merge for current config only:
python -m UPS_py_v2.live.analysis.merge_trade_logs

Merge everything at once:
python -m UPS_py_v2.live.analysis.merge_trade_logs --all-runs

'''



def _parse_iso_utc(raw: str | None) -> datetime | None:
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def _to_ms(raw: str | None) -> int | None:
    dt = _parse_iso_utc(raw)
    if dt is None:
        return None
    return int(dt.astimezone(timezone.utc).timestamp() * 1000)


def _entry_time_slug(raw_iso: str | None) -> str | None:
    dt = _parse_iso_utc(raw_iso)
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def _sort_by_time(items: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    return sorted(items, key=lambda item: parse_int(item.get(key)) or 0)


def load_trade_logs(log_dir: Path) -> list[dict[str, Any]]:
    logs: list[dict[str, Any]] = []
    for path in iter_trade_log_paths(log_dir):
        with open(path) as handle:
            record = json.load(handle)
        record["_source_path"] = str(path.relative_to(ROOT_DIR))
        logs.append(record)
    return sorted(logs, key=lambda item: item.get("logged_at_utc") or "")


def symbol_time_bounds(logs: list[dict[str, Any]]) -> dict[str, tuple[int, int]]:
    bounds: dict[str, tuple[int, int]] = {}
    padding_ms = 24 * 60 * 60 * 1000
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)

    for log in logs:
        symbol = str(log.get("symbol") or "")
        if not symbol:
            continue
        logged_ms = _to_ms(log.get("logged_at_utc")) or now_ms
        start_ms = max(0, logged_ms - padding_ms)
        end_ms = logged_ms + padding_ms
        if symbol not in bounds:
            bounds[symbol] = (start_ms, end_ms)
            continue
        current_start, current_end = bounds[symbol]
        bounds[symbol] = (min(current_start, start_ms), max(current_end, end_ms))

    return bounds


def summarize_entry_order(order: dict[str, Any] | None, entry_execs: list[dict[str, Any]]) -> dict[str, Any]:
    total_exec_fee = sum(parse_float(item.get("execFee")) or 0.0 for item in entry_execs)
    fee_currencies = sorted({str(item.get("feeCurrency") or "") for item in entry_execs if item.get("feeCurrency")})
    fill_time_ms = min((parse_int(item.get("execTime")) or 0 for item in entry_execs), default=0) or None

    avg_entry_price = None
    if order is not None:
        avg_entry_price = parse_float(order.get("avgPrice"))
    if avg_entry_price is None and entry_execs:
        avg_entry_price = parse_float(entry_execs[0].get("execPrice"))

    filled_qty = None
    if order is not None:
        filled_qty = parse_float(order.get("cumExecQty"))
    if filled_qty is None and entry_execs:
        filled_qty = sum(parse_float(item.get("execQty")) or 0.0 for item in entry_execs)

    return {
        "status": order.get("orderStatus") if order else None,
        "created_time_utc": iso_utc_from_ms(order.get("createdTime")) if order else None,
        "updated_time_utc": iso_utc_from_ms(order.get("updatedTime")) if order else None,
        "filled_time_utc": iso_utc_from_ms(fill_time_ms),
        "avg_price": avg_entry_price,
        "filled_qty": filled_qty,
        "exec_fee_total": total_exec_fee,
        "fee_currencies": fee_currencies,
    }


def _expected_close_side(log: dict[str, Any]) -> str | None:
    signal_type = str(log.get("signal_type") or "").lower()
    if signal_type == "long":
        # Closing a long requires a Sell.
        return "Sell"
    if signal_type == "short":
        # Closing a short requires a Buy.
        return "Buy"
    return None


def match_closed_record(
    log: dict[str, Any],
    order: dict[str, Any] | None,
    entry_execs: list[dict[str, Any]],
    closed_records: list[dict[str, Any]],
    used_close_order_ids: set[str],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    if not log.get("entry_order_id"):
        return None, None
    if order is None and not entry_execs:
        return None, None

    expected_side = _expected_close_side(log)
    if expected_side is None:
        return None, None

    reference_time_ms = None
    if entry_execs:
        reference_time_ms = min(parse_int(item.get("execTime")) or 0 for item in entry_execs) or None
    if reference_time_ms is None and order is not None:
        reference_time_ms = parse_int(order.get("createdTime"))
    if reference_time_ms is None:
        reference_time_ms = _to_ms(log.get("logged_at_utc"))

    reference_qty = None
    if order is not None:
        reference_qty = parse_float(order.get("cumExecQty"))
    if reference_qty is None:
        reference_qty = parse_float(log.get("intended_qty"))

    reference_price = None
    if order is not None:
        reference_price = parse_float(order.get("avgPrice"))
    if reference_price is None and entry_execs:
        reference_price = parse_float(entry_execs[0].get("execPrice"))
    if reference_price is None:
        reference_price = parse_float(log.get("intended_entry_price"))

    best_record: dict[str, Any] | None = None
    best_meta: dict[str, Any] | None = None
    best_score: tuple[float, float, float] | None = None

    for record in closed_records:
        exit_order_id = str(record.get("orderId") or "")
        if not exit_order_id or exit_order_id in used_close_order_ids:
            continue
        if record.get("side") != expected_side:
            continue

        created_ms = parse_int(record.get("createdTime"))
        closed_size = parse_float(record.get("closedSize"))
        avg_entry_price = parse_float(record.get("avgEntryPrice"))

        # A close record cannot happen before the reference entry time.
        if created_ms is not None and reference_time_ms is not None and created_ms < reference_time_ms:
            continue

        time_diff_ms = abs((created_ms or reference_time_ms or 0) - (reference_time_ms or 0))
        qty_rel_diff = abs((closed_size or 0.0) - (reference_qty or 0.0)) / max(abs(reference_qty or 0.0), 1e-9)
        price_rel_diff = abs((avg_entry_price or 0.0) - (reference_price or 0.0)) / max(abs(reference_price or 0.0), 1e-9)
        score = (float(time_diff_ms), float(qty_rel_diff), float(price_rel_diff))

        if best_score is None or score < best_score:
            best_score = score
            best_record = record
            best_meta = {
                "matched_on": "symbol+side+createdTime+qty+avgEntryPrice",
                "time_diff_ms": time_diff_ms,
                "qty_relative_diff": qty_rel_diff,
                "entry_price_relative_diff": price_rel_diff,
            }

    if best_score is None:
        return None, None

    if best_score[0] > 12 * 60 * 60 * 1000 and best_score[1] > 0.25 and best_score[2] > 0.01:
        return None, None

    return best_record, best_meta


def build_merged_record(
    log: dict[str, Any],
    orders_by_id: dict[str, dict[str, Any]],
    execs_by_order_id: dict[str, list[dict[str, Any]]],
    closed_records: list[dict[str, Any]],
    used_close_order_ids: set[str],
) -> dict[str, Any]:
    trade_id = str(log.get("trade_id") or "")
    entry_order_id = str(log.get("entry_order_id") or "")
    entry_order = orders_by_id.get(entry_order_id) if entry_order_id else None
    entry_execs = _sort_by_time(execs_by_order_id.get(entry_order_id, []), "execTime") if entry_order_id else []
    entry_summary = summarize_entry_order(entry_order, entry_execs)

    closed_record, match_meta = match_closed_record(log, entry_order, entry_execs, closed_records, used_close_order_ids)
    exit_order_id = str(closed_record.get("orderId") or "") if closed_record else ""
    if exit_order_id:
        used_close_order_ids.add(exit_order_id)
    exit_order = orders_by_id.get(exit_order_id) if exit_order_id else None
    exit_execs = _sort_by_time(execs_by_order_id.get(exit_order_id, []), "execTime") if exit_order_id else []

    if not entry_order_id:
        lifecycle_status = "signal_logged_no_entry_order"
    elif closed_record is not None:
        lifecycle_status = "closed"
    elif entry_order is None:
        lifecycle_status = "entry_order_not_found_in_history"
    else:
        lifecycle_status = "open_or_pending"

    merged = {
        "trade_id": trade_id,
        "order_link_id": trade_id,
        "symbol": log.get("symbol"),
        "signal_type": log.get("signal_type"),
        "lifecycle_status": lifecycle_status,
        "source": {
            "trade_log_path": log.get("_source_path"),
        },
        "signal": {key: value for key, value in log.items() if not key.startswith("_")},
        "summary": {
            "entry_order_id": entry_order_id or None,
            "entry_status": entry_summary["status"],
            "entry_created_time_utc": entry_summary["created_time_utc"],
            "entry_filled_time_utc": entry_summary["filled_time_utc"],
            "entry_avg_price": entry_summary["avg_price"],
            "entry_filled_qty": entry_summary["filled_qty"],
            "entry_exec_fee_total": entry_summary["exec_fee_total"],
            "entry_fee_currencies": entry_summary["fee_currencies"],
            "exit_order_id": exit_order_id or None,
            "exit_time_utc": iso_utc_from_ms(closed_record.get("updatedTime")) if closed_record else None,
            "avg_exit_price": parse_float(closed_record.get("avgExitPrice")) if closed_record else None,
            "closed_pnl": parse_float(closed_record.get("closedPnl")) if closed_record else None,
            "open_fee": parse_float(closed_record.get("openFee")) if closed_record else None,
            "close_fee": parse_float(closed_record.get("closeFee")) if closed_record else None,
            "closed_size": parse_float(closed_record.get("closedSize")) if closed_record else None,
            "leverage": parse_float(closed_record.get("leverage")) if closed_record else None,
        },
        "matching": match_meta,
        "bybit": {
            "entry_order": entry_order,
            "entry_executions": entry_execs,
            "exit_order": exit_order,
            "exit_executions": exit_execs,
            "closed_pnl": closed_record,
        },
    }
    return merged


def write_outputs(records: list[dict[str, Any]], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    used_names: set[str] = set()
    for record in records:
        summary = record.get("summary", {}) if isinstance(record.get("summary"), dict) else {}
        signal = record.get("signal", {}) if isinstance(record.get("signal"), dict) else {}
        entry_time = summary.get("entry_created_time_utc") or signal.get("logged_at_utc")
        base_name = _entry_time_slug(entry_time)
        if not base_name:
            continue

        name = base_name
        suffix = 1
        while name in used_names or (out_dir / f"{name}.json").exists():
            name = f"{base_name}_{suffix}"
            suffix += 1
        used_names.add(name)

        path = out_dir / f"{name}.json"
        with open(path, "w") as handle:
            json.dump(record, handle, indent=2, default=str)

    with open(out_dir / "all_trades.json", "w") as handle:
        json.dump(records, handle, indent=2, default=str)


def merge_one_run(
    *,
    client,
    category: str,
    log_dir: Path,
    out_dir: Path,
) -> int:
    logs = load_trade_logs(log_dir)
    if not logs:
        print(f"No trade logs found in {log_dir}")
        return 0

    bounds = symbol_time_bounds(logs)

    symbol_bundles: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for symbol, (start_ms, end_ms) in bounds.items():
        symbol_bundles[symbol] = fetch_symbol_bundle(
            client,
            category=category,
            symbol=symbol,
            start_ms=start_ms,
            end_ms=end_ms,
        )

    merged_records: list[dict[str, Any]] = []
    used_close_order_ids: dict[str, set[str]] = defaultdict(set)

    for log in logs:
        symbol = str(log.get("symbol") or "")
        bundle = symbol_bundles.get(symbol, {"orders": [], "executions": [], "closed_pnl": []})
        orders_by_id = {str(item.get("orderId") or ""): item for item in bundle["orders"] if item.get("orderId")}
        execs_by_order_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for item in bundle["executions"]:
            order_id = str(item.get("orderId") or "")
            if order_id:
                execs_by_order_id[order_id].append(item)
        closed_records = _sort_by_time(bundle["closed_pnl"], "createdTime")
        merged_records.append(
            build_merged_record(
                log,
                orders_by_id,
                execs_by_order_id,
                closed_records,
                used_close_order_ids[symbol],
            )
        )

    write_outputs(merged_records, out_dir)
    print(f"Merged {len(merged_records)} trade logs from {log_dir} into {out_dir}")
    return len(merged_records)


def discover_run_dirs(runs_root: Path) -> list[Path]:
    if not runs_root.exists():
        return []
    trade_log_dirs = sorted(runs_root.glob("**/trade_logs"))
    run_dirs = [path.parent for path in trade_log_dirs if path.is_dir()]
    return run_dirs


def category_for_run(run_dir: Path, fallback_category: str) -> str:
    cfg_path = run_dir / "run_config.json"
    if not cfg_path.exists():
        return fallback_category
    try:
        with open(cfg_path) as handle:
            data = json.load(handle)
        return str(data.get("config", {}).get("category") or fallback_category)
    except (json.JSONDecodeError, OSError, TypeError):
        return fallback_category


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge local trade logs with Bybit order, execution, and closed pnl data.")
    parser.add_argument(
        "--log-dir",
        default=None,
        help="Directory containing trade log JSON files. Defaults to the current config run directory.",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Directory to write merged trade JSON files into. Defaults to the current config run directory.",
    )
    parser.add_argument(
        "--all-runs",
        action="store_true",
        help="Merge all run directories under analysis/runs in one invocation.",
    )
    parser.add_argument(
        "--runs-root",
        default=str(ANALYSIS_RUNS_DIR),
        help="Root directory containing run folders (used with --all-runs).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = build_config_from_env()
    ensure_analysis_dirs(cfg)
    client, default_category = build_bybit_client()

    if args.all_runs:
        runs_root = Path(args.runs_root)
        run_dirs = discover_run_dirs(runs_root)
        if not run_dirs:
            print(f"No run directories found under {runs_root}")
            return

        total_merged = 0
        for run_dir in run_dirs:
            log_dir = run_dir / "trade_logs"
            out_dir = run_dir / "merged_trades"
            run_category = category_for_run(run_dir, default_category)
            total_merged += merge_one_run(
                client=client,
                category=run_category,
                log_dir=log_dir,
                out_dir=out_dir,
            )

        print(f"All-runs merge complete. Total records merged: {total_merged}")
        return

    log_dir = Path(args.log_dir) if args.log_dir else get_trade_log_dir(cfg)
    out_dir = Path(args.out_dir) if args.out_dir else get_merged_trade_dir(cfg)
    merge_one_run(
        client=client,
        category=default_category,
        log_dir=log_dir,
        out_dir=out_dir,
    )


if __name__ == "__main__":
    main()