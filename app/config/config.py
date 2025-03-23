import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///fallback.db")  # Usa SQLite si la variable está vacía
    SQLALCHEMY_TRACK_MODIFICATIONS = False