from flask import flash
from app.config.db import db
from app.models.Ingrediente import Ingrediente

def cargar_ingredientes():
    ingredientes = [
        {"nombre": "Vainilla", "precio": 1.0, "calorias": 150, "inventario": 100, "es_vegetariano": True, "tipo": "base"},
        {"nombre": "Chocolate", "precio": 1.2, "calorias": 180, "inventario": 80, "es_vegetariano": True, "tipo": "base"},
        {"nombre": "Banana", "precio": 0.8, "calorias": 120, "inventario": 50, "es_vegetariano": True, "tipo": "base"},
        {"nombre": "Fresa", "precio": 1.1, "calorias": 140, "inventario": 70, "es_vegetariano": True, "tipo": "base"},
        {"nombre": "Caramelo", "precio": 1.3, "calorias": 200, "inventario": 60, "es_vegetariano": False, "tipo": "complemento"},
        {"nombre": "Nueces", "precio": 1.5, "calorias": 220, "inventario": 40, "es_vegetariano": False, "tipo": "complemento"},
        {"nombre": "Crema Batida", "precio": 1.0, "calorias": 160, "inventario": 90, "es_vegetariano": False, "tipo": "complemento"},
        {"nombre": "Mango", "precio": 1.2, "calorias": 100, "inventario": 60, "es_vegetariano": True, "tipo": "base"},
        {"nombre": "Leche Condensada", "precio": 1.4, "calorias": 250, "inventario": 50, "es_vegetariano": False, "tipo": "complemento"},
        {"nombre": "Coco Rallado", "precio": 1.1, "calorias": 180, "inventario": 70, "es_vegetariano": True, "tipo": "complemento"}
    ]

    try:
        nuevos = 0
        for ing in ingredientes:
            existe = Ingrediente.query.filter_by(nombre=ing["nombre"]).first()
            if not existe:
                nuevo_ingrediente = Ingrediente(**ing)
                db.session.add(nuevo_ingrediente)
                nuevos += 1
        
        db.session.commit()
        mensaje = f"Se insertaron {nuevos} nuevos ingredientes." if nuevos > 0 else "Todos los ingredientes ya existían."
        flash(mensaje, "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al insertar ingredientes: {e}", "danger")
