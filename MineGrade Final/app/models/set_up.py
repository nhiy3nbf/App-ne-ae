import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 fullname TEXT NOT NULL,
                 email TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 is_admin INTEGER DEFAULT 0
                 )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS students (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 student_id TEXT UNIQUE,
                 fullname TEXT,
                 gender TEXT,
                 date_of_birth DATE,
                 major TEXT,
                 class TEXT,
                 enrollment_year INTEGER,
                 avatar TEXT,
                 national_id TEXT,
                 nationality TEXT,
                 phone_number TEXT,
                 address TEXT,
                 FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                 )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS semesters (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 semester_number TEXT,
                 academic_year TEXT,
                 start_month INTEGER,
                 duration INTEGER
                 )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS courses (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 course_code TEXT UNIQUE,
                 course_name TEXT,
                 credits INTEGER,
                 lecturer TEXT,
                 semester_id INTEGER,
                 description TEXT,
                 FOREIGN KEY (semester_id) REFERENCES semesters(id) ON DELETE CASCADE
                 )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS enrollments (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 student_id INTEGER,
                 course_id INTEGER,
                 enrollment_month INTEGER,
                 status TEXT,
                 FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                 FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
                 )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS grades (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 enrollment_id INTEGER,
                 attendance REAL,
                 assignment REAL,
                 quiz REAL,
                 midterm_exam REAL,
                 final_exam REAL,
                 total_score REAL,
                 letter_grade TEXT,
                 gpa_point REAL,
                 FOREIGN KEY (enrollment_id) REFERENCES enrollments(id) ON DELETE CASCADE
                 )""")
    conn.commit()
    conn.close()