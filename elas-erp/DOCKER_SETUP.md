# Docker Setup Guide for Elas ERP

## Install Docker Desktop for Windows

### Step 1: Download Docker Desktop

1. Visit: https://docs.docker.com/desktop/install/windows-install/
2. Click "Download Docker Desktop for Windows"
3. Run the installer `Docker Desktop Installer.exe`

### Step 2: System Requirements

**Before installing, ensure:**
- Windows 10 64-bit: Pro, Enterprise, or Education (Build 19041 or higher)
  - OR Windows 11 64-bit: Any edition
- WSL 2 feature enabled (installer will enable this if needed)
- Virtualization enabled in BIOS

### Step 3: Installation Steps

1. Double-click `Docker Desktop Installer.exe`
2. When prompted, ensure "Use WSL 2 instead of Hyper-V" is selected
3. Follow the installation wizard
4. **Restart your computer** when installation completes

### Step 4: Verify Docker Installation

After restarting, open PowerShell and run:

```powershell
docker --version
```

Expected output: `Docker version XX.X.X, build XXXXXXX`

```powershell
docker run hello-world
```

This should download and run a test container.

---

## Set Up Node.js Container for Elas ERP Frontend

Once Docker is installed and verified:

### Step 1: Pull Node.js Alpine Image

```powershell
docker pull node:25-alpine
```

This downloads a lightweight Node.js v25 image (~50MB vs 1GB for full image).

### Step 2: Start Node.js Container with Shell Access

```powershell
docker run -it --rm --entrypoint sh node:25-alpine
```

**Flags explained:**
- `-it` = Interactive terminal
- `--rm` = Remove container when you exit
- `--entrypoint sh` = Start shell instead of Node.js REPL

### Step 3: Verify Node.js and npm Versions

Inside the container shell:

```sh
node -v
# Should print: v25.0.0

npm -v
# Should print: 11.6.2 (or similar)
```

### Step 4: Exit the Container

```sh
exit
```

---

## Using Docker for Elas ERP Frontend Development

### Option A: Run Frontend in Docker Container

Create a container with your project mounted:

```powershell
# From the elas-erp directory:
docker run -it --rm `
  -v ${PWD}/frontend:/app `
  -w /app `
  -p 3000:3000 `
  node:25-alpine sh
```

Inside container:
```sh
npm install
npm run dev
```

Frontend will be accessible at http://localhost:3000

### Option B: Install Node.js Directly on Windows

If you prefer native installation instead of Docker:

1. Visit: https://nodejs.org/
2. Download Node.js v20 LTS or v22+ (recommended)
3. Run the installer
4. Verify: `node -v` and `npm -v` in PowerShell

Then from `elas-erp/frontend/`:
```powershell
npm install
npm run dev
```

---

## Troubleshooting Docker on Windows

### "WSL 2 installation is incomplete"

```powershell
# Enable WSL
wsl --install

# Set WSL 2 as default
wsl --set-default-version 2

# Restart computer
```

### "Docker Desktop requires a newer WSL kernel"

```powershell
wsl --update
```

### "Virtualization is not enabled"

1. Restart computer
2. Enter BIOS/UEFI (usually F2, F10, or Del during boot)
3. Find "Virtualization Technology" or "Intel VT-x" or "AMD-V"
4. Enable it
5. Save and exit

### Docker daemon not starting

1. Open Docker Desktop app
2. Check status in system tray
3. If issues persist, try: Settings → Reset → Reset to factory defaults

---

## Quick Reference

### Common Docker Commands

```powershell
# Check Docker version
docker --version

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# List downloaded images
docker images

# Remove an image
docker rmi node:25-alpine

# Stop a running container
docker stop <container-id>

# Remove stopped containers
docker container prune

# View Docker disk usage
docker system df
```

### Run Node.js Command in Container (without shell)

```powershell
# One-off command
docker run --rm node:25-alpine node -v

# Install packages
docker run --rm -v ${PWD}/frontend:/app -w /app node:25-alpine npm install

# Run development server
docker run --rm -v ${PWD}/frontend:/app -w /app -p 3000:3000 node:25-alpine npm run dev
```

---

## Recommendation for Elas ERP

For **quickest setup**, I recommend:

1. **Install Node.js directly on Windows** (not Docker) from https://nodejs.org/
   - Faster
   - Simpler for development
   - No Docker overhead

2. **Use Docker only if:**
   - You need exact version control (Node.js 25 specifically)
   - Submitting a containerized solution
   - Working in a team with different OS environments

---

## Next Steps

After installing Docker OR Node.js:

1. Navigate to frontend directory:
   ```powershell
   cd C:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP\elas-erp\frontend
   ```

2. Install dependencies:
   ```powershell
   npm install
   ```

3. Start development server:
   ```powershell
   npm run dev
   ```

4. Open http://localhost:3000 in your browser

5. Test the full stack:
   - Terminal 1: `cd elas-erp; python main.py` (backend)
   - Terminal 2: `cd elas-erp/frontend; npm run dev` (frontend)
