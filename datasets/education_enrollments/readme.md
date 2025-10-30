# Education Enrollments Dataset

## Overview
Realistic student enrollment data with courses, instructors, and financial information.

## Files

### enrollments.csv (~2,400 rows)
Student course enrollment records (2 academic terms):
- **enrollment_id**: Unique enrollment identifier
- **student_id**: Student identifier
- **student_name**: Student full name
- **course_id**: Course identifier
- **course_code**: Course code (e.g., CS101)
- **course_name**: Course title
- **program**: Degree program (7 programs)
- **cohort**: Student cohort year (2021-2025)
- **term**: Academic term (Fall 2024 | Spring 2025)
- **credits**: Course credit hours (1-4)
- **tuition**: Full tuition amount for course
- **financial_aid**: Aid amount received (~5% nulls, 60% receive aid)
- **net_tuition**: Tuition after aid (tuition - financial_aid)
- **payment_status**: Paid | Pending | Overdue | Refunded
- **enrollment_date**: Date student enrolled
- **status**: Enrolled | Completed | Withdrawn | On Leave
- **grade**: A to F, W (withdrawn), IP (in progress)
- **instructor_id**: Teaching instructor
- **instructor_name**: Instructor name
- **department**: Academic department

### instructors.csv (35 rows)
Faculty instructor data:
- **instructor_id**: Instructor identifier
- **instructor_name**: Full name with title (Dr./Prof.)
- **email**: University email
- **department**: Academic department (8 departments)
- **title**: Academic rank (Professor, Associate, Assistant, Lecturer, Adjunct)
- **hire_date**: Date hired (2015-2023)
- **office**: Office location
- **phone_ext**: Phone extension
- **max_courses_per_term**: Teaching load limit (2-4)

### courses.xlsx (~70 rows)
Course catalog for Fall 2024 and Spring 2025:
- **course_id**: Course identifier
- **course_code**: Department prefix + number
- **course_name**: Course title
- **department**: Academic department
- **credits**: Credit hours (1-4)
- **term**: Fall 2024 | Spring 2025
- **course_type**: Lecture | Lab | Seminar | Online | Hybrid
- **instructor_id**: Assigned instructor
- **instructor_name**: Instructor name
- **capacity**: Maximum enrollment
- **enrolled**: Current enrollment (50-110% of capacity)
- **waitlist**: Number on waitlist (if over capacity)
- **meeting_days**: MWF | TR | MW | W | Online
- **start_time**: Class start time
- **room**: Classroom location

## Data Quality Notes
- **Academic Years**: Fall 2024 and Spring 2025 terms
- **Students**: ~800 unique students
- **Enrollments per Student**: 3-6 courses per term
- **Course Capacity**: Some courses over-enrolled (110% capacity)
- **Completion Rate**: ~80% for Fall 2024, ~5% for Spring 2025 (still in progress)
- **Financial Aid**: 60% of students receive aid (10-80% coverage)
- **Payment Issues**: ~5% overdue payments
- **Withdrawal Rate**: ~8% withdrawal rate
- **Grades**: Realistic distribution from A to F
- **Nulls**: ~5% in financial_aid

## Status Definitions
- **Enrolled**: Currently taking course
- **Completed**: Course finished with grade
- **Withdrawn**: Student dropped course
- **On Leave**: Temporarily not attending

## Intended Visualizations
1. **Enrollment Trends**: Students per term over time
2. **Department Capacity**: Enrollment vs capacity by department
3. **Grade Distribution**: Histogram of grades by course/department
4. **Financial Aid Impact**: Aid amount vs net tuition
5. **Program Popularity**: Enrollments by degree program
6. **Instructor Load**: Courses taught per instructor
7. **Payment Status**: Outstanding tuition by status
8. **Completion Rate**: % of courses completed vs enrolled
9. **Waitlist Analysis**: Courses with highest demand
10. **Cohort Performance**: Average grades by cohort year
11. **Revenue Analysis**: Total tuition by program/term
12. **Retention**: Withdrawal rates by program/course level

## Join Keys
- `course_id` → courses.xlsx
- `instructor_id` → instructors.csv
- `student_id` → (group enrollments by student)

## Calculations
- **Net Tuition** = Tuition - Financial Aid
- **Course Fill Rate** = (Enrolled / Capacity) × 100
- **Completion Rate** = (Completed / Total Enrollments) × 100
- **Total Revenue** = SUM(Net Tuition)
- **Average GPA** = Calculate from letter grades (A=4.0, A-=3.7, etc.)
