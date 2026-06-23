from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.models.user import *
from werkzeug.security import generate_password_hash, check_password_hash

init_db()
auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form.get('fullname', '').strip()
        email = request.form.get('email', '').strip()
        password1 = request.form.get('password1', '')
        password2 = request.form.get('password2', '')

        if len(fullname) == 2:
            flash('Your fullname must be filled in.', category='error')
        elif len(email) == 0:
            flash('Email must be filled in.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be longer than 6 characters.', category='error')
        else:
            hash = generate_password_hash(password1)
            email_used = create_user(fullname, email, hash)
            if email_used:
                flash('Email has been used.', category='error')
            else:
                flash('Succesfully registered!', category='success')
                return redirect(url_for('dashboard.home'))

    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user_by_email(email)
        if not user:
            flash('Email does not exist.', category='error')
        elif not check_password_hash(user["password"], password):
            flash('Wrong password', category='error')
        else:
            session['user_id'] = user['id']
            flash('Login success', category='success')
            return redirect(url_for('dashboard.home'))

    return render_template('login.html')
