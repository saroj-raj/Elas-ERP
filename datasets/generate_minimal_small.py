"""
Generate minimal test datasets with edge cases.
"""
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# Set random seed
random.seed(46)

# Output directory
OUTPUT_DIR = Path(__file__).parent / "minimal_small"
OUTPUT_DIR.mkdir(exist_ok=True)

# Helper functions
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Generate Tiny Sales (30 rows)
print("Generating tiny_sales.csv...")
tiny_sales = []
for i in range(30):
    order_date = random_date(datetime(2025, 9, 1), datetime(2025, 10, 29))
    amount = round(random.uniform(10, 500), 2)
    
    tiny_sales.append({
        "order_id": f"ORD-{i+1}",
        "order_date": order_date.strftime("%Y-%m-%d"),
        "customer": random.choice(["Acme Corp", "TechStart Inc", "Global Ltd", "Local Shop", "Big Co"]),
        "product": random.choice(["Widget A", "Widget B", "Service X", "Service Y"]),
        "quantity": random.randint(1, 10),
        "amount": amount,
        "region": random.choice(["North", "South", "East", "West"]),
        "status": random.choice(["Shipped", "Pending", "Delivered"])
    })

tiny_sales_df = pd.DataFrame(tiny_sales)
tiny_sales_df.to_csv(OUTPUT_DIR / "tiny_sales.csv", index=False)

# Generate Weird Headers (40 rows)
print("Generating weird_headers.csv...")
weird_data = []
for i in range(40):
    order_date = random_date(datetime(2025, 1, 1), datetime(2025, 10, 29))
    
    # Add intentional spaces and special characters
    sales_person_name = random.choice(["John Smith ", " Jane Doe", "Bob Johnson  ", "Alice Wong"])
    region_zone = random.choice(["North/Central", "South-West", "East_Coast", "West/Pacific"])
    
    weird_data.append({
        "Order ID": f"ORD{i+1:04d}",
        "Order-Date": order_date.strftime("%Y-%m-%d"),
        "Sales Person": sales_person_name,  # Intentional space in column name
        "Revenue($)": round(random.uniform(100, 10000), 2),  # Special char in name
        "Units.Sold": random.randint(1, 100),  # Period in name
        "Region/Zone": region_zone,  # Multiple special chars
        "Product_Category": random.choice(["Electronics", "Furniture", "Supplies"]),  # Underscore
        "Customer Type": random.choice(["B2B", "B2C", "Enterprise"]),  # Space
        "Discount %": round(random.uniform(0, 25), 1),  # Percent sign
        "Tax Amount": round(random.uniform(0, 500), 2),
        "  Trailing  ": random.choice(["A", "B", "C", ""])  # Leading/trailing spaces in column
    })

weird_df = pd.DataFrame(weird_data)
weird_df.to_csv(OUTPUT_DIR / "weird_headers.csv", index=False)

# Generate README
print("Generating readme.md...")
readme_content = """# Minimal Small Dataset

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
"""

with open(OUTPUT_DIR / "readme.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print(f"✅ Minimal small dataset generated in {OUTPUT_DIR}")
print(f"   - tiny_sales.csv: {len(tiny_sales_df)} rows")
print(f"   - weird_headers.csv: {len(weird_df)} rows")
