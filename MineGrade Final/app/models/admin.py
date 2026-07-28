from app.models.set_up import get_connection
import sqlite3

def is_user_admin(user_id):
    conn = get_connection()
    row = conn.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return bool(row and row["is_admin"])


def get_all_students():
    conn = get_connection()
    rows = conn.execute("""
        SELECT s.*, u.email
        FROM students s
        JOIN users u ON s.user_id = u.id
        ORDER BY s.fullname
    """).fetchall()
    conn.close()
    return rows


def get_student_by_id(student_id):
    conn = get_connection()
    row = conn.execute("""
        SELECT s.*, u.email
        FROM students s
        JOIN users u ON s.user_id = u.id
        WHERE s.id = ?
    """, (student_id,)).fetchone()
    conn.close()
    return row


def update_student_info_by_id(student_id, data):
    conn = get_connection()
    enrollment_year = data.get('enrollment_year')
    conn.execute("""
        UPDATE students SET
            fullname = ?,
            student_id = ?,
            gender = ?,
            date_of_birth = ?,
            major = ?,
            class = ?,
            enrollment_year = ?,
            national_id = ?,
            nationality = ?,
            phone_number = ?,
            address = ?
        WHERE id = ?
    """, (
        data.get('fullname') or None,
        data.get('student_id') or None,
        data.get('gender') or None,
        data.get('date_of_birth') or None,
        data.get('major') or None,
        data.get('class') or None,
        int(enrollment_year) if enrollment_year else None,
        data.get('national_id') or None,
        data.get('nationality') or None,
        data.get('phone_number') or None,
        data.get('address') or None,
        student_id
    ))
    conn.commit()
    conn.close()


def get_all_courses():
    conn = get_connection()
    rows = conn.execute("""
        SELECT c.*, sem.semester_number, sem.academic_year
        FROM courses c
        JOIN semesters sem ON c.semester_id = sem.id
        ORDER BY sem.academic_year, sem.semester_number, c.course_code
    """).fetchall()
    conn.close()
    return rows


def get_student_enrollments_with_grades(student_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            e.id AS enrollment_id,
            e.course_id,
            e.enrollment_month,
            e.status,
            c.course_code,
            c.course_name,
            sem.semester_number,
            sem.academic_year,
            g.attendance,
            g.assignment,
            g.quiz,
            g.midterm_exam,
            g.final_exam,
            g.total_score,
            g.letter_grade,
            g.gpa_point
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        JOIN semesters sem ON c.semester_id = sem.id
        LEFT JOIN grades g ON g.enrollment_id = e.id
        WHERE e.student_id = ?
        ORDER BY sem.academic_year, sem.semester_number, c.course_code
    """, (student_id,)).fetchall()
    conn.close()
    return rows


def enroll_student(student_id, course_id, enrollment_month, status):
    conn = get_connection()
    conn.execute("""
        INSERT INTO enrollments (student_id, course_id, enrollment_month, status)
        VALUES (?, ?, ?, ?)
    """, (student_id, course_id, enrollment_month, status))
    conn.commit()
    conn.close()


def calculate_letter_and_gpa(total):
    if total is None:
        return None, None
    if total >= 90:
        return "A+", 4.0
    elif total >= 80:
        return "A", 4.0
    elif total >= 70:
        return "B", 3.0
    elif total >= 60:
        return "C", 2.0
    else:
        return "F", 0.0


def upsert_grade(enrollment_id, attendance, assignment, quiz, midterm, final):
    """Tạo mới nếu enrollment chưa có điểm, cập nhật nếu đã có."""
    conn = get_connection()
    cursor = conn.cursor()

    total = None
    if all(v is not None for v in [assignment, quiz, midterm, final]):
        total = round(assignment * 0.2 + quiz * 0.2 + midterm * 0.25 + final * 0.35, 2)
    letter, gpa_point = calculate_letter_and_gpa(total)

    existing = cursor.execute(
        "SELECT id FROM grades WHERE enrollment_id = ?", (enrollment_id,)
    ).fetchone()

    if existing:
        cursor.execute("""
            UPDATE grades SET
                attendance = ?, assignment = ?, quiz = ?, midterm_exam = ?, final_exam = ?,
                total_score = ?, letter_grade = ?, gpa_point = ?
            WHERE enrollment_id = ?
        """, (attendance, assignment, quiz, midterm, final, total, letter, gpa_point, enrollment_id))
    else:
        cursor.execute("""
            INSERT INTO grades
            (enrollment_id, attendance, assignment, quiz, midterm_exam, final_exam, total_score, letter_grade, gpa_point)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (enrollment_id, attendance, assignment, quiz, midterm, final, total, letter, gpa_point))

    conn.commit()
    conn.close()

def get_all_semesters():
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM semesters
        ORDER BY academic_year DESC, semester_number
    """).fetchall()
    conn.close()
    return rows


def create_semester(semester_number, academic_year, start_month, duration):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO semesters (semester_number, academic_year, start_month, duration)
        VALUES (?, ?, ?, ?)
    """, (semester_number, academic_year, start_month, duration))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def create_course(course_code, course_name, credits, lecturer, semester_id, description):
    """Trả về (course_id, None) nếu OK, (None, error_message) nếu course_code bị trùng."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO courses (course_code, course_name, credits, lecturer, semester_id, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (course_code, course_name, credits, lecturer, semester_id, description))
        conn.commit()
        return cursor.lastrowid, None
    except sqlite3.IntegrityError:
        return None, f"Course code '{course_code}' already exists."
    finally:
        conn.close()