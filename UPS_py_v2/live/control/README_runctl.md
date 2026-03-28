# Live Control Run Manager

`live/control` is the execution layer for live runs.

Use it to start, stop, restart, and recover live processes. Keep `live/analysis` for trade logs, merged results, and post-run analysis only.

## Quick Start

Move into the control folder:

```bash
cd /root/projects/pine_and_bachtesting_py/UPS_py_v2/live/control
chmod +x runctl.sh
```

### Example: create one saved profile

This saves a reusable setup for `COTIUSDT` on `5m`.

```bash
./runctl.sh profile-save coti_5m \
  --symbol COTIUSDT \
  --timeframe 5m \
  --category linear \
  --analysis-profile default \
  --trail-stop no \
  --dry-run no
```

What this does:

- Creates `profiles/coti_5m.env`.
- Stores the pair/timeframe/category settings there.
- Avoids editing the Python config file every time.

### Example: start that profile

```bash
./runctl.sh profile-start coti_5m
```

What happens when you start:

- `runctl.sh` loads `profiles/coti_5m.env`.
- It exports the `UPS_*` variables for that run.
- It starts the live runner in the background.
- It saves runtime state under `registry/`.
- It adds the run name to `registry/manifests/wanted_runs.yaml` so it can be resurrected after reboot.

### Example: check whether it is running

```bash
./runctl.sh status
```

Also useful:

```bash
cat registry/manifests/last_snapshot.txt
```

### Example: stop the run

```bash
./runctl.sh stop coti_5m
```

What happens when you stop:

- The supervisor process is terminated.
- The child live-runner process is terminated.
- The current run is no longer active.
- The saved profile still exists, so you can start it again later.

### Example: stop it and remove auto-restart on reboot

```bash
./runctl.sh stop coti_5m --disable
```

Use `--disable` when you do not want this run resurrected from `wanted_runs.yaml` anymore.

## Daily Use

List saved profiles:

```bash
./runctl.sh profile-list
```

Show one profile:

```bash
./runctl.sh profile-show coti_5m
```

Restart a running or saved run using its stored run config:

```bash
./runctl.sh restart coti_5m
```

Manually resurrect all wanted runs:

```bash
./runctl.sh resurrect
```

Install reboot recovery service:

```bash
sudo ./runctl.sh install-systemd
```

## How To Adjust Things

### Change the pair or timeframe

Save the profile again with the same name:

```bash
./runctl.sh profile-save coti_5m \
  --symbol COTIUSDT \
  --timeframe 15m \
  --category linear \
  --analysis-profile default
```

That overwrites `profiles/coti_5m.env` with the new values.

### Create a second profile instead of overwriting

```bash
./runctl.sh profile-save btc_15m \
  --symbol BTCUSDT \
  --timeframe 15m \
  --category linear \
  --analysis-profile default
```

Now you have two independent saved profiles.

### Start a saved profile under a different runtime name

Useful if you want a different process label than the profile name.

```bash
./runctl.sh profile-start coti_5m --run-name coti_live_main
```

### Use dry run

```bash
./runctl.sh profile-save coti_5m_paper \
  --symbol COTIUSDT \
  --timeframe 5m \
  --category linear \
  --analysis-profile default \
  --dry-run yes
```

### Use trail stop

```bash
./runctl.sh profile-save coti_5m_trail \
  --symbol COTIUSDT \
  --timeframe 5m \
  --category linear \
  --analysis-profile trail \
  --trail-stop yes
```

## Where Everything Lives

```text
UPS_py_v2/live/control/
  runctl.sh
  profiles/
    <profile_name>.env
  registry/
    active/
    inactive/
    configs/
    pids/
    manifests/
      wanted_runs.yaml
      last_snapshot.txt
```

- `profiles/<profile_name>.env`: saved pair/timeframe/category settings.
- `registry/active/<run_name>/<run_id>/`: currently active run attempts.
- `registry/inactive/<run_name>/<run_id>/`: finished or stopped run attempts.
- `registry/configs/<run_name>.conf`: stored launch command and restart policy for the run name.
- `registry/manifests/wanted_runs.yaml`: list of runs to resurrect after reboot.
- `registry/manifests/last_snapshot.txt`: latest human-readable status snapshot.

## Mental Model

- A `profile` is your saved market setup.
- A `run name` is the process label being managed.
- `profile-start` turns a saved profile into a managed running process.
- `status` tells you what is active or stopped.
- `stop` stops the process.
- `restart` restarts using the saved run config.

## Recommended Workflow

1. Save one profile per pair and timeframe you care about.
2. Start runs only through `runctl.sh`.
3. Check `status` instead of manually checking PIDs.
4. Keep strategy outputs in `live/analysis/runs/...`.
5. Treat `profiles/*.env` as your editable setup and `registry/` as runtime state.
