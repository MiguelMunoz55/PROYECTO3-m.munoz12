from app import create_app, login_manager
from app.config.config import Config
from app.config.db import db
from app.models.usuario import Usuario
from app.controllers.home_controller import home_blueprint
from app.controllers.auth_controller import auth_blueprint
from app.controllers.admin_controller import admin_blueprint
from app.controllers.user_controller import user_blueprint
from app.controllers.empleado_controller import empleado_blueprint
from app.controllers.api_controller import api_blueprint

app = create_app(Config)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Registrar blueprints
app.register_blueprint(home_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(empleado_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(api_blueprint)

