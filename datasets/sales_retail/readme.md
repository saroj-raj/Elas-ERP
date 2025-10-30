# Sales Retail Dataset

## Overview
Realistic retail sales transaction data with products and sales representatives.

## Files

### sales_transactions.csv (1,200 rows)
Main transaction dataset with:
- **order_id**: Unique order identifier (ORD-xxxxx)
- **order_date**: Date of order (2023-2025)
- **account_id**: Customer account ID
- **client_name**: Customer name (some with trailing spaces)
- **rep_id**: Sales representative ID
- **rep_name**: Sales representative name
- **region**: Sales region (North/South/East/West)
- **city**: City name (~5% nulls)
- **product_id**: Product identifier
- **product_name**: Product name
- **category**: Product category
- **qty**: Quantity ordered (1-50, outliers at 1000)
- **unit_price**: Price per unit
- **discount_pct**: Discount percentage (0-30%)
- **discount_amount**: Dollar amount of discount
- **tax**: Sales tax (8.25%)
- **shipping**: Shipping cost (~3% nulls)
- **amount**: Total order amount (includes outlier at $250,000)
- **channel**: Sales channel (Online/In-Store/Phone/Partner)

### sales_transactions.xlsx (300 rows)
Same schema as CSV, smaller subset for XLSX testing.

### products.csv (80 rows)
Product master data:
- **product_id**: Product identifier
- **product_name**: Product name
- **category**: Product category (7 categories)
- **unit_price**: Standard selling price
- **cost**: Product cost
- **weight_kg**: Weight in kilograms
- **supplier**: Supplier name
- **sku**: Stock keeping unit

### reps.csv (25 rows)
Sales representative data:
- **rep_id**: Rep identifier
- **rep_name**: Rep full name (includes accents)
- **email**: Email address
- **region**: Assigned region
- **hire_date**: Date hired (2018-2024)
- **quota**: Annual sales quota
- **commission_rate**: Commission rate (2-8%)

## Data Quality Notes
- **Duplicates**: ~1.5% duplicate transactions (test deduplication)
- **Nulls**: ~5% in city, ~3% in shipping
- **Outliers**: One $250K transaction with 1000 qty
- **Spaces**: ~10% of client names have trailing spaces
- **Dates**: Include weekends, span 2023-2025

## Intended Visualizations
1. **Revenue Trends**: Daily/weekly/monthly revenue over time
2. **Top Products**: Best-selling products by revenue/qty
3. **Sales by Region**: Geographic performance comparison
4. **Rep Performance**: Sales by rep vs quota
5. **Channel Mix**: Revenue distribution by channel
6. **Discount Impact**: Relationship between discount % and order size
7. **Category Analysis**: Product category performance
8. **Order Size Distribution**: Histogram of order amounts
9. **Commission Analysis**: Rep earnings by commission rate
10. **Seasonality**: Sales patterns by month/quarter

## Join Keys
- `product_id` → products.csv
- `rep_id` → reps.csv
- `account_id` → (could join to customer master in other scenarios)
