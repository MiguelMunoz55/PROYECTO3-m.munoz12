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

        # ✅ Importa y registra los blueprints aquí dentro del contexto
        from app.controllers.home_controller import home_blueprint
        from app.controllers.auth_controller import auth_blueprint
        from app.controllers.admin_controller import admin_blueprint
        from app.controllers.user_controller import user_blueprint
        from app.controllers.empleado_controller import empleado_blueprint
        from app.controllers.api_controller import api_blueprint

        app.register_blueprint(home_blueprint)
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(admin_blueprint)
        app.register_blueprint(empleado_blueprint)
        app.register_blueprint(user_blueprint)
        app.register_blueprint(api_blueprint)

    return app
