import os
from app.config.routes import app
from app.config.db import db
from app.models.usuario import Usuario

with app.app_context():
    if not Usuario.query.first():
        admin = Usuario(username="admin", password="1234", es_admin=True, es_empleado=False)
        empleado = Usuario(username="empleado", password="5678", es_admin=False, es_empleado=True)
        usuario = Usuario(username="usuario", password="9012", es_admin=False, es_empleado=False)

        db.session.add_all([admin, empleado, usuario])
        db.session.commit()

        print("✅ Usuarios insertados correctamente")
    else:
        print("⚠️ Usuarios ya existen en la base de datos")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))