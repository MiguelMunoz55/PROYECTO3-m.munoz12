from app.models.IProducto import IProducto
from app.config.db import db
from app.controllers.funciones import *

class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio_publico = db.Column(db.Float, nullable=False)
    costo = db.Column(db.Float, nullable=False)
    inventario = db.Column(db.Integer, nullable=False)

    id_ingrediente_1 = db.Column(db.Integer, db.ForeignKey("ingredientes.id"), nullable=True)
    id_ingrediente_2 = db.Column(db.Integer, db.ForeignKey("ingredientes.id"), nullable=True)
    id_ingrediente_3 = db.Column(db.Integer, db.ForeignKey("ingredientes.id"), nullable=True)

    ingrediente_1 = db.relationship("Ingrediente", foreign_keys=[id_ingrediente_1])
    ingrediente_2 = db.relationship("Ingrediente", foreign_keys=[id_ingrediente_2])
    ingrediente_3 = db.relationship("Ingrediente", foreign_keys=[id_ingrediente_3])

    def calcular_rentabilidad(self):
        return self.precio_publico - self.costo

    def tiene_inventario(self):
        return self.inventario > 0

    def consumir_ingredientes(self):
        ingredientes = [self.ingrediente_1, self.ingrediente_2, self.ingrediente_3]

        for ingrediente in ingredientes:
            if ingrediente and not ingrediente.consumir_ingredientes():
                raise ValueError(ingrediente.nombre)
        
        self.inventario -= 1
        return "¡Vendido!"
    
    def calcular_costo(self):
        ingredientes = [
            self.ingrediente_1,
            self.ingrediente_2,
            self.ingrediente_3
        ]
        
        # Filtramos ingredientes nulos (puede haber productos con menos de 3 ingredientes)
        ingredientes_validos = [ingrediente for ingrediente in ingredientes if ingrediente]
        
        if not ingredientes_validos:
            return 0  # Si el producto no tiene ingredientes, el costo es 0

        # Convertimos los ingredientes en diccionarios con precios
        ingredientes_dict = [{"precio": ing.precio} for ing in ingredientes_validos]

        # Llamamos a la función costos con los ingredientes disponibles
        return costos(*ingredientes_dict, *([{"precio": 0}] * (3 - len(ingredientes_dict))))
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio_publico": self.precio_publico,
            "costo": self.costo,
            "inventario": self.inventario,
            "id_ingrediente_1": self.id_ingrediente_1,
            "id_ingrediente_2": self.id_ingrediente_2,
            "id_ingrediente_3": self.id_ingrediente_3,
            "rentabilidad": self.calcular_rentabilidad(),
        }
    
    def consumir_ingredientes(self):
        ingredientes = [self.ingrediente_1, self.ingrediente_2, self.ingrediente_3]

        for ingrediente in ingredientes:
            if ingrediente:  # Verificamos que el ingrediente no sea None
                try:
                    vender_producto(ingrediente, 1)  # Usamos la función externa
                except ValueError:
                    raise ValueError(f"No hay suficiente stock de {ingrediente.nombre}")

        self.inventario -= 1  # Reducimos el inventario del producto
        return "¡Vendido!"