# Git Workflow Best Practices (Short & Precise)

> Use this workflow step-by-step and update the repo in a controlled manner.
> Each step should be analyzed and explained in short, precise notes.
> Include the command run and its purpose in each explanation.
> Proceed slowly and run the next command only on explicit `yes` from the user.

## 1) Start in target repo
- `cd /root/projects/pine_and_bachtesting_py`
- Keeps all commands local and consistent.

## 2) Check status before changing
- `git branch --show-current`
- `git status --short`
- Confirm branch and uncommitted changes.

## 3) Preserve local work
- If ready: `git add .` + `git commit -m "WIP: save local changes"`
- If temporary: `git stash push -m "WIP before pull"`
- Avoid lost updates and clean base state.

## 4) Update main from remote
- `git checkout main`
- `git pull --rebase origin main`
- Achieve up-to-date base without merge noise.

## 5) Use feature branch for changes
- `git checkout -b feature/update-from-remote`
- Work isolated, protect main from partial updates.

## 6) Sync feature branch continuously
- `git fetch origin`
- `git rebase origin/main` (or `git merge origin/main` if preferred)
- Keep branch current, reduce conflict scope.

## 7) Resolve conflicts carefully
- edit conflict markers in files
- `git add <file>`
- `git rebase --continue` (if rebasing)
- `git merge --continue` (if merging)

## 8) Install dependencies after code sync
- `source /root/.venv/bin/activate`
- `pip install -r requirements.txt`
- Ensure environment matches repository.

## 9) Validate locally
- `python -m UPS_py_v2.live.ups_live_runner`
- Run existing app entrypoint to check behavior.

## 10) Merge back and push
- `git checkout main`
- `git pull --rebase origin main`
- `git merge --no-ff feature/update-from-remote`
- `git push origin main`

## 11) Cleanup
- `git branch -d feature/update-from-remote`
- `git stash pop` (if stash was used)

## 12) Optional: global rebase policy
- `git config --global pull.rebase true`
- prefer linear history by default.

## Notes
- If remote is non-main, substitute branch name (dev, stable, etc.).
- Rebase keeps history clean, merge keeps original chronology.
