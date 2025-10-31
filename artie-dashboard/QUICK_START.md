# 🚀 Quick Start Guide

## Start Your Elas ERP System

### Step 1: Start Backend Server
Open PowerShell terminal and run:
```powershell
cd c:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP\elas-erp
uvicorn backend.app.main:app --reload --port 8000
```

**Leave this terminal running!**

---

### Step 2: Start Frontend Server
Open a **NEW** PowerShell terminal and run:
```powershell
cd c:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP\elas-erp\frontend
npm run dev
```

**Leave this terminal running too!**

---

### Step 3: Open Your Browser
Go to: **http://localhost:4000**

---

### Step 4: Login
Use any of these demo accounts:

**Admin Dashboard:**
- Email: `admin@elas-erp.com`
- Password: anything (mock auth)

**Finance Dashboard:**
- Email: `finance@elas-erp.com`
- Password: anything

**Manager Dashboard:**
- Email: `manager@elas-erp.com`
- Password: anything

**Employee Dashboard:**
- Email: `employee@elas-erp.com`
- Password: anything

---

## 🎯 What You'll See

### 1. Admin Dashboard
- 4 KPI cards (Revenue, AR, DSO, Cash Flow)
- Multiple interactive charts
- Blue role switcher button (top right)
- User menu with logout

### 2. Finance Dashboard
- Financial KPIs
- Cash flow analysis
- AR aging distribution
- Expense breakdown
- Revenue by client
- Budget vs actual

### 3. Manager Dashboard
- Team performance metrics
- Skills radar chart
- Weekly productivity
- Project status tracking
- Meeting schedule

### 4. Employee Dashboard
- Personal task list
- Time tracking
- Productivity trends
- Upcoming deadlines
- Recent activity

---

## 🔐 Real Authentication Test

### Option 1: Use Test Script
```powershell
cd c:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP\elas-erp
.\test_auth.ps1
```

### Option 2: Use API Docs
1. Open: http://localhost:8000/docs
2. Find `/api/auth/login`
3. Click "Try it out"
4. Login with:
   - email: `admin@elas-erp.com`
   - password: `admin123`
5. Should receive JWT tokens!

---

## ⚡ Quick Tips

- **Switch Roles:** Click the blue button in top-right corner
- **Logout:** Click your name in top-right, then logout
- **View API:** http://localhost:8000/docs
- **Check Database:**
  ```powershell
  & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U elas_user -d elas_erp
  # Password: elas_password
  ```

---

## 🆘 Problems?

### Backend won't start?
Make sure you're in the **elas-erp** folder (not frontend):
```powershell
cd c:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP\elas-erp
```

### Port already in use?
Stop any running servers first:
```powershell
# Find process on port 8000
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

# Kill it if needed
Stop-Process -Id <PID>
```

### PostgreSQL not running?
```powershell
Start-Service postgresql-x64-18
```

---

## 📚 More Information

- **Full Features:** See `IMPLEMENTATION_COMPLETE.md`
- **PostgreSQL Setup:** See `POSTGRESQL_SETUP_COMPLETE.md`
- **Quick Summary:** See `SETUP_COMPLETE_SUMMARY.md`

---

**That's it! You're all set!** 🎉

Enjoy your Elas ERP system!
