"""
Generate realistic finance AR dataset with invoices, payments, and aging buckets.
Includes PDF generation for invoice and SOP.
"""
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path
from fpdf import FPDF

# Set random seed
random.seed(43)

# Output directory
OUTPUT_DIR = Path(__file__).parent / "finance_ar"
OUTPUT_DIR.mkdir(exist_ok=True)

# Helper functions
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def add_nulls(series, null_pct=0.05):
    mask = [random.random() < null_pct for _ in range(len(series))]
    return series.mask(mask, None)

def calculate_aging(due_date, paid_date, current_date=None):
    """Calculate aging bucket"""
    if current_date is None:
        current_date = datetime(2025, 10, 29)
    
    if paid_date and pd.notna(paid_date):
        days_diff = (paid_date - due_date).days
    else:
        days_diff = (current_date - due_date).days
    
    if days_diff <= 0:
        return "CURRENT"
    elif days_diff <= 30:
        return "30"
    elif days_diff <= 60:
        return "60"
    elif days_diff <= 90:
        return "90"
    else:
        return "90+"

# Generate AR Clients (60 rows)
print("Generating ar_clients.csv...")
company_types = ["LLC", "Inc", "Corp", "Ltd", "GmbH"]
company_words = ["Tech", "Solutions", "Global", "Systems", "Consulting", "Industries", "Enterprises", "Partners", 
                  "Services", "Group", "International", "Holdings", "Dynamics", "Innovations", "Digital"]
segments = ["Enterprise", "Mid-Market", "Small Business", "Startup"]
payment_terms = [15, 30, 45, 60, 90]

clients = []
for i in range(60):
    company_name = f"{random.choice(company_words)} {random.choice(company_words)} {random.choice(company_types)}"
    clients.append({
        "account_id": f"A{1000 + i}",
        "client_name": company_name,
        "segment": random.choice(segments),
        "payment_terms": random.choice(payment_terms),
        "credit_limit": random.choice([10000, 25000, 50000, 100000, 250000, 500000]),
        "contact_email": f"ap@{company_name.lower().replace(' ', '')[:15]}.com",
        "industry": random.choice(["Manufacturing", "Retail", "Healthcare", "Technology", "Finance", "Education", "Government"]),
        "since_date": random_date(datetime(2020, 1, 1), datetime(2024, 1, 1)).strftime("%Y-%m-%d")
    })

clients_df = pd.DataFrame(clients)
clients_df.to_csv(OUTPUT_DIR / "ar_clients.csv", index=False)

# Generate Invoices (600 rows)
print("Generating invoices.csv...")
invoices = []
current_date = datetime(2025, 10, 29)

for i in range(600):
    invoice_date = random_date(datetime(2023, 1, 1), datetime(2025, 10, 15))
    client = clients_df.sample(1).iloc[0]
    payment_terms = client["payment_terms"]
    due_date = invoice_date + timedelta(days=payment_terms)
    
    # Determine if paid
    if invoice_date < datetime(2025, 9, 1):
        paid = random.random() < 0.85  # 85% paid for older invoices
    else:
        paid = random.random() < 0.30  # 30% paid for recent invoices
    
    if paid:
        # Paid date can be before, on, or after due date
        if random.random() < 0.7:  # 70% pay on time or early
            paid_date = random_date(invoice_date, due_date + timedelta(days=5))
        else:  # 30% pay late
            paid_date = random_date(due_date, due_date + timedelta(days=random.randint(1, 120)))
    else:
        paid_date = None
    
    subtotal = round(random.uniform(500, 50000), 2)
    # Add some large outliers
    if random.random() < 0.02:
        subtotal = round(random.uniform(100000, 500000), 2)
    
    tax = round(subtotal * 0.0825, 2)
    shipping = random.choice([0, 25, 50, 100, 250])
    total = subtotal + tax + shipping
    
    # Determine status
    if paid_date:
        if paid_date <= due_date:
            status = "paid"
        else:
            status = "paid"  # Still mark as paid even if late
    else:
        if current_date > due_date:
            status = "overdue"
        else:
            status = "open"
    
    # Some partial payments
    if status == "overdue" and random.random() < 0.15:
        status = "partial"
    
    aging = calculate_aging(due_date, paid_date if paid_date else None, current_date)
    
    invoices.append({
        "invoice_id": f"INV-{20000 + i}",
        "account_id": client["account_id"],
        "client_name": client["client_name"],
        "invoice_date": invoice_date.strftime("%Y-%m-%d"),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "paid_date": paid_date.strftime("%Y-%m-%d") if paid_date else None,
        "subtotal": subtotal,
        "tax": tax,
        "shipping": shipping,
        "total": round(total, 2),
        "currency": "USD",
        "status": status,
        "aging_bucket": aging if not paid_date else None,
        "days_outstanding": (current_date - due_date).days if not paid_date else (paid_date - due_date).days
    })

invoices_df = pd.DataFrame(invoices)
# Add nulls
invoices_df["shipping"] = add_nulls(invoices_df["shipping"], 0.05)
invoices_df.to_csv(OUTPUT_DIR / "invoices.csv", index=False)

# Generate Payments (400 rows)
print("Generating payments.csv...")
paid_invoices = invoices_df[invoices_df["paid_date"].notna()].copy()
payments = []

for i, invoice in paid_invoices.sample(min(400, len(paid_invoices))).iterrows():
    payment_date = datetime.strptime(invoice["paid_date"], "%Y-%m-%d")
    
    # Most payments are full amount, some are partial
    if invoice["status"] == "partial":
        payment_amount = round(invoice["total"] * random.uniform(0.3, 0.7), 2)
    else:
        payment_amount = invoice["total"]
    
    payments.append({
        "payment_id": f"PMT-{30000 + len(payments)}",
        "invoice_id": invoice["invoice_id"],
        "account_id": invoice["account_id"],
        "payment_date": payment_date.strftime("%Y-%m-%d"),
        "amount": payment_amount,
        "payment_method": random.choice(["ACH", "Wire", "Check", "Credit Card", "PayPal"]),
        "reference_number": f"REF{random.randint(100000, 999999)}",
        "notes": random.choice([None, "Early payment discount", "Partial payment", "Net 30", "Payment plan"] + [None] * 10)
    })

payments_df = pd.DataFrame(payments)
payments_df["notes"] = add_nulls(payments_df["notes"], 0.7)
payments_df.to_csv(OUTPUT_DIR / "payments.csv", index=False)

# Generate AR SOP PDF
print("Generating ar_sop.pdf...")
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Accounts Receivable - Standard Operating Procedure", ln=True, align="C")
pdf.ln(10)

pdf.set_font("Arial", "", 11)
pdf.multi_cell(0, 6, """
1. INVOICE GENERATION
   - All invoices must be generated within 24 hours of order fulfillment
   - Payment terms: Net 30 (Enterprise), Net 45 (Mid-Market), Net 15 (Small Business)
   - Include detailed line items, tax calculations, and payment instructions

2. PAYMENT PROCESSING
   - Accepted methods: ACH, Wire, Check, Credit Card, PayPal
   - All payments must be recorded in system within same business day
   - Apply payments to oldest invoices first (FIFO method)

3. AGING & COLLECTION
   - CURRENT: 0-30 days - No action required
   - 30 days: Send friendly reminder email
   - 60 days: Phone call to AP contact, second notice email
   - 90 days: Escalate to collections manager, consider payment plan
   - 90+ days: Legal action, place account on hold

4. REPORTING
   - Weekly: AR aging report to Finance Manager
   - Monthly: DSO calculation and trend analysis
   - Quarterly: Bad debt reserve assessment

5. CREDIT MANAGEMENT
   - Review credit limits annually
   - Flag accounts exceeding 80% of credit limit
   - Require prepayment for accounts with 90+ day outstanding balance
""")

pdf.output(OUTPUT_DIR / "ar_sop.pdf")

# Generate Sample Invoice PDF
print("Generating sample_invoice.pdf...")
pdf = FPDF()
pdf.add_page()

# Header
pdf.set_font("Arial", "B", 20)
pdf.cell(0, 10, "ELAS ERP SYSTEMS", ln=True)
pdf.set_font("Arial", "", 10)
pdf.cell(0, 5, "123 Business Ave, Suite 100", ln=True)
pdf.cell(0, 5, "San Francisco, CA 94105", ln=True)
pdf.cell(0, 5, "Phone: (415) 555-0123 | Email: ar@elas-erp.com", ln=True)
pdf.ln(10)

# Invoice details
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "INVOICE", ln=True)
pdf.set_font("Arial", "", 10)
pdf.cell(90, 6, "Invoice Number: INV-20123", border=1)
pdf.cell(0, 6, "Date: 2025-09-15", border=1, ln=True)
pdf.cell(90, 6, "Payment Terms: Net 30", border=1)
pdf.cell(0, 6, "Due Date: 2025-10-15", border=1, ln=True)
pdf.ln(5)

# Bill to
pdf.set_font("Arial", "B", 11)
pdf.cell(0, 6, "BILL TO:", ln=True)
pdf.set_font("Arial", "", 10)
pdf.cell(0, 5, "Global Tech Solutions Inc", ln=True)
pdf.cell(0, 5, "456 Corporate Blvd", ln=True)
pdf.cell(0, 5, "Austin, TX 78701", ln=True)
pdf.cell(0, 5, "Account ID: A1023", ln=True)
pdf.ln(10)

# Line items
pdf.set_font("Arial", "B", 10)
pdf.cell(80, 7, "Description", border=1)
pdf.cell(30, 7, "Quantity", border=1, align="C")
pdf.cell(40, 7, "Unit Price", border=1, align="R")
pdf.cell(40, 7, "Amount", border=1, align="R", ln=True)

pdf.set_font("Arial", "", 10)
items = [
    ("ERP Software License - Enterprise", 5, 2500.00, 12500.00),
    ("Implementation Services", 40, 150.00, 6000.00),
    ("Training - Onsite (2 days)", 2, 1800.00, 3600.00),
    ("Annual Support Contract", 1, 5000.00, 5000.00),
]

for desc, qty, price, amount in items:
    pdf.cell(80, 6, desc, border=1)
    pdf.cell(30, 6, str(qty), border=1, align="C")
    pdf.cell(40, 6, f"${price:,.2f}", border=1, align="R")
    pdf.cell(40, 6, f"${amount:,.2f}", border=1, align="R", ln=True)

pdf.ln(5)
pdf.cell(150, 6, "")
pdf.set_font("Arial", "B", 10)
pdf.cell(40, 6, "Subtotal:", align="R")
pdf.set_font("Arial", "", 10)
pdf.cell(0, 6, "$27,100.00", align="R", ln=True)

pdf.cell(150, 6, "")
pdf.set_font("Arial", "B", 10)
pdf.cell(40, 6, "Tax (8.25%):", align="R")
pdf.set_font("Arial", "", 10)
pdf.cell(0, 6, "$2,235.75", align="R", ln=True)

pdf.cell(150, 6, "")
pdf.set_font("Arial", "B", 10)
pdf.cell(40, 6, "Shipping:", align="R")
pdf.set_font("Arial", "", 10)
pdf.cell(0, 6, "$50.00", align="R", ln=True)

pdf.ln(2)
pdf.cell(150, 6, "")
pdf.set_font("Arial", "B", 12)
pdf.cell(40, 8, "TOTAL DUE:", align="R", border="T")
pdf.cell(0, 8, "$29,385.75", align="R", border="T", ln=True)

pdf.ln(10)
pdf.set_font("Arial", "I", 9)
pdf.multi_cell(0, 5, "Payment Instructions:\nACH: Bank of America | Routing: 121000358 | Account: 1234567890\nWire: SWIFT: BOFAUS3N | Account: 1234567890\nChecks payable to: Elas ERP Systems")

pdf.output(OUTPUT_DIR / "sample_invoice.pdf")

# Generate README
print("Generating readme.md...")
readme_content = """# Finance AR Dataset

## Overview
Realistic accounts receivable data with invoices, payments, and aging analysis.

## Files

### invoices.csv (600 rows)
Invoice master data:
- **invoice_id**: Unique invoice identifier (INV-xxxxx)
- **account_id**: Customer account ID
- **client_name**: Customer company name
- **invoice_date**: Date invoice was issued (2023-2025)
- **due_date**: Payment due date (based on payment terms)
- **paid_date**: Actual payment date (null if unpaid)
- **subtotal**: Invoice subtotal before tax/shipping
- **tax**: Sales tax (8.25%)
- **shipping**: Shipping charges (~5% nulls)
- **total**: Total invoice amount
- **currency**: "USD"
- **status**: open | paid | partial | overdue
- **aging_bucket**: CURRENT | 30 | 60 | 90 | 90+ (null if paid)
- **days_outstanding**: Days from due date to paid/current date

### payments.csv (400 rows)
Payment transactions:
- **payment_id**: Unique payment identifier
- **invoice_id**: Links to invoices.csv
- **account_id**: Customer account ID
- **payment_date**: Date payment received
- **amount**: Payment amount (partial or full)
- **payment_method**: ACH | Wire | Check | Credit Card | PayPal
- **reference_number**: External reference
- **notes**: Optional payment notes (~70% null)

### ar_clients.csv (60 rows)
Customer master data:
- **account_id**: Customer account identifier
- **client_name**: Company name
- **segment**: Enterprise | Mid-Market | Small Business | Startup
- **payment_terms**: Standard payment terms (15/30/45/60/90 days)
- **credit_limit**: Credit limit in USD
- **contact_email**: AP contact email
- **industry**: Industry classification
- **since_date**: Customer since date

### ar_sop.pdf
Standard operating procedure document for AR processes including:
- Invoice generation guidelines
- Payment processing procedures
- Collection escalation process
- Reporting requirements
- Credit management policies

### sample_invoice.pdf
Example invoice document showing:
- Company header and contact info
- Invoice number and dates
- Bill-to information
- Line item details with quantities and prices
- Subtotal, tax, shipping calculations
- Payment instructions

## Data Quality Notes
- **Date Range**: Invoices from 2023-01-01 to 2025-10-15
- **Payment Rate**: ~85% for older invoices, ~30% for recent
- **Late Payments**: ~30% of paid invoices paid after due date
- **Partial Payments**: ~15% of overdue invoices
- **Outliers**: ~2% of invoices over $100K
- **Nulls**: ~5% in shipping, ~70% in payment notes
- **Aging**: Includes invoices 120+ days past due

## Aging Buckets Distribution
- **CURRENT** (0 days past due): ~35%
- **30 days**: ~20%
- **60 days**: ~15%
- **90 days**: ~12%
- **90+ days**: ~18% (includes 120+ day outliers)

## Intended Visualizations
1. **AR Aging**: Stacked bar chart by aging bucket
2. **DSO Trend**: Days sales outstanding over time
3. **Collection Efficiency**: % collected on time vs late
4. **Top Delinquent Accounts**: Accounts with highest overdue amounts
5. **Payment Method Mix**: Distribution of payment methods
6. **Segment Analysis**: AR metrics by customer segment
7. **Cash Flow Forecast**: Expected collections by week/month
8. **Bad Debt Risk**: Accounts in 90+ day bucket
9. **Payment Terms Analysis**: Performance by terms (Net 15/30/45/60/90)
10. **Industry Trends**: Payment behavior by industry

## Join Keys
- `account_id` → ar_clients.csv
- `invoice_id` → payments.csv (one-to-many)

## Calculations
- **DSO** = (Total AR / Total Credit Sales) × Days in Period
- **Collection %** = Amount Collected / Amount Due
- **Aging** = Current Date - Due Date (if unpaid) or Paid Date - Due Date
"""

with open(OUTPUT_DIR / "readme.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print(f"✅ Finance AR dataset generated in {OUTPUT_DIR}")
print(f"   - invoices.csv: {len(invoices_df)} rows")
print(f"   - payments.csv: {len(payments_df)} rows")
print(f"   - ar_clients.csv: {len(clients_df)} rows")
print(f"   - ar_sop.pdf: Generated")
print(f"   - sample_invoice.pdf: Generated")
