from app.models.set_up import get_connection
from app.models.course import build_course_results
from app.models.prediction import get_dashboard_predictions


def get_enrolled_courses(student_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT c.course_code, c.course_name
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        WHERE e.student_id = ?
        ORDER BY c.course_code
    """, (student_id,)).fetchall()
    conn.close()
    return [{"code": r["course_code"], "name": r["course_name"]} for r in rows]


def get_dashboard_stats(student_id):
    """GPA / Attendance / Labs / Awards — tính thật từ DB, không hardcode nữa."""
    results = build_course_results(student_id)

    if not results:
        return {"gpa": "N/A", "attendance": "N/A", "labs": 0, "awards": 0}

    all_attendance = []
    completed_count = 0
    for sem in results["semesters"].values():
        completed_count += sem["completed"]
        for c in sem["courses"]:
            if c["attendance"]:
                all_attendance.append(c["attendance"])

    avg_attendance = round(sum(all_attendance) / len(all_attendance), 1) if all_attendance else 0

    return {
        "gpa": results["gpa"],
        "attendance": f"{avg_attendance}%",
        "labs": completed_count,
        "awards": results["achievements_count"],
    }


def get_dashboard_data(student_id):
    courses = get_enrolled_courses(student_id)
    stats = get_dashboard_stats(student_id)
    predictions, overall = get_dashboard_predictions(student_id)

    return {
        "courses": courses,
        "stats": stats,
        "predictions": predictions,
        "overall_prediction": overall["grade"],
        "overall_prediction_color": overall["color"],
    }