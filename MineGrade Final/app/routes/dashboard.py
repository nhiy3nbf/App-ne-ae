from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from app.models.student import get_student_by_user_id, update_student_avt
from app.models.home import get_dashboard_data

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/dashboard')
def home():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for('auth.login'))

    student = get_student_by_user_id(user_id)
    if not student:
        return render_template('dashboard.html', student=None, error="Student record not found.")

    data = get_dashboard_data(student["id"])

    return render_template(
        'dashboard.html',
        student=student,
        courses=data["courses"],
        stats=data["stats"],
        predictions=data["predictions"],
        overall_prediction=data["overall_prediction"],
        overall_prediction_color=data["overall_prediction_color"],
    )


@dashboard.route('/dashboard/update-profile', methods=['POST'])
def update_profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for('auth.login'))

    new_name = request.form.get('newName', '').strip()
    skin_name = request.form.get('skinName', '').strip()

    update_student_avt(
        user_id=user_id,
        fullname=new_name or None,
        skin_name=skin_name or None,
    )
    flash("Profile updated!")
    return redirect(url_for('dashboard.home'))