from flask import Flask
from .routes.dashboard import bp as dashboard_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(dashboard_bp)
    return app
