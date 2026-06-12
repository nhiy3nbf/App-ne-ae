from flask import Blueprint, render_template

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def home():
    return '<h1>Hello this is dashboard<h1>'