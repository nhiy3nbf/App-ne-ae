from app.models.set_up import get_connection

def calculate_grade(percent):
    if percent is None:
        return 'N/A', '#888888'
    if percent >= 90:
        return 'A+', '#55ff55'
    elif percent >= 80:
        return 'A', '#55ff55'
    elif percent >= 70:
        return 'B', '#ffff55'
    elif percent >= 60:
        return 'C', '#ffaa00'
    else:
        return 'F', '#ff5555'

def get_grade_color(percent):
    if percent > 80:
        return '#55ff55'
    elif percent > 70:
        return '#99ff33'
    elif percent > 60:
        return '#ffff55'
    else:
        return '#ff5555'

def get_gpa_color(gpa):
    if gpa > 3.0:
        return '#55ff55'
    elif gpa < 2.5:
        return '#ff5555'
    else:
        return '#ffffff'

def get_course_max_scores():
    """Điểm cao nhất mỗi môn, tính trên TẤT CẢ sinh viên — dùng để xét achievement 'Top Scorer'."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT c.course_code, MAX(g.total_score) as max_score
        FROM grades g
        JOIN enrollments e ON g.enrollment_id = e.id
        JOIN courses c ON e.course_id = c.id
        WHERE g.total_score IS NOT NULL
        GROUP BY c.course_code
    """).fetchall()
    conn.close()
    return {row["course_code"]: row["max_score"] for row in rows}

def get_student_enrollments(student_id):
    """Toàn bộ enrollment + course + semester + grade của 1 sinh viên."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            sem.id AS semester_id,
            sem.semester_number,
            sem.academic_year,
            c.course_code,
            c.course_name,
            c.credits,
            e.status,
            g.attendance,
            g.total_score
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        JOIN semesters sem ON c.semester_id = sem.id
        LEFT JOIN grades g ON g.enrollment_id = e.id
        WHERE e.student_id = ?
        ORDER BY sem.academic_year, sem.semester_number
    """, (student_id,)).fetchall()
    conn.close()
    return rows

def build_course_results(student_id):
    """Build dict 'results' đúng shape mà course.html đang cần — thay thế hoàn toàn phần đọc data.json cũ."""
    rows = get_student_enrollments(student_id)
    if not rows:
        return None

    max_scores = get_course_max_scores()

    semesters = {}
    all_percentages = []
    achievements_list = []

    for row in rows:
        sem_title = f"Semester {row['semester_number']}"

        if sem_title not in semesters:
            semesters[sem_title] = {
                'subtitle': row['academic_year'],
                'units': 0,
                'completed': 0,
                'earned_credits': 0.0,
                'total_credits': 0.0,
                'percentages': [],
                'courses': []
            }

        sem = semesters[sem_title]
        percent = row['total_score']

        sem['units'] += 1
        sem['total_credits'] += row['credits'] or 0

        if percent is not None:
            sem['percentages'].append(percent)
            all_percentages.append(percent)
            sem['completed'] += 1
            sem['earned_credits'] += row['credits'] or 0

            highest = max_scores.get(row['course_code'], 0)
            if percent > 85 and percent >= highest:
                achievements_list.append({
                    'course': row['course_code'],
                    'score': percent,
                    'title': f"Top Scorer in {row['course_code']}"
                })

        grade_letter, color = calculate_grade(percent)

        sem['courses'].append({
            'code': row['course_code'],
            'percent': percent if percent is not None else 0,
            'grade': grade_letter,
            'color': color,
            'attendance': round(row['attendance'], 1) if row['attendance'] is not None else 0
        })

    # Tính toán số liệu tổng hợp mỗi kỳ
    final_semesters = {}
    for title, sem in semesters.items():
        sem_avg = sum(sem['percentages']) / len(sem['percentages']) if sem['percentages'] else 0
        sem_gpa = round((sem_avg / 100) * 4.0, 2)
        progress = int((sem['completed'] / sem['units']) * 100) if sem['units'] else 0

        final_semesters[title] = {
            'subtitle': sem['subtitle'],
            'units': sem['units'],
            'progress': progress,
            'status_text': f"{progress}% complete" if progress == 100 else f"{progress}% in progress",
            'status_color': '#55ff55' if progress == 100 else '#ffaa00',
            'completed': sem['completed'],
            'earned_credits': sem['earned_credits'],
            'total_credits': sem['total_credits'],
            'sem_gpa': sem_gpa,
            'courses': sem['courses']
        }

    avg_grade = round(sum(all_percentages) / len(all_percentages), 2) if all_percentages else 0
    gpa = round((avg_grade / 100) * 4.0, 2)

    return {
        'avg_grade': avg_grade,
        'avg_grade_color': get_grade_color(avg_grade),
        'gpa': gpa,
        'gpa_color': get_gpa_color(gpa),
        'achievements_count': len(achievements_list),
        'achievements': achievements_list,
        'semesters': final_semesters
    }