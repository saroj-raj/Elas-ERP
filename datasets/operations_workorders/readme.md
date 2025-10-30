# Operations Work Orders Dataset

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
