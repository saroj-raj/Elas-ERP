# Artie Dashboard — Groq-powered Demo

Give every new customer role-aware charts in under 30 seconds from a single file upload. This demo uses Groq LLMs for proposal text and widget selection with LangChain + LangGraph-friendly services.

## Contents

- [What this is](#what-this-is)
- [Architecture](#architecture)
- [Tech stack](#tech-stack)
- [Quick start (local)](#quick-start-local)
- [Environment variables](#environment-variables)
- [Run with Docker](#run-with-docker)
- [Deploy for a demo URL](#deploy-for-a-demo-url)
- [API reference](#api-reference)
- [Demo flow](#demo-flow)
- [Notes](#notes)

---

## What this is

- **Fast path**: upload CSV → infer simple hints → Groq suggests 3–6 widgets → return Vega-Lite specs for instant preview.
- **Durable path** (stubbed): mapping → canonical tables → bind charts to SQL views. In this demo, we focus on the fast path for screening.

## Architecture

- Frontend: Next.js + react-vega renders Vega-Lite JSON.
- Backend: FastAPI exposes `/api/upload` and `/api/chat/propose`.
- LLM: Groq models via `langchain-groq` drive concise proposals and chart titles.
- Data: DuckDB profiles samples for dates, measures, and categories.

```text
Next.js  →  FastAPI  →  DuckDB
↘  Groq (LangChain)
```

## Tech stack

- Frontend: Next.js, React, Typescript, react-vega, TanStack Query
- Backend: FastAPI, Python, DuckDB, Pandas
- LLM: Groq via langchain-groq (`llama-3.1-70b-versatile` default)
- Infra: Docker Compose for local and demo deployments

---

## Quick start (local)

Requirements: Python 3.11+, Node 20+, Docker (optional)

```bash
# clone and enter
git clone <your-repo-url> artie-dashboard
cd artie-dashboard

# backend env
cp backend/.env.example backend/.env
# put your GROQ_API_KEY into backend/.env

# create venv and install
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# run API
uvicorn app.main:app --reload --port 8000
# health check: http://localhost:8000/health
```

In a second terminal:

```bash
cd frontend
npm install
# set API base if not using Docker:
echo "NEXT_PUBLIC_API_BASE=http://localhost:8000" > .env.local
npm run dev
# open http://localhost:3000
```

---

## Environment variables

`backend/.env`

* `GROQ_API_KEY` **required** — your Groq key
* `GROQ_MODEL` defaults to `llama-3.1-70b-versatile`
* Other values are optional for this demo

`frontend/.env.local`

* `NEXT_PUBLIC_API_BASE` e.g. `http://localhost:8000` or your hosted backend URL

Groq model options (typical):

* `llama-3.1-70b-versatile` — balanced quality
* `llama-3.1-8b-instant` — cheaper, faster

---

## Run with Docker

```bash
# at repo root
cp backend/.env.example backend/.env
# set GROQ_API_KEY in backend/.env

docker compose up --build
# web: http://localhost:3000
# api: http://localhost:8000/health
```

Compose sets `NEXT_PUBLIC_API_BASE=http://api:8000` so the frontend talks to the backend container.

---

## Deploy for a demo URL

### Option A: Frontend on Vercel, Backend on Render

1. **Backend (Render)**

	 * Create a new “Web Service”, point to `/backend`
	 * Runtime: Python 3.11
	 * Build Command: `pip install -r requirements.txt`
	 * Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
	 * Add env vars from `backend/.env` including `GROQ_API_KEY`
	 * Note the public URL, e.g. `https://artie-api.onrender.com`

2. **Frontend (Vercel)**

	 * Import project, set root to `/frontend`
	 * Set env var: `NEXT_PUBLIC_API_BASE=https://artie-api.onrender.com`
	 * Deploy

---

## API reference

`GET /health`
Returns `{ "status": "ok" }`

`POST /api/upload`
Form-data:

* `file`: CSV/XLSX
* `domain`: `"sales" | "finance" | "operations"`
* `intent`: `"trends" | "leaderboard" | "funnel" | "aging"`

Response:

```json
{
	"dataset_id": "uuid_filename.csv",
	"widgets": [
		{
			"title": "Monthly Trend",
			"explanation": "Short rationale",
			"vega_spec": { /* vega-lite JSON */ },
			"role": "auto"
		}
	]
}
```

`POST /api/chat/propose`
JSON:

```json
{
	"domain": "sales",
	"intent": "trends",
	"columns": ["order_date","region","amount","rep"],
	"hints": {"has_date": true, "date_field": "order_date", "measures":["amount"], "categories":["region","rep"]}
}
```

Returns a list of structured proposal objects.

---

## Demo flow

1. Open the frontend URL.
2. Upload a small CSV and select domain + intent.
3. You’ll get a grid of widgets; each renders via `react-vega`.
4. Show the code-free narrative: Groq suggested widgets; you can save or adjust.
5. If needed, call `/api/chat/propose` from a small admin tool to demonstrate proposal variability.

Recommended demo CSV columns:

* For sales: `order_date,rep,region,amount,cost,product,qty`
* For finance: `invoice_id,invoice_date,due_date,customer,amount,paid_amount`

---

## Notes

* This demo focuses on the **quick viz** path. The durable mapping/ETL to Postgres is intentionally stubbed to avoid scope blow-up during interviews.
* Groq use is minimal and safe: proposals and titles. All data logic stays deterministic.
* Vega-Lite keeps your charts declarative and portable; the UI can inject preview data for instant rendering.

---

## Scripts cheat sheet

Local API:

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Local web:

```bash
cd frontend
npm run dev
```

Docker:

```bash
docker compose up --build
```

Deploy:

* Render backend start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
* Vercel frontend env: `NEXT_PUBLIC_API_BASE=<render-backend-url>`

