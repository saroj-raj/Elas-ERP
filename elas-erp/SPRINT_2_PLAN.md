# Sprint 2: Durable Mapping Plan

## Overview
Transform Quick Viz (ephemeral, sampled data) into production-ready dashboards with a canonical schema, live updates, and role-based views.

## Goals
1. **Canonical Schema Design** - Define business entities (e.g., Customer, Order, Invoice) with standardized columns
2. **Mapping & Transforms** - Map uploaded raw files to canonical tables with aliasing and computed fields  
3. **Materialized Views** - Create aggregated views for dashboard KPIs (e.g., monthly_revenue, top_customers)
4. **Background Jobs** - Schedule periodic refreshes when source data changes
5. **Persistent Storage** - Move from JSON files to Postgres for canonical tables + widgets
6. **Live Dashboards** - Wire dashboards to query materialized views instead of static preview data

## Architecture

### 1. Canonical Schema Layer
**Storage:** Postgres with SQLAlchemy ORM

**Core Tables:**
- `canonical_customers` (id, name, email, segment, created_at)
- `canonical_orders` (id, customer_id, order_date, amount, status)
- `canonical_invoices` (id, order_id, invoice_date, amount, paid)
- `canonical_products` (id, name, category, price)
- ...

**Metadata Tables:**
- `data_sources` (id, name, file_path, upload_date, domain, status)
- `field_mappings` (id, source_id, source_col, canonical_table, canonical_col, transform)
- `refresh_jobs` (id, source_id, last_run, next_run, status)

### 2. Mapping Engine
**Endpoint:** `POST /api/mapping/propose`
- Input: uploaded file ID + domain hints
- LLM proposes field mappings (e.g., "Customer Name" → `canonical_customers.name`)
- Returns mapping JSON for user review

**Endpoint:** `POST /api/mapping/save`
- Persist approved mappings to `field_mappings` table

**Endpoint:** `POST /api/mapping/execute`
- Run DuckDB to transform raw CSV → canonical Postgres tables
- Apply transforms: UPPER(), date parsing, type casts, computed columns
- Insert/upsert into canonical tables

### 3. Materialized Views
**Creation:**
```sql
CREATE MATERIALIZED VIEW monthly_revenue AS
SELECT 
  DATE_TRUNC('month', order_date) AS month,
  SUM(amount) AS revenue,
  COUNT(*) AS order_count
FROM canonical_orders
GROUP BY 1;
```

**Refresh Strategy:**
- Incremental refresh on new data arrival
- Full refresh nightly for complex views
- Background worker (Celery or simple cron) triggers `REFRESH MATERIALIZED VIEW`

### 4. Dashboard Integration
**Widget Schema Update:**
```json
{
  "title": "Monthly Revenue",
  "vega_spec": { ... },
  "data_source": {
    "type": "materialized_view",
    "view_name": "monthly_revenue",
    "refresh_interval": "1h"
  }
}
```

**Endpoint:** `GET /api/dashboard/{id}/data`
- Fetch fresh data from materialized views
- Return to frontend for Vega-Lite rendering

### 5. Role-Based Views
**Access Control:**
- `dashboard_permissions` table (dashboard_id, role, can_view, can_edit)
- Filter views by role: CEO sees all metrics, Manager sees team-only

**View Filtering:**
```sql
CREATE VIEW manager_orders AS
SELECT * FROM canonical_orders
WHERE manager_id = current_user_id();
```

## Implementation Phases

### Phase 1: Schema & Mappings (Week 1)
- [ ] Define 5-10 canonical tables for common ERP entities
- [ ] Build LLM-based mapping proposal (domain → table.column)
- [ ] UI for reviewing/editing mappings
- [ ] Execute mapping to populate canonical tables

### Phase 2: Materialized Views (Week 2)
- [ ] Create 10+ common KPI views (revenue, expenses, inventory, etc.)
- [ ] Background worker for scheduled refreshes
- [ ] Incremental refresh logic for large datasets
- [ ] Monitor view staleness and trigger alerts

### Phase 3: Live Dashboards (Week 3)
- [ ] Update widget specs to reference views
- [ ] Build data fetching API for dashboard rendering
- [ ] Add role-based filtering to queries
- [ ] Real-time updates via WebSocket (optional)

### Phase 4: Hardening (Week 4)
- [ ] Schema migrations with Alembic
- [ ] Error handling for bad mappings
- [ ] Data validation and PII detection
- [ ] Audit logs for schema changes
- [ ] Performance optimization (indexes, query tuning)

## Tech Stack Additions
- **Postgres** - Canonical storage + materialized views
- **SQLAlchemy** - ORM for Python backend
- **Alembic** - Schema migrations
- **Celery + Redis** (optional) - Background job queue
- **pgBouncer** (optional) - Connection pooling for scale

## Success Criteria
✅ User uploads CSV → mapping proposed → canonical tables populated  
✅ Dashboards render live data from materialized views  
✅ New file upload triggers incremental refresh  
✅ Role-based access enforced at query level  
✅ Sub-second query times for all KPI views  

## Notes
- Start with simple cron-based refresh, upgrade to Celery if needed
- Use DuckDB for ETL transforms (fast, SQL-based)
- Keep Quick Viz for instant preview; promote to durable after review
- Add schema versioning if canonical tables evolve over time
