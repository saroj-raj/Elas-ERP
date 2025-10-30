# 📋 PROMPT FOR CLAUDE: Generate ERP Demo Dataset Files

## **Context**
I'm building an AI-powered ERP system called **Elas ERP** that uses Groq LLM to automatically generate data visualizations from uploaded business data files. The system needs realistic demo datasets to showcase its capabilities across different business domains and company sizes.

## **Your Task**
Generate comprehensive, realistic business datasets for demonstration purposes. These datasets will be uploaded to the system to showcase how the AI automatically creates meaningful charts, dashboards, and insights.

---

## **Dataset Requirements**

### **1. Business Domains (Create ONE dataset for EACH)**
- 📊 **Sales & Revenue** (retail, e-commerce)
- 💰 **Finance & Accounting** (accounts receivable, invoices, expenses)
- 📦 **Inventory & Supply Chain** (stock levels, suppliers, reorder alerts)
- 👥 **HR & Payroll** (employees, departments, salaries, attendance)
- 🏭 **Manufacturing** (production, defects, equipment, materials)
- 🏥 **Healthcare** (patients, appointments, billing, insurance)
- 🎓 **Education** (students, courses, enrollments, grades)

### **2. Company Sizes (Vary across datasets)**
- **Small**: 1-50 employees, single location
- **Medium**: 51-500 employees, 2-5 locations
- **Large**: 500+ employees, 10+ locations

### **3. File Formats (Mix these)**
- **CSV** (70% of files) - Most common
- **Excel/XLSX** (25% of files) - For formatted data
- **TXT** (5% of files) - For simple logs or notes

---

## **Dataset Specifications**

### **For EACH Domain, Create 2-4 Related Files:**

#### **Example: Sales & Revenue Domain**
1. **sales_transactions.csv** (500-1000 rows)
   - Columns: transaction_id, date, time, customer_id, product_id, product_name, category, quantity, unit_price, discount, total_amount, payment_method, sales_rep_id, region
   - Date range: Last 90 days
   - Realistic pricing, discounts (0-30%), payment methods (Cash/Credit/Debit)

2. **customers.csv** (100-300 rows)
   - Columns: customer_id, customer_name, email, phone, address, city, state, country, customer_since, loyalty_tier, lifetime_value
   - Linked to sales via customer_id

3. **products.csv** (50-150 rows)
   - Columns: product_id, product_name, category, supplier, cost_price, sell_price, stock_quantity, reorder_level, discontinued
   - Linked to sales via product_id

4. **sales_reps.xlsx** (10-50 rows)
   - Columns: rep_id, rep_name, region, hire_date, quota_monthly, ytd_sales, commission_rate
   - Excel format with formatting

#### **Data Quality Considerations:**
- **Include Realistic Issues:**
  - Some missing values (5-10% of cells)
  - Slight data quality issues (typos in names, inconsistent formatting)
  - Outliers (very high/low sales, stock levels)
  - Low stock scenarios (15-20% of inventory items)
  - Overdue invoices/payments

- **Include Relationships:**
  - Use foreign keys (customer_id, product_id, employee_id, etc.)
  - Ensure referential integrity (IDs should match across files)
  
- **Include Variety:**
  - Different date formats (YYYY-MM-DD, MM/DD/YYYY)
  - Different number formats ($1,234.56, 1234.56)
  - Mixed case text (TitleCase, lowercase, UPPERCASE)

---

## **Required Metadata for Each Dataset**

Create a **README.md** file for each domain with:

```markdown
# [Domain Name] Dataset

## Business Context
- **Company**: [Fictional company name]
- **Industry**: [Industry type]
- **Size**: [Small/Medium/Large]
- **Location**: [Country/Region]
- **Time Period**: [Date range of data]

## Files Included
1. **[filename]**: [Brief description, row count]
2. **[filename]**: [Brief description, row count]

## Use Case / Intent
What business questions this data can answer:
- Example: "Show me monthly revenue trends by region"
- Example: "Which products have low stock levels?"
- Example: "Identify top 10 customers by lifetime value"

## Expected Visualizations
The AI should be able to generate:
- 📈 Line Chart: Revenue over time
- 📊 Bar Chart: Sales by category
- 📋 Table: Top 10 products
- 🥧 Pie Chart: Payment method distribution
- 💳 KPI Cards: Total revenue, profit margin

## Data Schema
### [filename].csv
| Column | Type | Description | Sample Values |
|--------|------|-------------|---------------|
| transaction_id | String | Unique ID | TXN001, TXN002 |
| date | Date | Transaction date | 2025-10-01 |
...
```

---

## **Deliverables**

Create the following folder structure:

```
datasets/
├── sales_revenue/
│   ├── README.md
│   ├── sales_transactions.csv
│   ├── customers.csv
│   ├── products.csv
│   └── sales_reps.xlsx
├── finance_accounting/
│   ├── README.md
│   ├── invoices.csv
│   ├── payments.csv
│   ├── ar_aging.csv
│   └── expense_report.xlsx
├── inventory_supply_chain/
│   ├── README.md
│   ├── inventory_levels.csv
│   ├── suppliers.xlsx
│   ├── reorder_alerts.csv
│   └── shipments.csv
├── hr_payroll/
│   ├── README.md
│   ├── employees.csv
│   ├── attendance.csv
│   ├── payroll.xlsx
│   └── departments.csv
├── manufacturing/
│   ├── README.md
│   ├── production_log.csv
│   ├── defects.csv
│   ├── equipment.xlsx
│   └── materials.csv
├── healthcare/
│   ├── README.md
│   ├── patients.csv
│   ├── appointments.csv
│   ├── billing.xlsx
│   └── insurance_claims.csv
└── education/
    ├── README.md
    ├── students.csv
    ├── courses.csv
    ├── enrollments.csv
    └── grades.xlsx
```

---

## **Important Guidelines**

1. **Realistic Data**: Use plausible names, addresses, values
2. **Variety**: Mix different data patterns, trends (growth, decline, seasonal)
3. **Relationships**: Maintain referential integrity across files
4. **File Sizes**: 
   - Small files: 50-200 rows
   - Medium files: 200-500 rows
   - Large files: 500-1000 rows
5. **Data Types**: Include dates, numbers, text, categorical data
6. **Current Data**: Use dates from last 3-6 months (Oct 2024 - Oct 2025)

---

## **Example Commands to Generate Files**

For each domain, provide:
1. Python script to generate the CSV files
2. Use pandas, numpy, faker libraries
3. Seed random generators for reproducibility (seed=42)
4. Include comments explaining data generation logic

---

## **Success Criteria**

The generated datasets should enable the AI system to:
- ✅ Automatically detect data types (dates, numbers, categories)
- ✅ Generate appropriate charts (line, bar, pie, table, KPIs)
- ✅ Show meaningful business insights
- ✅ Handle relationships across multiple files
- ✅ Work with different file formats (CSV, XLSX, TXT)
- ✅ Demonstrate value across different business domains
- ✅ Showcase role-specific dashboards (CEO, CFO, Manager, Employee)

---

## **Additional Notes**

- **Domain**: For each file, suggest appropriate "domain" values (e.g., "Sales Analytics", "Financial Management")
- **Intent**: For each file, suggest appropriate "intent" values (e.g., "Show revenue trends", "Identify overdue invoices")
- **Charts**: Specify what charts the AI should generate for each dataset

---

**Start by creating the Sales & Revenue domain first, then proceed to the others.**
