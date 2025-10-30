"""
Generate realistic sales retail dataset with transactions, products, and reps.
"""
import pandas as pd
import random
import string
from datetime import datetime, timedelta
from pathlib import Path

# Set random seed for reproducibility
random.seed(42)

# Output directory
OUTPUT_DIR = Path(__file__).parent / "sales_retail"
OUTPUT_DIR.mkdir(exist_ok=True)

# Helper functions
def random_date(start_date, end_date):
    """Generate random date between start and end"""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def add_nulls(series, null_pct=0.05):
    """Add random nulls to series"""
    mask = [random.random() < null_pct for _ in range(len(series))]
    return series.mask(mask, None)

# Generate Products (80 rows)
print("Generating products.csv...")
product_categories = ["Electronics", "Furniture", "Clothing", "Food & Beverage", "Office Supplies", "Sports", "Home & Garden"]
product_names = {
    "Electronics": ["Laptop", "Monitor", "Keyboard", "Mouse", "Headphones", "Webcam", "USB Cable", "Power Bank", "Tablet", "Smartphone"],
    "Furniture": ["Office Chair", "Desk", "Filing Cabinet", "Bookshelf", "Conference Table", "Standing Desk", "Ergonomic Chair"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Shoes", "Hat", "Socks", "Belt", "Dress", "Sweater"],
    "Food & Beverage": ["Coffee", "Tea", "Snacks", "Water", "Energy Drink", "Lunch Box", "Protein Bar"],
    "Office Supplies": ["Pen", "Notebook", "Paper", "Stapler", "Tape", "Folder", "Binder", "Calculator"],
    "Sports": ["Yoga Mat", "Dumbbells", "Resistance Band", "Water Bottle", "Jump Rope", "Exercise Ball"],
    "Home & Garden": ["Plant Pot", "Garden Tools", "Light Bulb", "Picture Frame", "Candle", "Vase"]
}

products = []
product_id = 1000
for category in product_categories:
    for name in product_names[category]:
        base_price = random.uniform(5, 500)
        products.append({
            "product_id": f"P{product_id}",
            "product_name": name,
            "category": category,
            "unit_price": round(base_price, 2),
            "cost": round(base_price * 0.6, 2),
            "weight_kg": round(random.uniform(0.1, 25), 2),
            "supplier": random.choice(["GlobalSupply Inc", "TechDistro", "MegaWholesale", "DirectSource LLC", "PrimeVendors"]),
            "sku": f"SKU-{category[:3].upper()}-{product_id}"
        })
        product_id += 1

products_df = pd.DataFrame(products)
products_df.to_csv(OUTPUT_DIR / "products.csv", index=False)

# Generate Sales Reps (25 rows)
print("Generating reps.csv...")
first_names = ["John", "Sarah", "Michael", "Emily", "David", "Jessica", "James", "María", "Robert", "Jennifer", 
               "William", "Lisa", "José", "Karen", "Thomas", "Nancy", "Christopher", "Betty", "Daniel", "Patricia",
               "Matthew", "Sandra", "Anthony", "Ashley", "Mark"]
last_names = ["Smith", "Johnson", "Williams", "García", "Brown", "Jones", "Miller", "Davis", "Rodríguez", "Martinez",
              "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White",
              "Harris", "Clark", "Lewis", "Robinson", "Walker"]

regions = ["North", "South", "East", "West"]
reps = []
for i in range(25):
    hire_date = random_date(datetime(2018, 1, 1), datetime(2024, 6, 1))
    reps.append({
        "rep_id": f"R{1001 + i}",
        "rep_name": f"{random.choice(first_names)} {random.choice(last_names)}",
        "email": f"rep{i+1}@elas-erp.com",
        "region": random.choice(regions),
        "hire_date": hire_date.strftime("%Y-%m-%d"),
        "quota": random.randint(50000, 200000),
        "commission_rate": round(random.uniform(0.02, 0.08), 3)
    })

reps_df = pd.DataFrame(reps)
reps_df.to_csv(OUTPUT_DIR / "reps.csv", index=False)

# Generate Sales Transactions (1,200 rows in CSV, 300 in XLSX)
print("Generating sales_transactions.csv (1,200 rows)...")
channels = ["Online", "In-Store", "Phone", "Partner"]
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "Austin"]

def generate_transactions(n_rows):
    transactions = []
    for i in range(n_rows):
        order_date = random_date(datetime(2023, 1, 1), datetime(2025, 10, 1))
        product = products_df.sample(1).iloc[0]
        rep = reps_df.sample(1).iloc[0]
        
        # Quantities with variation
        qty = random.choices([1, 2, 3, 5, 10, 25, 50], weights=[30, 25, 20, 15, 5, 3, 2])[0]
        
        # Discount with some outliers
        discount_pct = random.choices([0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30], weights=[40, 20, 15, 10, 8, 5, 2])[0]
        
        subtotal = product["unit_price"] * qty
        discount_amount = subtotal * discount_pct
        tax = (subtotal - discount_amount) * 0.0825
        shipping = random.choice([0, 5.99, 9.99, 15.99, 25.99]) if random.random() > 0.3 else 0
        amount = subtotal - discount_amount + tax + shipping
        
        # Client name with occasional trailing spaces
        client_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        if random.random() < 0.1:
            client_name += " "  # trailing space
        
        transactions.append({
            "order_id": f"ORD-{10000 + i}",
            "order_date": order_date.strftime("%Y-%m-%d"),
            "account_id": f"A{random.randint(1000, 1300)}",
            "client_name": client_name,
            "rep_id": rep["rep_id"],
            "rep_name": rep["rep_name"],
            "region": rep["region"],
            "city": random.choice(cities),
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"],
            "qty": qty,
            "unit_price": product["unit_price"],
            "discount_pct": discount_pct,
            "discount_amount": round(discount_amount, 2),
            "tax": round(tax, 2),
            "shipping": shipping,
            "amount": round(amount, 2),
            "channel": random.choice(channels)
        })
    
    return pd.DataFrame(transactions)

# Generate CSV version (1,200 rows)
transactions_df = generate_transactions(1200)

# Add 1-2% duplicates
n_duplicates = int(len(transactions_df) * 0.015)
duplicate_indices = random.sample(range(len(transactions_df)), n_duplicates)
duplicates = transactions_df.iloc[duplicate_indices].copy()
transactions_df = pd.concat([transactions_df, duplicates], ignore_index=True)

# Add nulls to non-key columns
transactions_df["city"] = add_nulls(transactions_df["city"], 0.05)
transactions_df["shipping"] = add_nulls(transactions_df["shipping"], 0.03)

# Add large outlier
outlier_idx = random.randint(0, len(transactions_df) - 1)
transactions_df.loc[outlier_idx, "amount"] = 250000.00
transactions_df.loc[outlier_idx, "qty"] = 1000

transactions_df.to_csv(OUTPUT_DIR / "sales_transactions.csv", index=False)

# Generate XLSX version (300 rows)
print("Generating sales_transactions.xlsx (300 rows)...")
transactions_small_df = generate_transactions(300)
transactions_small_df.to_excel(OUTPUT_DIR / "sales_transactions.xlsx", index=False, engine='openpyxl')

# Generate README
print("Generating readme.md...")
readme_content = """# Sales Retail Dataset

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
"""

with open(OUTPUT_DIR / "readme.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print(f"✅ Sales retail dataset generated in {OUTPUT_DIR}")
print(f"   - sales_transactions.csv: {len(transactions_df)} rows")
print(f"   - sales_transactions.xlsx: 300 rows")
print(f"   - products.csv: {len(products_df)} rows")
print(f"   - reps.csv: {len(reps_df)} rows")
