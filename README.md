# Vizpilot - AI Data Intelligence Platform

> An intelligent data analysis and visualization platform with AI-powered insights, role-based dashboards, and secure authentication.

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://vizpilot.vercel.app)
[![Backend](https://img.shields.io/badge/backend-deployed-success)](https://vizpilot.onrender.com/health)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 🚀 Live Application

- **Frontend:** https://vizpilot.vercel.app
- **Backend API:** https://vizpilot.onrender.com
- **API Docs:** https://vizpilot.onrender.com/docs

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Documentation](#-documentation)
- [Deployment](#-deployment)
- [Development](#-development)

---

## ✨ Features

### Core Functionality
- 🏢 **Multi-Tenant Architecture** - Isolated data for multiple organizations
- 🔐 **Secure Authentication** - Supabase Auth with email/password and Google OAuth
- 👥 **Role-Based Access Control** - Admin, Manager, Employee, Finance roles
- 📊 **Interactive Dashboards** - AI-powered role-specific data insights
- 📄 **AI Data Processing** - Upload and analyze business data files
- 👥 **Team Collaboration** - Invitation system for team members
- 🔍 **Audit Logging** - Complete audit trail for all actions

### Current Status
✅ **Completed:**
- Authentication & authorization (signup, login, email confirmation)
- Multi-tenant database with Row Level Security
- Role-based routing and navigation
- File upload interface
- Backend API endpoints
- Production deployment

🔄 **In Progress:**
- Dashboard data integration
- AI document analysis
- Team invitation acceptance flow

⏸️ **Planned:**
- Advanced analytics
- Custom dashboard widgets
- Mobile responsiveness
- Real-time collaboration

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** Next.js 14.1.0 (App Router)
- **Language:** TypeScript
- **UI Library:** React 18
- **Styling:** Tailwind CSS
- **Authentication:** Supabase Client
- **Deployment:** Vercel

### Backend
- **Framework:** FastAPI (Python)
- **Server:** Uvicorn
- **Validation:** Pydantic
- **Authentication:** Supabase SDK
- **AI:** GROQ (Llama models)
- **Deployment:** Render

### Database
- **Database:** PostgreSQL (Neon)
- **Auth & Storage:** Supabase
- **Security:** Row Level Security (RLS)

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/VizPilot.git
   cd VizPilot
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your Supabase credentials
   python -m uvicorn app.main:app --reload --port 8000
   ```

3. **Frontend Setup** (in a new terminal)
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local
   # Edit .env.local with your API URL and Supabase credentials
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:4000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

---

## 📁 Project Structure

```
VizPilot/
├── frontend/                 # Next.js application
│   ├── app/
│   │   ├── components/      # Reusable React components
│   │   ├── contexts/        # React Context providers
│   │   ├── dashboard/       # Role-based dashboards
│   │   │   ├── [role]/     # Dynamic role routing
│   │   │   └── admin/      # Admin dashboard
│   │   ├── login/          # Login page
│   │   ├── signup/         # Signup page
│   │   └── onboarding/     # File upload flow
│   ├── lib/                # Utilities and helpers
│   ├── middleware.ts       # Route protection
│   └── package.json
│
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── db/
│   │   │   └── schema.sql  # Database schema with RLS
│   │   ├── models/         # Pydantic models
│   │   ├── services/       # Business logic layer
│   │   │   ├── auth_service.py
│   │   │   ├── invitation_service.py
│   │   │   └── supabase_client.py
│   │   └── api/
│   │       └── endpoints/  # API routes
│   │           ├── auth.py
│   │           └── upload.py
│   ├── requirements.txt
│   └── render.yaml         # Render deployment config
│
├── PROJECT_STATUS.md        # Comprehensive project analysis
├── DEPLOYMENT_GUIDE.md      # Deployment instructions
├── SUPABASE_SETUP.md        # Database setup guide
└── README.md               # This file
```

---

## 📚 Documentation

- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Complete project overview and status
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Step-by-step deployment guide
- **[QUICK_DEPLOY.md](QUICK_DEPLOY.md)** - Quick deployment reference
- **[PHASE_C_COMPLETE.md](PHASE_C_COMPLETE.md)** - Phase C completion summary
- **[SUPABASE_SETUP.md](SUPABASE_SETUP.md)** - Database and auth setup
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - API and command reference

---

## 🌐 Deployment

### Production Environment

**Frontend (Vercel):**
- Automatic deployment on `git push` to `main` branch
- Build time: ~60 seconds
- Environment variables configured in Vercel dashboard

**Backend (Render):**
- Automatic deployment on `git push` to `main` branch
- Free tier (sleeps after 15 min inactivity)
- Environment variables configured in Render dashboard

**Database (Supabase):**
- PostgreSQL database with automatic backups
- Row Level Security enabled
- Auth and Storage configured

### Environment Variables

**Frontend (.env.production):**
```bash
NEXT_PUBLIC_API_BASE=https://vizpilot.onrender.com
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

**Backend (.env):**
```bash
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
DATABASE_URL=your_postgresql_url
GROQ_API_KEY=your_groq_api_key
CORS_ORIGINS=https://vizpilot.vercel.app
FRONTEND_URL=https://vizpilot.vercel.app
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## 💻 Development

### Available Scripts

**Frontend:**
```bash
npm run dev          # Start development server
npm run build        # Production build
npm run start        # Start production server
npm run lint         # Run ESLint
```

**Backend:**
```bash
python -m uvicorn app.main:app --reload   # Development server
pytest                                     # Run tests
```

### Database Schema

The application uses 6 main tables:
- `businesses` - Organization information
- `users` - User accounts with roles
- `invitations` - Team member invitations
- `uploaded_files` - Document tracking
- `dashboards` - Dashboard configurations
- `audit_logs` - Activity tracking

All tables implement Row Level Security for multi-tenant isolation.

### API Endpoints

**Authentication:**
- `POST /api/auth/signup` - Create new business account
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - User logout

**Team Management:**
- `POST /api/auth/invite` - Invite team member
- `GET /api/auth/invite/{token}` - Get invitation details
- `POST /api/auth/invite/accept` - Accept invitation
- `GET /api/auth/invitations` - List invitations

**File Upload:**
- `POST /api/upload` - Upload documents
- `GET /api/files` - List uploaded files

See API documentation at `/docs` for complete reference.

---

## 🔐 Security

- Row Level Security (RLS) on all database tables
- JWT authentication with Supabase
- CORS configured for specific origins
- Environment variables for sensitive data
- httpOnly cookies for session management
- Input validation with Pydantic

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Saroj Raj** - [GitHub](https://github.com/saroj-raj)

---

## 🙏 Acknowledgments

- Supabase for authentication and database
- Vercel for frontend hosting
- Render for backend hosting
- GROQ for AI capabilities

---

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review [PROJECT_STATUS.md](PROJECT_STATUS.md) for current status

---

**Built with ❤️ using Next.js, FastAPI, and Supabase**

## Overview

Vizpilot is a full-stack AI data intelligence platform featuring:
- **Backend**: FastAPI (Python) REST API
- **Frontend**: Next.js 14 with TypeScript, React 18, and Tailwind CSS
- **Database**: PostgreSQL
- **Deployment**: Docker & Docker Compose support

## Quick Start

### Prerequisites

- **Node.js**: v20 or higher (v22.20.0 recommended)
- **npm**: v10 or higher
- **Python**: 3.11 or higher
- **Docker Desktop**: For containerized deployment (optional)

### Frontend-First Setup (Recommended for Development)

This approach runs the frontend locally for faster development and better debugging:

1. **Install Node.js dependencies**:
   ```powershell
   cd frontend
   npm install
   ```

2. **Start the frontend**:
   ```powershell
   npm run dev
   ```
   
   The frontend will be available at http://localhost:4000

3. **Start the backend** (choose one):
   
   **Option A - Docker (recommended)**:
   ```powershell
   docker compose up -d backend
   ```
   Backend API will be at http://localhost:8000
   
   **Option B - Local Python**:
   ```powershell
   cd backend
   python -m uvicorn app.main:app --reload --port 8000
   ```

### Docker Setup (Full Stack)

Run both frontend and backend in containers:

```powershell
docker compose up -d
```

- Frontend: http://localhost:4000
- Backend API: http://localhost:8000

Stop services:
```powershell
docker compose down
```

### Single Command Launcher

Run both frontend and backend with one command:

```powershell
python main.py
```

**Available flags**:
- `--backend-only` or `--no-frontend`: Start only backend (skip frontend)
- `--port <PORT>`: Custom port for frontend (default: 4000)

**Environment variables**:
- `WEB_PORT`: Frontend port (default: 4000)
- `LAUNCHER_BACKEND_ONLY=1`: Skip frontend startup
- `LAUNCHER_SKIP_FRONTEND_PROMPT=1`: Auto-skip frontend if npm missing

## Port Configuration

**Default ports**:
- Frontend: **4000** (changed from 3000 due to Windows port exclusions)
- Backend: **8000**

**Windows users**: Ports 2953-3052 are often reserved by Windows. If you encounter port conflicts, use port 4000 or higher.

## Troubleshooting

### npm not recognized / npm command not found

**Symptoms**: `npm : The term 'npm' is not recognized as the name of a cmdlet...`

**Cause**: Node.js is installed but not in your system PATH, or installed via NVM for Windows without activation.

**Solutions**:

1. **If using NVM for Windows** (check `nvm version`):
   ```powershell
   nvm use 22.20.0
   # Or install and use latest LTS
   nvm install lts
   nvm use lts
   ```

2. **Temporary PATH fix** (current PowerShell session only):
   ```powershell
   # Find your Node installation
   Get-Command node.exe -ErrorAction SilentlyContinue
   
   # If Node is at C:\Users\YourName\AppData\Local\nvm\v22.20.0:
   $env:Path = "C:\Users\YourName\AppData\Local\nvm\v22.20.0;" + $env:Path
   
   # Verify
   npm -v
   ```

3. **Permanent PATH fix**:
   - Open **System Properties** → **Environment Variables**
   - Under **User variables**, edit **Path**
   - Add your Node.js installation directory (e.g., `C:\Program Files\nodejs` or `C:\Users\YourName\AppData\Local\nvm\v22.20.0`)
   - Restart PowerShell/VS Code

4. **Fresh Node.js installation**:
   - Download from https://nodejs.org/
   - Run installer with "Add to PATH" option checked
   - Restart terminal

**Testing your fix**:
```powershell
node -v   # Should show v22.20.0 or similar
npm -v    # Should show v10.9.3 or similar
```

### Port Already in Use

**Error**: `EADDRINUSE: address already in use :::4000`

**Solutions**:

1. **Stop conflicting service**:
   ```powershell
   # Stop Docker frontend container
   docker stop vizpilot-frontend
   
   # Or stop all Docker services
   docker compose down
   ```

2. **Use different port**:
   ```powershell
   # In frontend/
   npm run dev -- -p 4001
   
   # Or with main.py
   python main.py --port 4001
   ```

3. **Find process using port**:
   ```powershell
   netstat -ano | findstr :4000
   # Kill process by PID
   taskkill /F /PID <PID>
   ```

### Python Virtual Environment Issues

**Error**: `ModuleNotFoundError: No module named 'backend'`

**Solution**: The virtual environment is located at `../VizPilot/.venv` (parent directory):

```powershell
# Activate venv
& "..\VizPilot\.venv\Scripts\Activate.ps1"

# Install backend dependencies
cd backend
pip install -r requirements.txt
```

### Docker Build Failures

**Error**: `failed to solve: failed to compute cache key`

**Solution**: Rebuild without cache:
```powershell
docker compose build --no-cache
docker compose up -d
```

## Development Workflow

### Frontend Development

```powershell
cd frontend
npm install          # First time only
npm run dev          # Start dev server on port 4000
npm run build        # Production build
npm run start        # Production server
npm run lint         # Check code style
```

### Backend Development

**Local development**:
```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**With Docker**:
```powershell
docker compose up -d backend
docker compose logs -f backend  # View logs
docker compose restart backend  # After code changes
```

### Running Tests

```powershell
# Backend tests (from backend/)
pytest

# Frontend tests (from frontend/)
npm test
```

## Project Structure

```
VizPilot/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── api/              # API routes
│   │   ├── models/           # Database models
│   │   └── schemas/          # Pydantic schemas
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── dashboard/[role]/ # Role-based dashboards
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/           # React components
│   ├── lib/                  # Utilities
│   ├── public/               # Static assets
│   ├── package.json
│   └── next.config.mjs
├── docker-compose.yml
├── main.py                   # Single-command launcher
└── README.md
```

## Technology Stack

### Backend
- **Framework**: FastAPI 0.115.12
- **Python**: 3.11+
- **ORM**: SQLAlchemy (likely)
- **Database**: PostgreSQL
- **Server**: Uvicorn

### Frontend
- **Framework**: Next.js 14.2.33
- **React**: 18.3.1
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 3.4.1
- **UI Components**: Radix UI, Lucide Icons
- **Forms**: React Hook Form + Zod validation
- **State**: React Context/Hooks

## Environment Variables

Create `.env` files for configuration:

**backend/.env**:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/vizpilot
SECRET_KEY=your-secret-key
DEBUG=True
```

**frontend/.env.local**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Docker Configuration

**docker-compose.yml** runs:
- `backend`: FastAPI on port 8000
- `frontend`: Next.js on port 4000:3000 (host:container)
- `db`: PostgreSQL on port 5432

**Useful Docker commands**:
```powershell
docker compose up -d              # Start all services
docker compose down               # Stop all services
docker compose logs -f backend    # View backend logs
docker compose restart frontend   # Restart frontend
docker compose build --no-cache   # Rebuild from scratch
docker compose ps                 # List running containers
```

## API Documentation

Once the backend is running, access interactive API docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -am 'Add my feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Submit a Pull Request

## License

[Add license information]

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation in the `docs/` folder
- Review DOCKER_QUICKSTART.md for Docker-specific help

## Additional Documentation

- **DOCKER_QUICKSTART.md**: Docker setup guide
- **DOCKER_SETUP.md**: Detailed Docker configuration
- **NODEJS_INSTALLATION.md**: Node.js installation guide
- **QUICKSTART.md**: Quick start guide
- **DEPLOYMENT_STATUS.md**: Current deployment status
