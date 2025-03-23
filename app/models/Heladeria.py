from app.models.Ingrediente import Ingrediente
from app.models.Producto import Producto
from app.config.db import db

class Heladeria:
    def __init__(self, nombre):
        self.nombre = nombre
        self.ingredientes = []
        self.productos = []

    def agregar_ingrediente(self, ingrediente: Ingrediente):
        self.ingredientes.append(ingrediente)

    def agregar_producto(self, producto: Producto):
        self.productos.append(producto)

    def mostrar_ingredientes(self):
        return [ing.nombre for ing in self.ingredientes]

    def mostrar_productos(self):
        return [prod.nombre for prod in self.productos]

    def buscar_producto(self, nombre):
        return next((prod for prod in self.productos if prod.nombre == nombre), None)

    def buscar_ingrediente(self, nombre):
        return next((ing for ing in self.ingredientes if ing.nombre == nombre), None)

    def guardar_cambios(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e