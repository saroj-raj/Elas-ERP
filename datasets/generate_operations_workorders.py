"""
Generate realistic operations work orders dataset with technicians and shifts.
"""
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# Set random seed
random.seed(44)

# Output directory
OUTPUT_DIR = Path(__file__).parent / "operations_workorders"
OUTPUT_DIR.mkdir(exist_ok=True)

# Helper functions
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def random_datetime(start_date, end_date):
    date = random_date(start_date, end_date)
    hour = random.randint(7, 18)  # Business hours
    minute = random.choice([0, 15, 30, 45])
    return date.replace(hour=hour, minute=minute, second=0)

def add_nulls(series, null_pct=0.05):
    mask = [random.random() < null_pct for _ in range(len(series))]
    return series.mask(mask, None)

# Generate Technicians (40 rows)
print("Generating technicians.csv...")
first_names = ["Alex", "Sam", "Jordan", "Taylor", "Morgan", "Casey", "Jamie", "Riley", "Avery", "Quinn",
               "Chris", "Pat", "Drew", "Skyler", "Dakota", "Rowan", "Sage", "River", "Phoenix", "Denver"]
last_names = ["Anderson", "Brown", "Clark", "Davis", "Evans", "Foster", "Green", "Harris", "Jackson", "King",
              "Lopez", "Miller", "Nelson", "O'Brien", "Parker", "Quinn", "Roberts", "Smith", "Taylor", "Williams"]

skills = ["HVAC", "Electrical", "Plumbing", "General Maintenance", "Carpentry", "Welding", "Equipment Repair", "Painting"]
regions = ["North", "South", "East", "West"]
certifications = ["EPA 608", "OSHA 30", "Master Electrician", "Journeyman", "Forklift", "Confined Space", "First Aid/CPR"]

technicians = []
for i in range(40):
    hire_date = random_date(datetime(2018, 1, 1), datetime(2024, 6, 1))
    primary_skill = random.choice(skills)
    secondary_skills = random.sample([s for s in skills if s != primary_skill], k=random.randint(1, 3))
    tech_certs = random.sample(certifications, k=random.randint(1, 4))
    
    technicians.append({
        "tech_id": f"T{2001 + i}",
        "tech_name": f"{random.choice(first_names)} {random.choice(last_names)}",
        "email": f"tech{i+1}@elas-erp.com",
        "phone": f"+1-555-{random.randint(1000, 9999)}",
        "region": random.choice(regions),
        "primary_skill": primary_skill,
        "secondary_skills": ", ".join(secondary_skills),
        "certifications": ", ".join(tech_certs),
        "hire_date": hire_date.strftime("%Y-%m-%d"),
        "hourly_rate": round(random.uniform(25, 65), 2),
        "status": random.choices(["Active", "On Leave", "Active"], weights=[85, 5, 10])[0]
    })

technicians_df = pd.DataFrame(technicians)
technicians_df.to_csv(OUTPUT_DIR / "technicians.csv", index=False)

# Get active technicians for work order assignment
active_techs = technicians_df[technicians_df["status"] == "Active"]["tech_id"].tolist()

# Generate Work Orders (500 rows)
print("Generating work_orders.csv...")
statuses = ["new", "assigned", "in_progress", "blocked", "done"]
priorities = ["Low", "Medium", "High", "Critical"]
wo_types = ["Preventive Maintenance", "Repair", "Installation", "Inspection", "Emergency", "Project Work"]
facilities = ["Building A", "Building B", "Building C", "Warehouse 1", "Warehouse 2", "Production Floor", "Office Wing"]

work_orders = []
for i in range(500):
    open_date = random_datetime(datetime(2024, 1, 1), datetime(2025, 10, 25))
    status = random.choices(statuses, weights=[5, 10, 20, 5, 60])[0]
    
    # Close date logic
    if status == "done":
        # Completed work orders
        hours_to_complete = random.uniform(2, 120)  # 2 hours to 5 days
        close_date = open_date + timedelta(hours=hours_to_complete)
        if close_date > datetime(2025, 10, 29):
            close_date = None
            status = "in_progress"
    else:
        close_date = None
    
    # Assignment logic
    if status in ["assigned", "in_progress", "done"]:
        assigned_to = random.choice(active_techs)
    elif status == "blocked":
        assigned_to = random.choice(active_techs) if random.random() < 0.7 else None
    else:  # new
        assigned_to = None
    
    priority = random.choices(priorities, weights=[30, 40, 20, 10])[0]
    wo_type = random.choice(wo_types)
    
    # Emergency work orders are high priority
    if wo_type == "Emergency":
        priority = "Critical"
    
    estimated_hours = round(random.uniform(1, 40), 1)
    actual_hours = None
    if close_date:
        actual_hours = round((close_date - open_date).total_seconds() / 3600, 1)
        # Add some variation
        actual_hours = round(actual_hours * random.uniform(0.8, 1.3), 1)
    
    work_orders.append({
        "wo_id": f"WO-{30000 + i}",
        "open_date": open_date.strftime("%Y-%m-%d %H:%M:%S"),
        "close_date": close_date.strftime("%Y-%m-%d %H:%M:%S") if close_date else None,
        "account_id": f"A{random.randint(1000, 1060)}",
        "facility": random.choice(facilities),
        "location": f"Room {random.randint(100, 599)}",
        "title": f"{wo_type} - {random.choice(['HVAC Unit', 'Electrical Panel', 'Plumbing Fixture', 'Equipment', 'Door', 'Window', 'Roof', 'Flooring'])} {random.randint(1, 50)}",
        "description": random.choice([
            "Unit not functioning properly",
            "Routine maintenance required",
            "Customer reported issue",
            "Safety inspection needed",
            "Equipment malfunction",
            "Scheduled preventive maintenance",
            "Emergency repair needed"
        ]),
        "status": status,
        "priority": priority,
        "wo_type": wo_type,
        "assigned_to": assigned_to,
        "region": random.choice(regions),
        "estimated_hours": estimated_hours,
        "actual_hours": actual_hours,
        "parts_cost": round(random.uniform(0, 2000), 2) if close_date else None,
        "labor_cost": round(actual_hours * random.uniform(40, 70), 2) if actual_hours else None
    })

work_orders_df = pd.DataFrame(work_orders)

# Add nulls
work_orders_df["location"] = add_nulls(work_orders_df["location"], 0.05)
work_orders_df["description"] = add_nulls(work_orders_df["description"], 0.03)

work_orders_df.to_csv(OUTPUT_DIR / "work_orders.csv", index=False)

# Generate Shifts (180 rows) - XLSX format
print("Generating shifts.xlsx...")
shift_types = ["Day Shift", "Evening Shift", "Night Shift", "Weekend"]
shift_times = {
    "Day Shift": ("07:00", "15:00"),
    "Evening Shift": ("15:00", "23:00"),
    "Night Shift": ("23:00", "07:00"),
    "Weekend": ("08:00", "16:00")
}

# Generate 30 days of shifts
shifts = []
start_date = datetime(2025, 10, 1)
for day_offset in range(30):
    current_date = start_date + timedelta(days=day_offset)
    day_of_week = current_date.strftime("%A")
    
    # Determine available shift types
    if day_of_week in ["Saturday", "Sunday"]:
        available_shifts = ["Weekend"]
    else:
        available_shifts = ["Day Shift", "Evening Shift", "Night Shift"]
    
    # Create shifts for this day
    for shift_type in available_shifts:
        # Assign 2-4 technicians per shift
        n_techs = random.randint(2, 4)
        assigned_techs = random.sample(active_techs, min(n_techs, len(active_techs)))
        
        for tech_id in assigned_techs:
            tech = technicians_df[technicians_df["tech_id"] == tech_id].iloc[0]
            start_time, end_time = shift_times[shift_type]
            
            shifts.append({
                "shift_id": f"SH-{40000 + len(shifts)}",
                "date": current_date.strftime("%Y-%m-%d"),
                "day_of_week": day_of_week,
                "shift_type": shift_type,
                "start_time": start_time,
                "end_time": end_time,
                "tech_id": tech_id,
                "tech_name": tech["tech_name"],
                "region": tech["region"],
                "primary_skill": tech["primary_skill"],
                "hourly_rate": tech["hourly_rate"],
                "hours": 8.0 if shift_type != "Night Shift" else 8.0,
                "overtime_hours": random.choice([0, 0, 0, 1, 2]) if random.random() < 0.15 else 0
            })

shifts_df = pd.DataFrame(shifts)
shifts_df.to_excel(OUTPUT_DIR / "shifts.xlsx", index=False, engine='openpyxl')

# Generate README
print("Generating readme.md...")
readme_content = """# Operations Work Orders Dataset

## Overview
Realistic work order management data with technicians and shift scheduling.

## Files

### work_orders.csv (500 rows)
Work order tracking data:
- **wo_id**: Unique work order identifier (WO-xxxxx)
- **open_date**: Date/time work order opened (2024-2025)
- **close_date**: Date/time work order closed (null if open)
- **account_id**: Customer/facility account ID
- **facility**: Facility name (7 facilities)
- **location**: Specific location (~5% nulls)
- **title**: Work order title/summary
- **description**: Detailed description (~3% nulls)
- **status**: new | assigned | in_progress | blocked | done
- **priority**: Low | Medium | High | Critical
- **wo_type**: Preventive Maintenance | Repair | Installation | Inspection | Emergency | Project Work
- **assigned_to**: Technician ID (null if not assigned)
- **region**: Geographic region
- **estimated_hours**: Estimated time to complete
- **actual_hours**: Actual time taken (null if not done)
- **parts_cost**: Cost of parts/materials (null if not done)
- **labor_cost**: Labor cost calculation (null if not done)

### technicians.csv (40 rows)
Technician master data:
- **tech_id**: Technician identifier
- **tech_name**: Full name
- **email**: Email address
- **phone**: Phone number
- **region**: Assigned region
- **primary_skill**: Main skill area (8 skill types)
- **secondary_skills**: Additional skills (1-3)
- **certifications**: Professional certifications (1-4)
- **hire_date**: Date hired (2018-2024)
- **hourly_rate**: Hourly billing rate ($25-65)
- **status**: Active | On Leave

### shifts.xlsx (180 rows)
Shift schedule data (30 days):
- **shift_id**: Unique shift identifier
- **date**: Shift date (Oct 2025)
- **day_of_week**: Day name
- **shift_type**: Day Shift | Evening Shift | Night Shift | Weekend
- **start_time**: Shift start time
- **end_time**: Shift end time
- **tech_id**: Assigned technician
- **tech_name**: Technician name
- **region**: Region
- **primary_skill**: Technician's primary skill
- **hourly_rate**: Technician's hourly rate
- **hours**: Regular hours (8.0)
- **overtime_hours**: Overtime hours (0-2, ~15% have OT)

## Data Quality Notes
- **Status Distribution**: 60% done, 20% in_progress, 10% assigned, 5% blocked, 5% new
- **Completion Time**: Ranges from 2 hours to 5 days
- **Priority Mix**: 30% Low, 40% Medium, 20% High, 10% Critical
- **Emergency Orders**: Automatically set to Critical priority
- **Active Technicians**: ~85% active, 5% on leave
- **Shifts**: 2-4 technicians per shift, weekday vs weekend coverage
- **Overtime**: ~15% of shifts include 1-2 hours overtime
- **Nulls**: ~5% in location, ~3% in description

## Status Workflow
1. **new** → Work order created, awaiting assignment
2. **assigned** → Technician assigned, not yet started
3. **in_progress** → Work actively being performed
4. **blocked** → Work stopped due to parts/approval/issues
5. **done** → Work completed

## Intended Visualizations
1. **Open vs Closed Trends**: Work order volume over time
2. **Status Pipeline**: Funnel showing WO progression
3. **Completion Rate**: % completed within estimated time
4. **Priority Distribution**: Work orders by priority level
5. **Technician Utilization**: Hours worked vs capacity
6. **Regional Workload**: Work orders by region
7. **Mean Time to Completion**: Average days to close by type
8. **Backlog Analysis**: Open work orders aging
9. **Cost Analysis**: Parts vs labor cost breakdown
10. **Skill Demand**: Work orders by required skill type
11. **Shift Coverage**: Technician availability by shift/region
12. **Overtime Tracking**: OT hours by technician
13. **SLA Compliance**: % completed within priority SLA

## Join Keys
- `tech_id` → technicians.csv
- `account_id` → (could join to facility master)
- `tech_id` in work_orders → assigned_to field

## Calculations
- **Utilization %** = (Actual Hours Worked / Available Hours) × 100
- **Completion Variance** = Actual Hours - Estimated Hours
- **Labor Cost** = Actual Hours × Hourly Rate
- **Total Cost** = Parts Cost + Labor Cost
- **Days to Complete** = Close Date - Open Date
"""

with open(OUTPUT_DIR / "readme.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print(f"✅ Operations work orders dataset generated in {OUTPUT_DIR}")
print(f"   - work_orders.csv: {len(work_orders_df)} rows")
print(f"   - technicians.csv: {len(technicians_df)} rows")
print(f"   - shifts.xlsx: {len(shifts_df)} rows")
