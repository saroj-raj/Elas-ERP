# Elas ERP - Docker Quick Reference

## ✅ Status: Both Backend and Frontend Running!

### 🌐 Access Your Application

- **Backend API**: http://localhost:8000
  - API Documentation (Swagger): http://localhost:8000/docs
  - Health Check: http://localhost:8000/health

- **Frontend**: http://localhost:4000
  - Main Application UI

---

## 🚀 Quick Start Commands

### Start Both Services (Backend + Frontend)
```powershell
# From elas-erp directory:
docker compose up -d
```

**Or use the helper script:**
```powershell
.\start-docker.ps1
```

### Stop Both Services
```powershell
docker compose down
```

**Or use the helper script:**
```powershell
.\stop-docker.ps1
```

### View Logs
```powershell
# All logs
docker compose logs -f

# Backend only
docker logs elas-erp-backend -f

# Frontend only
docker logs elas-erp-frontend -f
```

### Rebuild After Code Changes
```powershell
docker compose up --build -d
```

### Check Status
```powershell
docker ps
```

---

## 📦 What's Running?

| Service | Container Name | Port Mapping | Image |
|---------|---------------|--------------|-------|
| Backend | `elas-erp-backend` | 8000:8000 | Custom (Python 3.11) |
| Frontend | `elas-erp-frontend` | 4000:3000 | node:20 |

**Note**: Frontend runs on port 4000 (mapped from internal port 3000) due to Windows port restrictions on ports 3000-3052.

---

## 🛠️ Development Workflow

### 1. **Start the Application**
```powershell
cd C:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP\elas-erp
docker compose up -d
```

### 2. **Make Code Changes**
- Backend changes: Edit files in `backend/app/`
- Frontend changes: Edit files in `frontend/`
- Changes are automatically detected (hot reload enabled)

### 3. **View Changes**
- Backend: Watch logs with `docker logs elas-erp-backend -f`
- Frontend: Refresh http://localhost:4000

### 4. **Stop When Done**
```powershell
docker compose down
```

---

## 🔧 Troubleshooting

### Port Already in Use
If you see "port is already allocated":
```powershell
# Check what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :4000

# Stop the process or change port in docker-compose.yml
```

### Container Won't Start
```powershell
# Check logs
docker logs elas-erp-backend
docker logs elas-erp-frontend

# Restart containers
docker compose restart
```

### Backend Shows "ModuleNotFoundError"
This should be fixed, but if it happens:
```powershell
# Rebuild completely
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Frontend npm install is slow
First run takes 2-5 minutes to install packages. Subsequent runs are faster because `node_modules` is cached in a Docker volume.

### Database or S3 Errors
Make sure you have a `.env` file in the `backend` directory with:
```
GROQ_API_KEY=your_key_here
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
AWS_REGION=us-east-1
S3_BUCKET=elas-erp-demo
```

---

## 📊 Container Management

### Start/Stop Individual Services
```powershell
# Start only backend
docker start elas-erp-backend

# Stop only frontend
docker stop elas-erp-frontend
```

### Restart Services
```powershell
# Restart both
docker compose restart

# Restart backend only
docker restart elas-erp-backend
```

### Remove Everything (Clean Slate)
```powershell
# Stop and remove containers, networks
docker compose down

# Also remove volumes (deletes node_modules cache)
docker compose down -v

# Also remove images (forces rebuild)
docker compose down --rmi all
```

---

## 🔍 Useful Commands

### Execute Commands Inside Containers
```powershell
# Open shell in backend container
docker exec -it elas-erp-backend sh

# Open shell in frontend container
docker exec -it elas-erp-frontend sh
```

### Check Resource Usage
```powershell
docker stats elas-erp-backend elas-erp-frontend
```

### View Container Details
```powershell
docker inspect elas-erp-backend
docker inspect elas-erp-frontend
```

---

## 🌟 Benefits of Docker Setup

✅ **Single Command Start**: `docker compose up -d` starts everything  
✅ **No Node.js Installation**: Frontend runs in container  
✅ **No Python Installation**: Backend runs in container  
✅ **Isolated Environment**: No conflicts with system packages  
✅ **Consistent Across Machines**: Same environment everywhere  
✅ **Easy Cleanup**: `docker compose down` stops everything  
✅ **Hot Reload**: Code changes automatically detected  

---

## 🎯 Next Steps

1. ✅ Both services are running
2. Visit http://localhost:8000/docs to explore the API
3. Visit http://localhost:4000 to see the frontend
4. Make changes to code and see them live reload
5. Use `docker compose logs -f` to monitor both services

---

## 💡 Tips

- Use `docker compose up` (without `-d`) to see logs in the terminal
- Press `Ctrl+C` to stop when running in foreground mode
- Keep Docker Desktop running in the background
- Check Docker Desktop dashboard for visual container management

---

## 🔗 Related Files

- `docker-compose.yml` - Orchestrates both services
- `backend/Dockerfile` - Backend container definition
- `start-docker.ps1` - Helper script to start
- `stop-docker.ps1` - Helper script to stop
- `backend/.env` - Backend environment variables (create this!)

---

**Ready to develop!** 🚀
