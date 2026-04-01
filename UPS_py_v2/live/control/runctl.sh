#!/usr/bin/env bash
set -euo pipefail

# Live run controller (separate from analysis artifacts).
# Runtime state lives under: UPS_py_v2/live/control/registry

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
VENV_ACTIVATE="/root/.venv/bin/activate"

REGISTRY_DIR="$SCRIPT_DIR/registry"
ACTIVE_DIR="$REGISTRY_DIR/active"
INACTIVE_DIR="$REGISTRY_DIR/inactive"
MANIFESTS_DIR="$REGISTRY_DIR/manifests"
CONFIGS_DIR="$REGISTRY_DIR/configs"
PIDS_DIR="$REGISTRY_DIR/pids"
PROFILES_DIR="$SCRIPT_DIR/profiles"
STATUS_TXT="$MANIFESTS_DIR/last_snapshot.txt"
WANTED_RUNS_FILE="$MANIFESTS_DIR/wanted_runs.yaml"

mkdir -p "$ACTIVE_DIR" "$INACTIVE_DIR" "$MANIFESTS_DIR" "$CONFIGS_DIR" "$PIDS_DIR" "$PROFILES_DIR"
[[ -f "$WANTED_RUNS_FILE" ]] || cat > "$WANTED_RUNS_FILE" <<'EOF'
# Desired runs that should be resurrected on reboot.
# One run name per line, either plain or YAML-list style.
# Example:
# - coti_5m
# - btc_15m
EOF

usage() {
  cat <<'EOF'
Usage:
  runctl.sh start <run_name> [--auto-restart yes|no] [--restart-delay SEC] [--max-restarts N] -- <command>
  runctl.sh profile-save <profile_name> --symbol SYMBOL --timeframe TF [--category CAT] [--analysis-profile NAME] [--trail-stop yes|no] [--dry-run yes|no]
  runctl.sh profile-start <profile_name> [--run-name NAME] [--auto-restart yes|no] [--restart-delay SEC] [--max-restarts N]
  runctl.sh profile-show <profile_name>
  runctl.sh profile-list
  runctl.sh stop <run_name> [--disable]
  runctl.sh stop-all
  runctl.sh start-all
  runctl.sh restart <run_name>
  runctl.sh status
  runctl.sh list
  runctl.sh resurrect
  runctl.sh install-systemd

Examples:
  ./runctl.sh start coti_5m -- "cd /root/projects/pine_and_bachtesting_py && source /root/.venv/bin/activate && python -m UPS_py_v2.live.ups_live_runner"
  ./runctl.sh profile-save coti_5m --symbol COTIUSDT --timeframe 5m --category linear --analysis-profile default
  ./runctl.sh profile-start coti_5m
  ./runctl.sh profile-list
  ./runctl.sh stop coti_5m
  ./runctl.sh restart coti_5m
  ./runctl.sh status
  ./runctl.sh resurrect

Layout:
  registry/active/<run_name>/<run_id>/
  registry/inactive/<run_name>/<run_id>/
  registry/configs/<run_name>.conf
  registry/manifests/wanted_runs.yaml
  profiles/<profile_name>.env
EOF
}

now_utc() {
  date -u +"%Y-%m-%d %H:%M:%S UTC"
}

run_id_now() {
  date -u +"%Y%m%dT%H%M%SZ"
}

is_pid_running() {
  local pid="$1"
  [[ "$pid" =~ ^[0-9]+$ ]] && ps -p "$pid" > /dev/null 2>&1
}

require_venv() {
  if [[ ! -f "$VENV_ACTIVATE" ]]; then
    echo "ERROR: virtualenv activate file not found at $VENV_ACTIVATE" >&2
    exit 2
  fi
}

normalize_yes_no() {
  local raw="$1"
  local value
  value="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]')"
  case "$value" in
    yes|true|1|on|y) echo "yes" ;;
    no|false|0|off|n) echo "no" ;;
    *)
      echo "ERROR: expected yes/no value, got '$raw'" >&2
      exit 1
      ;;
  esac
}

profile_file_path() {
  local profile_name="$1"
  echo "$PROFILES_DIR/${profile_name}.env"
}

profile_command() {
  local profile_name="$1"
  local profile_file
  profile_file="$(profile_file_path "$profile_name")"
  if [[ ! -f "$profile_file" ]]; then
    echo "ERROR: profile not found: $profile_file" >&2
    exit 1
  fi

  printf '%s' "cd $PROJECT_DIR && source $VENV_ACTIVATE && set -a && source $profile_file && set +a && python -m UPS_py_v2.live.ups_live_runner"
}

cmd_profile_save() {
  local profile_name="$1"
  shift

  local symbol=""
  local timeframe=""
  local category="linear"
  local analysis_profile="$profile_name"
  local trail_stop="no"
  local dry_run="no"
  local use_ws_kline="yes"
  local order_type="Limit"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --symbol) symbol="$2"; shift 2 ;;
      --timeframe) timeframe="$2"; shift 2 ;;
      --category) category="$2"; shift 2 ;;
      --analysis-profile) analysis_profile="$2"; shift 2 ;;
      --trail-stop) trail_stop="$(normalize_yes_no "$2")"; shift 2 ;;
      --dry-run) dry_run="$(normalize_yes_no "$2")"; shift 2 ;;
      --use-ws-kline) use_ws_kline="$(normalize_yes_no "$2")"; shift 2 ;;
      --order-type) order_type="$2"; shift 2 ;;
      *)
        echo "Unknown profile-save option: $1" >&2
        exit 1
        ;;
    esac
  done

  if [[ -z "$symbol" || -z "$timeframe" ]]; then
    echo "ERROR: profile-save requires --symbol and --timeframe" >&2
    exit 1
  fi

  local profile_file
  profile_file="$(profile_file_path "$profile_name")"
  cat > "$profile_file" <<EOF
# Run profile: $profile_name
# Loaded by: runctl.sh profile-start $profile_name
UPS_PROFILE=$analysis_profile
UPS_CATEGORY=$category
UPS_SYMBOL=$symbol
UPS_TIMEFRAME=$timeframe
UPS_TRAIL_STOP=$([[ "$trail_stop" == "yes" ]] && echo true || echo false)
UPS_DRY_RUN=$([[ "$dry_run" == "yes" ]] && echo true || echo false)
UPS_USE_WS_KLINE=$([[ "$use_ws_kline" == "yes" ]] && echo true || echo false)
UPS_ORDER_TYPE=$order_type
EOF

  chmod 644 "$profile_file"
  echo "Saved profile: $profile_file"
}

cmd_profile_show() {
  local profile_name="$1"
  local profile_file
  profile_file="$(profile_file_path "$profile_name")"
  if [[ ! -f "$profile_file" ]]; then
    echo "ERROR: profile not found: $profile_file" >&2
    exit 1
  fi
  cat "$profile_file"
}

cmd_profile_list() {
  find "$PROFILES_DIR" -maxdepth 1 -type f -name '*.env' -printf '%f\n' | sed 's/\.env$//' | sort
}

cmd_profile_start() {
  local profile_name="$1"
  shift

  local run_name="$profile_name"
  local auto_restart="yes"
  local restart_delay="10"
  local max_restarts="0"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --run-name) run_name="$2"; shift 2 ;;
      --auto-restart) auto_restart="$2"; shift 2 ;;
      --restart-delay) restart_delay="$2"; shift 2 ;;
      --max-restarts) max_restarts="$2"; shift 2 ;;
      *)
        echo "Unknown profile-start option: $1" >&2
        exit 1
        ;;
    esac
  done

  local cmd
  cmd="$(profile_command "$profile_name")"

  require_venv
  write_config "$run_name" "$auto_restart" "$restart_delay" "$max_restarts" "$cmd"
  add_wanted_run "$run_name"
  start_supervisor "$run_name" "$auto_restart" "$restart_delay" "$max_restarts" "$cmd"
  status_table > /dev/null
}

wanted_runs_list() {
  sed -E 's/^\s*-\s*//; s/^\s+//; s/\s+$//' "$WANTED_RUNS_FILE" \
    | sed '/^$/d; /^#/d' \
    | sort -u
}

add_wanted_run() {
  local run_name="$1"
  if wanted_runs_list | grep -Fxq "$run_name"; then
    return
  fi
  echo "- $run_name" >> "$WANTED_RUNS_FILE"
}

remove_wanted_run() {
  local run_name="$1"
  local tmp
  tmp="$(mktemp)"
  while IFS= read -r raw; do
    local cleaned
    cleaned="$(printf '%s' "$raw" | sed -E 's/^\s*-\s*//; s/^\s+//; s/\s+$//')"
    if [[ "$cleaned" == "$run_name" ]]; then
      continue
    fi
    echo "$raw" >> "$tmp"
  done < "$WANTED_RUNS_FILE"
  mv "$tmp" "$WANTED_RUNS_FILE"
}

write_config() {
  local run_name="$1"
  local auto_restart="$2"
  local restart_delay="$3"
  local max_restarts="$4"
  local cmd="$5"

  local cmd_b64
  cmd_b64="$(printf '%s' "$cmd" | base64 -w0)"

  cat > "$CONFIGS_DIR/${run_name}.conf" <<EOF
RUN_NAME="$run_name"
AUTO_RESTART="$auto_restart"
RESTART_DELAY="$restart_delay"
MAX_RESTARTS="$max_restarts"
COMMAND_B64="$cmd_b64"
UPDATED_AT="$(now_utc)"
EOF
}

load_config() {
  local run_name="$1"
  local conf="$CONFIGS_DIR/${run_name}.conf"

  if [[ ! -f "$conf" ]]; then
    echo "ERROR: run config missing: $conf" >&2
    exit 1
  fi

  # shellcheck disable=SC1090
  source "$conf"

  if [[ -z "${COMMAND_B64:-}" ]]; then
    echo "ERROR: COMMAND_B64 missing in $conf" >&2
    exit 1
  fi

  RUN_COMMAND="$(printf '%s' "$COMMAND_B64" | base64 -d)"
  AUTO_RESTART="${AUTO_RESTART:-yes}"
  RESTART_DELAY="${RESTART_DELAY:-10}"
  MAX_RESTARTS="${MAX_RESTARTS:-0}"
}

start_supervisor() {
  local run_name="$1"
  local auto_restart="$2"
  local restart_delay="$3"
  local max_restarts="$4"
  local cmd="$5"

  local supervisor_pid_file="$PIDS_DIR/${run_name}.supervisor.pid"
  local child_pid_file="$PIDS_DIR/${run_name}.child.pid"

  if [[ -f "$supervisor_pid_file" ]]; then
    local existing
    existing="$(<"$supervisor_pid_file")"
    if is_pid_running "$existing"; then
      echo "Run '$run_name' already active (supervisor pid=$existing)." >&2
      exit 1
    fi
    rm -f "$supervisor_pid_file"
  fi

  (
    set -euo pipefail

    current_child=""
    restarts_done=0

    trap 'if [[ -n "$current_child" ]] && ps -p "$current_child" > /dev/null 2>&1; then kill -TERM "$current_child" || true; wait "$current_child" || true; fi; rm -f "'$supervisor_pid_file'" "'$child_pid_file'"; exit 0' SIGINT SIGTERM

    while true; do
      local_run_id="$(run_id_now)"
      local_run_dir="$ACTIVE_DIR/$run_name/$local_run_id"
      local_log_file="$local_run_dir/run.log"
      local_meta="$local_run_dir/meta.env"

      mkdir -p "$local_run_dir"

      {
        echo "RUN_NAME=$run_name"
        echo "RUN_ID=$local_run_id"
        echo "STARTED_AT=$(now_utc)"
        echo "AUTO_RESTART=$auto_restart"
        echo "RESTART_DELAY=$restart_delay"
        echo "MAX_RESTARTS=$max_restarts"
        echo "COMMAND_B64=$(printf '%s' "$cmd" | base64 -w0)"
      } > "$local_meta"

      bash -lc "$cmd" >> "$local_log_file" 2>&1 &
      current_child=$!
      echo "$current_child" > "$child_pid_file"
      echo "$current_child" > "$local_run_dir/pid"

      wait "$current_child"
      rc=$?

      {
        echo "ENDED_AT=$(now_utc)"
        echo "EXIT_CODE=$rc"
      } >> "$local_meta"
      echo "$rc" > "$local_run_dir/exit_code.txt"
      rm -f "$child_pid_file"

      mkdir -p "$INACTIVE_DIR/$run_name"
      mv "$local_run_dir" "$INACTIVE_DIR/$run_name/"

      if [[ "$auto_restart" != "yes" ]]; then
        break
      fi

      if [[ "$max_restarts" =~ ^[0-9]+$ ]] && [[ "$max_restarts" -gt 0 ]] && [[ "$restarts_done" -ge "$max_restarts" ]]; then
        break
      fi

      restarts_done=$((restarts_done + 1))
      sleep "$restart_delay"
    done

    rm -f "$supervisor_pid_file"
  ) &

  local spid=$!
  echo "$spid" > "$supervisor_pid_file"
  chmod 644 "$supervisor_pid_file"

  echo "Started run '$run_name' (supervisor pid=$spid)."
}

stop_run() {
  local run_name="$1"
  local disable_after_stop="$2"

  local supervisor_pid_file="$PIDS_DIR/${run_name}.supervisor.pid"
  local child_pid_file="$PIDS_DIR/${run_name}.child.pid"

  if [[ ! -f "$supervisor_pid_file" ]]; then
    echo "Run '$run_name' has no supervisor pid file."
    if [[ "$disable_after_stop" == "yes" ]]; then
      remove_wanted_run "$run_name"
      echo "Removed '$run_name' from wanted runs."
    fi
    return
  fi

  local spid
  spid="$(<"$supervisor_pid_file")"

  if is_pid_running "$spid"; then
    kill -TERM "$spid"
    for _ in {1..20}; do
      if ! is_pid_running "$spid"; then
        break
      fi
      sleep 0.5
    done
    if is_pid_running "$spid"; then
      kill -KILL "$spid" || true
    fi
  fi

  if [[ -f "$child_pid_file" ]]; then
    local cpid
    cpid="$(<"$child_pid_file")"
    if is_pid_running "$cpid"; then
      kill -TERM "$cpid" || true
      sleep 1
      if is_pid_running "$cpid"; then
        kill -KILL "$cpid" || true
      fi
    fi
    rm -f "$child_pid_file"
  fi

  rm -f "$supervisor_pid_file"
  echo "Stopped run '$run_name'."

  if [[ "$disable_after_stop" == "yes" ]]; then
    remove_wanted_run "$run_name"
    echo "Removed '$run_name' from wanted runs."
  fi
}

last_finished_attempt() {
  local run_name="$1"
  if [[ ! -d "$INACTIVE_DIR/$run_name" ]]; then
    echo "-"
    return
  fi
  local lf
  lf="$(find "$INACTIVE_DIR/$run_name" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort | tail -n 1 || true)"
  [[ -n "$lf" ]] && echo "$lf" || echo "-"
}

status_table() {
  {
    echo "Runtime Status"
    echo "Generated: $(now_utc)"
    echo
    printf '%-25s %-10s %-12s %-10s %-22s\n' "RUN_NAME" "STATE" "SUPERVISOR" "CHILD" "LAST_FINISHED"
    printf '%-25s %-10s %-12s %-10s %-22s\n' "--------" "-----" "----------" "-----" "-------------"

    local names=()
    while IFS= read -r n; do
      [[ -n "$n" ]] && names+=("$n")
    done < <(find "$CONFIGS_DIR" -maxdepth 1 -type f -name '*.conf' -printf '%f\n' | sed 's/\.conf$//' | sort)

    if [[ ${#names[@]} -eq 0 ]]; then
      echo "(no configured runs)"
    else
      local run_name state spid cpid
      for run_name in "${names[@]}"; do
        state="stopped"
        spid="-"
        cpid="-"

        if [[ -f "$PIDS_DIR/${run_name}.supervisor.pid" ]]; then
          spid="$(<"$PIDS_DIR/${run_name}.supervisor.pid")"
          if is_pid_running "$spid"; then
            state="running"
          else
            state="stale-pid"
          fi
        fi

        if [[ -f "$PIDS_DIR/${run_name}.child.pid" ]]; then
          cpid="$(<"$PIDS_DIR/${run_name}.child.pid")"
        fi

        printf '%-25s %-10s %-12s %-10s %-22s\n' "$run_name" "$state" "$spid" "$cpid" "$(last_finished_attempt "$run_name")"
      done
    fi

    echo
    echo "Wanted on reboot:"
    local had_any="no"
    while IFS= read -r n; do
      had_any="yes"
      echo "- $n"
    done < <(wanted_runs_list)
    if [[ "$had_any" == "no" ]]; then
      echo "- (none)"
    fi
  } | tee "$STATUS_TXT"
}

cmd_start() {
  local run_name="$1"
  shift

  local auto_restart="yes"
  local restart_delay="10"
  local max_restarts="0"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --auto-restart) auto_restart="$2"; shift 2 ;;
      --restart-delay) restart_delay="$2"; shift 2 ;;
      --max-restarts) max_restarts="$2"; shift 2 ;;
      --) shift; break ;;
      *) echo "Unknown start option: $1" >&2; exit 1 ;;
    esac
  done

  if [[ $# -eq 0 ]]; then
    echo "ERROR: missing command after '--'" >&2
    exit 1
  fi

  local cmd="$*"

  require_venv
  write_config "$run_name" "$auto_restart" "$restart_delay" "$max_restarts" "$cmd"
  add_wanted_run "$run_name"
  start_supervisor "$run_name" "$auto_restart" "$restart_delay" "$max_restarts" "$cmd"
  status_table > /dev/null
}

cmd_restart() {
  local run_name="$1"
  load_config "$run_name"

  stop_run "$run_name" "no"
  start_supervisor "$run_name" "$AUTO_RESTART" "$RESTART_DELAY" "$MAX_RESTARTS" "$RUN_COMMAND"
  add_wanted_run "$run_name"
  status_table > /dev/null
}

cmd_resurrect() {
  local had_any="no"
  while IFS= read -r run_name; do
    had_any="yes"

    local supervisor_pid_file="$PIDS_DIR/${run_name}.supervisor.pid"
    if [[ -f "$supervisor_pid_file" ]]; then
      local spid
      spid="$(<"$supervisor_pid_file")"
      if is_pid_running "$spid"; then
        echo "Run '$run_name' already active; skipping."
        continue
      fi
      rm -f "$supervisor_pid_file"
    fi

    load_config "$run_name"
    start_supervisor "$run_name" "$AUTO_RESTART" "$RESTART_DELAY" "$MAX_RESTARTS" "$RUN_COMMAND"
  done < <(wanted_runs_list)

  if [[ "$had_any" == "no" ]]; then
    echo "No wanted runs to resurrect."
  fi

  status_table > /dev/null
}

cmd_stop_all() {
  local lines
  lines=$(cmd_profile_list)
  if [[ -z "$lines" ]]; then
    echo "No configured runs to stop."
    return
  fi

  local run
  for run in $lines; do
    echo "Stopping run: $run"
    stop_run "$run" "yes"
  done

  status_table > /dev/null
}

cmd_start_all() {
  local lines
  lines=$(cmd_profile_list)
  if [[ -z "$lines" ]]; then
    echo "No configured profiles to start."
    return
  fi

  local run
  for run in $lines; do
    echo "Starting run: $run"
    cmd_profile_start "$run"
  done

  status_table > /dev/null
}

cmd_install_systemd() {
  local service_name="ups-live-control.service"
  local service_path="/etc/systemd/system/${service_name}"

  cat > "/tmp/${service_name}" <<EOF
[Unit]
Description=UPS Live Run Controller (resurrect wanted runs)
After=network.target

[Service]
Type=oneshot
WorkingDirectory=$PROJECT_DIR
ExecStart=$SCRIPT_DIR/runctl.sh resurrect
RemainAfterExit=true

[Install]
WantedBy=multi-user.target
EOF

  if [[ "$(id -u)" -ne 0 ]]; then
    echo "Run as root to install systemd service."
    echo "Planned file: /tmp/${service_name}"
    return
  fi

  mv "/tmp/${service_name}" "$service_path"
  chmod 644 "$service_path"
  systemctl daemon-reload
  systemctl enable "$service_name"
  echo "Installed and enabled: $service_path"
}

main() {
  if [[ $# -lt 1 ]]; then
    usage
    exit 1
  fi

  local command="$1"
  shift

  case "$command" in
    start)
      if [[ $# -lt 2 ]]; then
        usage
        exit 1
      fi
      cmd_start "$@"
      ;;
    profile-save)
      if [[ $# -lt 1 ]]; then
        usage
        exit 1
      fi
      local profile_name="$1"
      shift
      cmd_profile_save "$profile_name" "$@"
      ;;
    profile-start)
      if [[ $# -lt 1 ]]; then
        usage
        exit 1
      fi
      local profile_name="$1"
      shift
      cmd_profile_start "$profile_name" "$@"
      ;;
    profile-show)
      if [[ $# -ne 1 ]]; then
        usage
        exit 1
      fi
      cmd_profile_show "$1"
      ;;
    profile-list)
      cmd_profile_list
      ;;
    stop)
      if [[ $# -lt 1 ]]; then
        usage
        exit 1
      fi
      local run_name="$1"
      shift
      local disable_after_stop="no"
      if [[ "${1:-}" == "--disable" ]]; then
        disable_after_stop="yes"
      fi
      stop_run "$run_name" "$disable_after_stop"
      status_table > /dev/null
      ;;
    restart)
      if [[ $# -ne 1 ]]; then
        usage
        exit 1
      fi
      cmd_restart "$1"
      ;;
    status)
      status_table
      ;;
    list)
      wanted_runs_list
      ;;
    stop-all)
      cmd_stop_all
      ;;
    start-all)
      cmd_start_all
      ;;
    resurrect)
      cmd_resurrect
      ;;
    install-systemd)
      cmd_install_systemd
      ;;
    -h|--help|help)
      usage
      ;;
    *)
      echo "Unknown command: $command" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
