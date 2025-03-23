from app import create_app
from app.config.config import Config  # Asegúrate de importar Config

app = create_app(Config)  # Pasa la configuración correctamente