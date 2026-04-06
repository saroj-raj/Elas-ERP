# GIT WORKFLOW

## Purpose
This file defines the Git and GitHub workflow rules for Vizpilot.

The goal is to:
- avoid accidental loss of work
- avoid laptop-to-laptop divergence chaos
- keep `main` stable
- preserve working demo flows

---

## 1) Source of truth
- GitHub is the source of truth
- Never assume the local laptop copy is latest
- Never assume another laptop is latest without checking Git history
- Always inspect before syncing

---

## 2) Mandatory pre-sync inspection
Before any pull/merge/sync action, always inspect:

```bash
git status
git branch -vv
git remote -v
git log --oneline --decorate -15
git fetch --all --prune
git status
```

You must know:
- current branch
- ahead/behind status
- remote URL
- local uncommitted changes
- untracked files
- recent commits

---

## 3) Backup-first rule
If local changes exist:
- create a backup branch first

Example:
```bash
git checkout -b backup/pre-sync-YYYY-MM-DD
git add .
git commit -m "Backup local state before sync"
```

Never do risky sync operations without preserving local work first.

---

## 4) Destructive Git actions
The following must never be used casually:
- `git reset --hard`
- `git clean -fd`
- `git rebase`
- force-push
- branch deletion

These require:
- inspection
- justification
- manual approval
- backup branch first

---

## 5) Main branch rules
- `main` should remain stable
- do not push broken code to `main`
- do not merge if the golden path is broken
- prefer feature branches for meaningful changes

Suggested branch naming:
- `feature/...`
- `fix/...`
- `chore/...`
- `backup/...`

---

## 6) Commit rules
Commits should be:
- small
- working
- descriptive

Good examples:
- `fix: backend health endpoint import issue`
- `feat: add dashboard filter panel`
- `chore: archive obsolete status docs`

Bad examples:
- `update`
- `misc fixes`
- `changes`
- `final final`

---

## 7) Pre-push checklist
Before pushing:
- backend runs
- `/health` works
- frontend runs
- landing page loads
- login page loads
- golden path is tested

### Required golden path check
1. Get started
2. Login
3. Business onboarding
4. Team setup
5. File upload
6. Documents / proposal step
7. Dashboard render

If this is broken, do not push as "ready."

---

## 8) GitHub remote rules
Always verify remote:
```bash
git remote -v
```

If repo is renamed, update remote explicitly:
```bash
git remote set-url origin <new_repo_url>
```

Never assume GitHub redirects are enough.

---

## 9) Laptop sync rules
When working across multiple machines:
- inspect each machine separately
- determine which machine is ahead
- determine whether work was already pushed
- do not copy files manually unless Git-based sync is impossible
- Git sync is preferred over ad hoc folder copying

---

## 10) Copilot Git rules
Copilot must not automatically run:
- `commit`
- `push`
- `pull`
- `reset`
- `clean`
- `rebase`
- `branch delete`

Copilot may:
- inspect
- summarize
- compare
- propose commands

Human approval is required for any Git-changing command.

---

## 11) Merge/sync strategy
Preferred order:
1. inspect
2. backup local work if present
3. update remote URL if needed
4. fetch remote
5. pull safely
6. retest locally

Prefer:
```bash
git pull --ff-only origin main
```

Unless a manual merge is explicitly required and understood.

---

## 12) Cleanup rules
Do not delete files casually just because they "look old."

Use this order:
1. inspect
2. classify as keep / archive / delete candidate
3. archive first when uncertain
4. delete only if clearly obsolete

---

## 13) Release readiness
A branch or commit may be called release-ready only if:
- backend runs
- frontend runs
- env assumptions are verified
- golden path is working
- there are no known critical blockers in the demo flow

---

## 14) Safety override
If you are unsure whether a Git action is safe:
- stop
- inspect
- create backup branch
- ask for review

Safety beats speed.

---
