import sqlite3

DB_PATH = "app/models/database.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def add_course(
    course_code,
    course_name,
    grade,
    credit,
    progress
):
    conn = get_connection()

    conn.execute("""
        INSERT INTO courses
        (
            course_code,
            course_name,
            grade,
            credit,
            progress
        )
        VALUES (?, ?, ?, ?, ?)
    """,
    (
        course_code,
        course_name,
        grade,
        credit,
        progress
    ))

    conn.commit()
    conn.close()


def get_all_courses():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM courses
    """)

    courses = cursor.fetchall()

    conn.close()

    return courses