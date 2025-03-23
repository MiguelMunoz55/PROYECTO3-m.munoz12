from flask import Flask
from app.config.db import db
from flask_login import LoginManager

login_manager = LoginManager()

def create_app(config):
    app = Flask(__name__, template_folder="views")
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    with app.app_context():
        from app.models.usuario import Usuario
        db.create_all()

    return app