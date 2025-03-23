from dotenv import load_dotenv
import os

load_dotenv(override=True)

print("DATABASE_URI:", os.getenv("DATABASE_URI"))  # <-- Agrega esto para ver si se está cargando

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')