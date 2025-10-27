# 🐛 Groq AI Debugging Guide

## ✅ What We Just Fixed

### 1. **Component Files Fixed** ✨
- `Card.tsx` - Clean and working
- `Button.tsx` - Clean and working  
- `FileDropzone.tsx` - Clean and working
- Frontend builds successfully without errors!

### 2. **Comprehensive Logging Added** 📊

#### Backend Logging (Python console):
- **Upload endpoint** (`upload.py`): Shows file upload, domain, intent, widget count
- **Dashboard generator** (`dashboard_generator.py`): Shows CSV inference, column detection
- **Groq AI service** (`llm_service.py`): Shows request/response, parsing, fallback logic

#### Frontend Logging (Browser console):
- **Documents page** (`documents/page.tsx`): Shows upload process, API responses, widget proposals

---

## 🧪 How to Test

### Step 1: Access the App
- Frontend: http://localhost:4000
- Backend API: http://localhost:8000/docs

### Step 2: Navigate to Upload Page
1. Open http://localhost:4000/onboarding/documents
2. Open **Browser DevTools** (F12) → **Console tab**

### Step 3: Prepare Test Data
Create a simple CSV file with this content:

```csv
date,category,revenue,expenses
2024-01-01,Sales,50000,30000
2024-02-01,Sales,55000,32000
2024-03-01,Marketing,45000,28000
2024-04-01,Sales,60000,35000
2024-05-01,Marketing,48000,29000
```

Save as `test_data.csv`

### Step 4: Upload and Test
1. Enter **Domain**: `Business Analytics`
2. Enter **Intent**: `Revenue Growth Analysis`
3. Click **Browse Files** and select your CSV
4. **Watch the logs!** 👀

---

## 📋 What to Look For

### Backend Console (check the backend window):
```
================================================================================
📤 UPLOAD ENDPOINT CALLED
================================================================================
📁 File: test_data.csv
🏢 Domain: Business Analytics
🎯 Intent: Revenue Growth Analysis
💾 Saved to: app/tmp/uploads/...

🚀 GENERATE_QUICK_VIZ called
   Domain: Business Analytics
   Intent: Revenue Growth Analysis

🔍 Inferring hints from CSV: ...
   Columns found: ['date', 'category', 'revenue', 'expenses']
   📈 Measures: ['revenue', 'expenses']
   🏷️  Categories: ['category']
   📅 Date field: date

🤖 Calling Groq AI with:
   Columns: ['revenue', 'expenses', 'category']
   Hints: {...}

🧠 GROQ AI - propose_widgets called
📤 Sending to Groq:
   System prompt: You propose concise, role-aware dashboard widgets...
   User data: {...}
⏳ Waiting for Groq response...

📥 Groq raw response:
   [{"title": "Revenue Trend", "chart": "line", ...}]...

✅ Successfully parsed 3 widgets from Groq

✨ Groq returned 3 proposals:
   1. Revenue Trend (line)
   2. Category Performance (bar)
   3. Expense Analysis (area)

✅ Generated 3 widget specs

📊 Loading preview data with DuckDB...
✅ Loaded 5 preview rows
📋 Columns: ['date', 'category', 'revenue', 'expenses']

📦 Response summary:
   - Dataset ID: ...
   - Widgets: 3
   - Preview rows: 5
================================================================================
```

### Browser Console (F12 → Console):
```
================================================================================
📤 FRONTEND - Upload started
================================================================================
📁 File: test_data.csv (0.25 KB)
🏢 Domain: Business Analytics
🎯 Intent: Revenue Growth Analysis
⏳ Sending to backend /api/upload...
📥 Response status: 200 OK
📦 Response data: {dataset_id: "...", widgets: Array(3), preview: Array(5)}
   - Widgets: 3
   - Preview rows: 5
✨ Widget proposals:
   1. Revenue Trend
      Vega spec: {...}
   2. Category Performance  
      Vega spec: {...}
   3. Expense Analysis
      Vega spec: {...}
✅ State updated successfully
================================================================================
```

---

## 🔍 Debugging Scenarios

### Scenario 1: No Groq Response
**Symptoms:** Backend shows "⚠️ Using fallback widget generation"

**Check:**
1. Is `GROQ_API_KEY` set in `.env`?
2. Backend console shows Groq error message?
3. Check your Groq API quota/limits

**Fix:**
- Update `.env` with valid key
- Or use fallback widgets (still works!)

---

### Scenario 2: Widgets Generated but Not Rendering
**Symptoms:** Backend shows widgets, but frontend shows empty

**Check:**
1. Browser console shows "Widget proposals" log?
2. Any errors in browser console?
3. Check `preview` data exists

**Debug:**
```javascript
// In browser console after upload:
console.log(widgets);  // Should show array of widget objects
console.log(preview);  // Should show array of data rows
```

---

### Scenario 3: Groq Returns Invalid JSON
**Symptoms:** Backend shows "❌ JSON parse error"

**Check:**
1. Backend shows Groq raw response with parsing error
2. May contain markdown formatting or extra text

**Fix:**
- The fallback logic will automatically kick in
- Groq response parsing is already fault-tolerant

---

## 🎯 Next Steps

Once you confirm the logging shows:
1. ✅ File upload working
2. ✅ Domain/Intent passed correctly  
3. ✅ CSV columns detected
4. ✅ Groq AI called (or fallback used)
5. ✅ Widgets generated
6. ✅ Preview data loaded

Then we can focus on:
- **Vega-Lite visualization rendering** 📊
- **Dashboard save/load functionality** 💾
- **Improving widget proposals** 🎨
- **Dashboard page restoration** 🏠

---

## 📝 Test Checklist

- [ ] Backend console shows upload logs
- [ ] Backend console shows CSV column detection
- [ ] Backend console shows Groq AI request
- [ ] Backend console shows Groq AI response (or fallback)
- [ ] Backend console shows widget generation
- [ ] Browser console shows upload started
- [ ] Browser console shows API response
- [ ] Browser console shows widget proposals
- [ ] Frontend page shows uploaded file in list
- [ ] Frontend page shows widget cards (next step: rendering charts)

---

## 🆘 Common Issues

### Issue: "Upload failed. Please ensure backend is running"
- Check backend window is open and shows `Uvicorn running on http://0.0.0.0:8000`
- Try accessing http://localhost:8000/docs

### Issue: CORS errors in browser
- Backend already has CORS enabled in `main.py`
- Try refreshing the page

### Issue: Module not found errors
- Run `pip install -r backend/requirements.txt` in the venv
- Check venv is activated: `.venv\Scripts\activate`

---

**Ready to test!** Upload a CSV and watch both consoles light up with detailed logs! 🚀
