from flask import Blueprint, render_template, session, redirect, url_for
from app.models.student import get_student_by_user_id
from app.models.course import build_course_results

course = Blueprint('course', __name__)


@course.route('/course')
def grades():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for('auth.login'))

    student = get_student_by_user_id(user_id)
    if not student:
        return render_template('course.html', error="Student record not found.")

    results = build_course_results(student["id"])
    if results is None:
        return render_template('course.html', error="No enrollments found for this student.")

    return render_template('course.html', results=results)