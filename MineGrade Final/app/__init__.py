from flask import Flask
from app.models.set_up import *

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'dmbachtrungphonglong1234'

    from app.routes.auth import auth
    from app.routes.dashboard import dashboard
    from app.routes.profile import profile
    from app.routes.predict import predict
    from app.routes.course import course
    from app.routes.admin import admin
    from app.routes.start import start

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dashboard, url_prefix="/")
    app.register_blueprint(course, url_prefix="/")
    app.register_blueprint(predict, url_prefix="/")
    app.register_blueprint(profile, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(start, url_prefix="/")
    with app.app_context():
        init_db()
    return app