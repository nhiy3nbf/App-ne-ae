from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.admin import (
    is_user_admin, get_all_students, get_student_by_id, update_student_info_by_id,
    get_all_courses, get_student_enrollments_with_grades, enroll_student, upsert_grade
)

admin = Blueprint('admin', __name__)


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for('auth.login'))
        if not is_user_admin(user_id):
            return "Access denied. Admins only.", 403
        return view_func(*args, **kwargs)
    return wrapper


@admin.route('/')
@admin_required
def dashboard():
    students = get_all_students()
    return render_template('admin.html', students=students)


@admin.route('/student/<int:student_id>')
@admin_required
def student_detail(student_id):
    student = get_student_by_id(student_id)
    if not student:
        return "Student not found.", 404

    enrollments = get_student_enrollments_with_grades(student_id)
    all_courses = get_all_courses()

    enrolled_course_ids = {e["course_id"] for e in enrollments}
    available_courses = [c for c in all_courses if c["id"] not in enrolled_course_ids]

    return render_template(
        'admin_student.html',
        student=student,
        enrollments=enrollments,
        available_courses=available_courses
    )


@admin.route('/student/<int:student_id>/update-info', methods=['POST'])
@admin_required
def update_info(student_id):
    data = {
        'fullname': request.form.get('fullname', '').strip(),
        'student_id': request.form.get('student_id', '').strip(),
        'gender': request.form.get('gender', '').strip(),
        'date_of_birth': request.form.get('date_of_birth', '').strip(),
        'major': request.form.get('major', '').strip(),
        'class': request.form.get('class', '').strip(),
        'enrollment_year': request.form.get('enrollment_year', '').strip(),
        'national_id': request.form.get('national_id', '').strip(),
        'nationality': request.form.get('nationality', '').strip(),
        'phone_number': request.form.get('phone_number', '').strip(),
        'address': request.form.get('address', '').strip(),
    }
    update_student_info_by_id(student_id, data)
    flash('Student info updated.')
    return redirect(url_for('admin.student_detail', student_id=student_id))


@admin.route('/student/<int:student_id>/enroll', methods=['POST'])
@admin_required
def enroll(student_id):
    course_id = request.form.get('course_id')
    enrollment_month = request.form.get('enrollment_month', '').strip()
    status = request.form.get('status', 'enrolled')

    if course_id:
        enroll_student(
            student_id,
            int(course_id),
            int(enrollment_month) if enrollment_month else None,
            status
        )
        flash('Course enrolled.')

    return redirect(url_for('admin.student_detail', student_id=student_id))


@admin.route('/student/<int:student_id>/grades/save', methods=['POST'])
@admin_required
def save_grades(student_id):
    enrollment_ids = request.form.getlist('enrollment_id')

    def parse_score(field):
        value = request.form.get(field, '').strip()
        if not value:
            return None
        try:
            return max(0, min(100, float(value)))
        except ValueError:
            return None

    for eid in enrollment_ids:
        upsert_grade(
            int(eid),
            parse_score(f'attendance_{eid}'),
            parse_score(f'assignment_{eid}'),
            parse_score(f'quiz_{eid}'),
            parse_score(f'midterm_exam_{eid}'),
            parse_score(f'final_exam_{eid}'),
        )

    flash('Grades saved.')
    return redirect(url_for('admin.student_detail', student_id=student_id))