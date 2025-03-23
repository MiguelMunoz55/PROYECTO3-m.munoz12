from flask import Flask
from app.config.db import db
from app.models.IProducto import Producto  # Importa todos los modelos necesarios
from app.models.Ingrediente import Ingrediente  # Importa todos los modelos necesarios
from app.models.Producto import Producto  # Importa todos los modelos necesarios
from app.models.Heladeria import Heladeria  # Importa todos los modelos necesarios
from app.models.usuario import Usuario  # Importa todos los modelos necesarios


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"  # Asegúrate de que Render esté usando la misma DB
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()  # 🚀 Crea todas las tablas necesarias
    print("✅ Tablas creadas correctamente")