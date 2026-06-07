from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(username) < 5:
            flash('Username must be longer than 5 characters.', category='error')
        elif len(password1) < 7:
            flash('Password must be longer than 7 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        else:
            flash('Account created!', category='success')

    return render_template('signup.html')