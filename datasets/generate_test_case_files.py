"""
Generate Test Case Markdown Files

This script creates all 42 test case markdown files with proper structure.
Each test case is human-readable and ready for manual testing.
"""

from pathlib import Path

TEST_CASES_DIR = Path(__file__).parent / "test_cases"

# Test case definitions
RETAIL_TESTS = [
    {
        'id': 'TC001',
        'name': 'small_daily_sales',
        'title': 'Retail Small Business - Daily Sales Dashboard',
        'size': 'Small (1-50 employees)',
        'complexity': 'Basic',
        'company': 'Joe\'s Hardware Store',
        'persona': 'Store owner tracking daily sales performance',
        'question': 'How are my daily sales performing? Which products sell best? When are my peak hours?',
        'files': [
            {'name': 'TC001_sales_transactions.csv', 'rows': 500, 'desc': 'Primary sales data with transactions'},
            {'name': 'TC001_products.csv', 'rows': 80, 'desc': 'Product catalog with pricing'},
            {'name': 'TC001_employees.csv', 'rows': 15, 'desc': 'Employee roster'}
        ],
        'domain': 'Retail Sales Analytics',
        'intent': 'Show me daily sales trends, best-selling products, and peak shopping hours',
        'widgets': [
            {'type': 'Line Chart', 'title': 'Daily Revenue Trend (Last 90 Days)', 'desc': 'Track revenue over time'},
            {'type': 'Bar Chart', 'title': 'Revenue by Product Category', 'desc': 'Compare category performance'},
            {'type': 'Table', 'title': 'Top 10 Best-Selling Products', 'desc': 'Identify top performers'},
            {'type': 'Bar Chart', 'title': 'Transactions by Hour of Day', 'desc': 'Find peak hours'},
            {'type': 'Pie Chart', 'title': 'Payment Method Distribution', 'desc': 'Payment preferences'},
            {'type': 'KPI Card', 'title': 'Total Revenue (90 Days)', 'desc': 'Main revenue metric'},
        ]
    },
    {
        'id': 'TC002',
        'name': 'small_inventory_stock',
        'title': 'Retail Small Business - Inventory Stock Management',
        'size': 'Small (1-50 employees)',
        'complexity': 'Basic',
        'company': 'City Corner Store',
        'persona': 'Store manager managing inventory levels',
        'question': 'Which items are low on stock? What should I reorder? How much will it cost?',
        'files': [
            {'name': 'TC002_inventory.csv', 'rows': 200, 'desc': 'Current inventory levels'},
            {'name': 'TC002_suppliers.xlsx', 'rows': 25, 'desc': 'Supplier information'},
            {'name': 'TC002_reorder_alerts.csv', 'rows': 30, 'desc': 'Low stock alerts'}
        ],
        'domain': 'Inventory Management',
        'intent': 'Show me low stock items, reorder recommendations, and supplier performance',
        'widgets': [
            {'type': 'Bar Chart', 'title': 'Low Stock Items by Category', 'desc': 'Identify shortage areas'},
            {'type': 'Table', 'title': 'Urgent Reorder List', 'desc': 'Action items for purchasing'},
            {'type': 'KPI Card', 'title': 'Total Reorder Cost', 'desc': 'Budget needed'},
            {'type': 'Bar Chart', 'title': 'Supplier Lead Time Comparison', 'desc': 'Choose fastest supplier'},
            {'type': 'Gauge', 'title': 'Stock Adequacy Score', 'desc': 'Overall inventory health'},
        ]
    },
    # Add TC003-TC006 placeholders
    {'id': 'TC003', 'name': 'medium_multistore', 'title': 'Retail Medium - Multi-Store Comparison', 'placeholder': True},
    {'id': 'TC004', 'name': 'medium_customer_loyalty', 'title': 'Retail Medium - Customer Loyalty Program', 'placeholder': True},
    {'id': 'TC005', 'name': 'large_ecommerce', 'title': 'Retail Large - E-commerce Analytics', 'placeholder': True},
    {'id': 'TC006', 'name': 'large_supply_chain', 'title': 'Retail Large - Supply Chain Optimization', 'placeholder': True},
]

FINANCE_TESTS = [
    {'id': 'TC007', 'name': 'small_cashflow', 'title': 'Finance Small - Cash Flow Management', 'placeholder': True},
    {'id': 'TC008', 'name': 'small_expenses', 'title': 'Finance Small - Expense Tracking', 'placeholder': True},
    {'id': 'TC009', 'name': 'medium_ar_aging', 'title': 'Finance Medium - AR Aging Analysis', 'placeholder': True},
    {'id': 'TC010', 'name': 'medium_ap_management', 'title': 'Finance Medium - AP Management', 'placeholder': True},
    {'id': 'TC011', 'name': 'large_banking', 'title': 'Finance Large - Banking Operations', 'placeholder': True},
    {'id': 'TC012', 'name': 'large_investment', 'title': 'Finance Large - Investment Portfolio', 'placeholder': True},
]

# Similar lists for other industries...
ALL_TESTS = {
    'retail': RETAIL_TESTS,
    'finance': FINANCE_TESTS,
    # Add others as placeholders for now
}


def generate_full_test_case(test):
    """Generate complete test case markdown"""
    content = f"""# {test['id']}: {test['title']}

## 🏢 Test Case Metadata
- **Test Case ID**: {test['id']}
- **Industry**: Retail
- **Company Size**: {test['size']}
- **Complexity**: {test['complexity']}
- **Date Created**: 2025-10-29
- **Status**: Ready for Testing

---

## 📊 Business Context
**Company Profile**: "{test['company']}" - {test['persona']}.

**Business Question**: "{test['question']}"

---

## 📁 Required Data Files (Upload All {len(test['files'])})

"""
    
    for i, file in enumerate(test['files'], 1):
        content += f"""### File {i}: `{file['name']}`
- **Rows**: {file['rows']}
- **Description**: {file['desc']}

"""
    
    content += f"""---

## 🎯 User Input to Elas ERP

**Step 1: Upload Files**
"""
    
    for file in test['files']:
        content += f"- Upload `{file['name']}`\n"
    
    content += f"""
**Step 2: Quick-Viz Input**
- **Domain**: "{test['domain']}"
- **User Intent**: "{test['intent']}"

---

## ✅ Expected Widget Proposals ({len(test['widgets'])} widgets)

"""
    
    for i, widget in enumerate(test['widgets'], 1):
        content += f"""### Widget {i}: {widget['title']} ({widget['type']})
- **Type**: {widget['type']}
- **Title**: "{widget['title']}"
- **Purpose**: {widget['desc']}
- **Validation**: 
  - ☐ Widget generated
  - ☐ Correct type ({widget['type']})
  - ☐ Appropriate data shown
  - ☐ Renders without errors

"""
    
    content += """---

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
"""
    
    for file in test['files']:
        content += f"2. Upload `{file['name']}`\n"
    
    content += f"""
### 3. Generate Widgets
1. Navigate to Quick-Viz
2. Enter domain: "{test['domain']}"
3. Enter intent: "{test['intent']}"
4. Click "Generate Dashboard"

### 4. Validate Results
"""
    
    for i, widget in enumerate(test['widgets'], 1):
        content += f"- [ ] Widget {i}: {widget['title']} ({widget['type']})\n"
    
    content += f"""
**Overall Test Result**: ☐ PASS ☐ FAIL

---

## 📝 Notes
_Add any observations, issues, or screenshots here_

---

**Last Updated**: 2025-10-29
"""
    
    return content


def generate_placeholder_test_case(test):
    """Generate placeholder test case markdown"""
    return f"""# {test['id']}: {test['title']}

## 🏢 Test Case Metadata
- **Test Case ID**: {test['id']}
- **Industry**: {test['title'].split()[0]}
- **Status**: ⚠️ Placeholder - Not Yet Implemented

---

## 📋 TODO
This test case needs to be fully defined with:
1. Business context and company profile
2. Data file specifications (2-5 files)
3. Expected widget proposals (5-7 widgets)
4. Validation criteria
5. Test execution steps

---

**Last Updated**: 2025-10-29
"""


def main():
    print("\n" + "="*70)
    print("📝 GENERATING TEST CASE MARKDOWN FILES")
    print("="*70)
    
    total_generated = 0
    
    for industry, tests in ALL_TESTS.items():
        print(f"\n📦 {industry.upper()}")
        industry_dir = TEST_CASES_DIR / industry
        industry_dir.mkdir(parents=True, exist_ok=True)
        
        for test in tests:
            filename = f"{test['id']}_{test['name']}.md"
            filepath = industry_dir / filename
            
            if test.get('placeholder'):
                content = generate_placeholder_test_case(test)
                print(f"  ⚠️  {test['id']} (placeholder)")
            else:
                content = generate_full_test_case(test)
                print(f"  ✅ {test['id']} (complete)")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            total_generated += 1
    
    print("\n" + "="*70)
    print(f"✅ Generated {total_generated} test case files!")
    print("="*70)
    print(f"\n📁 Location: {TEST_CASES_DIR}")
    print("\n💡 Next steps:")
    print("   1. Review generated test cases")
    print("   2. Generate test data: python generate_test_case_data.py")
    print("   3. Start testing with TC001\n")


if __name__ == '__main__':
    main()
