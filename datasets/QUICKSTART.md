# Quick Start Guide - Elas ERP Demo Datasets

## 🚀 One-Command Setup

```powershell
# Navigate to project root
cd C:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP

# Run the generator script
.\datasets\run_all_generators.ps1
```

This will:
1. ✅ Check Python installation
2. ✅ Install required packages (pandas, openpyxl, fpdf)
3. ✅ Generate all 5 dataset scenarios
4. ✅ Create ~5,000+ rows across 20+ files

---

## 📋 Manual Setup (Alternative)

If you prefer to run generators individually:

```powershell
# Install dependencies
pip install pandas openpyxl fpdf

# Run individual generators
python datasets/generate_sales_retail.py
python datasets/generate_finance_ar.py
python datasets/generate_operations_workorders.py
python datasets/generate_education_enrollments.py
python datasets/generate_minimal_small.py
```

---

## 🗂️ Generated Structure

```
datasets/
├── run_all_generators.ps1          # Main runner script
├── README.md                        # This file
│
├── sales_retail/
│   ├── sales_transactions.csv      # 1,200 rows
│   ├── sales_transactions.xlsx     # 300 rows
│   ├── products.csv                # 80 rows
│   ├── reps.csv                    # 25 rows
│   └── readme.md
│
├── finance_ar/
│   ├── invoices.csv                # 600 rows
│   ├── payments.csv                # 400 rows
│   ├── ar_clients.csv              # 60 rows
│   ├── ar_sop.pdf                  # 1-page PDF
│   ├── sample_invoice.pdf          # 1-page PDF
│   └── readme.md
│
├── operations_workorders/
│   ├── work_orders.csv             # 500 rows
│   ├── technicians.csv             # 40 rows
│   ├── shifts.xlsx                 # 180 rows
│   └── readme.md
│
├── education_enrollments/
│   ├── enrollments.csv             # ~2,400 rows
│   ├── instructors.csv             # 35 rows
│   ├── courses.xlsx                # ~70 rows
│   └── readme.md
│
└── minimal_small/
    ├── tiny_sales.csv              # 30 rows
    ├── weird_headers.csv           # 40 rows
    └── readme.md
```

---

## 🎯 Testing Workflow

### 1. **Start Servers**
```powershell
# Kill any running servers first
Stop-Process -Name "python","node" -Force -ErrorAction SilentlyContinue

# Start backend (in terminal 1)
cd elas-erp
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

# Start frontend (in terminal 2)
cd elas-erp/frontend
npm run dev
```

### 2. **Test Onboarding Flow**
- Go to `http://localhost:4000/onboarding/documents`
- Upload files from any `datasets/*/` folder
- Test file detection, parsing, and preview

### 3. **Test Quick-Viz**
- Upload `sales_retail/sales_transactions.csv`
- Specify domain: "Sales Analytics"
- See widget proposals generated

### 4. **Test Data Mapping**
- Upload `finance_ar/invoices.csv`
- Map columns to AR aging buckets
- Verify aging calculations

### 5. **Test Edge Cases**
- Upload `minimal_small/weird_headers.csv`
- Verify column name sanitization
- Test empty value handling

---

## 💡 Dataset Highlights

### Sales Retail
- **Use Case**: Revenue analysis, product performance, rep quota tracking
- **Key Features**: Duplicates (1.5%), outliers ($250K order), nulls, trailing spaces
- **Best For**: Testing aggregations, time series, category breakdowns

### Finance AR
- **Use Case**: Accounts receivable aging, DSO, collection efficiency
- **Key Features**: Aging buckets (CURRENT, 30, 60, 90, 90+), partial payments, PDFs
- **Best For**: Financial dashboards, aging analysis, payment trends

### Operations Work Orders
- **Use Case**: Work order tracking, technician utilization, shift scheduling
- **Key Features**: Status workflow, completion times, overtime tracking
- **Best For**: Operational KPIs, resource allocation, SLA compliance

### Education Enrollments
- **Use Case**: Student enrollment tracking, course capacity, financial aid
- **Key Features**: Multi-term data, grades, tuition calculations, waitlists
- **Best For**: Academic dashboards, registration analysis, revenue forecasting

### Minimal Small
- **Use Case**: Edge case testing, UI validation, data quality checks
- **Key Features**: Only 30-40 rows, weird column names, special characters
- **Best For**: Unit testing, empty states, parser robustness

---

## 🔧 Troubleshooting

### Issue: "Python not found"
**Solution**: Install Python 3.10+ from python.org

### Issue: "pip not found"
**Solution**: 
```powershell
python -m ensurepip --upgrade
```

### Issue: "pandas not found"
**Solution**:
```powershell
pip install pandas openpyxl fpdf
```

### Issue: "Permission denied on script"
**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Files not generated
**Solution**: Check console for errors, ensure write permissions to `datasets/` folder

---

## 📊 Data Quality Features

All datasets include:
- ✅ **Realistic variation**: Dates, regions, amounts, outliers
- ✅ **Missing values**: ~5% nulls in non-key columns
- ✅ **Duplicates**: 1-2% in transaction datasets
- ✅ **Edge cases**: Trailing spaces, accents, special characters
- ✅ **Join keys**: Consistent IDs for multi-table scenarios
- ✅ **Calculations**: Pre-computed amounts, aging, costs

---

## 🚦 Kill Server Command

When you need to stop all servers:
```powershell
Stop-Process -Name "python","node" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Write-Host "`n✅ All servers stopped`n" -ForegroundColor Green
```

Or create a shortcut script:
```powershell
# Save as kill_servers.ps1
Stop-Process -Name "python","node" -Force -ErrorAction SilentlyContinue
Write-Host "✅ Servers killed" -ForegroundColor Green
```

---

## 📖 Additional Resources

- Each scenario folder has a `readme.md` with detailed column descriptions
- PDFs in `finance_ar/` demonstrate document handling
- Join keys documented for multi-table relationships
- Visualization suggestions in each readme

---

## ✨ Happy Testing!

You now have 5,000+ rows of realistic data across 5 scenarios to thoroughly test your Elas ERP onboarding pipeline!
