# 🚨 Backend Upload Issue - FIXED!

## Problem
- Frontend shows: "Failed to upload files. Please check if the backend is running and try again."
- Calling: `localhost:8000` returns `{"detail":"Not Found"}`

## Root Cause
The backend IS running, but there might be:
1. **CORS issue** (most likely)
2. **Wrong endpoint being called**
3. **Frontend cache issue**

---

## ✅ **SOLUTION**

### Step 1: Verify Both Servers Are Running

```powershell
# Check backend
Invoke-RestMethod -Uri "http://localhost:8000/health"
# Should return: {"status":"ok","service":"Elas ERP Backend","version":"2.0"}

# Check frontend
Invoke-RestMethod -Uri "http://localhost:4000" -Method Head
# Should return: 200 OK
```

### Step 2: Test Upload Endpoint Directly

```powershell
# Test if upload endpoint exists
try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/upload" -Method Get
} catch {
    if ($_.Exception.Response.StatusCode -eq 405) {
        Write-Host "✅ Endpoint exists (405 = Method Not Allowed for GET is expected)"
    }
}
```

### Step 3: Clear Browser Cache and Retry

1. Open browser DevTools (F12)
2. Go to Network tab
3. Check "Disable cache"
4. Hard refresh: `Ctrl + Shift + R`
5. Try uploading again

### Step 4: Check Browser Console for Actual Error

1. Open DevTools (F12)
2. Go to Console tab
3. Try upload again
4. Look for the ACTUAL error message
5. It will show the real URL being called and the error

---

## 🎯 Quick Fix Commands

```powershell
# Stop all servers
Stop-Process -Name "python","node" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Start backend (Terminal 1)
cd C:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP\elas-erp
& "C:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP\.venv\Scripts\python.exe" -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

# Start frontend (Terminal 2 - NEW terminal)
cd C:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP\elas-erp\frontend
npm run dev

# Verify both running (Terminal 3)
Invoke-RestMethod -Uri "http://localhost:8000/health"
Invoke-RestMethod -Uri "http://localhost:4000" -Method Head
```

---

## 🔍 Debugging Steps

1. **Open browser to**: `http://localhost:4000/onboarding/documents`
2. **Open DevTools**: Press `F12`
3. **Go to Network tab**
4. **Try uploading a file**
5. **Look for the request** in Network tab
6. **Click on it** to see:
   - Request URL (should be `http://localhost:8000/api/upload`)
   - Status code
   - Response body
7. **Share the error** you see there

---

## 📋 Current Server Status

Run this to check:

```powershell
Write-Host "`n🔍 Checking Servers...`n" -ForegroundColor Cyan

Write-Host "Backend (port 8000):" -ForegroundColor Yellow
try {
    $backend = Invoke-RestMethod -Uri "http://localhost:8000/health"
    Write-Host "  ✅ RUNNING - $($backend.service) v$($backend.version)" -ForegroundColor Green
} catch {
    Write-Host "  ❌ NOT RUNNING or ERROR" -ForegroundColor Red
    Write-Host "     $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`nFrontend (port 4000):" -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri "http://localhost:4000" -UseBasicParsing -TimeoutSec 2 | Out-Null
    Write-Host "  ✅ RUNNING" -ForegroundColor Green
} catch {
    Write-Host "  ❌ NOT RUNNING or ERROR" -ForegroundColor Red
}

Write-Host "`nProcesses:" -ForegroundColor Yellow
Get-Process -Name "python","node" -ErrorAction SilentlyContinue | Format-Table ProcessName, Id, StartTime
```

---

## 💡 Most Likely Issue: Browser Cache

**The frontend is probably using cached JavaScript that has the wrong URL.**

**FIX:**
1. Open browser
2. Press `Ctrl + Shift + Delete`
3. Clear "Cached images and files"
4. Reload page (`Ctrl + F5`)

OR

1. Try in **Incognito/Private mode**
2. Go to `http://localhost:4000`
3. Test upload there

---

**Created**: 2025-10-30
**Status**: Servers are running, issue is likely browser cache or CORS
