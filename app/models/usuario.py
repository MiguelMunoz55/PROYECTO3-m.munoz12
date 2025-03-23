from app.config.db import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    es_admin = db.Column(db.Boolean, nullable=False)
    es_empleado = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Usuario(id={self.id}, username='{self.username}', es_admin={self.es_admin})"