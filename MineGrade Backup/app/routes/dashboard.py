from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from app.models.student import get_student_by_user_id, update_student_avt

dashboard = Blueprint('dashboard', __name__)

COURSES = [
    {"code": "ICT1001", "name": "Database Systems"},
    {"code": "ICT1002", "name": "Web Development"},
    {"code": "ICT1003", "name": "Software Engineering"},
    {"code": "ICT1004", "name": "Artificial Intelligence"},
]

REMINDERS = [
    "Lab Project",
    "Database Assignment",
    "Presentation",
    "Final Exam",
]

@dashboard.route('/dashboard')
def home():
    student = get_student_by_user_id(session["user_id"])
    return render_template(
        'dashboard.html',
        student=student,
        courses=COURSES,
        reminders=REMINDERS,
    )

@dashboard.route('/dashboard/update-profile', methods=['POST'])
def update_profile():
    new_name = request.form.get('newName', '').strip()
    skin_name = request.form.get('skinName', '').strip()

    update_student_avt(
        user_id=session["user_id"],
        fullname=new_name or None,
        skin_name=skin_name or None,
    )
    flash("Profile updated!")
    return redirect(url_for('dashboard.home'))