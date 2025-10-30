# Elas ERP Demo Datasets

This directory contains realistic sample datasets for testing the onboarding → quick-viz → mapping pipeline.

## Structure

- **sales_retail/** - Retail sales transactions with products and sales reps
- **finance_ar/** - Accounts receivable with invoices, payments, and aging
- **operations_workorders/** - Work order management with technicians and shifts
- **education_enrollments/** - Student enrollments with courses and instructors
- **minimal_small/** - Small datasets for edge case testing

## Generating Data

Run the generator scripts to populate each scenario:

```powershell
# Install dependencies
pip install pandas openpyxl fpdf

# Generate all datasets
python datasets/generate_sales_retail.py
python datasets/generate_finance_ar.py
python datasets/generate_operations_workorders.py
python datasets/generate_education_enrollments.py
python datasets/generate_minimal_small.py
```

Or run all at once:
```powershell
Get-ChildItem datasets\generate_*.py | ForEach-Object { python $_.FullName }
```

## Features

- **Realistic variation**: Dates span 2023-2025, multiple regions, outliers
- **Data quality issues**: ~5% nulls, 1-2% duplicates, weird headers
- **Join capabilities**: Consistent IDs across related tables
- **Aging buckets**: Finance data includes CURRENT, 30, 60, 90, 90+ day aging
- **Multiple formats**: CSV, XLSX, and PDF files
- **Documentation**: Each scenario has a readme explaining columns and viz ideas
