from flask import Blueprint, render_template

course = Blueprint('course', __name__)

@course.route('/course')
def subject():
    return render_template('course.html')