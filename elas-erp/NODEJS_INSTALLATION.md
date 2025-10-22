# Node.js Installation Guide for Windows

## Step-by-Step Installation

### Step 1: Download Node.js

**I've opened the download page in your browser. If it didn't open, visit:**
👉 **https://nodejs.org/en/download/**

### Step 2: Choose the Right Version

**Recommended:** Download the **LTS (Long Term Support)** version
- Currently: Node.js v20.x or v22.x LTS
- Click the **Windows Installer (.msi)** button
- Choose **64-bit** for modern Windows systems

**Alternative:** If you specifically need Node.js v25 (latest), download from:
- https://nodejs.org/en/download/current/

### Step 3: Run the Installer

1. **Locate the downloaded file** (usually in `Downloads` folder)
   - File name: `node-v20.x.x-x64.msi` or similar

2. **Double-click the installer**

3. **Follow the installation wizard:**
   - ✅ Click "Next"
   - ✅ Accept the license agreement
   - ✅ Choose installation location (default is fine: `C:\Program Files\nodejs\`)
   - ✅ **Important:** Ensure "Add to PATH" is checked (default)
   - ✅ Check "Automatically install necessary tools" (optional but recommended)
   - ✅ Click "Install"

4. **Administrator permission:** Click "Yes" when prompted

5. **Wait for installation** (1-2 minutes)

6. **Click "Finish"**

### Step 4: Verify Installation

**Close and reopen PowerShell** (important - to reload PATH), then run:

```powershell
node --version
```
Expected output: `v20.x.x` or `v22.x.x`

```powershell
npm --version
```
Expected output: `10.x.x` or higher

```powershell
npx --version
```
Expected output: `10.x.x` or higher

---

## After Installation: Set Up Elas ERP Frontend

### Step 1: Navigate to Frontend Directory

```powershell
cd C:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP\elas-erp\frontend
```

### Step 2: Install Dependencies

```powershell
npm install
```

This will:
- Read `package.json`
- Download all required packages (~200-300 MB)
- Create `node_modules` folder
- Take 2-5 minutes depending on internet speed

### Step 3: Start Development Server

```powershell
npm run dev
```

Expected output:
```
> elas-erp-frontend@0.1.0 dev
> next dev

   ▲ Next.js 14.2.10
   - Local:        http://localhost:3000
   - Network:      http://192.168.x.x:3000

 ✓ Ready in 2.5s
```

### Step 4: Open Frontend in Browser

Visit: **http://localhost:3000**

You should see: **"Elas ERP Frontend up."**

---

## Running Full Stack (Backend + Frontend)

### Terminal 1: Backend
```powershell
cd C:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP\elas-erp
python main.py
```
Backend runs at: http://127.0.0.1:8000

### Terminal 2: Frontend
```powershell
cd C:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP\elas-erp\frontend
npm run dev
```
Frontend runs at: http://localhost:3000

### Test the Integration
- Backend API: http://127.0.0.1:8000/docs
- Frontend: http://localhost:3000
- Health Check: http://127.0.0.1:8000/health

---

## Troubleshooting

### "node is not recognized as a command"

**Solution:** Restart PowerShell or reopen VS Code terminal after installation.

If still not working:
1. Close all terminals
2. Reopen PowerShell
3. Run: `$env:Path` to verify Node.js path is included
4. If missing, log out and log back in to Windows

### npm install fails with permission errors

**Solution:** Run PowerShell as Administrator, or change npm cache location:

```powershell
npm config set cache C:\Users\rajsa\npm-cache --global
```

### Port 3000 already in use

**Solution:** 
```powershell
# Find process using port 3000
netstat -ano | findstr :3000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or use a different port
npm run dev -- -p 3001
```

### npm install is very slow

**Solution:** Use a faster registry (optional):

```powershell
# Check current registry
npm config get registry

# Use npm official registry (usually fastest)
npm config set registry https://registry.npmjs.org/
```

---

## Quick Commands Reference

```powershell
# Check Node.js version
node --version

# Check npm version
npm --version

# Install packages from package.json
npm install

# Install a specific package
npm install <package-name>

# Start development server
npm run dev

# Build for production
npm run build

# Start production server (after build)
npm start

# Clear npm cache (if issues)
npm cache clean --force

# Update npm to latest version
npm install -g npm@latest
```

---

## What Happens During npm install?

1. **Reads** `package.json` to see required dependencies:
   - next: 14.2.10
   - react: 18.3.1
   - react-vega: 7.6.0
   - @tanstack/react-query
   - etc.

2. **Downloads** packages from npm registry

3. **Creates** `node_modules/` folder with all dependencies

4. **Generates** `package-lock.json` (locks exact versions)

5. **Ready** to run with `npm run dev`

---

## Next Steps After Installation

1. ✅ Verify Node.js: `node --version`
2. ✅ Navigate to frontend: `cd frontend`
3. ✅ Install packages: `npm install`
4. ✅ Start dev server: `npm run dev`
5. ✅ Open browser: http://localhost:3000
6. ✅ Test full stack with backend running

---

## Installation Checklist

- [ ] Downloaded Node.js installer from nodejs.org
- [ ] Ran installer and accepted defaults
- [ ] Checked "Add to PATH" option
- [ ] Completed installation
- [ ] **Restarted PowerShell/Terminal**
- [ ] Verified: `node --version` works
- [ ] Verified: `npm --version` works
- [ ] Navigated to `elas-erp/frontend`
- [ ] Ran `npm install`
- [ ] Ran `npm run dev`
- [ ] Opened http://localhost:3000
- [ ] Saw "Elas ERP Frontend up." message

---

## Ready to Start!

Once installation is complete, return to this terminal and I'll help you run:

1. `npm install` in the frontend directory
2. `npm run dev` to start the development server
3. Test the full Elas ERP application

Let me know when Node.js installation is complete!
