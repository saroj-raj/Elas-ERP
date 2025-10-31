# 🚀 ELAS-ERP DEPLOYMENT - QUICK REFERENCE

## ✅ What's Complete
- ✅ All 4 dashboards (Admin, Finance, Manager, Employee)
- ✅ PostgreSQL database with authentication
- ✅ File upload (CSV, XLSX, TXT)
- ✅ Ready for deployment

---

## 🎯 Deploy in 3 Steps (30 minutes)

### STEP 1: Backend → Railway (15 min)
1. Go to **https://railway.app/** → Sign up with GitHub
2. **New Project** → Deploy from GitHub → Select `Elas-ERP`
3. **Add Database** → PostgreSQL (auto-configured)
4. **Set Variables:**
   ```
   GROQ_API_KEY=<your-key>
   SECRET_KEY=<generate-with-python>
   APP_ENV=production
   ```
5. **Configure:**
   - Root: `elas-erp`
   - Start: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
6. **Copy URL:** `https://elas-erp-backend-xxx.up.railway.app`

### STEP 2: Frontend → Vercel (5 min)
1. Go to **https://vercel.com/** → Sign up with GitHub
2. **Import Project** → Select `Elas-ERP`
3. **Configure:**
   - Framework: Next.js
   - Root: `elas-erp/frontend`
4. **Set Variable:**
   ```
   NEXT_PUBLIC_API_BASE=<your-railway-url>
   ```
5. **Deploy** → Get URL: `https://elas-erp.vercel.app`

### STEP 3: Initialize Database (5 min)
```bash
# Option 1: Railway CLI
railway run python -m backend.app.init_db

# Option 2: Local with production DB URL
DATABASE_URL=<railway-db-url> python -m backend.app.init_db
```

---

## 🔑 Generate SECRET_KEY
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## ✅ Test Your Demo
1. **Backend Health:** `https://your-backend.up.railway.app/health`
2. **Login:** admin@elas-erp.com / admin123
3. **Upload:** Test CSV file
4. **Dashboards:** Switch between 4 roles

---

## 📚 Detailed Guides
- **Full Guide:** `VERCEL_DEPLOYMENT_GUIDE.md`
- **Helper Script:** Run `.\deploy.ps1`
- **Tasks:** See `TASKS_STATUS.md`

---

## 🆘 Quick Troubleshooting

**Frontend can't reach backend?**
→ Check `NEXT_PUBLIC_API_BASE` in Vercel

**Database connection failed?**
→ Verify `DATABASE_URL` in Railway

**Build failed?**
→ Check Railway/Vercel logs

---

## 💰 Cost
- **Vercel:** Free (unlimited deployments)
- **Railway:** $5 credit/month (free tier)
- **Total:** ~$0-5/month

---

## ⏱️ Timeline
- Backend deploy: 15 min
- Frontend deploy: 5 min
- DB initialization: 5 min
- Testing: 10 min
- **Total: ~35 minutes** to live demo!

---

**Ready to deploy? Run:** `.\deploy.ps1`

**Or follow:** `VERCEL_DEPLOYMENT_GUIDE.md`

🎉 **Your demo will be live in 30 minutes!**
