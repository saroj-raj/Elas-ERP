"""
Generate realistic education enrollments dataset with students, instructors, and courses.
"""
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# Set random seed
random.seed(45)

# Output directory
OUTPUT_DIR = Path(__file__).parent / "education_enrollments"
OUTPUT_DIR.mkdir(exist_ok=True)

# Helper functions
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def add_nulls(series, null_pct=0.05):
    mask = [random.random() < null_pct for _ in range(len(series))]
    return series.mask(mask, None)

# Generate Instructors (35 rows)
print("Generating instructors.csv...")
first_names = ["Dr. Sarah", "Prof. Michael", "Dr. Emily", "Prof. David", "Dr. Jennifer", "Prof. James", 
               "Dr. María", "Prof. Robert", "Dr. Lisa", "Prof. William", "Dr. Jessica", "Prof. José",
               "Dr. Karen", "Prof. Thomas", "Dr. Patricia"]
last_names = ["Anderson", "Brown", "Chen", "Davis", "García", "Johnson", "Kim", "Lee", "Martinez", 
              "Miller", "Nguyen", "Patel", "Rodriguez", "Smith", "Taylor", "Williams", "Wilson", "Young"]

departments = ["Computer Science", "Business Administration", "Engineering", "Liberal Arts", 
               "Mathematics", "Data Science", "Healthcare", "Education"]
titles = ["Associate Professor", "Professor", "Assistant Professor", "Lecturer", "Adjunct Professor"]

instructors = []
for i in range(35):
    hire_date = random_date(datetime(2015, 1, 1), datetime(2023, 8, 1))
    department = random.choice(departments)
    
    instructors.append({
        "instructor_id": f"INS{5001 + i}",
        "instructor_name": f"{random.choice(first_names)} {random.choice(last_names)}",
        "email": f"instructor{i+1}@university.edu",
        "department": department,
        "title": random.choice(titles),
        "hire_date": hire_date.strftime("%Y-%m-%d"),
        "office": f"Building {random.choice(['A', 'B', 'C', 'D'])}-{random.randint(100, 599)}",
        "phone_ext": f"x{random.randint(1000, 9999)}",
        "max_courses_per_term": random.choice([2, 3, 4])
    })

instructors_df = pd.DataFrame(instructors)
instructors_df.to_csv(OUTPUT_DIR / "instructors.csv", index=False)

# Generate Courses (XLSX format)
print("Generating courses.xlsx...")
course_prefixes = {
    "Computer Science": ["CS", "CSE"],
    "Business Administration": ["BUS", "MGT", "FIN"],
    "Engineering": ["ENG", "ME", "EE"],
    "Liberal Arts": ["ENG", "HIS", "SOC"],
    "Mathematics": ["MATH", "STAT"],
    "Data Science": ["DS", "DSCI"],
    "Healthcare": ["NUR", "HCA"],
    "Education": ["EDU", "EDUC"]
}

course_types = ["Lecture", "Lab", "Seminar", "Online", "Hybrid"]
terms = ["Fall 2024", "Spring 2025"]

courses = []
course_id = 6000
for department in departments:
    prefixes = course_prefixes[department]
    # Generate 3-5 courses per department per term
    for term in terms:
        n_courses = random.randint(3, 5)
        for _ in range(n_courses):
            prefix = random.choice(prefixes)
            course_num = random.randint(100, 599)
            
            # Get instructor from same department if possible
            dept_instructors = instructors_df[instructors_df["department"] == department]
            if len(dept_instructors) > 0:
                instructor = dept_instructors.sample(1).iloc[0]
            else:
                instructor = instructors_df.sample(1).iloc[0]
            
            credits = random.choice([1, 2, 3, 4])
            capacity = random.choice([20, 25, 30, 35, 40, 50])
            enrolled = random.randint(int(capacity * 0.5), min(capacity, int(capacity * 1.1)))  # 50-110% capacity
            
            courses.append({
                "course_id": f"C{course_id}",
                "course_code": f"{prefix}{course_num}",
                "course_name": f"{department} - Level {course_num // 100}",
                "department": department,
                "credits": credits,
                "term": term,
                "course_type": random.choice(course_types),
                "instructor_id": instructor["instructor_id"],
                "instructor_name": instructor["instructor_name"],
                "capacity": capacity,
                "enrolled": enrolled,
                "waitlist": max(0, enrolled - capacity) if enrolled > capacity else 0,
                "meeting_days": random.choice(["MWF", "TR", "MW", "W", "Online"]),
                "start_time": random.choice(["08:00", "09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"]),
                "room": f"{random.choice(['Hall', 'Science', 'Business', 'Arts'])} {random.randint(100, 599)}"
            })
            course_id += 1

courses_df = pd.DataFrame(courses)
courses_df.to_excel(OUTPUT_DIR / "courses.xlsx", index=False, engine='openpyxl')

# Generate Enrollments (main dataset)
print("Generating enrollments.csv...")
programs = ["Computer Science BS", "Business Administration BS", "Engineering BS", 
            "Liberal Arts BA", "Data Science MS", "MBA", "Healthcare Administration MS"]
cohorts = ["2021", "2022", "2023", "2024", "2025"]
enrollment_statuses = ["Enrolled", "Completed", "Withdrawn", "On Leave"]
grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F", "W", "IP"]

# Generate student pool
n_students = 800
student_names = []
for _ in range(n_students):
    first = random.choice(["Alex", "Bailey", "Cameron", "Drew", "Elliot", "Finley", "Harper", "Jordan", 
                           "Kelly", "Logan", "Morgan", "Noah", "Olivia", "Parker", "Quinn", "Riley", 
                           "Sam", "Taylor", "Avery", "Blake"])
    last = random.choice(last_names)
    student_names.append(f"{first} {last}")

enrollments = []
enrollment_id = 7000

for student_idx in range(n_students):
    student_id = f"S{10000 + student_idx}"
    student_name = student_names[student_idx]
    program = random.choice(programs)
    cohort = random.choice(cohorts)
    
    # Students take 3-6 courses per term
    n_courses = random.randint(3, 6)
    student_courses = courses_df.sample(min(n_courses, len(courses_df)))
    
    for _, course in student_courses.iterrows():
        # Determine enrollment status
        if course["term"] == "Fall 2024":
            status = random.choices(enrollment_statuses, weights=[10, 80, 8, 2])[0]
            grade = random.choices(grades, weights=[15, 12, 15, 18, 8, 10, 12, 5, 3, 2, 0, 0])[0] if status == "Completed" else "IP"
        else:  # Spring 2025
            status = random.choices(enrollment_statuses, weights=[85, 5, 7, 3])[0]
            grade = "IP"
        
        # Financial info
        base_tuition = course["credits"] * random.choice([500, 750, 1000, 1250])  # per credit varies by program
        tuition = base_tuition
        
        # Financial aid (some students get it)
        if random.random() < 0.6:  # 60% receive some aid
            aid_pct = random.uniform(0.1, 0.8)
            financial_aid = round(tuition * aid_pct, 2)
        else:
            financial_aid = 0
        
        net_tuition = tuition - financial_aid
        
        # Payment status
        if status == "Withdrawn":
            payment_status = "Refunded"
        else:
            payment_status = random.choices(["Paid", "Pending", "Overdue"], weights=[80, 15, 5])[0]
        
        enrollments.append({
            "enrollment_id": f"E{enrollment_id}",
            "student_id": student_id,
            "student_name": student_name,
            "course_id": course["course_id"],
            "course_code": course["course_code"],
            "course_name": course["course_name"],
            "program": program,
            "cohort": cohort,
            "term": course["term"],
            "credits": course["credits"],
            "tuition": tuition,
            "financial_aid": financial_aid,
            "net_tuition": net_tuition,
            "payment_status": payment_status,
            "enrollment_date": random_date(
                datetime(2024, 8, 1) if course["term"] == "Fall 2024" else datetime(2025, 1, 1),
                datetime(2024, 9, 1) if course["term"] == "Fall 2024" else datetime(2025, 2, 1)
            ).strftime("%Y-%m-%d"),
            "status": status,
            "grade": grade,
            "instructor_id": course["instructor_id"],
            "instructor_name": course["instructor_name"],
            "department": course["department"]
        })
        enrollment_id += 1

enrollments_df = pd.DataFrame(enrollments)

# Add nulls
enrollments_df["financial_aid"] = add_nulls(enrollments_df["financial_aid"], 0.05)

enrollments_df.to_csv(OUTPUT_DIR / "enrollments.csv", index=False)

# Generate README
print("Generating readme.md...")
readme_content = """# Education Enrollments Dataset

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
"""

with open(OUTPUT_DIR / "readme.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print(f"✅ Education enrollments dataset generated in {OUTPUT_DIR}")
print(f"   - enrollments.csv: {len(enrollments_df)} rows")
print(f"   - instructors.csv: {len(instructors_df)} rows")
print(f"   - courses.xlsx: {len(courses_df)} rows")
