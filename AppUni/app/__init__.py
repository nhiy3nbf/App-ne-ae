from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'ditmetuim'

    from app.routes.auth import auth
    from app.routes.dashboard import dashboard

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dashboard, url_prefix="/")

    return app