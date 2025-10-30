# Minimal Small Dataset

## Overview
Small datasets for testing edge cases, empty states, and data quality issues.

## Files

### tiny_sales.csv (30 rows)
Minimal sales dataset for testing with small samples:
- **order_id**: Order identifier (ORD-1 to ORD-30)
- **order_date**: Order date (Sep-Oct 2025)
- **customer**: Customer name (5 customers)
- **product**: Product name (4 products)
- **quantity**: Quantity sold (1-10)
- **amount**: Order amount ($10-500)
- **region**: Geographic region (4 regions)
- **status**: Order status (Shipped | Pending | Delivered)

**Use Cases**:
- Test UI with minimal data
- Verify empty state handling
- Test quick aggregations with small dataset
- Validate chart rendering with limited points

### weird_headers.csv (40 rows)
Dataset with challenging column names:
- **Order ID**: Standard format
- **Order-Date**: Hyphen in name
- **Sales Person**: Space in column name + trailing spaces in values
- **Revenue($)**: Special character (dollar sign)
- **Units.Sold**: Period in name
- **Region/Zone**: Multiple special characters (slash)
- **Product_Category**: Underscore
- **Customer Type**: Space in name
- **Discount %**: Percent sign
- **Tax Amount**: Standard
- **  Trailing  **: Leading and trailing spaces in column name + empty values

**Data Quality Issues**:
- Leading/trailing spaces in values: `"John Smith "`, `" Jane Doe"`
- Complex region names: `"North/Central"`, `"South-West"`, `"East_Coast"`
- Empty values in last column (~25%)
- Mixed formatting in text fields

**Use Cases**:
- Test column name parsing and sanitization
- Verify handling of special characters in headers
- Test trim/cleanup utilities
- Validate mapping UI with problematic names
- Test export/import with special characters

## Testing Scenarios

### 1. Small Dataset Handling (tiny_sales.csv)
- Chart rendering with <50 points
- Table pagination with single page
- Aggregation with limited groups
- Filter behavior with few options
- Export functionality with small file

### 2. Data Quality (weird_headers.csv)
- Column name normalization
- Space trimming in values and headers
- Special character handling in names
- Empty value handling
- Type detection with messy data

### 3. Edge Cases
- Single customer with multiple orders
- Date range within 2 months
- Limited product variety (4 SKUs)
- Small dollar amounts (<$500)
- Repeated customer names

### 4. UI/UX Testing
- Empty state messages
- Minimum viable dataset
- Quick load times
- Simple filtering options
- Basic chart types

## Expected Visualizations

### tiny_sales.csv
1. **Bar Chart**: Revenue by region (4 bars)
2. **Line Chart**: Daily sales trend (short timeline)
3. **Pie Chart**: Product distribution (4 slices)
4. **Table**: All 30 rows visible on one page

### weird_headers.csv
1. **Revenue by Sales Person**: Test name trimming
2. **Region Analysis**: Handle slash/hyphen in names
3. **Discount Distribution**: Handle % in column name
4. **Data Quality Report**: Identify issues

## Integration Testing
Use these datasets to:
- Verify onboarding flow with minimal data
- Test quick-viz suggestions with limited columns
- Validate mapping interface with special characters
- Ensure error handling for empty/null values
- Test CSV parsing robustness
