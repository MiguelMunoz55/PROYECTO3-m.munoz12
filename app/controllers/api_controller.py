from flask import Flask, jsonify, request,Response
from flask_login import login_required, current_user
from app.models.Producto import Producto
from app.models.Ingrediente import Ingrediente
from app.config.db import db
from app.seeders.insertar_productos import cargar_productos
from app.seeders.insertar_ingredientes import cargar_ingredientes
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.controllers import funciones
import json


api_blueprint = Blueprint("api", __name__, url_prefix="/api")

# Verificar permisos
def is_admin():
    return current_user.is_authenticated and current_user.es_admin

def is_employee():
    return current_user.is_authenticated and current_user.es_empleado

def is_client():
    return current_user.is_authenticated and current_user.es_cliente

# Consultar todos los productos
@api_blueprint.route("/productos", methods=["GET"])
def get_productos():
    productos = Producto.query.all()
    return jsonify([producto.to_dict() for producto in productos])

# Consultar un producto por ID
@api_blueprint.route("/producto/<int:id>", methods=["GET"])
def get_producto(id):
    producto = Producto.query.get_or_404(id)
    return jsonify(producto.to_dict())

# Consultar un producto por nombre
@api_blueprint.route("/producto/nombre/<string:nombre>", methods=["GET"])
def get_producto_nombre(nombre):
    producto = Producto.query.filter_by(nombre=nombre).first_or_404()
    return jsonify(producto.to_dict())

@api_blueprint.route("/producto/<int:id>/calorias", methods=["GET"])
def get_calorias(id):
    producto = Producto.query.get_or_404(id)

    # Obtener las calorías de los ingredientes
    calorias_ingredientes = []
    if producto.ingrediente_1:
        calorias_ingredientes.append(producto.ingrediente_1.calorias)
    if producto.ingrediente_2:
        calorias_ingredientes.append(producto.ingrediente_2.calorias)
    if producto.ingrediente_3:
        calorias_ingredientes.append(producto.ingrediente_3.calorias)

    # Calcular las calorías usando la función
    total_calorias = funciones.las_calorias(calorias_ingredientes)

    return jsonify({"calorias": total_calorias})

# Consultar rentabilidad (Solo admin y empleados)
@api_blueprint.route("/producto/<int:id>/rentabilidad", methods=["GET"])
@login_required
def get_rentabilidad(id):
    if not (is_admin() or is_employee()):
        return jsonify({"error": "No autorizado"}), 403
    producto = Producto.query.get_or_404(id)
    return jsonify({"rentabilidad": producto.calcular_rentabilidad()})

# Consultar costo de producción (Solo admin y empleados)
@api_blueprint.route("/producto/<int:id>/costo", methods=["GET"])
@login_required
def get_costo(id):
    if not (is_admin() or is_employee()):
        return jsonify({"error": "No autorizado"}), 403
    producto = Producto.query.get_or_404(id)
    return jsonify({"costo": producto.calcular_costo()})

# Vender producto (Clientes y autenticados pueden acceder)
@api_blueprint.route("/producto/<int:id>/vender", methods=["POST", "GET"])
@login_required
def vender_producto(id):
    if not (is_admin() or is_employee() or is_client()):
        return jsonify({"error": "No autorizado"}), 403
    producto = Producto.query.get_or_404(id)
    try:
        mensaje = producto.consumir_ingredientes()
        db.session.commit()
        return Response(
            json.dumps({"mensaje": mensaje}, ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )
    except ValueError as e:
        db.session.rollback()
        return Response(
            json.dumps({"error": str(e)}, ensure_ascii=False),
            status=400,
            mimetype="application/json"
        )
    except Exception as e:
        db.session.rollback()
        return Response(
            json.dumps({"error": "Error inesperado"}, ensure_ascii=False),
            status=500,
            mimetype="application/json"
        )

# Consultar todos los ingredientes (Solo admin y empleados)
@api_blueprint.route("/ingredientes", methods=["GET"])
@login_required
def get_ingredientes():
    if not (is_admin() or is_employee()):
        return jsonify({"error": "No autorizado"}), 403
    ingredientes = Ingrediente.query.all()
    return jsonify([ingrediente.to_dict() for ingrediente in ingredientes])

# Consultar un ingrediente por ID
@api_blueprint.route("/ingrediente/<int:id>", methods=["GET"])
@login_required
def get_ingrediente(id):
    if not (is_admin() or is_employee()):
        return jsonify({"error": "No autorizado"}), 403
    ingrediente = Ingrediente.query.get_or_404(id)
    return jsonify(ingrediente.to_dict())


# Consultar un ingrediente por nombre
@api_blueprint.route("/ingrediente/nombre/<string:nombre>", methods=["GET"])
def get_ingrediente_nombre(nombre):
    ingrediente = Ingrediente.query.filter_by(nombre=nombre).first_or_404()
    return jsonify(ingrediente.to_dict())


# Consultar si un ingrediente es sano
@api_blueprint.route("/ingrediente/<int:id>/sano", methods=["GET"])
# @login_required
def get_sano(id):
    # if not (is_admin() or is_employee()):
    #     return jsonify({"error": "No autorizado"}), 403
    ingrediente = Ingrediente.query.get_or_404(id)
    return jsonify({"sano": ingrediente.es_sano()})

# Reabastecer producto (Solo admin y empleados)
@api_blueprint.route("/producto/<int:id>/reabastecer", methods=["POST", "GET"])
@login_required
def reabastecer_producto(id):
    if not (is_admin() or is_employee()):
        return jsonify({"error": "No autorizado"}), 403
    
    producto = Producto.query.get_or_404(id)

    ingredientes = [producto.ingrediente_1, producto.ingrediente_2, producto.ingrediente_3]
    for ingrediente in ingredientes:
        if ingrediente:
            funciones.abastecer_ingrediente(ingrediente, cantidad=10)  # Puedes cambiar la cantidad

    db.session.commit()
    return jsonify({"mensaje": "Producto reabastecido exitosamente"})

# Renovar inventario de un producto (Solo admin y empleados)
@api_blueprint.route("/producto/<int:id>/renovar", methods=["POST", "GET"])
# @login_required
def renovar_producto(id):
    # if not (is_admin() or is_employee()):
    #     return jsonify({"error": "No autorizado"}), 403

    producto = Producto.query.get_or_404(id)

    # Obtener los ingredientes del producto
    ingredientes = [producto.ingrediente_1, producto.ingrediente_2, producto.ingrediente_3]

    # Llamar a la función correcta para renovar inventario
    funciones.renovar_inventario(ingredientes)

    db.session.commit()
    return jsonify({"mensaje": "Inventario renovado exitosamente"})


