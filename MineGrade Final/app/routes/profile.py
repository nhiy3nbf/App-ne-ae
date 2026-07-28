from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.student import get_student_by_user_id, update_student_info

profile = Blueprint('profile', __name__)


@profile.route('/profile', methods=['GET', 'POST'])
def account():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        data = {
            'fullname': request.form.get('fullname', '').strip(),
            'student_id': request.form.get('student_id', '').strip(),
            'date_of_birth': request.form.get('date_of_birth', '').strip(),
            'national_id': request.form.get('national_id', '').strip(),
            'gender': request.form.get('gender', '').strip(),
            'nationality': request.form.get('nationality', '').strip(),
            'major': request.form.get('major', '').strip(),
            'phone_number': request.form.get('phone_number', '').strip(),
            'address': request.form.get('address', '').strip(),
        }
        update_student_info(user_id, data)
        return redirect(url_for('profile.account'))

    edit_mode = request.args.get('edit') == 'true'
    student = get_student_by_user_id(user_id)

    return render_template('profile.html', student=student, edit_mode=edit_mode)