from flask import flash
from app.config.db import db
from app.models.Producto import Producto
from app.models.Ingrediente import Ingrediente

def cargar_productos():
    productos = [
        {"nombre": "Helado de Mango", "precio_publico": 5.5, "costo": 2.8, "inventario": 80, "id_ingrediente_1": 8, "id_ingrediente_2": 10, "id_ingrediente_3": 7},
        {"nombre": "Helado de Fresa con Leche Condensada", "precio_publico": 6.0, "costo": 3.2, "inventario": 60, "id_ingrediente_1": 4, "id_ingrediente_2": 9, "id_ingrediente_3": 7},
        {"nombre": "Banana Split Deluxe", "precio_publico": 7.0, "costo": 3.5, "inventario": 50, "id_ingrediente_1": 3, "id_ingrediente_2": 5, "id_ingrediente_3": 6},
        {"nombre": "Helado de Chocolate con Coco", "precio_publico": 5.8, "costo": 3.0, "inventario": 70, "id_ingrediente_1": 2, "id_ingrediente_2": 10, "id_ingrediente_3": 7}
    ]

    try:
        nuevos = 0
        for prod in productos:
            existe = Producto.query.filter_by(nombre=prod["nombre"]).first()
            if not existe:
                nuevo_producto = Producto(**prod)
                db.session.add(nuevo_producto)
                nuevos += 1
        
        db.session.commit()
        
        if nuevos > 0:
            flash(f"Se insertaron {nuevos} nuevos productos correctamente.", "success")
        else:
            flash("Todos los productos ya existían, no se insertaron nuevos registros.", "info")
    
    except Exception as e:
        db.session.rollback()
        flash(f"Error al insertar productos: {e}", "danger")


