"""
Generate Test Case Data for Elas ERP Widget Testing

This script generates sample data files for all 42 test cases across 7 industries.
Each test case has 2-5 data files with realistic business data.

Usage:
    python generate_test_case_data.py                    # Generate all
    python generate_test_case_data.py --industry retail  # Generate retail only
    python generate_test_case_data.py --test TC001       # Generate specific test
"""

import pandas as pd
import random
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict

# Set seed for reproducibility
random.seed(42)

OUTPUT_DIR = Path(__file__).parent / "sample_data"

#  =============================================================================
#  RETAIL TEST CASES (TC001-TC006)
#  =============================================================================

def generate_TC001_retail_small_daily_sales():
    """TC001: Small Hardware Store - Daily Sales Dashboard"""
    print("  📦 TC001: Retail Small - Daily Sales")
    
    output_dir = OUTPUT_DIR / "retail"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # File 1: Sales Transactions (500 rows)
    categories = ['Hardware', 'Plumbing', 'Electrical', 'Garden', 'Paint', 'Tools']
    regions = ['North', 'South', 'East', 'West']
    payment_methods = ['Cash', 'Credit', 'Debit']
    
    transactions = []
    start_date = datetime(2025, 8, 1)
    
    for i in range(500):
        txn_date = start_date + timedelta(days=random.randint(0, 89))
        txn_time = f"{random.randint(8, 19):02d}:{random.randint(0, 59):02d}:00"
        
        category = random.choice(categories)
        unit_price = round(random.uniform(5, 150), 2)
        qty = random.randint(1, 20)
        discount = round(random.uniform(0, 20), 2) if random.random() < 0.3 else 0
        subtotal = unit_price * qty
        discount_amt = subtotal * (discount / 100)
        tax = (subtotal - discount_amt) * 0.0825
        total = subtotal - discount_amt + tax
        
        transactions.append({
            'transaction_id': f'TXN-{i+1:05d}',
            'date': txn_date.strftime('%Y-%m-%d'),
            'time': txn_time,
            'product_id': f'PROD-{random.randint(1, 80):03d}',
            'product_name': f'{category} Item {random.randint(1, 20)}',
            'category': category,
            'quantity': qty,
            'unit_price': unit_price,
            'discount': discount,
            'total_amount': round(total, 2),
            'payment_method': random.choice(payment_methods),
            'cashier_id': f'EMP-{random.randint(1, 15):03d}'
        })
    
    df_txn = pd.DataFrame(transactions)
    df_txn.to_csv(output_dir / 'TC001_sales_transactions.csv', index=False)
    print(f"    ✅ TC001_sales_transactions.csv ({len(df_txn)} rows)")
    
    # File 2: Products (80 rows)
    products = []
    for i in range(80):
        category = random.choice(categories)
        cost = round(random.uniform(3, 80), 2)
        sell = round(cost * random.uniform(1.3, 2.5), 2)
        
        products.append({
            'product_id': f'PROD-{i+1:03d}',
            'product_name': f'{category} Item {i+1}',
            'category': category,
            'supplier': f'Supplier {random.choice(["A", "B", "C", "D"])}',
            'cost_price': cost,
            'sell_price': sell,
            'stock_quantity': random.randint(10, 500),
            'reorder_level': random.randint(5, 50)
        })
    
    df_prod = pd.DataFrame(products)
    df_prod.to_csv(output_dir / 'TC001_products.csv', index=False)
    print(f"    ✅ TC001_products.csv ({len(df_prod)} rows)")
    
    # File 3: Employees (15 rows)
    employees = []
    roles = ['Manager', 'Cashier', 'Cashier', 'Cashier', 'Stock Clerk', 'Stock Clerk']
    
    for i in range(15):
        hire_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1800))
        employees.append({
            'employee_id': f'EMP-{i+1:03d}',
            'employee_name': f'Employee {i+1}',
            'role': random.choice(roles),
            'hire_date': hire_date.strftime('%Y-%m-%d'),
            'hourly_rate': round(random.uniform(12, 25), 2)
        })
    
    df_emp = pd.DataFrame(employees)
    df_emp.to_csv(output_dir / 'TC001_employees.csv', index=False)
    print(f"    ✅ TC001_employees.csv ({len(df_emp)} rows)")


def generate_TC002_retail_small_inventory():
    """TC002: Small Retail - Inventory Stock Management"""
    print("  📦 TC002: Retail Small - Inventory")
    
    output_dir = OUTPUT_DIR / "retail"
    
    # File 1: Inventory (200 rows)
    categories = ['Electronics', 'Clothing', 'Home', 'Sports', 'Books']
    
    inventory = []
    for i in range(200):
        category = random.choice(categories)
        cost = round(random.uniform(5, 200), 2)
        sell = round(cost * random.uniform(1.4, 2.8), 2)
        stock = random.randint(0, 300)
        reorder = random.randint(10, 50)
        
        # Add some low stock items
        if random.random() < 0.15:
            stock = random.randint(0, reorder - 1)
        
        inventory.append({
            'product_id': f'INV-{i+1:04d}',
            'product_name': f'{category} Product {i+1}',
            'category': category,
            'current_stock': stock,
            'reorder_level': reorder,
            'max_stock': reorder * 5,
            'cost_per_unit': cost,
            'sell_price': sell,
            'supplier_id': f'SUP-{random.randint(1, 25):03d}',
            'last_restock_date': (datetime.now() - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d'),
            'status': 'Low Stock' if stock < reorder else 'In Stock'
        })
    
    df_inv = pd.DataFrame(inventory)
    df_inv.to_csv(output_dir / 'TC002_inventory.csv', index=False)
    print(f"    ✅ TC002_inventory.csv ({len(df_inv)} rows)")
    
    # File 2: Suppliers (25 rows) - Excel format
    suppliers = []
    for i in range(25):
        suppliers.append({
            'supplier_id': f'SUP-{i+1:03d}',
            'supplier_name': f'Supplier Company {i+1}',
            'contact_person': f'Contact {i+1}',
            'phone': f'555-{random.randint(1000, 9999)}',
            'email': f'supplier{i+1}@example.com',
            'lead_time_days': random.randint(3, 30),
            'min_order_qty': random.randint(10, 100),
            'rating': round(random.uniform(3.5, 5.0), 1)
        })
    
    df_sup = pd.DataFrame(suppliers)
    df_sup.to_excel(output_dir / 'TC002_suppliers.xlsx', index=False)
    print(f"    ✅ TC002_suppliers.xlsx ({len(df_sup)} rows)")
    
    # File 3: Reorder Alerts (30 rows)
    low_stock_items = df_inv[df_inv['status'] == 'Low Stock'].head(30)
    reorder_alerts = []
    
    for _, item in low_stock_items.iterrows():
        shortage = item['reorder_level'] - item['current_stock']
        recommended_order = max(shortage, item['reorder_level'] * 2)
        
        reorder_alerts.append({
            'product_id': item['product_id'],
            'product_name': item['product_name'],
            'current_stock': item['current_stock'],
            'reorder_level': item['reorder_level'],
            'shortage': shortage,
            'recommended_order_qty': recommended_order,
            'estimated_cost': round(recommended_order * item['cost_per_unit'], 2),
            'priority': 'High' if item['current_stock'] == 0 else 'Medium',
            'supplier_id': item['supplier_id']
        })
    
    df_alerts = pd.DataFrame(reorder_alerts)
    df_alerts.to_csv(output_dir / 'TC002_reorder_alerts.csv', index=False)
    print(f"    ✅ TC002_reorder_alerts.csv ({len(df_alerts)} rows)")


# TODO: Add functions for TC003-TC042...
# For now, create placeholders that generate basic data

def generate_retail_test_data():
    """Generate all retail test case data"""
    print("\n🏪 Generating RETAIL test data...")
    generate_TC001_retail_small_daily_sales()
    generate_TC002_retail_small_inventory()
    # TODO: Add TC003-TC006
    print("  ⚠️  TC003-TC006 placeholders (to be implemented)")


def generate_finance_test_data():
    """Generate all finance test case data"""
    print("\n💰 Generating FINANCE test data...")
    print("  ⚠️  TC007-TC012 placeholders (to be implemented)")


def generate_healthcare_test_data():
    """Generate all healthcare test case data"""
    print("\n🏥 Generating HEALTHCARE test data...")
    print("  ⚠️  TC013-TC018 placeholders (to be implemented)")


def generate_manufacturing_test_data():
    """Generate all manufacturing test case data"""
    print("\n🏭 Generating MANUFACTURING test data...")
    print("  ⚠️  TC019-TC024 placeholders (to be implemented)")


def generate_education_test_data():
    """Generate all education test case data"""
    print("\n🎓 Generating EDUCATION test data...")
    print("  ⚠️  TC025-TC030 placeholders (to be implemented)")


def generate_saas_test_data():
    """Generate all SaaS test case data"""
    print("\n☁️ Generating SAAS test data...")
    print("  ⚠️  TC031-TC036 placeholders (to be implemented)")


def generate_logistics_test_data():
    """Generate all logistics test case data"""
    print("\n🚚 Generating LOGISTICS test data...")
    print("  ⚠️  TC037-TC042 placeholders (to be implemented)")


def main():
    parser = argparse.ArgumentParser(description='Generate Test Case Data')
    parser.add_argument('--industry', choices=['retail', 'finance', 'healthcare', 'manufacturing', 
                                               'education', 'saas', 'logistics'],
                      help='Generate data for specific industry only')
    parser.add_argument('--test', help='Generate data for specific test case (e.g., TC001)')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("🎨 ELAS ERP - TEST CASE DATA GENERATOR")
    print("="*70)
    
    if args.test:
        test_id = args.test.upper()
        print(f"\n📊 Generating data for {test_id}...")
        
        if test_id == 'TC001':
            generate_TC001_retail_small_daily_sales()
        elif test_id == 'TC002':
            generate_TC002_retail_small_inventory()
        else:
            print(f"  ⚠️  {test_id} not yet implemented")
    
    elif args.industry:
        if args.industry == 'retail':
            generate_retail_test_data()
        elif args.industry == 'finance':
            generate_finance_test_data()
        elif args.industry == 'healthcare':
            generate_healthcare_test_data()
        elif args.industry == 'manufacturing':
            generate_manufacturing_test_data()
        elif args.industry == 'education':
            generate_education_test_data()
        elif args.industry == 'saas':
            generate_saas_test_data()
        elif args.industry == 'logistics':
            generate_logistics_test_data()
    
    else:
        # Generate all
        generate_retail_test_data()
        generate_finance_test_data()
        generate_healthcare_test_data()
        generate_manufacturing_test_data()
        generate_education_test_data()
        generate_saas_test_data()
        generate_logistics_test_data()
    
    print("\n" + "="*70)
    print("✅ DATA GENERATION COMPLETE!")
    print("="*70)
    print(f"\n📁 Output directory: {OUTPUT_DIR}")
    print("\n💡 Next steps:")
    print("   1. Review generated files in sample_data/")
    print("   2. Run test cases manually or use run_test_cases.py")
    print("   3. Validate widget generation results\n")


if __name__ == '__main__':
    main()
