from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.Producto import Producto
from app.config.db import db

user_blueprint = Blueprint("user", __name__, url_prefix="/user")

# Dashboard principal (accesible a cualquier usuario autenticado)
@user_blueprint.route("/dashboard")
@login_required
def dashboard():
    productos = Producto.query.all()
    return render_template(
        "user/dashboard.html",
        user=current_user,
        productos=productos
    )

# Ruta para vender un producto
@user_blueprint.route("/vender-producto/<int:producto_id>", methods=["POST"])
@login_required
def vender_producto_route(producto_id):
    producto = Producto.query.get_or_404(producto_id)

    try:
        mensaje = producto.consumir_ingredientes()
        db.session.commit()
        flash(mensaje, "success")
    except ValueError as e:
        db.session.rollback()
        flash(f"¡Oh no! Nos hemos quedado sin {e}", "danger")
    except Exception:
        db.session.rollback()
        flash("Ocurrió un error inesperado al intentar vender el producto.", "danger")

    return redirect(url_for("user.dashboard"))