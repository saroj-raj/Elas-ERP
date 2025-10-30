# TC002: Retail Small Business - Inventory Stock Management

## 🏢 Test Case Metadata
- **Test Case ID**: TC002
- **Industry**: Retail
- **Company Size**: Small (1-50 employees)
- **Complexity**: Basic
- **Date Created**: 2025-10-29
- **Status**: Ready for Testing

---

## 📊 Business Context
**Company Profile**: "City Corner Store" - Store manager managing inventory levels.

**Business Question**: "Which items are low on stock? What should I reorder? How much will it cost?"

---

## 📁 Required Data Files (Upload All 3)

### File 1: `TC002_inventory.csv`
- **Rows**: 200
- **Description**: Current inventory levels

### File 2: `TC002_suppliers.xlsx`
- **Rows**: 25
- **Description**: Supplier information

### File 3: `TC002_reorder_alerts.csv`
- **Rows**: 30
- **Description**: Low stock alerts

---

## 🎯 User Input to Elas ERP

**Step 1: Upload Files**
- Upload `TC002_inventory.csv`
- Upload `TC002_suppliers.xlsx`
- Upload `TC002_reorder_alerts.csv`

**Step 2: Quick-Viz Input**
- **Domain**: "Inventory Management"
- **User Intent**: "Show me low stock items, reorder recommendations, and supplier performance"

---

## ✅ Expected Widget Proposals (5 widgets)

### Widget 1: Low Stock Items by Category (Bar Chart)
- **Type**: Bar Chart
- **Title**: "Low Stock Items by Category"
- **Purpose**: Identify shortage areas
- **Validation**: 
  - ☐ Widget generated
  - ☐ Correct type (Bar Chart)
  - ☐ Appropriate data shown
  - ☐ Renders without errors

### Widget 2: Urgent Reorder List (Table)
- **Type**: Table
- **Title**: "Urgent Reorder List"
- **Purpose**: Action items for purchasing
- **Validation**: 
  - ☐ Widget generated
  - ☐ Correct type (Table)
  - ☐ Appropriate data shown
  - ☐ Renders without errors

### Widget 3: Total Reorder Cost (KPI Card)
- **Type**: KPI Card
- **Title**: "Total Reorder Cost"
- **Purpose**: Budget needed
- **Validation**: 
  - ☐ Widget generated
  - ☐ Correct type (KPI Card)
  - ☐ Appropriate data shown
  - ☐ Renders without errors

### Widget 4: Supplier Lead Time Comparison (Bar Chart)
- **Type**: Bar Chart
- **Title**: "Supplier Lead Time Comparison"
- **Purpose**: Choose fastest supplier
- **Validation**: 
  - ☐ Widget generated
  - ☐ Correct type (Bar Chart)
  - ☐ Appropriate data shown
  - ☐ Renders without errors

### Widget 5: Stock Adequacy Score (Gauge)
- **Type**: Gauge
- **Title**: "Stock Adequacy Score"
- **Purpose**: Overall inventory health
- **Validation**: 
  - ☐ Widget generated
  - ☐ Correct type (Gauge)
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
2. Upload `TC002_inventory.csv`
2. Upload `TC002_suppliers.xlsx`
2. Upload `TC002_reorder_alerts.csv`

### 3. Generate Widgets
1. Navigate to Quick-Viz
2. Enter domain: "Inventory Management"
3. Enter intent: "Show me low stock items, reorder recommendations, and supplier performance"
4. Click "Generate Dashboard"

### 4. Validate Results
- [ ] Widget 1: Low Stock Items by Category (Bar Chart)
- [ ] Widget 2: Urgent Reorder List (Table)
- [ ] Widget 3: Total Reorder Cost (KPI Card)
- [ ] Widget 4: Supplier Lead Time Comparison (Bar Chart)
- [ ] Widget 5: Stock Adequacy Score (Gauge)

**Overall Test Result**: ☐ PASS ☐ FAIL

---

## 📝 Notes
_Add any observations, issues, or screenshots here_

---

**Last Updated**: 2025-10-29
