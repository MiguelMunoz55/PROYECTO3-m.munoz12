from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')

# 🔎 Imprimir valores para verificar que se cargan correctamente
print("DATABASE_URI en config.py:", os.getenv("DATABASE_URI"))
print("SECRET_KEY en config.py:", os.getenv("SECRET_KEY"))