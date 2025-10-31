# 🚀 Vercel Deployment Guide for Elas-ERP

Complete step-by-step guide to deploy your Elas-ERP demo on Vercel (Frontend) and Railway/Render (Backend).

---

## 📋 Overview

Your application consists of:
1. **Frontend (Next.js)** → Deploy to **Vercel** ✅
2. **Backend (FastAPI + PostgreSQL)** → Deploy to **Railway** or **Render** 🚂
3. **Database (PostgreSQL)** → Use Vercel Postgres or Railway DB 🗄️

---

## 🎯 Deployment Strategy

### Option 1: Vercel + Railway (Recommended)
- **Frontend:** Vercel (fastest, best Next.js support)
- **Backend:** Railway (easy, includes PostgreSQL)
- **Database:** Railway PostgreSQL (included)

### Option 2: Vercel + Render
- **Frontend:** Vercel
- **Backend:** Render (free tier available)
- **Database:** Render PostgreSQL or Vercel Postgres

---

## 📦 Part 1: Backend Deployment (Railway)

### Step 1: Prepare Backend for Deployment

1. **Create production requirements file:**
   Already exists at: `elas-erp/backend/requirements.txt`

2. **Create Railway configuration:**

Create `railway.json` in backend folder:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 2: Deploy Backend to Railway

1. **Create Railway Account:**
   - Go to https://railway.app/
   - Sign up with GitHub

2. **Create New Project:**
   - Click "New Project"
   - Choose "Deploy from GitHub repo"
   - Select your Elas-ERP repository
   - Choose the `elas-erp` directory

3. **Configure Backend Service:**
   ```
   Root Directory: elas-erp/backend
   Start Command: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Add PostgreSQL Database:**
   - In Railway dashboard, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically provide `DATABASE_URL`

5. **Set Environment Variables:**
   In Railway dashboard → Variables:
   ```
   DATABASE_URL=<automatically set by Railway>
   GROQ_API_KEY=<your-groq-api-key>
   APP_NAME=Elas ERP Backend
   APP_ENV=production
   SECRET_KEY=<generate-random-string>
   ```

   Generate SECRET_KEY:
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```

6. **Initialize Database:**
   After deployment, run database initialization:
   - Railway → Service → Settings → Variables
   - Add all env vars
   - Use Railway's command runner or connect via psql

7. **Get Backend URL:**
   Railway will provide a URL like:
   `https://elas-erp-backend-production-xxxx.up.railway.app`

---

## 🌐 Part 2: Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. **Update package.json build command:**
   Already configured: `"build": "next build"`

2. **Verify environment variables:**
   File: `frontend/.env.production`
   ```
   NEXT_PUBLIC_API_BASE=https://your-backend-url.up.railway.app
   ```

### Step 2: Deploy to Vercel

1. **Create Vercel Account:**
   - Go to https://vercel.com/
   - Sign up with GitHub

2. **Import Project:**
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Vercel will auto-detect Next.js

3. **Configure Project Settings:**
   ```
   Framework Preset: Next.js
   Root Directory: elas-erp/frontend
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   ```

4. **Set Environment Variables:**
   In Vercel → Settings → Environment Variables:
   ```
   Variable Name: NEXT_PUBLIC_API_BASE
   Value: https://elas-erp-backend-production-xxxx.up.railway.app
   Environment: Production
   ```

5. **Deploy:**
   - Click "Deploy"
   - Wait for build to complete
   - Your demo will be live at: `https://elas-erp.vercel.app`

---

## 🗄️ Part 3: Database Migration

### Option A: Using Railway PostgreSQL

Railway automatically provides PostgreSQL. Initialize it:

1. **Connect to Railway Database:**
   ```bash
   # Get connection string from Railway dashboard
   psql <railway-database-url>
   ```

2. **Run init script:**
   ```bash
   # Update DATABASE_URL in Railway env vars
   # Trigger redeploy or use Railway CLI
   railway run python -m backend.app.init_db
   ```

### Option B: Using Vercel Postgres

1. **Create Vercel Postgres:**
   - In Vercel dashboard
   - Go to Storage → Create Database
   - Choose Postgres

2. **Link to Backend:**
   - Copy connection string
   - Add to Railway environment variables

3. **Initialize:**
   ```bash
   # Run locally with production DB URL
   DATABASE_URL=<vercel-postgres-url> python -m backend.app.init_db
   ```

---

## ✅ Part 4: Post-Deployment Checklist

### Backend Verification

1. **Health Check:**
   ```bash
   curl https://your-backend.up.railway.app/health
   ```
   Expected: `{"status": "ok", "service": "Elas ERP Backend", "version": "2.0"}`

2. **API Documentation:**
   Visit: `https://your-backend.up.railway.app/docs`

3. **Test Authentication:**
   ```bash
   curl -X POST https://your-backend.up.railway.app/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@elas-erp.com", "password": "admin123"}'
   ```

### Frontend Verification

1. **Open Demo Site:**
   `https://elas-erp.vercel.app`

2. **Test Login:**
   - Email: admin@elas-erp.com
   - Password: admin123

3. **Test Upload:**
   - Go to upload page
   - Upload a CSV file
   - Verify widgets are generated

### Database Verification

1. **Check Tables:**
   ```sql
   \dt
   ```
   Should see: users, dashboards, widgets, business_info

2. **Check Admin User:**
   ```sql
   SELECT * FROM users WHERE email = 'admin@elas-erp.com';
   ```

---

## 🔧 Environment Variables Summary

### Backend (Railway)
```env
# Database
DATABASE_URL=<from Railway PostgreSQL>

# Security
SECRET_KEY=<generated-random-string>

# App Config
APP_NAME=Elas ERP Backend
APP_ENV=production

# AI Service
GROQ_API_KEY=<your-groq-api-key>

# Optional
DEBUG=false
```

### Frontend (Vercel)
```env
# Backend URL
NEXT_PUBLIC_API_BASE=https://elas-erp-backend-production.up.railway.app
```

---

## 📝 Quick Commands

### Deploy Frontend
```bash
# From elas-erp/frontend
vercel --prod
```

### Deploy Backend (Railway CLI)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

### Update Environment Variables
```bash
# Railway
railway variables set KEY=value

# Vercel
vercel env add NEXT_PUBLIC_API_BASE
```

---

## 🚨 Troubleshooting

### Frontend can't reach backend
- Check CORS settings in `backend/app/main.py`
- Verify `NEXT_PUBLIC_API_BASE` in Vercel
- Check Railway backend logs

### Database connection failed
- Verify `DATABASE_URL` in Railway
- Check PostgreSQL is running
- Ensure init_db.py was executed

### Build failed on Vercel
- Check Node version (should be 20+)
- Verify all dependencies in package.json
- Check build logs for specific errors

### Backend 500 errors
- Check Railway logs
- Verify all environment variables set
- Ensure database tables exist

---

## 🎉 Demo URLs

After deployment, you'll have:

- **Frontend:** `https://elas-erp.vercel.app`
- **Backend:** `https://elas-erp-backend.up.railway.app`
- **API Docs:** `https://elas-erp-backend.up.railway.app/docs`
- **Health:** `https://elas-erp-backend.up.railway.app/health`

---

## 💰 Cost Estimate

### Free Tier Limits

**Vercel:**
- Unlimited deployments
- 100GB bandwidth/month
- No credit card required

**Railway:**
- $5 free credit/month
- ~550 hours runtime
- PostgreSQL included
- Credit card required after trial

**Alternative (Render):**
- Free tier: 750 hours/month
- PostgreSQL: $7/month
- Credit card required

---

## 📚 Next Steps

1. ✅ Deploy backend to Railway
2. ✅ Deploy frontend to Vercel  
3. ✅ Initialize production database
4. ✅ Test complete flow
5. ✅ Share demo URL!

---

## 🔗 Useful Links

- **Vercel Docs:** https://vercel.com/docs
- **Railway Docs:** https://docs.railway.app/
- **Render Docs:** https://render.com/docs
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/
- **Next.js Deployment:** https://nextjs.org/docs/deployment

---

**Status:** Ready for deployment! 🚀

Follow the steps above and your demo will be live in ~15 minutes!
