from flask import Blueprint, render_template

profile = Blueprint('profile', __name__)

@profile.route('/profile')
def account():
    return render_template('profile.html')