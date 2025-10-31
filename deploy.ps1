#!/usr/bin/env pwsh
# Quick Deployment Script for Elas-ERP

Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     🚀 ELAS-ERP DEPLOYMENT HELPER                       ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "This script will help you deploy Elas-ERP for your demo.`n" -ForegroundColor White

# Check if git is initialized
Write-Host "📋 Step 1: Checking Git Status..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    Write-Host "  ⚠️  Git not initialized. Initializing..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit for deployment"
    Write-Host "  ✅ Git initialized`n" -ForegroundColor Green
} else {
    Write-Host "  ✅ Git already initialized`n" -ForegroundColor Green
}

# Check for uncommitted changes
$status = git status --porcelain
if ($status) {
    Write-Host "  ⚠️  You have uncommitted changes." -ForegroundColor Yellow
    Write-Host "  Committing changes..." -ForegroundColor Yellow
    git add .
    git commit -m "Pre-deployment updates"
    Write-Host "  ✅ Changes committed`n" -ForegroundColor Green
}

# Backend deployment info
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚂 BACKEND DEPLOYMENT (Railway)                        ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "1. Go to: https://railway.app/" -ForegroundColor White
Write-Host "2. Sign up/Login with GitHub" -ForegroundColor White
Write-Host "3. Create New Project → Deploy from GitHub" -ForegroundColor White
Write-Host "4. Select this repository: Elas-ERP" -ForegroundColor White
Write-Host "`n📁 Configuration:" -ForegroundColor Yellow
Write-Host "   Root Directory: elas-erp" -ForegroundColor Gray
Write-Host "   Start Command:  uvicorn backend.app.main:app --host 0.0.0.0 --port `$PORT`n" -ForegroundColor Gray

Write-Host "5. Add PostgreSQL:" -ForegroundColor White
Write-Host "   - Click 'New' → Database → PostgreSQL" -ForegroundColor Gray
Write-Host "   - Railway will auto-set DATABASE_URL`n" -ForegroundColor Gray

Write-Host "6. Set Environment Variables:" -ForegroundColor White
Write-Host "   DATABASE_URL    = (auto-set by Railway)" -ForegroundColor Gray
Write-Host "   GROQ_API_KEY    = <your-groq-key>" -ForegroundColor Gray
Write-Host "   SECRET_KEY      = (generate below)" -ForegroundColor Gray
Write-Host "   APP_ENV         = production" -ForegroundColor Gray

Write-Host "`n🔑 Generate SECRET_KEY:" -ForegroundColor Yellow
Write-Host "   Run this and copy the output:`n" -ForegroundColor Gray
Write-Host "   python -c `"import secrets; print(secrets.token_urlsafe(32))`"`n" -ForegroundColor Cyan

$generateSecret = Read-Host "Generate SECRET_KEY now? (y/n)"
if ($generateSecret -eq 'y' -or $generateSecret -eq 'Y') {
    $secret = python -c "import secrets; print(secrets.token_urlsafe(32))"
    Write-Host "`n  Your SECRET_KEY:" -ForegroundColor Green
    Write-Host "  $secret" -ForegroundColor White
    Write-Host "`n  Copy this to Railway environment variables!`n" -ForegroundColor Yellow
}

Write-Host "7. After deployment, copy your Railway URL" -ForegroundColor White
Write-Host "   Example: https://elas-erp-backend-production-xxxx.up.railway.app`n" -ForegroundColor Gray

$backendUrl = Read-Host "Enter your Railway backend URL (or press Enter to skip)"

# Frontend deployment info
Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🌐 FRONTEND DEPLOYMENT (Vercel)                        ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "1. Go to: https://vercel.com/" -ForegroundColor White
Write-Host "2. Sign up/Login with GitHub" -ForegroundColor White
Write-Host "3. Import Project → Select Elas-ERP repository" -ForegroundColor White
Write-Host "`n📁 Configuration:" -ForegroundColor Yellow
Write-Host "   Framework:       Next.js" -ForegroundColor Gray
Write-Host "   Root Directory:  elas-erp/frontend" -ForegroundColor Gray
Write-Host "   Build Command:   npm run build" -ForegroundColor Gray
Write-Host "   Output Dir:      .next`n" -ForegroundColor Gray

Write-Host "4. Set Environment Variable:" -ForegroundColor White
if ($backendUrl) {
    Write-Host "   NEXT_PUBLIC_API_BASE = $backendUrl`n" -ForegroundColor Gray
    
    # Update .env.production
    Write-Host "  📝 Updating .env.production..." -ForegroundColor Yellow
    "NEXT_PUBLIC_API_BASE=$backendUrl" | Out-File -FilePath "elas-erp\frontend\.env.production" -Encoding UTF8
    Write-Host "  ✅ Updated!`n" -ForegroundColor Green
} else {
    Write-Host "   NEXT_PUBLIC_API_BASE = <your-railway-backend-url>`n" -ForegroundColor Gray
}

Write-Host "5. Click Deploy and wait for build to complete" -ForegroundColor White
Write-Host "6. Your demo will be live at: https://elas-erp.vercel.app`n" -ForegroundColor White

# Database initialization
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🗄️  DATABASE INITIALIZATION                            ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "After backend is deployed, initialize the database:`n" -ForegroundColor White
Write-Host "Option 1: Railway CLI" -ForegroundColor Yellow
Write-Host "  railway run python -m backend.app.init_db`n" -ForegroundColor Gray

Write-Host "Option 2: Local with Production DB" -ForegroundColor Yellow
Write-Host "  DATABASE_URL=<railway-db-url> python -m backend.app.init_db`n" -ForegroundColor Gray

# Summary
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ DEPLOYMENT CHECKLIST                                ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "☐ Backend deployed to Railway" -ForegroundColor White
Write-Host "☐ PostgreSQL added to Railway project" -ForegroundColor White
Write-Host "☐ Environment variables set in Railway" -ForegroundColor White
Write-Host "☐ Database initialized (run init_db.py)" -ForegroundColor White
Write-Host "☐ Frontend deployed to Vercel" -ForegroundColor White
Write-Host "☐ NEXT_PUBLIC_API_BASE set in Vercel" -ForegroundColor White
Write-Host "☐ Test login at your Vercel URL" -ForegroundColor White
Write-Host "☐ Test file upload" -ForegroundColor White

Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  📚 RESOURCES                                           ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "📖 Full Guide:    VERCEL_DEPLOYMENT_GUIDE.md" -ForegroundColor White
Write-Host "🚂 Railway:       https://railway.app/" -ForegroundColor White
Write-Host "🌐 Vercel:        https://vercel.com/" -ForegroundColor White
Write-Host "📝 Railway Docs:  https://docs.railway.app/" -ForegroundColor White
Write-Host "📝 Vercel Docs:   https://vercel.com/docs`n" -ForegroundColor White

Write-Host "🎉 Your demo will be ready in ~15 minutes!" -ForegroundColor Green
Write-Host "Good luck with your presentation! 🚀`n" -ForegroundColor Yellow
