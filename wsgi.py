import os
from app.config.routes import app  # Importa la instancia de la app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))