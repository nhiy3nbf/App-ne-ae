import re
from app.models.set_up import get_connection

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


# ============================================================
# Logic tính prediction — chuyển từ routes/predict.py qua đây để
# dashboard.py và predict.py dùng chung, không phải import chéo
# giữa 2 file route với nhau.
# ============================================================

def update_assignment_statuses(semesters):
    for semester in semesters:
        for course in semester.get("courses", []):
            for assign in course.get("assignments", []):
                score = str(assign.get("score", "")).strip()
                score_match = re.match(r"^(\d+(\.\d+)?)\s*/\s*100$", score)
                assign["status"] = "completed" if score_match else "pending"
    return semesters


def get_asia_uni_grade_info(mark):
    if mark >= 90:
        return {"grade": "A+", "points": 4.00, "percent": 100, "color": "green", "status": "PASS"}
    elif mark >= 85:
        return {"grade": "A",  "points": 3.75, "percent": 88,  "color": "green", "status": "PASS"}
    elif mark >= 80:
        return {"grade": "A-", "points": 3.50, "percent": 82,  "color": "green", "status": "PASS"}
    elif mark >= 75:
        return {"grade": "B+", "points": 3.25, "percent": 77,  "color": "yellow-green", "status": "PASS"}
    elif mark >= 70:
        return {"grade": "B",  "points": 3.00, "percent": 72,  "color": "yellow-green", "status": "PASS"}
    elif mark >= 65:
        return {"grade": "B-", "points": 2.75, "percent": 67,  "color": "yellow", "status": "PASS"}
    elif mark >= 60:
        return {"grade": "C+", "points": 2.50, "percent": 62,  "color": "yellow", "status": "PASS"}
    elif mark >= 55:
        return {"grade": "C",  "points": 2.25, "percent": 57,  "color": "orange", "status": "FAIL"}
    elif mark >= 50:
        return {"grade": "C-", "points": 2.00, "percent": 52,  "color": "orange", "status": "FAIL"}
    else:
        return {"grade": "F",  "points": 0.00, "percent": 15,  "color": "red", "status": "FAIL"}


def get_color_by_gpa(gpa_value):
    if gpa_value >= 3.25:
        return "green"
    elif gpa_value >= 2.50:
        return "yellow-green"
    elif gpa_value >= 2.25:
        return "yellow"
    elif gpa_value >= 2.00:
        return "orange"
    return "red"


def calculate_course_predicted_mark(course):
    completed_weight = 0.0
    earned_points = 0.0
    for assign in course.get("assignments", []):
        if assign.get("status") == "completed" and assign.get("score") != "--/100":
            weight = float(assign["weight"].replace("%", ""))
            score_match = re.match(r"(\d+(\.\d+)?)/100", assign["score"])
            if score_match:
                score = float(score_match.group(1))
                earned_points += (score * (weight / 100.0))
                completed_weight += weight
    if completed_weight > 0:
        return round((earned_points / completed_weight) * 100, 1)
    return 0.0


def calculate_semester_progress(courses):
    if not courses:
        return 0
    total_progress = 0.0
    for c in courses:
        completed_weight = 0.0
        for assign in c.get("assignments", []):
            if assign.get("status") == "completed":
                weight = float(assign.get("weight", "0%").replace("%", ""))
                completed_weight += weight
        total_progress += completed_weight
    return round(total_progress / len(courses))


def get_dashboard_predictions(student_id):
    """Prediction gọn cho từng môn + 1 prediction tổng — dùng riêng cho Dashboard."""
    raw_semesters = get_student_semesters_for_prediction(student_id)
    if not raw_semesters:
        return [], {"grade": "N/A", "color": "gray"}

    raw_semesters = update_assignment_statuses(raw_semesters)

    predictions = []
    marks = []

    for sem in raw_semesters:
        for c in sem["courses"]:
            mark = calculate_course_predicted_mark(c)
            info = get_asia_uni_grade_info(mark)
            predictions.append({"code": c["code"], "prediction": info["grade"], "color": info["color"]})
            marks.append(mark)

    overall_mark = sum(marks) / len(marks) if marks else 0
    overall_info = get_asia_uni_grade_info(overall_mark)

    return predictions, {"grade": overall_info["grade"], "color": overall_info["color"]}