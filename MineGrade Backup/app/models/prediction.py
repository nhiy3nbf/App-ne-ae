from app.models.set_up import get_connection

# Weight cố định cho mỗi cột điểm trong bảng grades — tổng = 100%
ASSIGNMENT_WEIGHTS = [
    ("Attendance", "attendance", "10%"),
    ("Assignment", "assignment", "20%"),
    ("Quiz", "quiz", "20%"),
    ("Midterm Exam", "midterm_exam", "25%"),
    ("Final Exam", "final_exam", "25%"),
]

def format_term(start_month, academic_year):
    if start_month in (8, 9, 10, 11, 12):
        season = "FALL"
    elif start_month in (1, 2, 3, 4):
        season = "SPRING"
    else:
        season = "SUMMER"
    return f"{season} {academic_year}"

def get_student_semesters_for_prediction(student_id):
    """Build list semester đúng shape mà logic tính GPA/prediction trong predict.py cần."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            sem.id AS semester_id,
            sem.semester_number,
            sem.academic_year,
            sem.start_month,
            c.course_code,
            g.attendance,
            g.assignment,
            g.quiz,
            g.midterm_exam,
            g.final_exam
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        JOIN semesters sem ON c.semester_id = sem.id
        LEFT JOIN grades g ON g.enrollment_id = e.id
        WHERE e.student_id = ?
        ORDER BY sem.academic_year, sem.semester_number, c.course_code
    """, (student_id,)).fetchall()
    conn.close()

    semesters_map = {}
    for row in rows:
        key = row["semester_id"]
        if key not in semesters_map:
            semesters_map[key] = {
                "title": f"Semester {row['semester_number']}",
                "term": format_term(row["start_month"], row["academic_year"]),
                "is_open": False,
                "courses": []
            }

        assignments = []
        for label, col, weight in ASSIGNMENT_WEIGHTS:
            value = row[col]
            score = f"{value}/100" if value is not None else "--/100"
            assignments.append({"title": label, "score": score, "weight": weight})

        semesters_map[key]["courses"].append({
            "code": row["course_code"],
            "assignments": assignments
        })

    return list(semesters_map.values())