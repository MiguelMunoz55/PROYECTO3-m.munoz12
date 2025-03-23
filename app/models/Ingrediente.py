from app.config.db import db

class Ingrediente(db.Model):
    __tablename__ = "ingredientes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Float, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    inventario = db.Column(db.Float, nullable=False)
    es_vegetariano = db.Column(db.Boolean, nullable=True)
    tipo = db.Column(db.String(20), nullable=True)  

    def abastecer(self, cantidad: float):
        self.inventario += cantidad

    def es_sano(self):
        return self.calorias < 100 or self.es_vegetariano

    def tiene_inventario(self) -> bool:
        return self.inventario > 0

    def consumir_ingredientes(self, cantidad: float = 1) -> bool:
        if self.inventario >= cantidad:
            self.inventario -= cantidad
            return True
        else:
            return False

    def abastecer(self, cantidad: float):
        self.inventario += cantidad

    def es_sano(self):
        return self.calorias < 100 or self.es_vegetariano

    def tiene_inventario(self) -> bool:
        return self.inventario > 0

    def consumir_ingredientes(self, cantidad: float = 1) -> bool:
        if self.inventario >= cantidad:
            self.inventario -= cantidad
            return True
        else:
            return False
        
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "calorias": self.calorias,
            "inventario": self.inventario,
            "es_vegetariano": self.es_vegetariano,
            "tipo": self.tipo
        }