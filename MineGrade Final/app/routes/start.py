from flask import Blueprint, redirect, url_for

start = Blueprint('start', __name__)

@start.route('/')
def index():
    return redirect(url_for('auth.login'))