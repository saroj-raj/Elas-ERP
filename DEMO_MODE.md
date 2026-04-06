# DEMO MODE

## Purpose
This file defines how to operate Vizpilot under deadline pressure, especially before demos, presentations, and client calls.

The goal is not perfection.
The goal is a **working, believable, stable demo path**.

---

## 1) Demo priority order
When a demo is close, prioritize in this exact order:

1. Backend runs locally
2. `/health` works
3. Frontend runs locally
4. Landing page works
5. Login works
6. Business onboarding works
7. Team setup works
8. File upload works
9. Documents/proposal step works
10. Dashboard renders

Everything else is secondary.

---

## 2) Golden path
This is the only flow that must be protected during demo crunch:

1. Landing
2. Login
3. Business onboarding
4. Team setup
5. File upload
6. Documents / proposal step
7. Dashboard render

If this works, the product is demo-safe.

---

## 3) What to de-prioritize
These are explicitly secondary during demo crunch:
- Google OAuth
- forgot password
- account settings polish
- deep refactors
- broad cleanup
- archive perfection
- production deployment elegance
- complete test automation
- feature creep
- advanced roadmap items

---

## 4) Demo-safe decision rule
If a feature is unstable and not required for the golden path:
- hide it
- disable it
- defer it
- mention it as next phase if needed

Do not allow a side feature to break the demo path.

---

## 5) Live demo strategy
Preferred presentation order:
1. business problem
2. product flow
3. screenshots
4. architecture
5. optional live demo

Do not make the live demo the backbone if the system is unstable.

---

## 6) Screenshot fallback rule
Always keep these ready:
- landing page screenshot
- onboarding screenshot
- team setup screenshot
- upload/documents screenshot
- dashboard screenshot

If live flow breaks:
- continue with screenshots
- continue with architecture explanation
- continue with business value narrative

Never panic and improvise nonsense.

---

## 7) Presentation truthfulness
Allowed language:
- MVP
- prototype
- implemented core flow
- production hardening in progress
- next phase includes
- pre-rebrand prototype visuals

Not allowed unless verified:
- fully production ready
- everything complete
- all deployment paths stable
- forecasting is built
- all auth methods work

---

## 8) Handling unfinished features
If asked about unfinished items:
- separate "implemented now" from "planned next"
- answer clearly
- do not pretend roadmap items are done

Example:
- "The core onboarding-to-dashboard workflow is implemented."
- "Predictive analytics and forecasting are part of the next phase."

---

## 9) Demo build rules
Before demo time:
- do not rename unnecessary files/folders
- do not attempt risky infra migrations
- do not change the stack
- do not take large refactor risks
- do not debug five unrelated issues at once

Correct behavior:
1. identify current blocker
2. fix blocker
3. retest golden path
4. stop when golden path works

---

## 10) Local vs production rule
If local is stable and production is flaky:
- present local
- do not gamble everything on production deployment

Local stability beats remote instability.

---

## 11) Final pre-demo checklist

### Technical
- backend running
- `/health` working
- frontend running
- login page opens
- onboarding opens
- upload works
- dashboard opens

### Presentation
- screenshots ready
- architecture slide ready
- opening pitch rehearsed
- closing pitch rehearsed
- likely Q&A answers prepared

### Narrative
You must be able to explain:
- what problem Vizpilot solves
- how the workflow works
- how the architecture works
- what is built
- what comes next
- why the product is valuable

---

## 12) Future-feature rule
Roadmap items must remain roadmap items.

Examples:
- dashboard prompt refinement
- durable schema mapping
- anomaly detection
- alerts
- retail inventory and demand forecasting
- project progress analytics
- predictive modules

These should be described as:
- next phase
- planned module
- future extension
- roadmap capability

Not as completed functionality unless fully implemented.

---

## 13) Final principle
During demo crunch:
- working beats elegant
- clarity beats ambition
- honesty beats bluffing
- stable flow beats fancy extras

---
