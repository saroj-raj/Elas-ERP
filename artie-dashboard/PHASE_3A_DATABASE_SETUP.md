# 🗄️ Phase 3A - Database & Authentication Setup Guide

## ✅ What's Complete

### Backend Infrastructure
1. **Database Configuration** (`backend/app/database.py`)
   - SQLAlchemy engine with connection pooling
   - Session management with `get_db()` dependency
   - Base class for all models

2. **Database Models** (`backend/app/models.py`)
   - ✅ **User**: Authentication with roles (CEO, CFO, Manager, Employee)
   - ✅ **Dashboard**: Per-user dashboard configurations with JSON layout
   - ✅ **Widget**: Dashboard widgets with positions, data, and Vega specs
   - ✅ **BusinessInfo**: Onboarding data storage

3. **Authentication System** (`backend/app/auth.py`)
   - ✅ Password hashing with bcrypt
   - ✅ JWT access tokens (30-minute expiry)
   - ✅ JWT refresh tokens (7-day expiry)
   - ✅ Token verification and decoding

4. **Authentication Endpoints** (`backend/app/api/endpoints/auth.py`)
   - ✅ **POST /api/auth/signup**: Register new user
   - ✅ **POST /api/auth/login**: Login with username/password
   - ✅ **GET /api/auth/me**: Get current user info
   - ✅ **POST /api/auth/refresh**: Refresh access token
   - ✅ OAuth2PasswordBearer integration
   - ✅ Protected route dependencies

5. **Database Initialization** (`backend/app/init_db.py`)
   - ✅ Table creation script
   - ✅ Default admin user creation

6. **Main App Integration** (`backend/app/main.py`)
   - ✅ Auth router added to FastAPI app

### Python Packages Installed
```
✅ SQLAlchemy 2.0.35 (ORM)
✅ psycopg2-binary 2.9.9 (PostgreSQL driver)
✅ alembic 1.13.3 (migrations)
✅ python-jose 3.5.0 (JWT tokens)
✅ passlib 1.7.4 (password hashing)
✅ bcrypt 5.0.0 (hashing algorithm)
✅ python-multipart (form data)
```

---

## 🚀 Quick Start: Database Setup

### Step 1: Install PostgreSQL

**Windows (using Chocolatey):**
```powershell
choco install postgresql
```

**Or download from:** https://www.postgresql.org/download/windows/

**MacOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

---

### Step 2: Create Database and User

Open PostgreSQL command line:
```powershell
# Windows
psql -U postgres

# MacOS/Linux
sudo -u postgres psql
```

Run these SQL commands:
```sql
-- Create database
CREATE DATABASE elas_erp;

-- Create user
CREATE USER elas_user WITH PASSWORD 'elas_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE elas_erp TO elas_user;

-- Connect to database
\c elas_erp

-- Grant schema privileges (PostgreSQL 15+)
GRANT ALL ON SCHEMA public TO elas_user;

-- Exit
\q
```

---

### Step 3: Configure Database URL

**Option A: Environment Variable (Recommended)**
Create `.env` file in `backend/` directory:
```env
DATABASE_URL=postgresql://elas_user:elas_password@localhost:5432/elas_erp
SECRET_KEY=your-secret-key-here-change-in-production
```

**Option B: Direct Configuration**
Edit `backend/app/database.py` (line 7):
```python
DATABASE_URL = "postgresql://elas_user:elas_password@localhost:5432/elas_erp"
```

---

### Step 4: Initialize Database

Run the initialization script:
```powershell
# From project root
cd backend
python -m app.init_db
```

Expected output:
```
============================================================
🚀 ELAS ERP - Database Initialization
============================================================
🔧 Creating database tables...
✅ Database tables created successfully!
✅ Default admin user created!
   📧 Email: admin@elas-erp.com
   🔑 Password: admin123
   ⚠️  IMPORTANT: Change this password in production!

============================================================
✅ Database initialization completed successfully!
============================================================
```

---

### Step 5: Verify Backend is Running

Start the FastAPI backend:
```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open API documentation: http://localhost:8000/docs

You should see new endpoints:
- 🔐 **POST /api/auth/signup**
- 🔐 **POST /api/auth/login**
- 🔐 **GET /api/auth/me**
- 🔐 **POST /api/auth/refresh**

---

## 🧪 Testing the Authentication API

### Test 1: Health Check
```powershell
curl http://localhost:8000/health
```

### Test 2: Login with Default Admin
```powershell
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@elas-erp.com&password=admin123"
```

Expected response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "admin@elas-erp.com",
    "username": "admin",
    "full_name": "System Administrator",
    "role": "ceo",
    "is_active": true
  }
}
```

### Test 3: Get Current User Info
```powershell
# Replace YOUR_ACCESS_TOKEN with token from login response
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Test 4: Create New User (Signup)
```powershell
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "cfo@elas-erp.com",
    "username": "cfo_user",
    "password": "SecurePass123!",
    "full_name": "Chief Financial Officer",
    "role": "cfo"
  }'
```

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'employee',
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Dashboards Table
```sql
CREATE TABLE dashboards (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    description TEXT,
    layout JSONB,  -- Stores widget positions
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Widgets Table
```sql
CREATE TABLE widgets (
    id SERIAL PRIMARY KEY,
    dashboard_id INTEGER REFERENCES dashboards(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    chart_type VARCHAR,
    data JSONB,  -- Chart data
    config JSONB,  -- Widget config
    vega_spec JSONB,  -- Vega-Lite spec
    position_x INTEGER DEFAULT 0,
    position_y INTEGER DEFAULT 0,
    width INTEGER DEFAULT 4,
    height INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔐 Security Configuration

### Change Default Credentials

**1. Generate Strong Secret Key:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

**2. Update in `.env`:**
```env
SECRET_KEY=your-new-secret-key-here
```

**3. Change Admin Password:**
```sql
-- Connect to database
psql -U elas_user -d elas_erp

-- Update admin password (use hashed password from Python)
UPDATE users SET hashed_password = '$2b$12$...' WHERE email = 'admin@elas-erp.com';
```

---

## 🛠️ Troubleshooting

### Issue: "psycopg2.OperationalError: could not connect to server"
**Solution:**
1. Check PostgreSQL is running: `pg_isready`
2. Check credentials in DATABASE_URL
3. Verify PostgreSQL is listening: `netstat -an | findstr 5432`

### Issue: "permission denied for schema public"
**Solution:**
```sql
-- Connect as superuser
psql -U postgres -d elas_erp

-- Grant permissions
GRANT ALL ON SCHEMA public TO elas_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO elas_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO elas_user;
```

### Issue: "relation 'users' does not exist"
**Solution:**
```powershell
# Re-run database initialization
python -m backend.app.init_db
```

### Issue: Backend won't start
**Solution:**
```powershell
# Check for import errors
cd backend
python -c "from app.main import app; print('✅ Imports OK')"

# Check database connection
python -c "from app.database import engine; engine.connect(); print('✅ DB Connected')"
```

---

## 📋 Next Steps

Once database setup is complete, proceed with:

### ⏸️ Phase 3B - Widget Persistence APIs
- Create `/api/widgets` endpoints (save, list, update, delete)
- Create `/api/dashboards` endpoints (save, load, list)
- Test widget CRUD operations

### ⏸️ Phase 3C - Frontend Authentication Pages
- Create `app/login/page.tsx`
- Create `app/signup/page.tsx`
- Create auth context/provider
- Create protected route wrapper
- Update navigation with auth state

### ⏸️ Phase 3D - Role-Based Dashboards
- Create `/dashboard/CEO/page.tsx`
- Create `/dashboard/CFO/page.tsx`
- Create `/dashboard/Manager/page.tsx`
- Create `/dashboard/Employee/page.tsx`
- Define role-specific widget defaults
- Implement widget customization UI

---

## 🔍 Database Inspection Commands

```sql
-- Connect to database
psql -U elas_user -d elas_erp

-- List all tables
\dt

-- Show users
SELECT id, email, username, role, is_active, created_at FROM users;

-- Show dashboards
SELECT id, user_id, role, name, is_default FROM dashboards;

-- Show widgets
SELECT id, dashboard_id, title, type, chart_type FROM widgets;

-- Count records
SELECT 
    (SELECT COUNT(*) FROM users) as users,
    (SELECT COUNT(*) FROM dashboards) as dashboards,
    (SELECT COUNT(*) FROM widgets) as widgets;
```

---

## 📦 Phase 3A Status: 100% Complete ✅

All backend infrastructure for authentication and database is now ready!
- ✅ Database configuration
- ✅ Models defined
- ✅ Auth utilities
- ✅ Auth endpoints
- ✅ Main app integration
- ✅ Initialization script
- ✅ Documentation

**Ready to proceed with Phase 3B (Widget APIs) or Phase 3C (Frontend Auth)!**
