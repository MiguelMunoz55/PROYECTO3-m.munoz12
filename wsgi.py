import os
from app import create_app
from app.config.config import Config

# 🔎 Depuración: Imprime la variable para verificar si Render la está cargando
print("DATABASE_URI en wsgi.py antes de crear la app:", os.getenv("DATABASE_URI"))

# Si no se carga correctamente, forzarla con un valor por defecto (esto es opcional)
if not os.getenv("DATABASE_URI"):
    os.environ["DATABASE_URI"] = "mysql+pymysql://root:root@localhost/proyecto_modulo_3_heladeria_uniandes"

app = create_app(Config)

print("DATABASE_URI en wsgi.py después de crear la app:", os.getenv("DATABASE_URI"))