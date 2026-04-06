# COPILOT RULES

## Purpose
This file defines how Copilot must behave while working on Vizpilot.

Copilot is an assistant for:
- inspection
- analysis
- code generation
- debugging
- proposing safe changes

Copilot is **not** allowed to act like an autonomous release engineer, Git operator, or infrastructure improviser.

---

## 1) Required operating pattern
Copilot must always follow this sequence:

1. **Inspect first**
2. **Explain findings**
3. **Identify root cause**
4. **Propose the minimal safe fix**
5. **Wait for approval**
6. **Apply only approved changes**
7. **Retest**
8. **Report outcome clearly**

Copilot must never skip directly to large changes without confirming what is actually true.

---

## 2) Anti-hallucination rules
Copilot must not invent:
- files
- directories
- routes
- environment variables
- APIs
- service names
- deployment paths
- repo structure
- database schema
- feature completeness

If something is not verified, Copilot must say:
- verified
- not verified
- needs manual confirmation

If a file/path/env key is missing, Copilot must say so explicitly.

---

## 3) Git safety rules
Copilot must never automatically run:
- `git commit`
- `git push`
- `git pull`
- `git reset --hard`
- `git clean -fd`
- `git rebase`
- branch deletion
- force-push
- destructive stash operations

Copilot may:
- inspect git state
- summarize git state
- compare branches
- explain divergence
- propose safe commands

Any Git-changing command requires explicit human approval.

---

## 4) Scope control rules
Copilot must solve **one blocker at a time**.

Correct order:
1. verify current blocker
2. fix blocker
3. retest
4. move to next blocker

Copilot must not:
- refactor unrelated code while debugging startup
- clean docs while auth is broken
- rename things while the demo flow is unstable
- debug deployment before local flow works
- mix multiple unrelated fixes into one change set unless approved

---

## 5) Demo-first rule
When a presentation or demo deadline is near:
- optimize for the **golden path**
- prioritize working local flow over full deployment polish
- prefer hiding unstable features over fixing everything
- do not waste time on non-demo cleanup

### Golden path
1. Landing
2. Login
3. Business onboarding
4. Team setup
5. File upload
6. Documents / proposal step
7. Dashboard render

If the golden path is broken, Copilot must prioritize fixing it above all else.

---

## 6) Local-before-production rule
Copilot must not prioritize production deployment until:
- backend runs locally
- frontend runs locally
- `/health` works
- login page loads
- onboarding works
- upload works
- dashboard renders

If local is broken, production debugging is secondary.

---

## 7) Deployment guardrails
Approved deployment stack only:
- Vercel for frontend
- Render for backend
- Supabase for auth/storage/database
- Groq for LLM

Copilot must not suggest:
- Railway
- AWS
- S3
- R2
- Firebase
- random paid add-ons

Unless explicitly approved.

---

## 8) Environment variable rules
Copilot must never invent env keys.

Copilot must only use env vars that are verified in code or explicitly approved.

Examples commonly allowed only when verified:
- `NEXT_PUBLIC_API_BASE`
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `GROQ_API_KEY`
- `FRONTEND_URL`
- `ALLOWED_ORIGINS`
- `APP_ENV`

---

## 9) Backend rules
Copilot must treat backend startup issues as:
1. environment issue first
2. import-path issue second
3. application code issue third

Preferred backend run context:
- run from `backend/`
- preferred command:
  ```bash
  python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
  ```

Copilot must verify:
- `/health`
- `/docs`

Before claiming backend is fixed.

---

## 10) Frontend rules
Preferred frontend run context:
- run from `frontend/`
- preferred command:
  ```bash
  npm run dev -- -p 4000
  ```

Frontend must use:
- `NEXT_PUBLIC_API_BASE`

Copilot must not leave hardcoded localhost in production code.

---

## 11) AI / LLM rules
Copilot must treat AI integration carefully.

Rules:
- AI output should be structured
- prefer Vega-Lite style specs
- no inline data arrays
- no code fences in payload
- validate outputs before render
- fallback deterministically if AI fails

If AI is unstable, Copilot must not allow it to break the golden path.

---

## 12) Communication rules
Copilot must describe project status honestly.

Allowed:
- prototype
- MVP
- partial
- implemented core flow
- next phase
- production hardening in progress

Not allowed unless verified:
- fully production ready
- complete
- universal
- all flows stable

---

## 13) File discipline
Copilot must preserve:
- `README.md`
- `RULES.md`
- `TODO.md`
- `DEPLOYMENT_GUIDE.md`
- deployment configs
- `.env.example`

Copilot may archive:
- status docs
- debug summaries
- cleanup notes
- phase summaries
- duplicate deploy notes

Archive before delete when uncertain.

---

## 14) End condition
Copilot must stop and report once:
- the approved blocker is fixed
- the approved test passes
- the next blocker is identified

Copilot must not continue making extra changes "while already there."

---
