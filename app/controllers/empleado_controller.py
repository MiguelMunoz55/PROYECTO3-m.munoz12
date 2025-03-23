from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.Producto import Producto
from app.models.Ingrediente import Ingrediente
from app.config.db import db


empleado_blueprint = Blueprint("empleado", __name__, url_prefix="/empleado")

# Dashboard principal
@empleado_blueprint.route("/dashboard")
@login_required
def dashboard():
    if not current_user.es_admin and not current_user.es_empleado:
        return redirect(url_for("auth.no_autorizado"))  # Redirige si no es admin

    productos = Producto.query.all()
    ingredientes = Ingrediente.query.all()

    return render_template(
        "empleado/dashboard.html",
        user=current_user,
        productos=productos,
        ingredientes=ingredientes
    )

# Ruta para vender un producto
@empleado_blueprint.route("/vender-producto/<int:producto_id>", methods=["POST"])
@login_required
def vender_producto_route(producto_id):
    if not current_user.es_admin and not current_user.es_empleado:
        return redirect(url_for("auth.no_autorizado"))  # Redirige si no es admin

    producto = Producto.query.get_or_404(producto_id)
    
    try:
        mensaje = producto.consumir_ingredientes()
        db.session.commit()
        flash(mensaje, "success")
    except ValueError as e:
        db.session.rollback()
        flash(f"¡Oh no! Nos hemos quedado sin {e}", "danger")
    except Exception as e:
        db.session.rollback()
        flash("Ocurrió un error inesperado al intentar vender el producto.", "danger")
    
    return redirect(url_for("empleado.dashboard"))




