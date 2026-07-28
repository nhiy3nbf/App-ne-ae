from werkzeug.security import generate_password_hash
from app.models.set_up import get_connection, init_db


def calculate_letter_and_gpa(total):
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


def seed():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    # --- USERS ---
    cursor.execute(
        "INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)",
        ("Nguyen Van A", "a@test.com", generate_password_hash("123456a"))
    )
    user_id = cursor.lastrowid

    # --- STUDENTS (đủ cột mới) ---
    cursor.execute("""
        INSERT INTO students
        (user_id, student_id, fullname, gender, date_of_birth, major, class,
         enrollment_year, avatar, national_id, nationality, phone_number, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, "AUS12899", "Nguyen Van A", "Male", "2004-05-10",
        "Information Technology", "CNTT1", 2022, None,
        "001204012345", "Vietnamese", "0901234567", "123 Le Loi, Da Nang"
    ))
    student_id = cursor.lastrowid

    # --- SEMESTERS ---
    cursor.execute(
        "INSERT INTO semesters (semester_number, academic_year, start_month, duration) VALUES (?, ?, ?, ?)",
        ("1", "2025-2026", 9, 4)
    )
    sem1_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO semesters (semester_number, academic_year, start_month, duration) VALUES (?, ?, ?, ?)",
        ("2", "2025-2026", 1, 4)
    )
    sem2_id = cursor.lastrowid

    # --- COURSES (chia 2 kỳ) ---
    courses_sem1 = [
        ("ICT1001", "Database Systems", 3, "Mr. Tran", sem1_id, "Intro to relational databases"),
        ("ICT1002", "Web Development", 3, "Ms. Le", sem1_id, "HTML, CSS, JS, Flask"),
        ("ICT1003", "Software Engineering", 4, "Mr. Pham", sem1_id, "SDLC and design patterns"),
    ]
    courses_sem2 = [
        ("ICT1004", "Artificial Intelligence", 3, "Ms. Hoang", sem2_id, "Intro to AI and ML"),
        ("ICT1005", "Computer Networks", 3, "Mr. Nguyen", sem2_id, "TCP/IP, routing, security basics"),
    ]

    course_ids = []
    for code, name, credits, lecturer, sem_id, desc in courses_sem1 + courses_sem2:
        cursor.execute(
            """INSERT INTO courses (course_code, course_name, credits, lecturer, semester_id, description)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (code, name, credits, lecturer, sem_id, desc)
        )
        course_ids.append(cursor.lastrowid)

    # --- ENROLLMENTS + GRADES (thang điểm 0-100) ---
    # attendance(%), assignment, quiz, midterm, final -- tất cả 0-100
    sample_grades = [
        (95, 88, 90, 85, 92),   # ICT1001
        (100, 95, 92, 90, 96),  # ICT1002
        (80, 75, 70, 72, 78),   # ICT1003
        (90, 85, 88, 84, 89),   # ICT1004
        (70, 65, 60, 68, 66),   # ICT1005
    ]

    for course_id, (att, asg, quiz, mid, final) in zip(course_ids, sample_grades):
        cursor.execute(
            """INSERT INTO enrollments (student_id, course_id, enrollment_month, status)
               VALUES (?, ?, ?, ?)""",
            (student_id, course_id, 9, "enrolled")
        )
        enrollment_id = cursor.lastrowid

        # weight: assignment 20%, quiz 20%, midterm 25%, final 35%
        total = round(asg * 0.2 + quiz * 0.2 + mid * 0.25 + final * 0.35, 2)
        letter, gpa_point = calculate_letter_and_gpa(total)

        cursor.execute(
            """INSERT INTO grades
               (enrollment_id, attendance, assignment, quiz, midterm_exam, final_exam,
                total_score, letter_grade, gpa_point)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (enrollment_id, att, asg, quiz, mid, final, total, letter, gpa_point)
        )

    conn.commit()
    conn.close()
    print("Seeded successfully.")
    print("Login: a@test.com / 123456a")


if __name__ == "__main__":
    seed()