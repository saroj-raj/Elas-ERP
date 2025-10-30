# TC001: Retail Small Business - Daily Sales Dashboard

## 🏢 Test Case Metadata
- **Test Case ID**: TC001
- **Industry**: Retail
- **Company Size**: Small (1-50 employees)
- **Complexity**: Basic
- **Date Created**: 2025-10-29
- **Status**: Ready for Testing

---

## 📊 Business Context
**Company Profile**: "Joe's Hardware Store" - Store owner tracking daily sales performance.

**Business Question**: "How are my daily sales performing? Which products sell best? When are my peak hours?"

---

## 📁 Required Data Files (Upload All 3)

### File 1: `TC001_sales_transactions.csv`
- **Rows**: 500
- **Description**: Primary sales data with transactions

### File 2: `TC001_products.csv`
- **Rows**: 80
- **Description**: Product catalog with pricing

### File 3: `TC001_employees.csv`
- **Rows**: 15
- **Description**: Employee roster

---

## 🎯 User Input to Elas ERP

**Step 1: Upload Files**
- Upload `TC001_sales_transactions.csv`
- Upload `TC001_products.csv`
- Upload `TC001_employees.csv`

**Step 2: Quick-Viz Input**
- **Domain**: "Retail Sales Analytics"
- **User Intent**: "Show me daily sales trends, best-selling products, and peak shopping hours"

---

## ✅ Expected Widget Proposals (6 widgets)

### Widget 1: Daily Revenue Trend (Last 90 Days) (Line Chart)
- **Type**: Line Chart
- **Title**: "Daily Revenue Trend (Last 90 Days)"
- **Purpose**: Track revenue over time
- **Validation**: 
  - ☐ Widget generated
  - ☐ Correct type (Line Chart)
  - ☐ Appropriate data shown
  - ☐ Renders without errors

### Widget 2: Revenue by Product Category (Bar Chart)
- **Type**: Bar Chart
- **Title**: "Revenue by Product Category"
- **Purpose**: Compare category performance
- **Validation**: 
  - ☐ Widget generated
  - ☐ Correct type (Bar Chart)
  - ☐ Appropriate data shown
  - ☐ Renders without errors

### Widget 3: Top 10 Best-Selling Products (Table)
- **Type**: Table
- **Title**: "Top 10 Best-Selling Products"
- **Purpose**: Identify top performers
- **Validation**: 
  - ☐ Widget generated
  - ☐ Correct type (Table)
  - ☐ Appropriate data shown
  - ☐ Renders without errors

### Widget 4: Transactions by Hour of Day (Bar Chart)
- **Type**: Bar Chart
- **Title**: "Transactions by Hour of Day"
- **Purpose**: Find peak hours
- **Validation**: 
  - ☐ Widget generated
  - ☐ Correct type (Bar Chart)
  - ☐ Appropriate data shown
  - ☐ Renders without errors

### Widget 5: Payment Method Distribution (Pie Chart)
- **Type**: Pie Chart
- **Title**: "Payment Method Distribution"
- **Purpose**: Payment preferences
- **Validation**: 
  - ☐ Widget generated
  - ☐ Correct type (Pie Chart)
  - ☐ Appropriate data shown
  - ☐ Renders without errors

### Widget 6: Total Revenue (90 Days) (KPI Card)
- **Type**: KPI Card
- **Title**: "Total Revenue (90 Days)"
- **Purpose**: Main revenue metric
- **Validation**: 
  - ☐ Widget generated
  - ☐ Correct type (KPI Card)
  - ☐ Appropriate data shown
  - ☐ Renders without errors

---

## 🧪 Test Execution Steps

### 1. Start Servers
```powershell
# Backend
cd elas-erp
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

# Frontend (new terminal)
cd elas-erp/frontend
npm run dev
```

### 2. Upload Files
1. Open browser: `http://localhost:4000/onboarding/documents`
2. Upload `TC001_sales_transactions.csv`
2. Upload `TC001_products.csv`
2. Upload `TC001_employees.csv`

### 3. Generate Widgets
1. Navigate to Quick-Viz
2. Enter domain: "Retail Sales Analytics"
3. Enter intent: "Show me daily sales trends, best-selling products, and peak shopping hours"
4. Click "Generate Dashboard"

### 4. Validate Results
- [ ] Widget 1: Daily Revenue Trend (Last 90 Days) (Line Chart)
- [ ] Widget 2: Revenue by Product Category (Bar Chart)
- [ ] Widget 3: Top 10 Best-Selling Products (Table)
- [ ] Widget 4: Transactions by Hour of Day (Bar Chart)
- [ ] Widget 5: Payment Method Distribution (Pie Chart)
- [ ] Widget 6: Total Revenue (90 Days) (KPI Card)

**Overall Test Result**: ☐ PASS ☐ FAIL

---

## 📝 Notes
_Add any observations, issues, or screenshots here_

---

**Last Updated**: 2025-10-29
