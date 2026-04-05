# MASTER RULES

## 0) Non-negotiables
- Stack is locked to free tiers: **Vercel (FE)**, **Render (BE)**, **Neon or Supabase Postgres (DB)**, **Supabase Storage (files)**, **Groq LLM** (`llama-3.3-70b-versatile`).
- No paid services, no surprise infra (no Railway/AWS unless explicitly approved).
- Never commit secrets. All secrets via provider env managers.

## 1) Deployment contracts
- Frontend reads `process.env.NEXT_PUBLIC_API_BASE` only (no hardcoded localhost in prod).
- Backend exposes stable endpoints:
  - `POST /api/upload`
  - `POST /api/widgets/propose`
  - `POST /api/widgets/save`
  - `GET  /api/dashboard/{role}`
  - `GET  /health`, `GET /version`
- CORS allowlist is explicit: dev `http://localhost:4000`, prod Vercel URL(s) only.

## 2) LLM & chart spec rules
- LLM returns **Vega-Lite JSON only**, no inline `data.values`, no code fences.
- Backend validates via Pydantic; on invalid JSON: **deterministic fallbacks** (trend, top-N).
- Never let LLM generate SQL or access secrets.

## 3) Data handling
- Uploads → **Supabase Storage** (bucket `vizpilot-uploads`), local temp allowed only in dev.
- Canonical tables + views in Postgres; widgets bind to data by name (no inline arrays in specs).
- PII: mask likely PII in previews; row-level exports only via authenticated endpoints.

## 4) Auth & roles
- Supabase Auth (email/password). Roles: `admin`, `finance`, `manager`, `viewer`.
- Role-based dashboards: `/dashboard/{role}` loads saved widgets + layout.

## 5) Git discipline
- Small, working commits with descriptive messages.
- Blocked files: `.env*`, `node_modules/`, `.next/`, `__pycache__/`, `.vercel/`, `.DS_Store`, `*.log`.
- PRs must pass **lint + unit tests + e2e flow** before merge to `main`.

## 6) Copilot guardrails (anti-hallucination)
- Do not suggest other clouds or paid add-ons.
- Do not invent files/paths; follow the repo structure.
- Where code relies on envs, show the exact key name (don’t fabricate).
- If uncertain, generate **minimal stubs** and TODOs rather than assumptions.

## 7) Observability & Testing
- **Current observability:** Add `X-Request-ID` per request; log LLM latency and fallback usage. Never log secrets or full file contents.
- **Current testing:** Backend unit tests (`backend/tests/`) validate `/health`, `/api/upload`, `/api/widgets/propose` endpoints.
- **E2E testing planned for Phase 2:** Will implement Playwright flow (login → upload → save dashboard) once mock services (`APP_ENV=test`, `GROQ_MODE=mock`, `AUTH_MODE=mock`) are built.
  - **Future test user:** `test@vizpilot.local` / `password`.

## 8) Release process
- `main` is protected. Merge only via PR after CI green.
- Tag releases `vX.Y.Z` once FE+BE are live and smoke tests pass.
