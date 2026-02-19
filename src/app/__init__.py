from flask import Flask
from flask_cors import CORS


def create_app():
    """Application factory to create and configure the Flask app."""

    app = Flask(__name__)
    CORS(app)

    from app.routes.auth import auth_bp
    from app.routes.crm import crm_bp

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(crm_bp, url_prefix="/api/crm")

    return app
