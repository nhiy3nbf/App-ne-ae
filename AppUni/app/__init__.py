from flask import Flask
from app.models.user import *

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'dmbachtrungphonglong1234'

    from app.routes.auth import auth
    from app.routes.dashboard import dashboard

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dashboard, url_prefix="/")

    with app.app_context():
        init_db()

    return app