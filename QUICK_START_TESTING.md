# 🚀 QUICK START GUIDE - Test Your Changes

## **1. Restart Servers**

### Stop Everything First:
```powershell
Stop-Process -Name "python","node" -Force -ErrorAction SilentlyContinue
```

### Start Backend:
```powershell
cd elas-erp
python start.py
```

Wait for: "✅ SERVERS STARTED!"

---

## **2. Test Country Dropdown**

1. Open: `http://localhost:4000/onboarding/business`
2. Scroll to "Country" field
3. Click the dropdown
4. Type "united" → Should show:
   - 🇺🇸 United States
   - 🇬🇧 United Kingdom
   - 🇦🇪 United Arab Emirates
5. ✅ **SUCCESS**: Dropdown is searchable and shows flags

---

## **3. Test File Upload (All Types)**

1. Open: `http://localhost:4000/onboarding/upload`
2. Fill in:
   - **Domain**: "Sales Analytics"
   - **Intent**: "Show revenue trends"
3. Upload ONE file at a time to test each type:

### Test CSV:
- Create a simple CSV file:
```csv
date,revenue,expenses
2025-01-01,1000,600
2025-02-01,1200,650
2025-03-01,1500,700
```
- Save as `test.csv`
- Upload it
- ✅ **EXPECTED**: Upload succeeds, charts generated

### Test Excel:
- Create Excel file with same data
- Save as `test.xlsx`
- Upload it
- ✅ **EXPECTED**: Upload succeeds

### Test PDF:
- Create any PDF with text/table
- Upload it
- ✅ **EXPECTED**: Upload attempts extraction (may show raw text if no tables)

### Test Word:
- Create DOCX with a table
- Upload it
- ✅ **EXPECTED**: Upload succeeds, table extracted

---

## **4. Test Error Messages**

### Test Network Error:
1. Stop backend: `Stop-Process -Name python -Force`
2. Try to upload a file
3. ✅ **EXPECTED**: "Cannot reach the server. Please check if the backend is running on port 8000."

### Test Invalid File:
1. Restart backend
2. Upload a `.txt` file with just random text (no table structure)
3. ✅ **EXPECTED**: May work or show parsing error with helpful message

---

## **5. Test Loading States**

1. Upload a file
2. ✅ **EXPECTED TO SEE**:
   - Spinning icon (⚙️)
   - Button says "Processing..."
   - Blue box appears with:
     - "Uploading files..."
     - "Analyzing data structure..."
     - "Generating smart visualizations..."
   - Progress bar animates
   - Message: "This may take 10-30 seconds..."

---

## **6. Generate Datasets with Claude**

1. Open `CLAUDE_DATASET_PROMPT.md`
2. Copy entire content
3. Go to Claude AI (claude.ai)
4. Paste prompt
5. Ask: "Generate Sales & Revenue dataset with Python scripts"
6. Save Python scripts to `datasets/` folder
7. Run scripts: `python datasets/generate_sales_data.py`
8. Test upload with generated files

---

## **🐛 Troubleshooting**

### Frontend won't build:
```powershell
cd elas-erp\frontend
npm install
npm run build
```

### Backend crashes on upload:
Check logs in terminal for Python errors

### Country dropdown doesn't show:
```powershell
cd elas-erp\frontend
npm install react-select
npm run dev
```

### PDF/DOCX parsing fails:
```powershell
cd elas-erp
& ".venv\Scripts\python.exe" -m pip install PyPDF2 python-docx openpyxl Pillow
```

---

## **✅ Success Checklist**

- [ ] Country dropdown works and is searchable
- [ ] CSV files upload successfully
- [ ] Excel files upload successfully  
- [ ] PDF files upload (may show text extraction)
- [ ] Word documents upload (may show table extraction)
- [ ] Error messages are specific and helpful
- [ ] Loading animation appears during upload
- [ ] Progress bar shows activity
- [ ] Upload completes and redirects to dashboard

---

## **📋 What to Report**

Tell me:
1. Which file types worked ✅
2. Which file types failed ❌
3. What error messages you saw
4. Any unexpected behavior
5. Screenshots if possible

---

**Ready? Start testing!** 🚀
