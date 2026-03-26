# 🔍 Repository Audit Report — VizPilot / Elas ERP

> **Generated:** 2026-03-26  
> **Purpose:** Inspect local repo state before any sync operation. No changes made. No destructive commands run.

---

## 1. Repo Root

```
/home/runner/work/VizPilot/VizPilot
```

**Top-Level Contents:**

| Path | Type | Notes |
|---|---|---|
| `frontend/` | Directory | Next.js 14 frontend (VizPilot rebrand) |
| `backend/` | Directory | FastAPI Python backend (VizPilot rebrand) |
| `elas-erp/` | Directory | Original Elas ERP source (pre-rebrand snapshot) |
| `app/` | Directory | Contains only a `tmp/` subfolder (nearly empty) |
| `docker-compose.yml` | File | Root-level Docker config (Elas branding) |
| `package.json` | File | Root-level (only has `@vercel/speed-insights` dep) |
| `start.py` | File | Dev launcher script (says "Elas ERP" in header) |
| `README.md` | File | Rebranded to Vizpilot |
| `DEPLOY.md` | File | Still references Elas-ERP deployment |
| `*.md` (many) | Files | Mix of status, cleanup, and implementation docs |
| `.github/` | Directory | GitHub Actions CI workflows |
| `.husky/` | Directory | Git hooks (pre-push) |

---

## 2. Branch Information

### Current Branch
```
copilot/vscode-mn7kqs1q-4lel
```

### All Local Branches
```
* copilot/vscode-mn7kqs1q-4lel
```
> ⚠️ Only one local branch exists. There is no local `main` branch.

### All Remote Branches
```
remotes/origin/copilot/vscode-mn7kqs1q-4lel
```
> ⚠️ Only one remote branch exists. There is **no** `origin/main` on this remote (or it was never fetched into this shallow clone).

### Remote URLs
```
origin  https://github.com/saroj-raj/VizPilot (fetch)
origin  https://github.com/saroj-raj/VizPilot (push)
```

---

## 3. Working Tree Status

```
On branch copilot/vscode-mn7kqs1q-4lel
Your branch is up to date with 'origin/copilot/vscode-mn7kqs1q-4lel'.

nothing to commit, working tree clean
```

| Item | Status |
|---|---|
| Uncommitted changes | ✅ None |
| Untracked files | ✅ None |
| Modified tracked files | ✅ None |
| Staged changes | ✅ None |

---

## 4. Commit History

### Last 15 Commits on Current Branch
```
0544ed9 (HEAD -> copilot/vscode-mn7kqs1q-4lel, origin/copilot/vscode-mn7kqs1q-4lel) Checkpoint from VS Code for cloud agent session
20e6aa2 (grafted) Initial import from Elas ERP (rebrand to Vizpilot)
```
> ⚠️ Only **2 commits** exist in this clone. The second commit is marked `(grafted)`, confirming this is a **shallow clone** — full history is not present.

### Local Commits Not Pushed
```
(none)
```

### Remote Commits Not Pulled
```
(none — as visible from this shallow clone)
```

---

## 5. Branch Divergence from Remote

| Comparison | Result |
|---|---|
| Local vs `origin/copilot/vscode-mn7kqs1q-4lel` | **0 ahead, 0 behind** (fully in sync) |
| Local vs `origin/main` | **Cannot compare — `origin/main` does not exist** in this clone |

> ⚠️ This is a shallow clone (`--depth` clone or grafted history). The true divergence from the real `main` branch on GitHub cannot be calculated without running `git fetch --unshallow origin` and `git fetch origin main:refs/remotes/origin/main`.

### Changed Files Summary (HEAD vs HEAD~1)
The latest commit (`0544ed9`) changed only:
```
package-lock.json | 2 +-
1 file changed, 1 insertion(+), 1 deletion(-)
```

---

## 6. Monorepo Detection

**Yes — this is a monorepo.**

| Path | Role | Tech Stack |
|---|---|---|
| `frontend/` | **Active Frontend Root** | Next.js 14, TypeScript, TailwindCSS, Supabase, Playwright |
| `backend/` | **Active Backend Root** | FastAPI (Python 3.x), Supabase, Groq AI |
| `elas-erp/frontend/` | Legacy Frontend Snapshot | Same stack, original Elas branding |
| `elas-erp/backend/` | Legacy Backend Snapshot | Same stack, original Elas branding |
| `app/tmp/` | Unknown / Scratch space | Empty / temp files only |

**Frontend package name:** `vizpilot-frontend` (`frontend/package.json`)  
**Legacy package name:** `elas-erp-frontend` (`elas-erp/frontend/package.json`)

---

## 7. Project Identity / Branding Status

### Root `package.json`
```json
{ "dependencies": { "@vercel/speed-insights": "^1.2.0" } }
```
> No `name` field in root `package.json`.

### README.md (root)
```
# Vizpilot - AI Data Intelligence Platform
```
✅ Rebranded to **Vizpilot**

### Backend Config (`backend/app/core/config.py`, `backend/app/main.py`)
✅ Rebranded to **Vizpilot**

### Frontend Layout (`frontend/app/layout.tsx`)
✅ `title: 'Vizpilot - AI Data Intelligence Platform'`

### ⚠️ Mixed / Residual Elas Branding Found In Active Code

| File | Elas Reference |
|---|---|
| `frontend/app/page.tsx` | Footer: `© 2025 Elas ERP. All rights reserved.` and `Join hundreds of companies using Elas ERP...` |
| `frontend/app/signup/page.tsx` | `<h1>Elas ERP</h1>` |
| `frontend/app/onboarding/business/page.tsx` | `Elas ERP` in heading |
| `frontend/app/onboarding/upload/page.tsx` | `Elas` reference |
| `frontend/app/onboarding/documents/page.tsx` | `Elas` reference |
| `frontend/app/onboarding/team/page.tsx` | `Elas` reference |
| `frontend/app/components/ArtieChat.tsx` | `Elas` reference |
| `frontend/app/dashboard/[role]/page.tsx` | Both `Elas` and `Vizpilot` present |
| `frontend/app/dashboard/admin/page.tsx` | `Elas` reference |
| `start.py` (root) | Header: `"Elas ERP Development Server Launcher"` |
| `DEPLOY.md` (root) | `# 🚀 Elas-ERP Deployment Guide` |
| `docker-compose.yml` (root) | `container_name: elas-erp-backend`, `elas-erp-frontend`, `elas-erp-network` |
| `backend/render.yaml` | `name: elas-api`, `APP_NAME: Elas ERP`, `CORS_ORIGINS: elas-erp.vercel.app` |
| `backend/.env.example` | `APP_NAME=Elas ERP Backend`, `DATABASE_URL=elas_erp` |
| `backend/.env.template` | `APP_NAME=Elas ERP`, multiple `Elas ERP` references |
| `frontend/.env.example` | Comment says `elas-api.onrender.com` |

### Branding Verdict
> 🟡 **MIXED STATE** — Core configuration (layout title, backend service name, frontend package name) has been rebranded to Vizpilot, but a significant number of UI pages, Docker configs, Render deployment files, environment templates, and helper scripts still carry Elas ERP branding. The rebrand is **incomplete**.

---

## 8. Deployment-Related Files

| File | Location | Status |
|---|---|---|
| `vercel.json` | `frontend/vercel.json` | ✅ Present — generic (no brand name), rewrites `https://your-backend-url.com` (placeholder URL) |
| `render.yaml` | `backend/render.yaml` | ⚠️ Present — references `elas-api`, `elas-erp.vercel.app`, `Elas ERP` |
| `render.yaml` | `elas-erp/backend/render.yaml` | Legacy copy (Elas branding throughout) |
| `docker-compose.yml` | `./docker-compose.yml` | ⚠️ Present — container names and network use `elas-erp-*` |
| `docker-compose.yml` | `elas-erp/docker-compose.yml` | Legacy copy (Elas branding) |
| `.env.example` | `frontend/.env.example` | ⚠️ Comment references `elas-api.onrender.com` |
| `.env.example` | `backend/.env.example` | ⚠️ `APP_NAME=Elas ERP Backend`, DB name `elas_erp` |
| `.env.template` | `backend/.env.template` | ⚠️ `APP_NAME=Elas ERP` throughout |
| `railway.json` | `backend/railway.json` | ✅ Present — minimal, no brand name |
| `Dockerfile` | `backend/Dockerfile` | ✅ Present — no brand name |

---

## 9. Structured Summary

### Repo Root
```
/home/runner/work/VizPilot/VizPilot
```

### Current Branch
```
copilot/vscode-mn7kqs1q-4lel  (tracks origin/copilot/vscode-mn7kqs1q-4lel)
```

### Working Tree Status
```
Clean — no uncommitted changes, no untracked files
```

### Branch Divergence from Remote
```
0 ahead, 0 behind (fully in sync with origin)
origin/main: NOT PRESENT (shallow clone — cannot determine divergence from main)
```

### Uncommitted Local Work
```
None
```

### Branding Status
```
MIXED STATE
  ✅ Vizpilot: README.md, layout.tsx, backend config, frontend package name
  ⚠️ Still Elas: signup page, onboarding pages, footer, dashboard pages,
                 docker-compose.yml, render.yaml, .env templates, start.py, DEPLOY.md
```

### Frontend / Backend Paths
```
Active Frontend:  frontend/           (Next.js 14, package name: vizpilot-frontend)
Active Backend:   backend/            (FastAPI Python, Vizpilot config)
Legacy Source:    elas-erp/frontend/  (original Elas ERP frontend)
                  elas-erp/backend/   (original Elas ERP backend)
```

### Recommended Safe Next Action
```
1. Before pulling/syncing: run `git fetch --unshallow origin` then
   `git fetch origin main:refs/remotes/origin/main` to get the full
   history and compare with the real main branch.

2. Complete the Elas → Vizpilot rebrand sweep in:
   - frontend/app/page.tsx (footer)
   - frontend/app/signup/page.tsx
   - frontend/app/onboarding/*.tsx
   - frontend/app/dashboard/*.tsx
   - frontend/app/components/ArtieChat.tsx
   - docker-compose.yml (container/network names)
   - backend/render.yaml (service name, CORS origins, APP_NAME)
   - backend/.env.example and backend/.env.template
   - frontend/.env.example (comment URL)
   - start.py (script header)
   - DEPLOY.md (title and all references)

3. Decide whether to keep the `elas-erp/` directory (legacy snapshot)
   or remove it to reduce confusion.

4. The `frontend/vercel.json` has a placeholder backend URL
   (`https://your-backend-url.com`) — update before deploying.
```

---

## 10. Plain-English Summary

> **"This branch is 0 commits ahead and 0 commits behind its remote tracking branch — it is fully in sync with `origin/copilot/vscode-mn7kqs1q-4lel`."**
>
> **"There are NO uncommitted changes — the working tree is completely clean."**
>
> **"This looks like a MIXED STATE: the project has been partially rebranded from Elas ERP to Vizpilot. The core framework (layout title, backend app name, package.json name) says Vizpilot, but a significant number of UI pages, deployment configs, Docker files, and helper scripts still say Elas ERP. The rebrand is roughly 50–60% complete."**
>
> **Additional notes:**
> - This is a **shallow clone** with only 2 visible commits. Full Git history from `main` is not available without unshallowing.
> - No `origin/main` branch is visible in this clone, so a direct ahead/behind comparison to main is not possible.
> - The `elas-erp/` directory contains the original full Elas ERP codebase as a snapshot — it is a reference copy, not the active code.
