# Test Cases - Elas ERP Widget Generation

## 📋 Overview
This directory contains **42 comprehensive test cases** for validating Elas ERP's widget generation system across 7 industries, 3 company sizes, and various data scenarios.

---

## 🎯 Test Coverage

### Industries (7)
- **Retail**: Daily sales, inventory, multi-store, customer loyalty, e-commerce, supply chain
- **Finance**: Cash flow, expenses, AR aging, AP management, banking, investments
- **Healthcare**: Clinic visits, patient billing, hospital ops, pharmacy, claims processing
- **Manufacturing**: Job shop, quality control, production line, supply chain, factory network
- **Education**: Private school, student performance, college ops, faculty workload, university, research grants
- **SaaS**: Startup MRR, customer churn, subscription growth, usage metrics, enterprise
- **Logistics**: Courier deliveries, vehicle maintenance, warehouse ops, route optimization, 3PL, international shipping

### Company Sizes (3)
- **Small**: 1-50 employees, single location, basic operations
- **Medium**: 51-500 employees, multiple locations, moderate complexity
- **Large**: 500+ employees, enterprise-scale, high complexity

### Test Case Distribution
| Industry | Small | Medium | Large | **Total** |
|----------|-------|--------|-------|-----------|
| Retail | 2 | 2 | 2 | **6** |
| Finance | 2 | 2 | 2 | **6** |
| Healthcare | 2 | 2 | 2 | **6** |
| Manufacturing | 2 | 2 | 2 | **6** |
| Education | 2 | 2 | 2 | **6** |
| SaaS | 2 | 2 | 2 | **6** |
| Logistics | 2 | 2 | 2 | **6** |
| **TOTAL** | **14** | **14** | **14** | **42** |

---

## 📁 Directory Structure

```
test_cases/
├── README.md (this file)
├── run_test_cases.py          # BONUS: Automated test runner
├── test_results/               # Test execution logs (auto-generated)
│
├── retail/
│   ├── TC001_small_daily_sales.md
│   ├── TC002_small_inventory_stock.md
│   ├── TC003_medium_multistore.md
│   ├── TC004_medium_customer_loyalty.md
│   ├── TC005_large_ecommerce.md
│   └── TC006_large_supply_chain.md
│
├── finance/
│   ├── TC007_small_cashflow.md
│   ├── TC008_small_expenses.md
│   ├── TC009_medium_ar_aging.md
│   ├── TC010_medium_ap_management.md
│   ├── TC011_large_banking.md
│   └── TC012_large_investment_portfolio.md
│
├── healthcare/
│   ├── TC013_small_clinic_visits.md
│   ├── TC014_small_patient_billing.md
│   ├── TC015_medium_hospital_ops.md
│   ├── TC016_medium_pharmacy.md
│   ├── TC017_large_hospital_network.md
│   └── TC018_large_claims_processing.md
│
├── manufacturing/
│   ├── TC019_small_job_shop.md
│   ├── TC020_small_quality_control.md
│   ├── TC021_medium_production_line.md
│   ├── TC022_medium_supply_chain.md
│   ├── TC023_large_factory_network.md
│   └── TC024_large_global_operations.md
│
├── education/
│   ├── TC025_small_private_school.md
│   ├── TC026_small_student_performance.md
│   ├── TC027_medium_college.md
│   ├── TC028_medium_faculty_workload.md
│   ├── TC029_large_university.md
│   └── TC030_large_research_grants.md
│
├── saas/
│   ├── TC031_small_startup_mrr.md
│   ├── TC032_small_customer_churn.md
│   ├── TC033_medium_subscription_growth.md
│   ├── TC034_medium_usage_metrics.md
│   ├── TC035_large_enterprise_saas.md
│   └── TC036_large_global_expansion.md
│
└── logistics/
    ├── TC037_small_courier_deliveries.md
    ├── TC038_small_vehicle_maintenance.md
    ├── TC039_medium_warehouse_ops.md
    ├── TC040_medium_route_optimization.md
    ├── TC041_large_3pl_operations.md
    └── TC042_large_international_shipping.md
```

---

## 📝 Test Case Format

Each test case is a **human-readable Markdown file** containing:

### 1. Metadata
- Test Case ID
- Industry, company size, complexity
- Status (Ready/In Progress/Blocked)

### 2. Business Context
- Company profile (fictional but realistic)
- User persona
- Business question being answered

### 3. Required Data Files
- 2-5 CSV/XLSX files per test case
- Column schemas documented
- Row counts and date ranges
- Data quality characteristics

### 4. User Input
- Domain to specify
- User intent/question
- Expected behavior

### 5. Expected Widgets
- 5-7 widget proposals per test case
- Each widget fully specified:
  - Type (line, bar, pie, table, KPI, etc.)
  - Title
  - Axes/columns
  - Aggregations
  - Expected patterns
  - Validation checklist

### 6. Test Execution Steps
- Setup instructions
- Upload sequence
- Input values
- Validation checkpoints

### 7. Results Template
- Checklist for each widget
- Pass/Fail criteria
- Screenshots required
- Issue tracking

---

## 🚀 Quick Start

### Manual Testing (Individual Test Case)

```powershell
# 1. Navigate to test cases
cd datasets/test_cases

# 2. Pick a test case (start with TC001)
code retail/TC001_small_daily_sales.md

# 3. Prepare data files
cd ../sample_data/retail
ls TC001_*.csv  # Should see 3 files

# 4. Start Elas ERP servers
# (See test case for specific commands)

# 5. Follow test execution steps in the markdown file

# 6. Fill out results template

# 7. Save results
# Copy results section to: test_results/TC001_results_YYYY-MM-DD.md
```

### Automated Testing (All Test Cases)

```powershell
# 1. Install dependencies
pip install pandas requests pytest

# 2. Run automated test suite
python test_cases/run_test_cases.py

# Options:
python test_cases/run_test_cases.py --industry retail  # Test only retail
python test_cases/run_test_cases.py --size small      # Test only small companies
python test_cases/run_test_cases.py --test TC001      # Test specific case
python test_cases/run_test_cases.py --parallel 4      # Run 4 tests in parallel

# 3. View results
# Generates: test_results/test_run_YYYY-MM-DD_HH-MM-SS.html
```

---

## 📊 Sample Data Files

All test case data files are in `../sample_data/`:

```
sample_data/
├── retail/
│   ├── TC001_sales_transactions.csv (500 rows)
│   ├── TC001_products.csv (80 rows)
│   ├── TC001_employees.csv (15 rows)
│   ├── TC002_inventory.csv (200 rows)
│   ├── TC002_suppliers.xlsx (25 rows)
│   └── ... (30+ files)
│
├── finance/
│   ├── TC007_cashflow.csv
│   ├── TC007_bank_accounts.csv
│   └── ... (30+ files)
│
├── healthcare/
├── manufacturing/
├── education/
├── saas/
└── logistics/

TOTAL: ~150 data files across all test cases
```

---

## ✅ Validation Criteria

Each test case is considered **PASS** if:

1. ✅ **File Upload**: All files upload without errors
2. ✅ **Parsing**: Columns and data types correctly detected
3. ✅ **Widget Count**: 5-7 widgets generated (as specified)
4. ✅ **Widget Types**: Correct chart types chosen for data
5. ✅ **Data Accuracy**: Spot-check values match source files
6. ✅ **Joins**: Multi-file relationships work (IDs resolve to names)
7. ✅ **Aggregations**: Time-based grouping (daily/monthly) correct
8. ✅ **Visual Quality**: Charts render cleanly, no overlap
9. ✅ **Performance**: Response time under 10 seconds
10. ✅ **User Intent**: Widgets answer the business question

---

## 🧪 Test Progression

### Phase 1: Smoke Tests (4 test cases)
Start with these to validate core functionality:
- **TC001**: Retail Small - Daily Sales (simplest, clean data)
- **TC007**: Finance Small - Cash Flow (basic financial)
- **TC013**: Healthcare Small - Clinic Visits (date-heavy)
- **TC019**: Manufacturing Small - Job Shop (status tracking)

**Goal**: Ensure basic widget generation works end-to-end

### Phase 2: Data Quality Tests (6 test cases)
Test handling of problematic data:
- **TC002**: Retail - Has nulls in optional columns
- **TC008**: Finance - Has duplicate transactions
- **TC014**: Healthcare - Has outliers in billing amounts
- **TC020**: Manufacturing - Has missing status values
- **TC026**: Education - Has grade formatting issues
- **TC032**: SaaS - Has churn date nulls

**Goal**: Validate robustness against real-world data issues

### Phase 3: Complexity Tests (8 test cases)
Test multi-file scenarios and complex joins:
- **TC003**: Retail Medium - Multi-Store (regional aggregation)
- **TC009**: Finance Medium - AR Aging (aging bucket calculations)
- **TC015**: Healthcare Medium - Hospital Ops (department breakdowns)
- **TC021**: Manufacturing Medium - Production Line (shift analysis)
- **TC027**: Education Medium - College (term-over-term comparisons)
- **TC033**: SaaS Medium - Subscription Growth (cohort analysis)
- **TC039**: Logistics Medium - Warehouse Ops (zone performance)
- **TC041**: Logistics Large - 3PL Operations (multi-client)

**Goal**: Ensure complex scenarios work correctly

### Phase 4: Enterprise Tests (6 test cases)
Test large-scale scenarios:
- **TC005**: Retail Large - E-commerce (online vs in-store)
- **TC011**: Finance Large - Banking (account type segmentation)
- **TC017**: Healthcare Large - Hospital Network (multi-facility)
- **TC023**: Manufacturing Large - Factory Network (global ops)
- **TC029**: Education Large - University (multi-campus)
- **TC035**: SaaS Large - Enterprise (tier-based analysis)

**Goal**: Validate scalability and advanced analytics

### Phase 5: Full Regression (All 42 test cases)
Run complete test suite before major releases

---

## 📈 Automated Test Runner (BONUS)

The `run_test_cases.py` script provides:

### Features
- ✅ Automated file upload via API
- ✅ Parallel test execution (configurable)
- ✅ Real-time progress tracking
- ✅ Widget validation (count, types, data accuracy)
- ✅ Performance metrics (response times)
- ✅ HTML test report generation
- ✅ Failure screenshots
- ✅ Groq log capture per test
- ✅ Pass/Fail statistics
- ✅ Trend analysis (compare runs over time)

### Usage Examples

```powershell
# Run all tests (sequential)
python run_test_cases.py

# Run specific industry
python run_test_cases.py --industry retail

# Run specific size
python run_test_cases.py --size small

# Run single test case
python run_test_cases.py --test TC001

# Run with parallelism (4 workers)
python run_test_cases.py --parallel 4

# Run and generate detailed report
python run_test_cases.py --report detailed

# Compare with previous run
python run_test_cases.py --compare test_results/test_run_2025-10-28.html
```

### Output
```
╔═══════════════════════════════════════════════════════════╗
║             ELAS ERP TEST SUITE - RUN SUMMARY            ║
╚═══════════════════════════════════════════════════════════╝

Start Time: 2025-10-29 14:30:00
Total Tests: 42
Duration: 8m 32s

✅ PASSED:  38 tests (90.5%)
❌ FAILED:   3 tests (7.1%)
⚠️  SKIPPED: 1 test  (2.4%)

═══════════════════════════════════════════════════════════

FAILURES:
  TC015 - Healthcare Medium: Widget 4 type mismatch (expected pie, got bar)
  TC023 - Manufacturing Large: Join failed (employee names not resolved)
  TC035 - SaaS Large: Timeout (response took 14.2s, limit 10s)

═══════════════════════════════════════════════════════════

DETAILED REPORT: test_results/test_run_2025-10-29_14-30-00.html
GROQ LOGS: test_results/groq_logs/
```

---

## 🎯 Test Case Development Status

| ID | Test Case | Status | Data Files | Priority |
|----|-----------|--------|-----------|----------|
| TC001 | Retail Small - Daily Sales | ✅ Ready | 3 files | P0 |
| TC002 | Retail Small - Inventory | 🚧 In Progress | 2/3 files | P0 |
| TC003 | Retail Medium - Multi-Store | 📝 Planned | 0/4 files | P1 |
| ... | ... | ... | ... | ... |

**Legend**:
- ✅ **Ready**: Test case + data files complete
- 🚧 **In Progress**: Test case drafted, data files in progress
- 📝 **Planned**: Specification only, not yet implemented
- ⏸️ **Blocked**: Waiting on dependency or feature

---

## 📚 Additional Resources

### Related Documentation
- [Dataset Generators README](../README.md) - How to generate sample data
- [Quick Start Guide](../QUICKSTART.md) - Setup instructions
- [Elas ERP Onboarding Docs](../../elas-erp/docs/onboarding.md)
- [Widget Spec Documentation](../../elas-erp/docs/widgets.md)

### Test Data Generation
If you need to regenerate or modify test data:
```powershell
# Regenerate all retail test data
python datasets/generate_test_case_data.py --industry retail

# Generate specific test case data
python datasets/generate_test_case_data.py --test TC001
```

### Troubleshooting
- **Issue**: Test case fails with "File not found"
  - **Solution**: Run data generators first: `python datasets/generate_test_case_data.py`

- **Issue**: Automated test runner hangs
  - **Solution**: Check backend is running on port 8000

- **Issue**: Widget validation fails but looks correct
  - **Solution**: Check validation criteria in test case MD file, may need adjustment

---

## 🤝 Contributing

To add new test cases:

1. **Create test case markdown** in appropriate industry folder
2. **Follow naming convention**: `TC###_size_description.md`
3. **Generate sample data** for the test case
4. **Document expected widgets** with validation criteria
5. **Test manually** first to ensure it works
6. **Update this README** with new test case in table

---

## 📞 Support

For questions about test cases:
- Check [SAMPLE_TC001](SAMPLE_TC001_retail_small_daily_sales.md) for reference
- Review existing test cases in `retail/` folder
- Contact: [Your support channel]

---

**Last Updated**: 2025-10-29
**Version**: 1.0
**Total Test Cases**: 42
**Total Data Files**: ~150
